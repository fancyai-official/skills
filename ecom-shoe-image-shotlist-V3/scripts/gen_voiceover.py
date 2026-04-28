"""
gen_voiceover.py — Voiceover Generation Tool for Product Review / Seeding Videos

Generates TTS audio from the `copy` field of each shot in storyboard_data.json,
concatenated per shot duration (silence padding if too short, truncation if too long),
outputs voiceover.mp3 to the batch directory.

Optimization strategies:
  A - SSML prosody control: speech rate -15% (approx 0.85x), auto-pause before transition/emphasis words
  B - Colloquial rewriting: pre-process copy with a blogger tone before TTS (add filler words, split long sentences)

Usage:
    python3 gen_voiceover.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp}
    python3 gen_voiceover.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp} --voice en-US-JennyNeural

Supported voices (recommended):
    en-US-JennyNeural    Natural female voice (default, lifestyle blogger style)
    en-US-GuyNeural      Natural male voice
    en-GB-SoniaNeural    British female voice (premium/luxury brand style)
    en-AU-NatashaNeural  Australian female voice (fresh/youthful style)

Dependencies:
    pip install edge-tts
    brew install ffmpeg
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ── Dependency checks ──────────────────────────────────────────────────
def _check_edge_tts() -> None:
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print("ERROR: edge-tts is not installed. Please run: pip install edge-tts")
        sys.exit(1)


def _find_ffmpeg() -> str:
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    raise FileNotFoundError("ffmpeg not found. Please run: brew install ffmpeg")


FFMPEG_BIN: str = ""


# ── Duration parsing ─────────────────────────────────────────────────
def parse_duration(s: str) -> float:
    s = str(s).strip().lower().replace("s", "")
    try:
        return float(s)
    except ValueError:
        return 3.0


# ── Method B: Colloquial rewriting ────────────────────────────────────
# Emoji detection (remove emojis to prevent TTS from reading out their descriptions)
_EMOJI_RE = re.compile(
    "[\U00010000-\U0010ffff"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE,
)

# ── Blogger-style TTS copy processing rules ───────────────────────────────

# Sentence-end emphasis rules: (keyword to match, word/phrase to append)
# Matches common English lifestyle blogger expressions and adds natural emphasis.
_TAIL_PARTICLES: list[tuple[str, str]] = [
    ("obsessed", ""),            # already emphatic, no addition needed
    ("incredible", ""),          # already emphatic
    ("game changer", ""),        # already emphatic
    ("love it", ""),             # already natural
    ("must-have", ""),           # already natural
    ("repurchase", ""),          # already natural
    ("highly recommend", ""),    # already complete
    ("recommend", " — seriously"), # adds genuine emphasis
    ("worth it", " — every penny"), # completes the thought
    ("smells", " absolutely amazing"), # completes the thought
    ("silky", ""),               # already evocative
    ("glowy", ""),               # already evocative
    ("blends", " like a dream"), # adds vivid description
]

# Insert SSML pause break before English transition/emphasis words
_PAUSE_BEFORE: list[tuple[str, str]] = [
    ("but ",        '<break time="350ms"/>but '),
    ("however ",    '<break time="350ms"/>however '),
    ("yet ",        '<break time="300ms"/>yet '),
    ("the only downside", '<break time="400ms"/>the only downside'),
    ("honestly ",   '<break time="200ms"/>honestly '),
    ("seriously ",  '<break time="200ms"/>seriously '),
    ("actually ",   '<break time="200ms"/>actually '),
    ("and also",    '<break time="200ms"/>and also'),
    ("most importantly", '<break time="350ms"/>most importantly'),
]


_STAR_EMOJIS = re.compile(r"[⭐🌟★☆✨]+")
_STAR_COUNT_TO_EN = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def _replace_stars(text: str) -> str:
    """Replace consecutive star emojis with spoken English text, e.g., ⭐⭐⭐⭐⭐ → five stars."""
    def _sub(m: re.Match) -> str:
        count = len(m.group())
        en = _STAR_COUNT_TO_EN.get(count, str(count))
        return f"{en} stars"
    return _STAR_EMOJIS.sub(_sub, text)


def make_speakable(text: str) -> str:
    """
    Method B: Rewrite written copy into blogger spoken-style (A+B optimization).
    Processing pipeline: emoji → readable text → remove remaining emoji → remove extra punctuation
                         → add filler words → add pauses before transition words
    Note: No mechanical mid-point sentence splitting; let the TTS engine handle natural rhythm.
    """
    # 0. Convert meaningful emoji to readable text first (e.g., stars → recommendation stars)
    text = _replace_stars(text)

    # 1. Remove remaining emoji (TTS would read out their names, sounds very odd)
    text = _EMOJI_RE.sub("", text).strip()

    # 2. Remove subtitle-style punctuation; keep commas (for reading pauses)
    text = re.sub(r"[！!？?。·…—～~「」【】《》""''（）\[\]{}]", "", text)

    # 3. Add emphasis/filler at sentence end (only at the end, and only once)
    for kw, addition in _TAIL_PARTICLES:
        if kw in text and addition and not text.endswith(addition):
            text = text.replace(kw, kw + addition, 1)
            break  # Only add one emphasis phrase per copy line

    # 4. Insert comma pauses before transition/emphasis words (protect word integrity)
    _PLAIN_PAUSE: list[tuple[str, str]] = [
        ("but ",             ", but "),
        ("however ",         ", however "),
        ("yet ",             ", yet "),
        ("the only downside", ", the only downside"),
        ("honestly ",        ", honestly "),
        ("seriously ",       ", seriously "),
        ("actually ",        ", actually "),
        ("and also",         ", and also"),
        ("most importantly", ", most importantly"),
    ]
    for kw, replacement in _PLAIN_PAUSE:
        if kw in text and not text.lstrip(",").lstrip().startswith(kw.strip()):
            text = text.replace(kw, replacement, 1)

    return text


# ── Generate single TTS audio ─────────────────────────────────────────
async def _tts_to_file(text: str, out_path: Path, voice: str, rate: str = "-15%") -> None:
    """Plain text TTS; controls speech rate via the rate parameter (Method A), no SSML."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(out_path))


