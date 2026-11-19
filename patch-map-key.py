#!/usr/bin/env python3
"""Add a CARTO basemaps API key to NetzSec Loot's map tile URL.

Since 25 Sep 2026 CARTO only serves raster basemap tiles with a ?key= parameter.
NetzSec Loot hardcodes a keyless tile URL in an embedded JavaScript chunk, so
this rewrites that one spot in a copy of the binary.

The embedded file cannot change length, so the bytes for "?key=..." are freed
by rewriting a duplicated colour table in the same module:
    k={Open:..,WEP:..,WPA:..,WPA2:..,WPA3:..,Other:"#9ca3af"}
 -> k={...x,Other:"#9ca3af"}          (x already holds the first five entries)
which builds an identical object. Leftover bytes become spaces.

Usage:
    python3 -I patch-map-key.py [--input BIN] [--output BIN] [--key-file FILE]

The input binary is never modified. Install the output yourself, e.g.
    sudo install -m 755 OUTPUT /usr/local/bin/netzsec-loot
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HOME = os.path.expanduser("~")
DEFAULT_INPUT = "/usr/local/bin/netzsec-loot"
DEFAULT_OUTPUT = os.path.join(HOME, ".local/share/netzsec-loot-patch/netzsec-loot.patched")
DEFAULT_KEY = os.path.join(HOME, ".config/NetzSec Loot/carto-key.txt")

OLD_K = b'k={Open:"#ef4444",WEP:"#f59e0b",WPA:"#eab308",WPA2:"#22c55e",WPA3:"#3b82f6",Other:"#9ca3af"}'
NEW_K = b'k={...x,Other:"#9ca3af"}'
# x must be the same five entries, declared before k in the same `let`.
X_DEF = b'let x={Open:"#ef4444",WEP:"#f59e0b",WPA:"#eab308",WPA2:"#22c55e",WPA3:"#3b82f6"}'
OLD_URL = b'w=e=>`https://{s}.basemaps.cartocdn.com/${S[e].path}/{z}/{x}/{y}{r}.png`'
URL_PREFIX = b'w=e=>`https://{s}.basemaps.cartocdn.com/${S[e].path}/{z}/{x}/{y}{r}.png'
PATCHED_MARK = URL_PREFIX + b"?key="


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def chunk_bounds(data, pos):
    """Extent of the NUL-delimited embedded file containing pos."""
    start = data.rfind(b"\x00", 0, pos) + 1
    end = data.find(b"\x00", pos)
    return start, end


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--input", default=DEFAULT_INPUT)
    ap.add_argument("--output", default=DEFAULT_OUTPUT)
    ap.add_argument("--key-file", default=DEFAULT_KEY)
    args = ap.parse_args()

    key = open(args.key_file, "rb").read().decode("ascii", "strict").strip().encode()
    if not re.fullmatch(rb"[A-Za-z0-9._~-]+", key):
        fail("key contains characters that are not safe in a URL/JS template")

    data = bytearray(open(args.input, "rb").read())

    if PATCHED_MARK in data:
        fail("input is already patched (tile URL already has ?key=). Patch the original binary instead.")
    for name, needle in (("tile URL", OLD_URL), ("colour table k", OLD_K), ("colour table x", X_DEF)):
        n = data.count(needle)
        if n != 1:
            fail(f"expected exactly 1 {name}, found {n}; app version changed, patch needs review")

    k_pos = data.find(OLD_K)
    url_pos = data.find(OLD_URL)
    x_pos = data.find(X_DEF)
    c_start, c_end = chunk_bounds(data, url_pos)
    if not (c_start <= x_pos < k_pos < url_pos < c_end):
        fail("unexpected layout: x, k and the tile URL are not in order within one embedded file")

    win_start, win_end = k_pos, url_pos + len(OLD_URL)
    old_win = bytes(data[win_start:win_end])
    middle = old_win[len(OLD_K):len(old_win) - len(OLD_URL)]  # ",j=...,S={...}," untouched
    new_url = URL_PREFIX + b"?key=" + key + b"`"
    pad = len(old_win) - (len(NEW_K) + len(middle) + len(new_url))
    if pad < 0:
        fail(f"key is {-pad} bytes too long to fit (max key length {len(key) + pad})")
    new_win = NEW_K + b" " * pad + middle + new_url
    assert len(new_win) == len(old_win)
    data[win_start:win_end] = new_win

    # Verify: same size, only the window changed, embedded file still parses.
    orig = open(args.input, "rb").read()
    assert len(data) == len(orig)
    assert data[:win_start] == orig[:win_start] and data[win_end:] == orig[win_end:]
    assert chunk_bounds(data, url_pos) == (c_start, c_end)

    node = shutil.which("node") or shutil.which("nodejs")
    if node:
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as tf:
            tf.write(bytes(data[c_start:c_end]))
        r = subprocess.run([node, "--check", tf.name], capture_output=True, text=True)
        os.unlink(tf.name)
        if r.returncode != 0:
            fail("patched JavaScript failed to parse:\n" + r.stderr)
        print("JS syntax check: OK")
    else:
        print("JS syntax check: skipped (node not found)")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    tmp = args.output + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o755)
    os.replace(tmp, args.output)

    shown = new_url.decode().replace(key.decode(), key[:4].decode() + "…")
    print(f"Changed {len(new_win)} bytes at offset {win_start} (embedded file {c_start}-{c_end}, size unchanged)")
    print("New tile URL: " + shown)
    print("Wrote " + args.output)
    print(f"Install with:\n  sudo install -m 755 '{args.output}' {DEFAULT_INPUT}")


if __name__ == "__main__":
    main()
