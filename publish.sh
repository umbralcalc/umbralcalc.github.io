#!/bin/bash
# Publish: rebuild the site, commit everything and push to main. The push
# is the deploy: .github/workflows/pages.yml builds and publishes the site
# on every push to main.
#
#   ./publish.sh ["commit message"]
#
# Stops without committing if the build or its lint fails.

set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

remote="https://github.com/umbralcalc/umbralcalc.github.io.git"
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

# Bring in anything that landed on main elsewhere, then push
git pull -q --rebase "$remote" main
git push -q "$remote" HEAD:main
echo "Pushed to main; the pages workflow is deploying it."
