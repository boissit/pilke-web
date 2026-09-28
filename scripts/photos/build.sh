#!/bin/sh
# Every composite, in both languages, then the cut-out and the crops the site
# draws. Run from this directory, with the originals in full/; see docs/pictures.md.
set -e
PY=${PYTHON:-python3}
for lang in fi en; do
  for s in hero loop ex2 beta; do "$PY" $s.py $lang > /dev/null; done
done
"$PY" cutout.py > /dev/null
"$PY" crops.py
