#!/bin/bash
pandoc --template template.html \
--mathjax \
-f markdown \
-t html \
-o text.html \
_posts/2023-12-06-solving-non-Markovian-master-equations-with-Libtorch.md;
