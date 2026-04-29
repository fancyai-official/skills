"""
Storyboard Video Concatenation Tool

Concatenates shot clips under the batch directory in the order defined by storyboard_data.json.
Automatically reads the `transition` field for each shot and applies the corresponding transition effect.

Transition mapping rules:
  Cut / Seamless → hard cut (no effect)
  Dissolve       → crossfade dissolve 0.5s
  Fade to Black  → fade out to black at end 0.5s
  Slide          → slide left 0.5s (ffmpeg xfade=slideleft)

Usage:
    python concat_videos.py output/storyboard_data.json --batch-dir output/{ProductName}/{timestamp}
    python concat_videos.py output/storyboard_data.json  # auto-find latest batch

Dependencies (ffmpeg xfade preferred; moviepy as fallback):
    pip install moviepy==1.0.3
    brew install ffmpeg  (macOS, recommended)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TRANSITION_DURATION = 0.5  # transition duration in seconds


# ── ffmpeg binary path resolution ───────────────────────────────────
def _find_ffmpeg() -> str:
    """Use system PATH ffmpeg first; fall back to imageio_ffmpeg bundled binary."""
    import shutil
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    raise FileNotFoundError(
        "ffmpeg not found. Please run: brew install ffmpeg\n"
        "or: pip install imageio-ffmpeg"
    )


FFMPEG_BIN = _find_ffmpeg()

# Canonical transition name → ffmpeg xfade effect mapping
FFMPEG_XFADE: dict[str, str] = {
    "dissolve":      "dissolve",
    "fade to black": "fadeblack",
    "slide":         "slideleft",
}

# English canonical normalization
TRANSITION_NORMALIZE: dict[str, str] = {
    "dissolve": "dissolve", "fade to black": "fade to black",
    "fade black": "fade to black", "fadeblack": "fade to black",
    "slide": "slide", "slide left": "slide", "slide push": "slide",
    "slideleft": "slide", "cut": "cut", "seamless": "cut",
}


def normalize_transition(raw: str) -> str:
    """Normalize Chinese/English transition names to canonical English form."""
    return TRANSITION_NORMALIZE.get(raw.strip().lower(), "cut")


# ── Utility functions ────────────────────────────────────────────────

def find_latest_batch(product_name: str, output_root: Path) -> Path | None:
    """Auto-find the latest batch directory."""
    product_dir = output_root / product_name
    if not product_dir.exists():
        return None
    batches = sorted(
        [d for d in product_dir.iterdir() if d.is_dir() and (d / "videos").exists()],
        reverse=True,
    )
    return batches[0] if batches else None


def _probe_duration(path: str) -> float:
    """Probe video duration via ffmpeg -i (no separate ffprobe needed)."""
    try:
        result = subprocess.run(
            [FFMPEG_BIN, "-i", path],
            capture_output=True, text=True,
        )
        for line in result.stderr.splitlines():
            if "Duration:" in line:
                # Format: "  Duration: HH:MM:SS.ss, start: ..."
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
    except Exception:
        pass
    return 0.0


# ── ffmpeg concatenation (preferred, supports xfade) ────────────────

def concat_with_ffmpeg(video_paths: list, transitions: list, output_path: str):
    """
    Concatenate videos using ffmpeg.
    All hard-cuts → lossless concat demuxer;
    transitions with effects → xfade filter chain.
    """
    td = TRANSITION_DURATION
    n = len(video_paths)
    has_effect = any(transitions[i] in FFMPEG_XFADE for i in range(len(transitions)))

    # ── All hard cuts: lossless concat demuxer ──
    if not has_effect:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for p in video_paths:
                f.write(f"file '{os.path.abspath(p)}'\n")
            list_file = f.name
        cmd = [FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0",
               "-i", list_file, "-c", "copy", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        os.unlink(list_file)
        if result.returncode != 0:
            print(f"  WARNING: ffmpeg concat failed: {result.stderr[-300:]}")
            return None
        return sum(_probe_duration(p) for p in video_paths)

    # ── Transitions with effects: xfade (video) + acrossfade (audio) filter chain ──
    print("  ffmpeg xfade transition concatenation...")
    durations = [_probe_duration(p) for p in video_paths]
    inputs = []
    for p in video_paths:
        inputs += ["-i", p]

    video_parts = []
    audio_parts = []
    for i in range(n):
        video_parts.append(f"[{i}:v]fps=24[vfps{i}]")

    last_v = "[vfps0]"
    last_a = "[0:a]"
    offset = 0.0

    for i in range(n - 1):
        trans = transitions[i] if i < len(transitions) else "cut"
        xfade = FFMPEG_XFADE.get(trans)
        offset += durations[i]
        out_v = f"[v{i}]"
        out_a = f"[a{i}]"

        if xfade:
            xfade_offset = max(0.0, offset - td)
            video_parts.append(
                f"{last_v}[vfps{i+1}]xfade=transition={xfade}"
                f":duration={td}:offset={xfade_offset:.3f}{out_v}"
            )
            audio_parts.append(
                f"{last_a}[{i+1}:a]acrossfade=d={td}:c1=tri:c2=tri{out_a}"
            )
            offset -= td
        else:
            video_parts.append(
                f"{last_v}[vfps{i+1}]concat=n=2:v=1:a=0{out_v}"
            )
            audio_parts.append(
                f"{last_a}[{i+1}:a]concat=n=2:v=0:a=1{out_a}"
            )
        last_v = out_v
        last_a = out_a

    filter_complex = ";".join(video_parts + audio_parts)

    cmd = ([FFMPEG_BIN, "-y"] + inputs
           + ["-filter_complex", filter_complex,
              "-map", last_v, "-map", last_a,
              "-c:v", "libx264", "-preset", "fast", "-c:a", "aac",
              output_path])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  WARNING: ffmpeg xfade failed: {result.stderr[-400:]}")
        return None
    return _probe_duration(output_path)


# ── moviepy concatenation (fallback) ────────────────────────────────

def concat_with_moviepy(video_paths: list, transitions: list, output_path: str):
    """Concatenate using moviepy, supporting dissolve / fade-to-black transitions."""
    try:
        from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
    except ImportError:
        print("  WARNING: moviepy not installed. Please run: pip install moviepy==1.0.3")
        return None

    td = TRANSITION_DURATION
    print("  moviepy concatenation (with transition effects)...")

    clips = []
    for p in video_paths:
        c = VideoFileClip(p)
        clips.append(c)
        print(f"     ✓ {Path(p).name}  {c.duration:.1f}s  {c.size[0]}×{c.size[1]}")

    _OVERLAP_KEYS = {"dissolve", "slide"}  # slide → dissolve as best-effort fallback
    _FADEBLACK_KEYS = {"fade to black"}

    segments = []
    i = 0
    while i < len(clips):
        trans = transitions[i] if i < len(transitions) else "cut"
        clip = clips[i]

        if trans in _OVERLAP_KEYS and i + 1 < len(clips):
            next_clip = clips[i + 1]
            c1 = clip.crossfadeout(td)
            c2 = next_clip.set_start(clip.duration - td).crossfadein(td)
            merged = CompositeVideoClip([c1, c2]).set_duration(
                clip.duration + next_clip.duration - td
            )
            segments.append(merged)
            i += 2
        elif trans in _FADEBLACK_KEYS:
            segments.append(clip.fadeout(td))
            i += 1
        else:
            segments.append(clip)
            i += 1

    try:
        final = concatenate_videoclips(segments, method="compose")
        total = final.duration
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="fast",
            logger=None,
        )
        for c in clips:
            c.close()
        final.close()
        return total
    except Exception as e:
        print(f"  WARNING: moviepy concatenation failed: {e}")
        import traceback; traceback.print_exc()
        return None


# ── Main function ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Storyboard video concatenation tool")
    parser.add_argument("json_file", help="Path to storyboard_data.json")
    parser.add_argument("--batch-dir", default=None, help="Specify batch directory")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (default: batch_dir/final_video.mp4)")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "storyboard")
    safe_title = title.replace(" ", "_").replace("/", "-")
    shots = data.get("shots", [])

    # Determine batch directory
    if args.batch_dir:
        batch_dir = Path(args.batch_dir)
    else:
        batch_dir = find_latest_batch(safe_title, json_path.parent)
        if batch_dir is None:
            print(f"ERROR: No batch directory with videos found under {json_path.parent}/{safe_title}/")
            sys.exit(1)
        print(f"  Auto-selected latest batch: {batch_dir}")

    video_dir = batch_dir / "videos"
    if not video_dir.exists():
        print(f"ERROR: videos/ folder not found in batch directory: {video_dir}")
        sys.exit(1)

    # Collect video paths + transitions
    video_paths = []
    transitions = []
    missing = []
    for shot in shots:
        filename = shot["shot_num"].replace(" ", "_") + ".mp4"
        p = str(video_dir / filename)
        if os.path.exists(p):
            video_paths.append(p)
            transitions.append(normalize_transition(shot.get("transition", "cut")))
        else:
            missing.append(filename)

    if missing:
        print(f"  WARNING: Missing video files (will skip): {missing}")
    if not video_paths:
        print("ERROR: No video files found")
        sys.exit(1)

    output_path = args.output or str(batch_dir / "final_video.mp4")

    # Print concatenation plan
    print(f"\nConcatenation plan: {title}")
    print(f"  Batch directory: {batch_dir}")
    for idx, (p, t) in enumerate(zip(video_paths, transitions)):
        arrow = f"──[{t}]──▶" if idx < len(video_paths) - 1 else f"──[{t}]──■"
        print(f"  {Path(p).name} {arrow}")
    print(f"  Output: {output_path}\n")

    # Try ffmpeg first, fall back to moviepy
    total = concat_with_ffmpeg(video_paths, transitions, output_path)
    if total is None:
        total = concat_with_moviepy(video_paths, transitions, output_path)

    if total is None or not os.path.exists(output_path):
        print("\nERROR: Concatenation failed. Please check dependencies (moviepy / ffmpeg)")
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"\n✅ Final video concatenated successfully")
    print(f"   Output: {output_path}")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   Duration: {total:.1f}s")
    print(f"   Total shots concatenated: {len(video_paths)}")


if __name__ == "__main__":
    main()