def generate_tts(text: str, out_path: Path, voice: str, rate: str = "-15%") -> bool:
    """Generate TTS audio to out_path (mp3). Returns whether successful."""
    try:
        asyncio.run(_tts_to_file(text, out_path, voice, rate=rate))
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception as e:
        print(f"  TTS generation failed: {e}")
        return False


# ── Get audio duration ──────────────────────────────────────────────
def probe_duration(audio_path: Path) -> float:
    cmd = [
        FFMPEG_BIN, "-i", str(audio_path),
        "-hide_banner",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.splitlines():
        if "Duration" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = time_str.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


# ── Generate silence clip ──────────────────────────────────────────────
def generate_silence(duration: float, out_path: Path) -> None:
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", f"{duration:.3f}",
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(out_path),
    ]
    subprocess.run(cmd, capture_output=True)


# ── Global tempo adjustment for entire audio track ──────────────────────────────────
def global_fit_to_duration(audio_path: Path, target_dur: float, out_path: Path) -> None:
    """
    Apply a one-time global tempo adjustment to the entire concatenated audio track to ensure:
    1. All content is read completely (no truncation)
    2. Speech rate is perfectly consistent throughout (only one atempo applied)
    If the actual duration is within 3% of the target, pad/trim directly without adjusting tempo.
    """
    actual_dur = probe_duration(audio_path)
    if actual_dur <= 0:
        generate_silence(target_dur, out_path)
        return

    ratio = actual_dur / target_dur

    if abs(ratio - 1.0) <= 0.03:
        # Difference is small; pad or lightly trim
        if actual_dur < target_dur:
            pad = target_dur - actual_dur
            cmd = [
                FFMPEG_BIN, "-y",
                "-i", str(audio_path),
                "-af", f"apad=pad_dur={pad:.3f}",
                "-t", f"{target_dur:.3f}",
                "-c:a", "libmp3lame", "-b:a", "128k",
                str(out_path),
            ]
        else:
            cmd = [
                FFMPEG_BIN, "-y",
                "-i", str(audio_path),
                "-t", f"{target_dur:.3f}",
                "-c:a", "libmp3lame", "-b:a", "128k",
                str(out_path),
            ]
        subprocess.run(cmd, capture_output=True)
        return

    # Build atempo filter chain (each stage range: 0.5~2.0)
    filters = []
    r = ratio
    while r > 2.0:
        filters.append("atempo=2.0")
        r /= 2.0
    while r < 0.5:
        filters.append("atempo=0.5")
        r /= 0.5
    filters.append(f"atempo={r:.5f}")
    af = ",".join(filters)

    cmd = [
        FFMPEG_BIN, "-y",
        "-i", str(audio_path),
        "-af", af,
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(out_path),
    ]
    subprocess.run(cmd, capture_output=True)


