#!/bin/bash

# generate home page
pandoc --template template.html \
--mathjax \
-f markdown \
-t html \
-o index.html \
README.md;

# generate other posts
pandoc --template template.html \
--mathjax \
-f markdown \
-t html \
-o text.html \
_posts/solving-non-Markovian-master-equations-with-Libtorch.md;
