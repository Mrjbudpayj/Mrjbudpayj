#!/usr/bin/env python3
"""
Phase 1: Manifest generator for canonicalization.

Usage: python3 manifest_generator.py <repo_path> <output.json>
Produces a deterministic manifest listing files and SHA1 content hashes sorted by path.
"""
import sys, os, hashlib, json


def file_hash(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            b = f.read(8192)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def build_manifest(root):
    entries = []
    for dirpath, dirs, files in os.walk(root):
        dirs.sort()
        files.sort()
        for fn in files:
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, root)
            entries.append({'path': rel.replace(os.sep, '/'), 'sha1': file_hash(fp)})
    entries.sort(key=lambda e: e['path'])
    return {'version': 1, 'entries': entries}


def main():
    if len(sys.argv) < 3:
        print("Usage: manifest_generator.py <repo_path> <output.json>")
        sys.exit(2)
    root = sys.argv[1]
    out = sys.argv[2]
    m = build_manifest(root)
    with open(out, 'w') as f:
        json.dump(m, f, indent=2, sort_keys=True)
    print("Wrote", out)


if __name__ == '__main__':
    main()
