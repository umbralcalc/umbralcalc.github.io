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
  title SRC            print a post's title
  chain SRC            print the post's parents, root first, as markdown links
  posts OUT.json       write posts.json (title, slug, url, tag, draft, images)
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

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "_posts")
FORECASTS_JSON = os.path.join(ROOT, "forecasts.json")
FORECASTS_ROOT = "Forecasts"
BASE_URL = "https://umbralcalc.github.io"
SITE_NAME = "umbralcalculations"
AUTHOR = "Hardwick, Robert J."
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
    """Read a post's YAML front matter (as Obsidian writes it, quoted or not)
    and its body."""
    slug = os.path.basename(path)[:-3]
    text = open(path, encoding="utf-8").read()
    fm_lines, body = split_frontmatter(text)
    try:
        meta = yaml.safe_load("\n".join(fm_lines)) or {}
    except yaml.YAMLError as e:
        print(f"[ERROR] {slug}: front matter is not valid YAML: {e}")
        sys.exit(1)

    def as_list(v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return [str(x) for x in v]

    nocite = meta.get("nocite") or ""
    if isinstance(nocite, list):
        nocite = " ".join(str(x) for x in nocite)
    return {
        "slug": slug,
        "title": str(meta.get("title") or slug),
        "draft": bool(meta.get("draft")),
        "images": as_list(meta.get("images")),
        "cites": [m.group(1) for m in (WIKI_LINK.search(c) for c in as_list(meta.get("cites"))) if m],
        "nocite": re.findall(r"@([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*)", str(nocite)),
        "body": body,
        "frontmatter": fm_lines,
    }


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
            "draft": False,
            "excerpt": f.get("headline", ""),
            "images": [f["thumbnail"]] if f.get("thumbnail") else [],
            "date": f.get("date", ""),
            # Blog questions the forecast builds on; the first is its parent
            "cites": list(f.get("cites", [])),
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
    fm = {"title": post["title"]}
    posts = all_posts()
    chain = ancestors_of_each(posts)[post["slug"]]
    if chain:
        fm["chain"] = " \u203a ".join(f"[{titles[s]}](/posts/{s}.html)" for s in chain)
    if keys:
        fm["nocite"] = ", ".join(f"@{k}" for k in keys)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---" + body)


def cmd_title(src):
    print(parse_post(src)["title"])


def cmd_chain(src):
    """Print the post's parents as a markdown breadcrumb, root first, or
    nothing if it is a root."""
    post = parse_post(src)
    posts = all_posts()
    chain = ancestors_of_each(posts)[post["slug"]]
    if chain:
        titles = {p["slug"]: p["title"] for p in posts}
        print(" \u203a ".join(f"[{titles[s]}](/posts/{s}.html)" for s in chain))


def root_of_each(posts):
    """A question's parent is the first entry of its `cites` property, and
    its root is found by following parents upward. A post with no `cites`
    is a root. Links in the prose do not count, so a root can still point
    at other roots for context."""
    by_slug = {p["slug"]: p for p in posts}

    def first_post_cite(p):
        for key in p["cites"]:
            if key in by_slug and key != p["slug"]:
                return key
        return None

    roots = {}
    for p in posts:
        roots[p["slug"]] = ancestors_of(p, by_slug, first_post_cite)[0] if ancestors_of(p, by_slug, first_post_cite) else p["slug"]
    return roots


def ancestors_of(p, by_slug, first_post_cite):
    """The chain of parents above a post, root first; empty for a root."""
    chain = []
    seen = {p["slug"]}
    cur = p
    while True:
        nxt = first_post_cite(cur)
        if nxt is None or nxt in seen:
            break
        chain.append(nxt)
        seen.add(nxt)
        cur = by_slug[nxt]
    return list(reversed(chain))


def ancestors_of_each(posts):
    by_slug = {p["slug"]: p for p in posts}

    def first_post_cite(p):
        for key in p["cites"]:
            if key in by_slug and key != p["slug"]:
                return key
        return None

    return {p["slug"]: ancestors_of(p, by_slug, first_post_cite) for p in posts}


def cmd_posts(out_path):
    """posts.json: the plain post list the feed and older scripts read."""
    posts = []
    all_ = all_posts()
    roots = root_of_each(all_)
    titles = {p["slug"]: p["title"] for p in all_}
    for post in all_:
        posts.append({
            "title": post["title"],
            "slug": post["slug"],
            "url": f"/posts/{post['slug']}.html",
            "root": roots[post["slug"]],
            "root_title": titles.get(roots[post["slug"]], roots[post["slug"]]),
            "draft": post["draft"],
            "date": "",
            "images": post["images"],
        })
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
        f.write("\n")


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
    roots = root_of_each(posts)
    ancestors = ancestors_of_each(posts)
    titles = {p["slug"]: p["title"] for p in posts}
    slugs = {p["slug"] for p in posts} | {f["slug"] for f in forecasts}
    questions = []
    used = set()
    for fc in forecasts:
        # Forecasts keep their own group on the home page, but carry a parent
        # chain and citations like any post, so the card shows what they
        # build on and the cited questions list them as citing answers
        cites = [k for k in fc["cites"] if k in titles]
        parent = cites[0] if cites else ""
        chain = (ancestors[parent] + [parent]) if parent else []
        questions.append({
            "slug": fc["slug"],
            "title": fc["title"],
            "url": fc["url"],
            "root": "forecasts",
            "root_title": FORECASTS_ROOT,
            "parent": parent,
            "ancestors": [{"slug": s, "title": titles[s]} for s in chain],
            "draft": False,
            "date": fc["date"],
            "excerpt": fc["excerpt"],
            "images": fc["images"],
            "references": cites,
            "cites": cites,
            "cited_by": [],
        })
    for post in posts:
        keys = reference_keys(post)
        used.update(keys)
        questions.append({
            "slug": post["slug"],
            "title": post["title"],
            "url": f"/posts/{post['slug']}.html",
            "root": roots[post["slug"]],
            "root_title": titles[roots[post["slug"]]],
            "parent": ancestors[post["slug"]][-1] if ancestors[post["slug"]] else "",
            "ancestors": [{"slug": s, "title": titles[s]} for s in ancestors[post["slug"]]],
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
    elif cmd == "title" and len(args) == 1:
        cmd_title(args[0])
    elif cmd == "chain" and len(args) == 1:
        cmd_chain(args[0])
    elif cmd == "posts" and len(args) == 1:
        cmd_posts(args[0])
    elif cmd == "json" and "-o" in args:
        i = args.index("-o")
        cmd_json(args[:i], args[i + 1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
