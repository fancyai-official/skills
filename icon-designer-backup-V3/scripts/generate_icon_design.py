#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Icon Designer prompt builder.

Remote image generation, polling, download, and file publishing logic has been removed.
This script only builds prompts for the host environment's image generation capability.
"""

import argparse
import json
import os


DESIGNER_DIRECTIVES = {
    "coco chanel": "Liberation through simplicity: relaxed structure, tweed, jersey, pearls, black/white/navy/beige, practical elegance.",
    "alexander mcqueen": "Romantic brutalism: sharp tailoring, gothic romance, dramatic volume, black/blood red/bone white, savage beauty.",
    "giorgio armani": "The power of restraint: soft deconstruction, fluid tailoring, greige/navy/taupe, quiet authority.",
    "valentino garavani": "Couture drama: Valentino red, romance, opera-level glamour, lace, silk gazar, grand gestures.",
    "christian dior": "The New Look: cinched waist, rounded shoulders, full skirt, flower-like femininity, architectural construction.",
    "yves saint laurent": "Borrowed wardrobe as power: Le Smoking, safari, trench, art references, masculine structure with sensual femininity.",
}


SHOT_DIRECTIVES = {
    "front": "Front view, full body, model facing camera directly, complete outfit visible from head to shoes.",
    "side": "Side view, profile angle, same garment and model identity as the front reference.",
    "back": "Back view, full body from behind, same garment and model identity as the front reference.",
}


QUALITY_DIRECTIVE = (
    "Photorealistic professional fashion lookbook image. Sharp focus, natural skin texture, "
    "accurate fabric drape, clean studio backdrop, no text, no watermark, no AI artifacts."
)


def build_prompt(args: argparse.Namespace) -> str:
    designer_key = (args.designer or "").strip().lower()
    designer_block = DESIGNER_DIRECTIVES.get(
        designer_key,
        f"Design in the aesthetic philosophy of {args.designer}."
    )

    parts = [
        f"Professional fashion lookbook photograph designed by {args.designer}.",
        SHOT_DIRECTIVES[args.shot],
        f"Piece: {args.piece_name}" if args.piece_name else "",
        f"Category: {args.category}" if args.category else "",
        f"Silhouette: {args.silhouette}" if args.silhouette else "",
        f"Material: {args.materials}" if args.materials else "",
        f"Colorway: {args.palette}" if args.palette else "",
        f"Construction: {args.construction}" if args.construction else "",
        f"Signature elements: {args.signatures}" if args.signatures else "",
        f"Styling: {args.styling}" if args.styling else "",
        f"Gender: {args.gender}" if args.gender else "",
        f"Designer DNA: {designer_block}",
        QUALITY_DIRECTIVE,
    ]
    return "\n".join(part for part in parts if part)


def write_output(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build icon-designer image prompts.")
    parser.add_argument("--designer", required=True)
    parser.add_argument("--shot", default="front", choices=["front", "side", "back"])
    parser.add_argument("--piece_name", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--silhouette", default="")
    parser.add_argument("--materials", default="")
    parser.add_argument("--palette", default="")
    parser.add_argument("--construction", default="")
    parser.add_argument("--signatures", default="")
    parser.add_argument("--styling", default="")
    parser.add_argument("--gender", default="")
    parser.add_argument("--ratio", default="3:4")
    parser.add_argument("--resolution", default="2K")
    parser.add_argument("--reference", nargs="*", default=[])
    parser.add_argument("--face_lock", default=None)
    parser.add_argument("--output", default=None, help="Optional JSON file for the generated prompt payload.")
    args = parser.parse_args()

    payload = {
        "prompt": build_prompt(args),
        "shot": args.shot,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "references": args.reference,
        "face_lock": args.face_lock,
    }

    if args.output:
        write_output(args.output, payload)
        print(f"[PROMPT_FILE] {args.output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
