#!/bin/bash
# Publish: rebuild the site, then open a pull request with the changes and
# set it to merge itself once the build check passes. Merging into main is
# what deploys, via .github/workflows/pages.yml.
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
    echo "Nothing new to publish."
    exit 0
fi

# Work from an up-to-date main; the staged changes come along to the branch
git fetch -q "$remote" main:refs/remotes/origin/main
if [ "$(git branch --show-current)" = "main" ]; then
    git merge -q --ff-only origin/main 2>/dev/null || true
fi
branch="publish/$(date -u +%Y%m%d-%H%M%S)"
git checkout -q -b "$branch"
git commit -q -m "$message"
git push -q -u "$remote" "$branch"

url=$(gh pr create --repo umbralcalc/umbralcalc.github.io --base main --head "$branch" \
    --title "$message" --body "Published from the vault with publish.sh.")
gh pr merge --repo umbralcalc/umbralcalc.github.io --auto --squash --delete-branch "$url" > /dev/null
echo "Opened $url; it merges and deploys once the build check passes."

git checkout -q main
