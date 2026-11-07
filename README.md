# umbralcalculations

Visual explorations in science and computation.

## How a post is structured

Every post in `_posts/` answers one question, and the folder doubles as an
Obsidian vault: open the repository root in Obsidian and each post is a note.

- **Question.** The post's title, in plain words, repeated in `aliases` so
  Obsidian finds the note by its question.
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
tag: "How can I trust the actions I take in simulations?"   # its root question
draft: true            # listed only at /?drafts=1, kept out of the feed
images:                # thumbnails on the home page
- "https://.../predictions-leading-to-actions.svg"
aliases:
- "How can a simulation be wrong?"
cites:
- "[[what_if_i_can_only_partly_observe_the_system]]"
nocite: |
  @box1976, @sargent2013
```

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
