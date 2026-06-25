#!/bin/bash
# Commit all changes and push to origin/main
if [ -z "$1" ]; then
  echo "Error: Commit message required."
  exit 1
fi

git add .
git commit -m "$1" --no-gpg-sign
git push
