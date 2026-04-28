#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Image Compressor — compress local product images for efficient
Claude vision analysis.

Resizes images to fit within 1024x1024, converts to JPEG (quality 100),
and progressively shrinks if the file exceeds 1 MB.

Usage:
  python3 compress_product_img.py --images "/local/path.jpg" "/local/path-2.png"

Output per image:
  [COMPRESSED] /tmp/compressed_product_20260327143015_a1b2c3d4e5f6.jpg (1200KB -> 450KB, 1024x768)
"""

import argparse
import io
import os
import sys
import uuid
from datetime import datetime

from PIL import Image, ImageOps

MAX_DIM = 1024
MAX_BYTES = 148_480  # 145 KB — must stay under SDK's ~146.5KB Read tool limit
OUTPUT_DIR = "/tmp"

def load_image_bytes(src: str) -> bytes | None:
    if src.startswith(("http://", "https://")):
        print(f"[Error] Remote URLs are disabled: {src}")
        return None
    if os.path.isfile(src):
        with open(src, "rb") as f:
            return f.read()
    print(f"[Error] Not a valid local file path: {src}")
    return None


def compress(raw: bytes) -> tuple[bytes, int, int]:
    """Return (jpeg_bytes, width, height) after resize + JPEG conversion."""
    img = Image.open(io.BytesIO(raw))
    img = ImageOps.exif_transpose(img) or img

    orig_w, orig_h = img.size

    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    if orig_w > MAX_DIM or orig_h > MAX_DIM:
        ratio = min(MAX_DIM / orig_w, MAX_DIM / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    result = buf.getvalue()

    quality = 75
    scale = 0.9
    while len(result) > MAX_BYTES and (quality >= 30 or scale >= 0.3):
        target_w = max(1, round(min(orig_w, MAX_DIM) * scale))
        target_h = max(1, round(min(orig_h, MAX_DIM) * scale))
        resized = Image.open(io.BytesIO(raw))
        resized = ImageOps.exif_transpose(resized) or resized
        if resized.mode in ("RGBA", "P", "LA"):
            resized = resized.convert("RGB")
        resized = resized.resize((target_w, target_h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        resized.save(buf, format="JPEG", quality=quality)
        result = buf.getvalue()
        if quality > 30:
            quality -= 10
        else:
            scale -= 0.1

    final = Image.open(io.BytesIO(result))
    return result, final.width, final.height


def main():
    parser = argparse.ArgumentParser(
        description="Compress product images for Claude vision analysis"
    )
    parser.add_argument(
        "--images", nargs="+", required=True,
        help="One or more local image file paths"
    )
    args = parser.parse_args()

    for idx, src in enumerate(args.images):
        raw = load_image_bytes(src)
        if raw is None:
            print(f"[ERROR] Could not load: {src}")
            continue

        orig_kb = len(raw) // 1024
        try:
            jpeg_bytes, w, h = compress(raw)
        except Exception as e:
            print(f"[ERROR] Compression failed for {src}: {e}")
            continue

        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        out_path = os.path.join(OUTPUT_DIR, f"compressed_product_{ts}_{uuid.uuid4().hex[:12]}.jpg")
        with open(out_path, "wb") as f:
            f.write(jpeg_bytes)

        comp_kb = len(jpeg_bytes) // 1024
        print(f"[COMPRESSED] {out_path} ({orig_kb}KB -> {comp_kb}KB, {w}x{h})")


if __name__ == "__main__":
    main()
