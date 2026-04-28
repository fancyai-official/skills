"""
Phase 7: Xiaohongshu-Style Subtitle Burning Tool (Pillow + ffmpeg overlay)

Uses Pillow to render subtitle layers (with color emoji support), overlaid onto video via ffmpeg overlay filter.
Falls back to ffmpeg ASS subtitle filter if Pillow is unavailable (emoji may not display correctly).

Subtitle style (Xiaohongshu aesthetic):
  - CJK font: Hiragino Sans GB (macOS system font)
  - Emoji font: Apple Color Emoji (color rendering)
  - Font size: video height × 4.5% (≥ 48px)
  - Color: white text + black stroke, centered in bottom safe zone

Usage:
    python3 add_subtitles.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp}
    python3 add_subtitles.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp} --font-size 72

Dependencies: ffmpeg (system PATH or imageio-ffmpeg), Pillow (pip install pillow)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Pillow detection ───────────────────────────────────────────────
try:
    from PIL import Image, ImageDraw, ImageFont
    import PIL as _pil_module
    _pil_ver = tuple(int(x) for x in _pil_module.__version__.split(".")[:2])
    HAS_PILLOW = True
    HAS_EMBEDDED_COLOR = _pil_ver >= (9, 2)   # embedded_color for color emoji
    HAS_STROKE = _pil_ver >= (6, 2)            # stroke_width / stroke_fill
except ImportError:
    HAS_PILLOW = False
    HAS_EMBEDDED_COLOR = False
    HAS_STROKE = False


# ── ffmpeg path resolution ───────────────────────────────────────────
def _find_ffmpeg() -> str:
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    raise FileNotFoundError(
        "ffmpeg not found. Please run: brew install ffmpeg or pip install imageio-ffmpeg"
    )


FFMPEG_BIN = _find_ffmpeg()


# ── Font paths (macOS) ────────────────────────────────────────────────
# CJK font candidates: (path, TTC index)
# Prefer Alibaba PuHuiTi 3.0; fall back to system fonts
_CN_FONT_CANDIDATES: list[tuple[str, int]] = [
    ("/Users/fancy/Library/Fonts/AlibabaPuHuiTi-3-55-Regular.otf", 0),  # Alibaba PuHuiTi 3.0 ← preferred
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 1),   # Bold/W6 ← fallback
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),   # Regular/W3
    ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 0),
]
_EMOJI_FONT_PATH = "/System/Library/Fonts/Apple Color Emoji.ttc"

# Font name used in ASS fallback mode
_ASS_FONT_NAME = "AlibabaPuHuiTi"


# ── Emoji character detection ─────────────────────────────────────────
def _is_emoji_char(ch: str) -> bool:
    """Determine whether a single character is an emoji or emoji modifier."""
    cp = ord(ch)
    return (
        0x1F000 <= cp <= 0x1FFFF  # Main emoji block
        or 0x2600 <= cp <= 0x27BF  # Misc symbols & Dingbats
        or 0x2B00 <= cp <= 0x2BFF  # Misc symbols (extended)
        or 0x2300 <= cp <= 0x23FF  # Technical symbols (⭐ etc.)
        or 0xFE00 <= cp <= 0xFE0F  # Variation selectors
        or cp == 0x200D             # ZWJ (zero-width joiner)
    )


def split_text_runs(text: str) -> list[tuple[str, bool]]:
    """Split text into alternating list of (segment content, is_emoji)."""
    if not text:
        return []
    runs: list[tuple[str, bool]] = []
    i = 0
    while i < len(text):
        is_em = _is_emoji_char(text[i])
        j = i + 1
        while j < len(text) and _is_emoji_char(text[j]) == is_em:
            j += 1
        runs.append((text[i:j], is_em))
        i = j
    return runs


# ── Emoji auto-append ─────────────────────────────────────────────────
_EMOJI_RULES: list[tuple[list[str], str]] = [
    (["unboxing", "package", "delivery", "box", "parcel"],              "📦"),
    (["tear", "tape", "seal", "unwrap"],                                 "✂️"),
    (["lining", "tissue", "filled", "packed", "cushion"],               "😍"),
    (["surprise", "unexpected", "shocked", "omg", "wow"],               "😱"),
    (["beautiful", "gorgeous", "stunning", "pretty", "lovely"],         "✨"),
    (["texture", "bottle", "feel", "quality", "luxurious"],             "💎"),
    (["fragrance", "scent", "floral", "smells", "aroma"],               "🌸"),
    (["recommend", "must buy", "must-have", "perfect", "love it"],      "💯"),
    (["amazing", "incredible", "obsessed", "game changer"],             "🔥"),
    (["shaking", "excited", "can't believe", "freaking out"],           "😅"),
    (["appearance", "look", "aesthetic", "vibe", "glowy"],              "😍"),
    (["finally", "waited", "worth the wait", "at last"],                "❤️"),
    (["flat lay", "overview", "display", "layout", "arrangement"],      "👇"),
]

_EMOJI_RE = re.compile(
    r"[\U0001F000-\U0001FFFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF\uFE00-\uFE0F\u200D]+",
    re.UNICODE,
)


def _has_emoji(text: str) -> bool:
    return bool(_EMOJI_RE.search(text))


_PUNCTUATION_TO_STRIP = set("！!？?。，,、；;：:…—～~「」『』【】《》〈〉""''（）()[]{}·")

def strip_punctuation(text: str) -> str:
    """Remove punctuation from text (keep emoji and alphanumerics) for cleaner, more natural subtitles."""
    return "".join(ch for ch in text if ch not in _PUNCTUATION_TO_STRIP)


def enrich_with_emoji(text: str) -> str:
    """If the copy text doesn't end with an emoji, auto-append a relevant emoji based on keywords."""
    if _has_emoji(text):
        return text
    for keywords, emoji in _EMOJI_RULES:
        if any(kw in text for kw in keywords):
            return text + emoji
    return text + "✨"


