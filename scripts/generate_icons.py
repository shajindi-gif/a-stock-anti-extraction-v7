#!/usr/bin/env python3
"""Generate PNG icons for Chrome extension (stdlib only)."""

import struct
import zlib
from pathlib import Path

COLORS = {
    16: (31, 111, 235),
    48: (31, 111, 235),
    128: (88, 166, 255),
}


def write_png(path: Path, size: int, rgb: tuple[int, int, int]) -> None:
    r, g, b = rgb
    raw = b""
    for _ in range(size):
        raw += b"\x00" + bytes([r, g, b] * size)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "chrome_extension" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    for size, color in COLORS.items():
        write_png(out / f"icon{size}.png", size, color)
        print(f"Created icon{size}.png")


if __name__ == "__main__":
    main()