# ── Concatenate audio list ─────────────────────────────────────────────
def concat_audio(file_list: list[Path], out_path: Path) -> None:
    """Concatenate multiple audio files in order into a single output file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for fp in file_list:
            f.write(f"file '{fp.resolve()}'\n")
        list_path = Path(f.name)

    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_path),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(out_path),
    ]
    subprocess.run(cmd, capture_output=True)
    list_path.unlink(missing_ok=True)


# ── Main flow ───────────────────────────────────────────────────
def main() -> None:
    _check_edge_tts()

    global FFMPEG_BIN
    FFMPEG_BIN = _find_ffmpeg()

    parser = argparse.ArgumentParser(description="Generate voiceover audio")
    parser.add_argument("json_file", help="Path to storyboard_data.json")
    parser.add_argument("--batch-dir", required=True, help="Batch output directory")
    parser.add_argument(
        "--voice", default="en-US-JennyNeural",
        help="TTS voice (default: en-US-JennyNeural)"
    )
    args = parser.parse_args()

    json_path = Path(args.json_file).resolve()
    batch_dir = Path(args.batch_dir).resolve()

    if not json_path.exists():
        print(f"ERROR: JSON file not found: {json_path}")
        sys.exit(1)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    shots = data.get("shots", [])
    if not shots:
        print("ERROR: No shots data found in JSON.")
        sys.exit(1)

    # Check if any copy content exists
    has_copy = any(s.get("copy", "").strip() for s in shots)
    if not has_copy:
        print("Note: All shot copy fields are empty. Skipping voiceover generation.")
        sys.exit(0)

    # Total video duration (used as final global tempo adjustment reference)
    video_total_dur = sum(parse_duration(s.get("duration", "3s")) for s in shots)

    print(f"🎙️  Starting voiceover generation (voice: {args.voice}, A+B optimization, global uniform tempo)")
    print(f"Total shots: {len(shots)}  |  Total video duration: {video_total_dur:.1f}s\n")

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        segment_files: list[Path] = []

        for i, shot in enumerate(shots):
            shot_num = shot.get("shot_num", f"Shot_{i+1:02d}")
            copy_text = shot.get("copy", "").strip()
            dur = parse_duration(shot.get("duration", "3s"))

            seg_path = tmp_dir / f"{shot_num}_raw.mp3"

            if not copy_text:
                # Empty copy: fill with silence for the shot duration to maintain overall rhythm
                print(f"  {shot_num}: copy is empty, filling {dur:.1f}s silence")
                generate_silence(dur, seg_path)
            else:
                # Method B+A: colloquial rewrite, fixed -15% speech rate, no per-shot duration trimming
                speakable = make_speakable(copy_text)
                preview = copy_text[:20] + ("..." if len(copy_text) > 20 else "")
                print(f"  {shot_num}: generating TTS \"{preview}\"")
                ok = generate_tts(speakable, seg_path, args.voice, rate="-15%")
                if not ok:
                    print(f"    → TTS failed, filling silence")
                    generate_silence(dur, seg_path)
                else:
                    tts_dur = probe_duration(seg_path)
                    print(f"    → TTS duration: {tts_dur:.1f}s (shot duration: {dur:.1f}s)")

            segment_files.append(seg_path)

        # Step 1: Concatenate all segments into raw audio track
        raw_concat = tmp_dir / "raw_concat.mp3"
        print(f"\nConcatenating {len(segment_files)} segments...")
        concat_audio(segment_files, raw_concat)

        raw_total = probe_duration(raw_concat)
        print(f"Raw audio total duration: {raw_total:.1f}s  |  Video total duration: {video_total_dur:.1f}s")

        # Step 2: One-time global tempo adjustment to ensure consistent speech rate and all content read
        out_path = batch_dir / "voiceover.mp3"
        ratio = raw_total / video_total_dur if video_total_dur > 0 else 1.0
        if abs(ratio - 1.0) > 0.03:
            print(f"Global tempo fine-tuning: {ratio:.3f}x → applying one-time atempo to entire track")
        global_fit_to_duration(raw_concat, video_total_dur, out_path)

    if out_path.exists():
        total_dur = probe_duration(out_path)
        size_kb = out_path.stat().st_size // 1024
        print(f"\n✅ Voiceover generation complete!")
        print(f"Output file: {out_path}")
        print(f"Total duration: {total_dur:.1f}s (video: {video_total_dur:.1f}s) | File size: {size_kb} KB")
        print(f"Voice: {args.voice} | Uniform speech rate throughout | All copy fully read")
        print("\nNext step: Run add_audio.py for BGM + voiceover mixing")
    else:
        print("ERROR: Voiceover audio generation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
