# umbralcalculations

Visual explorations in science and computation.

## How a post is structured

Every post in `_posts/` answers one question, and the folder doubles as an
Obsidian vault: open the repository root in Obsidian and each post is a note.

- **Question.** The post's title, in plain words. The file is named by the
  same words in lower case with underscores.
- **Answer.** Free prose, with diagrams and widgets wherever they help. Any
  assumptions, justifications and caveats are written into the answer. When
  the answer leans on another question, link it as a wikilink,
  `[[what_is_a_state_partition|state partition]]`; when it leans on a paper,
  link the words to its bibliography entry as `[those words](#ref-KEY)`. The
  answer never links straight out to the web.
- **References and further reading.** Printed from `_refs/references.bib`
  via pandoc's citeproc, and it holds every outbound link: papers, books,
  code, data, web pages, and other questions on this site. Two properties
  feed it without a link in the prose: `cites`, a list of wikilinks to other
  questions, and `nocite`, bibliography keys. Anything linked from the prose
  is printed automatically.

Front matter, by example:

```yaml
title: "How can a simulation be wrong?"
draft: true            # listed only at /?drafts=1, kept out of the feed
images:                # thumbnails on the home page
- "https://.../predictions-leading-to-actions.svg"
cites:
- "[[how_can_i_trust_the_actions_i_take_in_simulations]]"   # first entry = parent
- "[[what_if_i_can_only_partly_observe_the_system]]"
nocite: |
  @box1976, @sargent2013
```

A question's parent is the first entry of its `cites` list, and its root is found by following parents upward; a post with no `cites` is a root. The home page groups questions by root, and the feed
uses the root as each item's category.

Obsidian's graph view and backlinks follow the `cites` wikilinks and the
wikilinks in the prose, so the editor shows the same tree the site builds.

The build (`./build.sh`) derives everything structural from the question and
the references alone, via `_build/questions.py`:

- Every post gets a bibliography entry, so a question is cited like a paper.
  Wikilinks in the prose become links to that entry under References.
- `questions.json`: each question with its references, the questions it
  cites, and the questions that cite it.
- Under each post, "Questions whose answers cite this one".
- The home page, `index.html`: a search box over the questions, each shown
  with its diagrams as thumbnails.
- A warning for any link in an answer that bypasses the references, and a
  failed build for any citation that no bibliography defines.
- Redirect pages for old post URLs listed in `_build/redirects.txt`.

## Publishing

Pushing to main is the deploy: `.github/workflows/pages.yml` builds the site
and publishes it to GitHub Pages on every push, and pull requests build too.
Nothing generated is committed; `posts/`, `posts.json`, `questions.json`,
`feed.xml`, `sitemap.xml` and `robots.txt` are built on the runner (and
locally by `./build.sh`, where they are ignored by git). Main allows direct
pushes from the repository admin but no force pushes or deletion.

`./publish.sh ["commit message"]` rebuilds locally, stops if the build or
its lint fails, commits everything, pulls anything new on main and pushes.
From Obsidian, the Shell Commands community plugin can run it as a command
or ribbon button, with the vault root as the working directory.
