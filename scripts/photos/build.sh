#!/usr/bin/env bash
# Every picture the site makes from the app's stills: the photographs in both
# languages, the hero's cut-out and the crops, into src/assets/photos. Run by
# `npm run pictures:build`, which then builds the site and checks the inventory;
# docs/pictures.md is the runbook.
#
# From a clean checkout it needs only a network and macOS (the iOS bars are drawn
# in the system's San Francisco):
#
#   * Python 3.9 with the pins in requirements.txt, in .venv here, made on the
#     first run and again whenever requirements.txt changes. 3.9 because the
#     committed pictures were made with it: a different interpreter can mean
#     different wheels and a picture a few levels off everywhere. PICTURES_PYTHON
#     names an interpreter to use instead of looking for one.
#   * The Unsplash originals, into full/, from the URLs in originals.json. Each is
#     checked against its size and SHA-256 there, so a photo that changed upstream
#     stops the build instead of moving every screen corner fitted on the old one.
#
# The same inputs give the same bytes out, every run.
set -euo pipefail
cd "$(dirname "$0")"

want=3.9

python_ok() {
  [[ -n "$1" ]] && command -v "$1" >/dev/null 2>&1 &&
    [[ "$("$1" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)" == "$want" ]]
}

find_python() {
  local c
  for c in "${PICTURES_PYTHON:-}" python$want /usr/bin/python3 python3; do
    if python_ok "$c"; then command -v "$c"; return; fi
  done
  if command -v uv >/dev/null 2>&1; then
    c="$(uv python find "$want" 2>/dev/null || { uv python install "$want" >&2 && uv python find "$want"; })"
    if python_ok "$c"; then echo "$c"; return; fi
  fi
  echo "no Python $want found: install one (uv python install $want), or set PICTURES_PYTHON" >&2
  exit 1
}

stamp="$(shasum -a 256 requirements.txt | cut -d' ' -f1)"
if [[ ! -x .venv/bin/python || "$(cat .venv/requirements.sha256 2>/dev/null)" != "$stamp" ]]; then
  py="$(find_python)"
  echo "→ making .venv with $py ($("$py" --version 2>&1))"
  rm -rf .venv
  "$py" -m venv .venv
  .venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt
  echo "$stamp" >.venv/requirements.sha256
fi
PY=.venv/bin/python

# The originals: fetched when missing, and every one checked, fetched or not.
mkdir -p full
"$PY" - <<'EOF'
import hashlib, json, os, sys, urllib.request

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

bad = 0
for o in json.load(open('originals.json')):
    path = os.path.join('full', o['file'])
    if not os.path.exists(path):
        print(f"→ fetching {o['file']} from {o['url']}")
        with urllib.request.urlopen(o['url'], timeout=60) as r:
            data = r.read()
        open(path + '.part', 'wb').write(data)
        os.replace(path + '.part', path)
    size, digest = os.path.getsize(path), sha(path)
    if size != o['bytes'] or digest != o['sha256']:
        print(f"{path} is {size} bytes, sha256 {digest}; originals.json says {o['bytes']} and {o['sha256']}.\n"
              f"  Unsplash may have re-encoded it ({o['page']}). Every screen corner is fitted on the\n"
              f"  recorded file, so check the fits against the new one before recording it.", file=sys.stderr)
        bad += 1
sys.exit(1 if bad else 0)
EOF

"$PY" stills.py

for lang in fi en; do
  for s in hero loop ex2 beta; do
    echo "→ $s.py $lang"
    "$PY" -W ignore::RuntimeWarning $s.py $lang >/dev/null
  done
done
echo "→ cutout.py"
"$PY" cutout.py >/dev/null
echo "→ crops.py"
"$PY" crops.py
