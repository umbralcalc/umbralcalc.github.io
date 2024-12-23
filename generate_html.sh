#!/bin/bash

# generate about page
pandoc --template template.html \
--wrap=preserve \
--citeproc \
--csl=ieee.csl \
--bibliography=biblio.bib \
--mathjax \
-f markdown \
-t html \
-o posts/about.html \
README.md;

# generate other posts
for filename in _posts/*.md; do
    prefix="_posts/"
    suffix=".md"
    newFilename=${filename%"$suffix"}
    newFilename=${newFilename#"$prefix"}
    pandoc --template template.html \
    --wrap=preserve \
    --citeproc \
    --csl=ieee.csl \
    --bibliography=biblio.bib \
    --mathjax \
    -f markdown \
    -t html \
    -o posts/${newFilename}.html \
    ${filename};
done
