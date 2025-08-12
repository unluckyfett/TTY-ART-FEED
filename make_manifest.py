#!/usr/bin/env python3
"""
make_manifest.py — Build a manifest.json for the RTTY bundled mode.

Scans a local folder laid out like:
  <ROOT>/ARTWORK-01/000
  <ROOT>/ARTWORK-01/001
  ...
  <ROOT>/ARTWORK-08/###

Outputs one of three formats the web app supports:

1) --format array  =>  JSON array
   [
     "ARTWORK-01/000",
     "ARTWORK-01/001"
   ]

2) --format items  =>  JSON object with base + items   (DEFAULT)
   {
     "base": "rtty_offline",
     "items": ["ARTWORK-01/000", "ARTWORK-02/042"]
   }

3) --format map    =>  Directory map (plus base)
   {
     "base": "rtty_offline",
     "ARTWORK-01": ["000","001"],
     "ARTWORK-02": ["042"]
   }

Filtering:
  --filter nude,girl,mrs    # skip if content contains any of those words (case-insensitive)
  --path-filter regex       # skip if relative path matches regex (e.g. '(?i)nude|girl|mrs')

Examples:
  python make_manifest.py --root ./rtty_offline --out ./rtty_offline/manifest.json
  python make_manifest.py --root ./rtty_offline --out ./rtty_offline/manifest_safe.json --filter nude,girl,mrs
  python make_manifest.py --root ./public/rtty_offline --format map --base rtty_offline

Only uses the standard library.
"""

import argparse
import json
import os
import re
import sys

DIR_RE = re.compile(r"^ARTWORK-0[1-8]$")
FILE_RE = re.compile(r"^\d{3}$")

def eprint(*a, **k):
    print(*a, **k, file=sys.stderr)

def read_text(path):
    # Read as UTF-8 with fallback to latin-1, preserve bytes where needed
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            return f.read()
    except Exception:
        with open(path, "r", encoding="latin-1", errors="replace", newline="") as f:
            return f.read()

def build_index(root):
    root = os.path.abspath(root)
    out = {}
    if not os.path.isdir(root):
        raise SystemExit(f"Root not found or not a directory: {root}")
    for entry in os.listdir(root):
        dpath = os.path.join(root, entry)
        if not os.path.isdir(dpath):
            continue
        if not DIR_RE.match(entry):
            continue
        files = []
        for fname in os.listdir(dpath):
            if FILE_RE.match(fname) and os.path.isfile(os.path.join(dpath, fname)):
                files.append(fname)
        files.sort(key=lambda s: int(s))
        out[entry] = files
    return out

def apply_filters(root, index, filters, path_regex):
    if not filters and not path_regex:
        return index
    lowered = [w.lower() for w in filters]
    compiled = re.compile(path_regex, flags=re.IGNORECASE) if path_regex else None
    kept = {}
    total = 0
    dropped = 0
    for d, files in index.items():
        kept_list = []
        for f in files:
            total += 1
            rel = f"{d}/{f}"
            # Path-based reject
            if compiled and compiled.search(rel):
                dropped += 1
                continue
            if lowered:
                p = os.path.join(root, d, f)
                txt = read_text(p)
                low = txt.lower()
                if any(w in low for w in lowered):
                    dropped += 1
                    continue
            kept_list.append(f)
        if kept_list:
            kept[d] = kept_list
    eprint(f"apply_filters: kept={sum(len(v) for v in kept.values())} dropped={dropped} total={total}")
    return kept

def to_array(index):
    arr = []
    for d in sorted(index.keys()):
        for f in index[d]:
            arr.append(f"{d}/{f}")
    return arr

def to_items(index, base):
    return {"base": base, "items": to_array(index)}

def to_map(index, base):
    obj = {"base": base}
    for d in sorted(index.keys()):
        obj[d] = index[d]
    return obj

def main():
    ap = argparse.ArgumentParser(description="Build manifest.json for bundled mode (stdlib only).")
    ap.add_argument("--root", default="./rtty_offline", help="Root directory containing ARTWORK-0X folders")
    ap.add_argument("--out", default=None, help="Output manifest path (default: <root>/manifest.json)")
    ap.add_argument("--format", choices=["items","array","map"], default="items", help="Manifest format")
    ap.add_argument("--base", default=None, help="Base path to put in manifest (default: basename of --root)")
    ap.add_argument("--filter", default="", help="Comma separated content words to exclude (case-insensitive)")
    ap.add_argument("--path-filter", default="", help="Regex to exclude by relative path (e.g. '(?i)nude|girl|mrs')")
    args = ap.parse_args()

    root = args.root
    out = args.out or os.path.join(root, "manifest.json")
    base = args.base if args.base is not None else os.path.basename(os.path.normpath(root))
    filters = [w.strip() for w in args.filter.split(",") if w.strip()]

    index = build_index(root)
    if not index:
        raise SystemExit("No ARTWORK-0X folders found with files")

    index = apply_filters(root, index, filters, args.path_filter)

    if args.format == "array":
        data = to_array(index)
    elif args.format == "map":
        data = to_map(index, base)
    else:
        data = to_items(index, base)

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out} ({'array' if isinstance(data, list) else 'object'}, {len(to_array(index))} items)")

if __name__ == "__main__":
    main()
