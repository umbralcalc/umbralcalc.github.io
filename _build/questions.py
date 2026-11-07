#!/usr/bin/env python3
"""Question-and-answer structure derived from posts.

Every post answers one question (its title). The structure of the site is
read from two things only: the question, and the references the answer
cites. Nothing in the answer's prose is parsed for structure.

Sub-commands, all run from build.sh:

  bib OUT.json         write a CSL JSON bibliography entry for every post,
                       so one question can cite another exactly like a paper
  lint REFS.bib ...    warn about links that bypass the references, and fail
                       on citation keys that no bibliography defines
  prepare SRC OUT      copy a post for pandoc, adding every #ref-KEY the
                       answer links to into its nocite list so the entry is
                       printed under References
  json REFS.bib ... -o questions.json
                       write the question graph: each post with its
                       references, which other questions it cites, and which
                       cite it
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "_posts")
FORECASTS_JSON = os.path.join(ROOT, "forecasts.json")
FORECASTS_TAG = "Forecasts"
BASE_URL = "https://umbralcalc.github.io"
SITE_NAME = "umbralcalculations"
AUTHOR = "Hardwick, Robert"
ASSET_HOST = "r2.dev"

REF_LINK = re.compile(r"\]\(#ref-([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*)\)")
# Obsidian-style links to other posts: [[slug]] or [[slug|shown text]]
WIKI_LINK = re.compile(r"\[\[([A-Za-z0-9_-]+)(?:\|([^\]]*))?\]\]")
EXTERNAL_LINK = re.compile(r"\]\((https?://[^)\s]+)\)")


# ----------------------------------------------------------------- posts

def split_frontmatter(text):
    if not text.startswith("---"):
        return [], text
    end = text.find("\n---", 3)
    if end == -1:
        return [], text
    return text[3:end].strip("\n").split("\n"), text[end + 4:]


def parse_post(path):
    slug = os.path.basename(path)[:-3]
    text = open(path, encoding="utf-8").read()
    fm, body = split_frontmatter(text)
    post = {
        "slug": slug,
        "title": slug,
        "tag": "",
        "draft": False,
        "images": [],
        "nocite": [],
        "cites": [],
        "body": body,
        "frontmatter": fm,
    }
    i = 0
    while i < len(fm):
        line = fm[i]
        m = re.match(r'^title:\s*"(.*)"\s*$', line)
        if m:
            post["title"] = m.group(1)
        m = re.match(r'^tag:\s*"(.*)"\s*$', line)
        if m:
            post["tag"] = m.group(1).strip()
        if re.match(r"^draft:\s*true\s*$", line):
            post["draft"] = True
        m = re.match(r"^cites:\s*$", line)
        if m:
            j = i + 1
            while j < len(fm) and re.match(r"^\s*-\s*", fm[j]):
                w = WIKI_LINK.search(fm[j])
                if w:
                    post["cites"].append(w.group(1))
                j += 1
            i = j
            continue
        m = re.match(r"^images:\s*(.*)$", line)
        if m:
            rest = m.group(1).strip()
            if rest.startswith("["):
                post["images"] = re.findall(r'"([^"]+)"', rest)
            elif rest:
                post["images"] = [rest.strip('"')]
            else:
                j = i + 1
                while j < len(fm) and re.match(r"^\s*-\s*", fm[j]):
                    post["images"].append(re.sub(r'^\s*-\s*"?|"?\s*$', "", fm[j]))
                    j += 1
                i = j
                continue
        m = re.match(r"^nocite:\s*(.*)$", line)
        if m:
            rest = m.group(1).strip()
            keys = []
            if rest and rest != "|":
                keys.append(rest)
            j = i + 1
            while j < len(fm) and (fm[j].startswith(" ") or fm[j] == ""):
                keys.append(fm[j])
                j += 1
            post["nocite"] = re.findall(r"@([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*)", " ".join(keys))
            i = j
            continue
        i += 1
    return post


def all_posts():
    posts = []
    for name in sorted(os.listdir(POSTS_DIR)):
        if name.endswith(".md"):
            posts.append(parse_post(os.path.join(POSTS_DIR, name)))
    return posts


def all_forecasts():
    """Forecast dashboards are questions too: the title asks, the live
    dashboard answers. They live outside _posts, so they are read from
    forecasts.json and keyed by the last part of their URL."""
    if not os.path.exists(FORECASTS_JSON):
        return []
    forecasts = []
    for i, f in enumerate(json.load(open(FORECASTS_JSON, encoding="utf-8"))):
        slug = re.sub(r"[^A-Za-z0-9]+", "_", f["url"].rstrip("/").rsplit("/", 1)[-1]).strip("_").lower()
        forecasts.append({
            "slug": slug,
            "title": f["title"],
            "url": f["url"],
            "tag": FORECASTS_TAG,
            "draft": False,
            "excerpt": f.get("headline", ""),
            "images": [f["thumbnail"]] if f.get("thumbnail") else [],
            "date": f.get("date", ""),
        })
    return forecasts


def strip_code_and_html(body):
    """Drop fenced blocks and raw HTML lines so widget embeds are not linted."""
    out = []
    in_fence = False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.lstrip().startswith("<"):
            continue
        out.append(line)
    return "\n".join(out)


def cited_keys(post):
    """Keys the answer links to, as #ref-KEY or [[slug]], in order of first
    appearance."""
    seen = []
    text = strip_code_and_html(post["body"])
    for m in re.finditer(r"\]\(#ref-([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*)\)|\[\[([A-Za-z0-9_-]+)(?:\|[^\]]*)?\]\]", text):
        key = m.group(1) or m.group(2)
        if key not in seen:
            seen.append(key)
    return seen


def reference_keys(post):
    """nocite keys, then the cites property, then keys linked from the prose."""
    keys = list(post["nocite"])
    for key in post["cites"] + cited_keys(post):
        if key not in keys:
            keys.append(key)
    return keys


def titles_by_slug():
    return {p["slug"]: p["title"] for p in all_posts()}


def first_commit_date(slug):
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "log", "--diff-filter=A", "--follow",
             "--format=%aI", "--", f"_posts/{slug}.md"],
            capture_output=True, text=True, check=False,
        ).stdout.strip().split("\n")
        if out and out[-1]:
            return datetime.fromisoformat(out[-1].replace("Z", "+00:00"))
    except (OSError, ValueError):
        pass
    return datetime.now()


def excerpt(body):
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or block.startswith("#") or block.startswith("<") or block.startswith("```"):
            continue
        block = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", block)
        block = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", block)
        block = re.sub(r"\s*\[-?@[^\]]*\]", "", block)
        block = re.sub(r"[_*`]", "", block)
        block = re.sub(r"\s+", " ", block).strip()
        if len(block) > 280:
            block = block[:277].rstrip() + "..."
        return block
    return ""


# ------------------------------------------------------------------- bib

def bib_title(post):
    return post["title"]


def nocase(text):
    """Stop the citation style re-capitalising a question or the site name."""
    return f'<span class="nocase">{text}</span>'


def cmd_bib(out_path):
    family, given = [part.strip() for part in AUTHOR.split(",", 1)]
    entries = []
    for post in all_posts():
        date = first_commit_date(post["slug"])
        entries.append({
            "id": post["slug"],
            "type": "webpage",
            "author": [{"family": family, "given": given}],
            "title": nocase(bib_title(post)),
            "container-title": nocase(SITE_NAME),
            "issued": {"date-parts": [[date.year, date.month]]},
            "URL": f"{BASE_URL}/posts/{post['slug']}.html",
        })
    for fc in all_forecasts():
        try:
            d = datetime.fromisoformat(fc["date"])
            issued = [[d.year, d.month]]
        except ValueError:
            issued = [[datetime.now().year]]
        entries.append({
            "id": fc["slug"],
            "type": "webpage",
            "author": [{"family": family, "given": given}],
            "title": nocase(fc["title"]),
            "container-title": nocase(SITE_NAME),
            "issued": {"date-parts": issued},
            "URL": fc["url"],
        })
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_csl(bib_paths):
    """Every bibliography entry as CSL JSON, keyed by citation key."""
    entries = {}
    for path in bib_paths:
        if path.endswith(".json"):
            items = json.load(open(path, encoding="utf-8"))
        else:
            result = subprocess.run(
                ["pandoc", path, "-t", "csljson"],
                capture_output=True, text=True, check=True,
            )
            items = json.loads(result.stdout)
        for item in items:
            entries[item["id"]] = item
    return entries


# ------------------------------------------------------------------ lint

def cmd_lint(bib_paths):
    entries = load_csl(bib_paths)
    errors = 0
    bypass = []
    for post in all_posts():
        for key in reference_keys(post):
            if key not in entries:
                print(f"[ERROR] {post['slug']}: cites unknown reference '@{key}'")
                errors += 1
        links = [u for u in EXTERNAL_LINK.findall(strip_code_and_html(post["body"]))
                 if ASSET_HOST not in u]
        if links:
            bypass.append((post["slug"], len(links)))
    if bypass:
        total = sum(n for _, n in bypass)
        print(f"[WARNING] {total} links in {len(bypass)} posts bypass the references "
              "(answers should link to #ref-KEY entries instead):")
        for slug, n in sorted(bypass, key=lambda x: -x[1]):
            print(f"[WARNING]   {slug}: {n}")
    if errors:
        sys.exit(1)


# --------------------------------------------------------------- prepare

def cmd_prepare(src, out):
    post = parse_post(src)
    keys = reference_keys(post)
    titles = titles_by_slug()

    def to_ref_link(m):
        slug, text = m.group(1), m.group(2)
        return f"[{text or titles.get(slug, slug)}](#ref-{slug})"

    # Rewrite [[slug|text]] outside fenced blocks only
    chunks = re.split(r"(```.*?```)", post["body"], flags=re.S)
    body = "".join(c if c.startswith("```") else WIKI_LINK.sub(to_ref_link, c) for c in chunks)
    post["body"] = body
    fm = []
    skip = False
    for line in post["frontmatter"]:
        if re.match(r"^(nocite|cites|aliases):", line):
            skip = True
            continue
        if skip and (line.startswith(" ") or line.startswith("-") or line == ""):
            continue
        skip = False
        fm.append(line)
    if keys:
        fm.append("nocite: |")
        fm.append("  " + ", ".join(f"@{k}" for k in keys))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("---\n" + "\n".join(fm) + "\n---" + post["body"])


# ------------------------------------------------------------------ json

def csl_year(item):
    try:
        return item["issued"]["date-parts"][0][0]
    except (KeyError, IndexError, TypeError):
        return None


def csl_authors(item):
    names = []
    for a in item.get("author", []):
        if "family" in a:
            names.append(a["family"])
        elif "literal" in a:
            names.append(a["literal"])
    return names


def cmd_json(bib_paths, out_path):
    entries = load_csl(bib_paths)
    posts = all_posts()
    forecasts = all_forecasts()
    slugs = {p["slug"] for p in posts} | {f["slug"] for f in forecasts}
    questions = []
    used = set()
    for fc in forecasts:
        questions.append({
            "slug": fc["slug"],
            "title": fc["title"],
            "url": fc["url"],
            "tag": fc["tag"],
            "draft": False,
            "date": fc["date"],
            "excerpt": fc["excerpt"],
            "images": fc["images"],
            "references": [],
            "cites": [],
            "cited_by": [],
        })
    for post in posts:
        keys = reference_keys(post)
        used.update(keys)
        questions.append({
            "slug": post["slug"],
            "title": post["title"],
            "url": f"/posts/{post['slug']}.html",
            "tag": post["tag"],
            "draft": post["draft"],
            "date": first_commit_date(post["slug"]).date().isoformat(),
            "excerpt": excerpt(post["body"]),
            "images": post["images"],
            "references": keys,
            "cites": [k for k in keys if k in slugs],
            "cited_by": [],
        })
    by_slug = {q["slug"]: q for q in questions}
    for q in questions:
        for target in q["cites"]:
            by_slug[target]["cited_by"].append(q["slug"])
    references = {}
    for key in sorted(used):
        item = entries.get(key)
        if not item:
            continue
        references[key] = {
            "type": "question" if key in slugs else item.get("type", ""),
            "title": re.sub(r"<[^>]+>", "", item.get("title", key)),
            "authors": csl_authors(item),
            "year": csl_year(item),
            "url": item.get("URL") or (f"https://doi.org/{item['DOI']}" if item.get("DOI") else ""),
        }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"questions": questions, "references": references}, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ------------------------------------------------------------------ main

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd, args = argv[1], argv[2:]
    if cmd == "bib" and len(args) == 1:
        cmd_bib(args[0])
    elif cmd == "lint" and args:
        cmd_lint(args)
    elif cmd == "prepare" and len(args) == 2:
        cmd_prepare(args[0], args[1])
    elif cmd == "json" and "-o" in args:
        i = args.index("-o")
        cmd_json(args[:i], args[i + 1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
