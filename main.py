#!/usr/bin/env python3
"""THE TUESDAY ATLAS - MakeFun entry carrier for Akun 10
(@sindyariana115203), news-image-20261124, Wave 1.

Stdlib-only copy-only carrier: verifies the PNG signature and the IHDR
dimensions and REFUSES to ship an image that breaks the 1024x1024 gate,
copies entry.png byte-for-byte into MAKEFUN_OUTPUT_DIR (fallback
/output), then verifies the copy is byte-identical. No network, no
imports beyond the standard library.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def fail(message):
    sys.stderr.write("main.py: refusing to ship: %s\n" % message)
    sys.exit(1)


def main():
    if not os.path.isfile(SRC):
        fail("entry.png missing next to main.py")
    with open(SRC, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1048576 byte gate" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG (bad signature)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where expected")
    width, height = struct.unpack(">II", data[16:24])
    if width != MAX_SIDE or height != MAX_SIDE:
        fail("entry.png is %dx%d, gate needs exactly 1024x1024" % (width, height))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    with open(dest, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        fail("output copy differs from entry.png")
    sys.stdout.write(
        "main.py: shipped entry.png %dx%d %d bytes sha256=%s\n"
        % (width, height, len(data), hashlib.sha256(data).hexdigest())
    )


if __name__ == "__main__":
    main()
