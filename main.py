#!/usr/bin/env python3
"""news-23 b138 heroes-scene: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to
MAKEFUN_OUTPUT_DIR, which the grader sets to a directory outside the repo.
Validates the PNG strictly before copying: signature, IHDR geometry
(1024x1024, bit depth 8, colour type 2 or 6), zero compression/filter/
interlace bytes, per-chunk CRCs, non-empty IDAT payload, IEND last with
no trailing data, and size within 10_000..1_048_576 bytes.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "f7e1c394276e5347f7f555470a23c4cec5b082882d36a9763d167736438bb790"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576
MIN_IDAT_PAYLOAD = 1000


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Validate PNG bytes; return (width, height) or exit(1)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 8 + 25:
        fail("file too short for IHDR")
    # chunk layout: 4-byte length, 4-byte type, data, 4-byte CRC;
    # the next chunk starts 12 bytes after the length field plus data len.
    # Note: the stored CRC covers type + data only (not the length field),
    # and the chunk after IEND must not exist, so IEND must end exactly
    # at the end of the file.
    pos = 8
    first = True
    idat_total = 0
    seen_iend = False
    while True:
        if pos + 8 > len(data):
            fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[pos + 8:pos + 8 + clen]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        crc_calc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail(f"{ctype.decode('latin1')} CRC mismatch")
        if first:
            if ctype != b"IHDR":
                fail("first chunk is not IHDR")
            if clen != 13:
                fail("IHDR length is not 13")
            w, h, depth, ctype_n, comp, filt, inter = struct.unpack(
                ">IIBBBBB", chunk_data)
            if (w, h) != (1024, 1024):
                fail(f"bad dimensions {w}x{h}, want 1024x1024")
            if depth != 8:
                fail(f"bad bit depth {depth}, want 8")
            if ctype_n not in (2, 6):
                fail(f"bad colour type {ctype_n}, want 2 or 6")
            if comp != 0 or filt != 0 or inter != 0:
                fail("compression/filter/interlace must be 0")
            first = False
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be empty")
            if pos + 12 + clen != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if first:
        fail("no IHDR chunk")
    if not seen_iend:
        fail("no IEND chunk")
    if idat_total < MIN_IDAT_PAYLOAD:
        fail(f"IDAT payload too small ({idat_total} bytes)")
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        fail(f"entry.png not found next to main.py ({src})")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) < MIN_BYTES:
        fail(f"entry.png too small ({len(data)} bytes)")
    if len(data) > MAX_BYTES:
        fail(f"entry.png too large ({len(data)} bytes)")
    check_png(data)
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        fail(f"sha256 mismatch: got {sha}, want {EXPECTED_SHA256}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if os.path.commonpath([out_dir_abs, here_abs]) == here_abs:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.isfile(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output differs from source after copy")
    print(f"wrote {dst} ({len(data)} bytes, sha256 {sha})")


if __name__ == "__main__":
    main()
