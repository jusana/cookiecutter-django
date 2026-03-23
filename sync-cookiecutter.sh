#!/usr/bin/env bash
# Synchronise le fork avec upstream et rebase la branche custom.
# Usage : ./sync-cookiecutter.sh

set -e

CUSTOM_BRANCH="custom_a_utiliser_pour_projets"

echo "==> Fetch upstream..."
git fetch upstream

echo "==> Fast-forward main..."
git checkout main
git merge --ff-only upstream/main
git push origin main

echo "==> Tag cruft-base avant rebase (préserve le commit pour cruft update)..."
git checkout "$CUSTOM_BRANCH"
CRUFT_TAG="cruft-base-$(date +%Y-%m-%d)"
git tag "$CRUFT_TAG"
git push origin "$CRUFT_TAG"

echo "==> Rebase $CUSTOM_BRANCH sur main..."
git rebase main

echo ""
echo "Rebase OK. Vérifie les conflits éventuels, puis :"
echo "  git push --force-with-lease origin $CUSTOM_BRANCH"
echo ""
echo "Tag $CRUFT_TAG poussé — les projets existants peuvent toujours faire cruft update."