def wrap_text(text: str, max_chars: int = 12) -> str:
    """Auto-wrap text if single line exceeds max_chars.
    - First split by existing \\N, then evaluate each segment independently
    - Count rule: each character (including emoji) counts as 1
    - Wrap point: split roughly in half to avoid large line imbalances (e.g., 16 chars → 8+8 not 12+4)
    """
    segments = text.split(r"\N")
    result = []
    for seg in segments:
        if len(seg) <= max_chars:
            result.append(seg)
        else:
            mid = len(seg) // 2
            result.append(seg[:mid])
            result.append(seg[mid:])
    return r"\N".join(result)


# ── Utility functions ───────────────────────────────────────────────────
def parse_duration(s: str) -> float:
    try:
        return float(str(s).replace("s", "").strip())
    except ValueError:
        return 3.0


def get_video_size(video_path: Path) -> tuple[int, int]:
    """Return actual video (width, height); returns default (1080, 1440) on failure."""
    try:
        r = subprocess.run(
            [FFMPEG_BIN, "-hide_banner", "-i", str(video_path)],
            capture_output=True, text=True,
        )
        m = re.search(r"(\d{3,5})x(\d{3,5})(?:\s|,|\[)", r.stderr)
        if m:
            return int(m.group(1)), int(m.group(2))
    except Exception:
        pass
    return 1080, 1440


def probe_video_duration(video_path: Path) -> float:
    """Probe actual video duration (seconds) using ffmpeg -i; returns 0.0 on failure."""
    try:
        r = subprocess.run(
            [FFMPEG_BIN, "-hide_banner", "-i", str(video_path)],
            capture_output=True, text=True,
        )
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr)
        if m:
            h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
            return h * 3600 + mi * 60 + s
    except Exception:
        pass
    return 0.0


def has_audio_stream(video_path: Path) -> bool:
    r = subprocess.run(
        [FFMPEG_BIN, "-hide_banner", "-i", str(video_path)],
        capture_output=True, text=True,
    )
    return "Audio:" in r.stderr


# ── Pillow subtitle rendering ───────────────────────────────────────────
# Apple Color Emoji supported bitmap sizes (fixed list)
_EMOJI_SUPPORTED_SIZES = [20, 32, 40, 48, 64, 96, 160]


def _nearest_emoji_size(font_size: int) -> int:
    """Snap font size to the nearest Apple Color Emoji supported size (≤ font_size preferred)."""
    candidates = [s for s in _EMOJI_SUPPORTED_SIZES if s <= font_size]
    if candidates:
        return max(candidates)
    return _EMOJI_SUPPORTED_SIZES[0]


def _load_fonts(font_size: int):
    """Load CJK font and emoji font; returns (cn_font, emoji_font|None)."""
    cn_font = None
    for path, idx in _CN_FONT_CANDIDATES:
        if Path(path).exists():
            try:
                cn_font = ImageFont.truetype(path, font_size, index=idx)
                print(f"CJK font: {Path(path).name} (index={idx})")
                break
            except Exception:
                continue
    if cn_font is None:
        print("Warning: CJK font not found; using built-in default font (may not support CJK characters)")
        cn_font = ImageFont.load_default()

    emoji_font = None
    if Path(_EMOJI_FONT_PATH).exists():
        emoji_size = _nearest_emoji_size(font_size)
        try:
            emoji_font = ImageFont.truetype(_EMOJI_FONT_PATH, emoji_size)
            print(
                f"Emoji font: Apple Color Emoji "
                f"({emoji_size}px, CJK font size {font_size}px, "
                f"embedded_color={'supported' if HAS_EMBEDDED_COLOR else 'not supported'})"
            )
        except Exception as e:
            print(f"Warning: Apple Color Emoji failed to load: {e}")
    else:
        print("Note: Apple Color Emoji.ttc not found; emoji will render with CJK font")

    return cn_font, emoji_font


