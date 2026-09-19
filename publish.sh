#!/usr/bin/env bash
set -e
git init -b main
git add .
git commit -m "Intermediate Heat Transfer lecture notes as an MkDocs site"
gh repo create intermediate-heat-transfer --public --source=. --push \
  --description "Lecture notes on convection and thermal radiation, published as a searchable website (MkDocs Material) from LaTeX sources"
