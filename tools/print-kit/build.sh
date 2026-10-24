#!/bin/sh
# Rebuilds tools/print-kit/out/ from pilke-web and ../pilke-app. See docs/print-kit.md.
set -e
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv --quiet --python 3.12 .venv
    uv pip install --quiet --python .venv/bin/python -r requirements.txt
  else
    python3 -m venv .venv
    .venv/bin/pip install --quiet -r requirements.txt
  fi
fi
exec .venv/bin/python build.py "$@"