def _measure_line(
    line: str,
    draw: ImageDraw.ImageDraw,
    cn_font: ImageFont.FreeTypeFont,
    emoji_font: ImageFont.FreeTypeFont | None,
) -> tuple[int, int]:
    """Return (total width, max height) for a single line of text."""
    total_w, max_h = 0, 0
    for seg, is_em in split_text_runs(line):
        font = emoji_font if (is_em and emoji_font) else cn_font
        try:
            bbox = draw.textbbox((0, 0), seg, font=font)
            total_w += bbox[2] - bbox[0]
            max_h = max(max_h, bbox[3] - bbox[1])
        except Exception:
            total_w += len(seg) * (font.size if hasattr(font, "size") else 48)
            max_h = max(max_h, font.size if hasattr(font, "size") else 48)
    return total_w, max_h


def render_subtitle_frame(
    text: str,
    width: int,
    height: int,
    font_size: int,
    margin_v: int,
    cn_font: ImageFont.FreeTypeFont,
    emoji_font: ImageFont.FreeTypeFont | None,
) -> Image.Image:
    """Render subtitle text as a full-size RGBA transparent image."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Split into multiple lines by \N (from " / " conversion)
    lines = text.split(r"\N")
    line_height = int(font_size * 1.25)
    total_text_h = len(lines) * line_height

    # Start from margin_v pixels above the bottom edge within the safe zone
    base_y = height - margin_v - total_text_h
    outline_w = max(2, font_size // 22)

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        line_w, _ = _measure_line(line, draw, cn_font, emoji_font)
        start_x = max(20, (width - line_w) // 2)
        line_y = base_y + i * line_height
        cursor_x = start_x

        for seg, is_em in split_text_runs(line):
            font = emoji_font if (is_em and emoji_font) else cn_font
            try:
                bbox = draw.textbbox((0, 0), seg, font=font)
                seg_w = bbox[2] - bbox[0]
                y_offset = max(0, bbox[1])  # Correct for font top-embedded space
            except Exception:
                seg_w = len(seg) * font_size
                y_offset = 0

            x = cursor_x
            y = line_y - y_offset

            if is_em and emoji_font and HAS_EMBEDDED_COLOR:
                # Color emoji rendering
                try:
                    draw.text((x, y), seg, font=emoji_font, embedded_color=True)
                except Exception:
                    draw.text((x, y), seg, font=cn_font, fill=(255, 255, 255, 255))
            else:
                # CJK / ASCII: white text + black stroke
                if HAS_STROKE:
                    draw.text(
                        (x, y), seg, font=font,
                        fill=(255, 255, 255, 255),
                        stroke_width=outline_w,
                        stroke_fill=(0, 0, 0, 210),
                    )
                else:
                    for dx in range(-outline_w, outline_w + 1):
                        for dy in range(-outline_w, outline_w + 1):
                            if dx != 0 or dy != 0:
                                draw.text((x + dx, y + dy), seg, font=font,
                                          fill=(0, 0, 0, 210))
                    draw.text((x, y), seg, font=font, fill=(255, 255, 255, 255))

            cursor_x += seg_w

    return img


# ── Pillow mode: render + ffmpeg overlay ─────────────────────────
def burn_with_pillow(
    shots: list[dict],
    input_video: Path,
    output_video: Path,
    width: int,
    height: int,
    font_size: int,
    margin_v: int,
    tmp_dir: Path,
    time_scale: float = 1.0,
) -> bool:
    """Render subtitle layers using Pillow, then overlay via ffmpeg. Returns whether successful.
    time_scale: timestamp scaling ratio for B-2 coherent full-film mode (actual_dur / json_total_dur).
    """
    cn_font, emoji_font = _load_fonts(font_size)

    # Render subtitle PNGs per shot
    subtitle_entries: list[tuple[float, float, Path]] = []
    current_t = 0.0

    for i, shot in enumerate(shots):
        dur = parse_duration(shot.get("duration", "3s")) * time_scale
        raw_copy = shot.get("copy", "").strip()
        end_t = current_t + dur

        if raw_copy:
            enriched = enrich_with_emoji(strip_punctuation(raw_copy))
            # " / " → newline
            text = enriched.replace(" / ", r"\N").replace(" /", r"\N").replace("/ ", r"\N")
            text = wrap_text(text)   # Auto-wrap if over 12 chars

            img = render_subtitle_frame(
                text, width, height, font_size, margin_v, cn_font, emoji_font
            )
            png_path = tmp_dir / f"sub_{i:02d}.png"
            img.save(str(png_path), "PNG")
            subtitle_entries.append((current_t, end_t, png_path))
            print(f"  {shot.get('shot_num','?'):8s}  {enriched[:32]}")

        current_t += dur

    if not subtitle_entries:
        print("No subtitles to render, skipping.")
        return True

    # Build ffmpeg filter_complex overlay chain
    # inputs: [0]=video, [1]=sub_0, [2]=sub_1, ...
    extra_inputs: list[str] = []
    for _, _, png in subtitle_entries:
        extra_inputs += ["-i", str(png)]

    filter_parts: list[str] = []
    prev_tag = "0:v"
    for idx, (start, end, _) in enumerate(subtitle_entries):
        in_tag = idx + 1
        out_tag = f"ov{idx}"
        filter_parts.append(
            f"[{prev_tag}][{in_tag}:v]"
            f"overlay=0:0:enable='between(t,{start:.3f},{end:.3f})'"
            f"[{out_tag}]"
        )
        prev_tag = out_tag

    filter_complex = ";".join(filter_parts)
    video_has_audio = has_audio_stream(input_video)

    cmd = [
        FFMPEG_BIN, "-y",
        "-i", str(input_video),
        *extra_inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{prev_tag}]",
    ]
    if video_has_audio:
        cmd += ["-map", "0:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "fast", str(output_video)]

    print(f"\nBurning subtitles ({len(subtitle_entries)} entries, Pillow color emoji mode)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: ffmpeg execution failed:\n{result.stderr[-3000:]}")
        return False
    return True


# ── ASS fallback mode ───────────────────────────────────────────────────
def _seconds_to_ass(t: float) -> str:
    h, rem = divmod(max(0.0, t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{int(s):02d}.{int(round((s % 1) * 100)):02d}"


def burn_with_ass(
    shots: list[dict],
    input_video: Path,
    output_video: Path,
    width: int,
    height: int,
    font_size: int,
    margin_v: int,
    tmp_dir: Path,
    time_scale: float = 1.0,
) -> bool:
    """ASS fallback mode (used when Pillow is unavailable; emoji may not display correctly).
    time_scale: timestamp scaling ratio for B-2 coherent full-film mode (actual_dur / json_total_dur).
    """
    header = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {width}\nPlayResY: {height}\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{_ASS_FONT_NAME},{font_size},"
        "&H00FFFFFF,&H000000FF,&H00000000,&H64000000,"
        "-1,0,0,0,100,100,2,0,1,3,2,2,20,20,"
        f"{margin_v},1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events: list[str] = [header]
    current_t = 0.0
    for shot in shots:
        dur = parse_duration(shot.get("duration", "3s")) * time_scale
        raw_copy = shot.get("copy", "").strip()
        end_t = current_t + dur
        if raw_copy:
            enriched = enrich_with_emoji(strip_punctuation(raw_copy))
            text = enriched.replace(" / ", r"\N").replace("/", r"\N")
            text = wrap_text(text)   # Auto-wrap if over 12 chars
            events.append(
                f"Dialogue: 0,{_seconds_to_ass(current_t)},{_seconds_to_ass(end_t)},"
                f"Default,,0,0,0,,{text}"
            )
        current_t += dur

    ass_path = tmp_dir / "subtitles.ass"
    ass_path.write_text("\n".join(events), encoding="utf-8")

    cmd = [
        FFMPEG_BIN, "-y",
        "-i", str(input_video),
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy",
        str(output_video),
    ]
    print("\nBurning subtitles (ASS fallback mode)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: ffmpeg execution failed:\n{result.stderr[-2000:]}")
        return False
    return True


# ── Main flow ────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Xiaohongshu-style subtitle burning tool (Pillow color emoji)")
    parser.add_argument("json_file", help="Path to storyboard_data.json")
    parser.add_argument("--batch-dir", required=True, help="Batch output directory (containing final_video_mixed.mp4)")
    parser.add_argument("--font-size", type=int, default=0, help="Font size (px); auto-calculated from video height if 0")
    args = parser.parse_args()

    batch_dir = Path(args.batch_dir).resolve()
    json_path = Path(args.json_file).resolve()

    # Input video detection (checked in priority order):
    # 1. final_video_mixed.mp4          — B-1 per-shot after audio mixing
    # 2. final_video_coherent_mixed.mp4 — B-2 coherent film after audio mixing (Phase 6 not skipped)
    # 3. final_video_coherent.mp4       — B-2 coherent film with native audio (Phase 6 skipped; burn subs directly)
    # 4. final_video.mp4                — Per-shot concat without mixing (fallback)
    _candidates = [
        batch_dir / "final_video_mixed.mp4",
        batch_dir / "final_video_coherent_mixed.mp4",
        batch_dir / "final_video_coherent.mp4",
        batch_dir / "final_video.mp4",
    ]
    input_video = next((p for p in _candidates if p.exists()), None)
    if input_video is None:
        print(f"ERROR: No usable input video found (checked: {[p.name for p in _candidates]})\nPath: {batch_dir}")
        sys.exit(1)
    if not input_video.name.endswith("_mixed.mp4"):
        print(f"Note: Mixed video not found; using {input_video.name} as subtitle input")

    # Output path derived from input filename to maintain naming consistency
    # final_video_mixed.mp4          → final_video_subtitled.mp4
    # final_video_coherent_mixed.mp4 → final_video_coherent_subtitled.mp4
    # final_video.mp4                → final_video_subtitled.mp4
    stem = input_video.stem  # e.g. "final_video_mixed" or "final_video_coherent_mixed"
    if stem.endswith("_mixed"):
        output_stem = stem[:-len("_mixed")] + "_subtitled"
    else:
        output_stem = stem + "_subtitled"
    output_video = batch_dir / f"{output_stem}.mp4"

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    shots = data.get("shots", [])
    if not shots:
        print("ERROR: No shots data found in JSON.")
        sys.exit(1)

    has_copy = any(s.get("copy", "").strip() for s in shots)
    if not has_copy:
        print("Note: All shot copy fields are empty. Skipping subtitle burning.")
        sys.exit(0)

    width, height = get_video_size(input_video)
    font_size = args.font_size if args.font_size > 0 else max(48, int(height * 0.045))
    margin_v = max(120, int(height * 0.15))   # Safe zone: bottom 15%

    subtitle_count = sum(1 for s in shots if s.get("copy", "").strip())
    json_total_dur = sum(parse_duration(s.get("duration", "3s")) for s in shots)

    # B-2 coherent full-film mode: actual duration may differ from JSON cumulative duration;
    # scale subtitle timestamps proportionally
    is_coherent = "coherent" in input_video.stem
    time_scale = 1.0
    if is_coherent and json_total_dur > 0:
        actual_dur = probe_video_duration(input_video)
        if actual_dur > 0:
            time_scale = actual_dur / json_total_dur
            print(
                f"B-2 Coherent Full-Film Mode: actual duration {actual_dur:.1f}s / "
                f"JSON cumulative duration {json_total_dur:.1f}s → subtitle timestamp scale factor {time_scale:.3f}"
            )
        else:
            print("Note: Unable to probe actual video duration; using JSON original timestamps")
    total_dur = json_total_dur * time_scale  # For summary display

    print(f"\nVideo dimensions: {width}×{height}  Font size: {font_size}px  MarginV: {margin_v}px")
    print(f"Pillow: {'available v' + _pil_module.__version__ if HAS_PILLOW else 'unavailable (will use ASS fallback)'}")
    print(f"Subtitle count: {subtitle_count} entries / {total_dur:.0f}s"
          + (f" (JSON {json_total_dur:.0f}s × {time_scale:.3f})" if time_scale != 1.0 else ""))
    print("── Subtitle preview ──")

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

        if HAS_PILLOW:
            success = burn_with_pillow(
                shots, input_video, output_video,
                width, height, font_size, margin_v, tmp_dir,
                time_scale=time_scale,
            )
        else:
            print("Pillow unavailable; using ASS fallback mode (emoji may not display correctly)")
            success = burn_with_ass(
                shots, input_video, output_video,
                width, height, font_size, margin_v, tmp_dir,
                time_scale=time_scale,
            )

    if not success:
        sys.exit(1)

    file_size = output_video.stat().st_size / 1024 / 1024
    print(f"\n✅ Subtitle burning complete!")
    print(f"Output file: {output_video}")
    print(f"File size: {file_size:.1f} MB ({total_dur:.0f}s, {subtitle_count} subtitle entries)")
    print(f"Render mode: {'Pillow color emoji' if HAS_PILLOW else 'ASS fallback'}")


if __name__ == "__main__":
    main()
