#!/bin/bash
# Rebuild the site and push it to main.
#
# Meant to be run from Obsidian (Shell Commands plugin) or the terminal:
#   ./publish.sh ["commit message"]
#
# Stops without committing if the build or its lint fails. With nothing to
# commit, pushes whatever is already committed.

set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

message="${1:-Publish $(date -u +%Y-%m-%d\ %H:%M)}"

./build.sh > .publish.log 2>&1 || {
    echo "Build failed. Last lines of .publish.log:"
    tail -n 15 .publish.log
    exit 1
}
grep -E '^\[(WARNING|ERROR)\]' .publish.log || true
rm -f .publish.log

git add -A
if git diff --cached --quiet; then
    echo "Nothing new to commit."
else
    git commit -q -m "$message"
    echo "Committed: $message"
fi

git push -q https://github.com/umbralcalc/umbralcalc.github.io.git HEAD:main
echo "Pushed to main."
