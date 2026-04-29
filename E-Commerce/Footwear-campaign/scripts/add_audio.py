"""
BGM Mixing Tool
Selects the best emotionally matching music from the online music library (background_music.json),
mixes it into final_video.mp4, and automates the BGM volume curve based on the 2nd segment
(music emotion) of each shot's sound_design field in storyboard_data.json.
Outputs final_video_mixed.mp4.

Natively generated SFX is already included in the final_video.mp4 audio track;
this script only adds the BGM layer — it does not replace existing SFX.

Usage:
    python3 add_audio.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp}
    python3 add_audio.py storyboard_data.json --batch-dir output/{ProductName}/{timestamp} --bgm <local path or URL>

BGM auto-selection rules:
    If --bgm is not specified, read the music library from BGM_JSON_PATH (background_music.json),
    score each track based on the storyboard JSON's title (brand/product) and sound_design emotion keywords
    vs each track's label tags, select the highest-scoring track and download it to a temp file.

Volume automation keyword mapping (2nd segment, music emotion):
    Music pause / silence / music momentarily pauses → 0.0 (mute)
    Music murmur / very soft / gently returns       → 0.08
    Strings single note starts / music fades in     → fade in (0→0.25)
    Strings gentle sustain / gentle sustain         → 0.25
    Background music continues / warm reverb        → 0.30
    Theme music warming up / warming up             → 0.45
    Music rises to peak / orchestral burst          → 0.70
    Music fades to silence / wrap-up / ambient      → fade out (current→0)

Dependencies:
    brew install ffmpeg
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

# Online music library JSON path (each entry: {"url": "...", "label": "upbeat,soft"})
BGM_JSON_PATH = Path(__file__).resolve().parent.parent / "assets" / "bgm_library.json"


# ── ffmpeg binary resolution ──────────────────────────────────────
def _find_ffmpeg() -> str:
    """Prefer system PATH ffmpeg; fall back to imageio_ffmpeg built-in binary if not found."""
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

def _find_ffprobe() -> str:
    """Prefer system PATH ffprobe; fall back to ffprobe in the same directory as imageio_ffmpeg,
    or ultimately fall back to ffmpeg (ffmpeg -hide_banner can also detect streams)."""
    if shutil.which("ffprobe"):
        return "ffprobe"
    try:
        import imageio_ffmpeg
        ffmpeg_exe = Path(imageio_ffmpeg.get_ffmpeg_exe())
        for name in ("ffprobe", "ffprobe.exe"):
            candidate = ffmpeg_exe.parent / name
            if candidate.exists():
                return str(candidate)
    except ImportError:
        pass
    return FFMPEG_BIN

FFPROBE_BIN = _find_ffprobe()


# ---------- Volume automation rules ----------
# (keyword list, volume value, fade_in, fade_out)
MOOD_RULES: list[tuple[list[str], float, bool, bool]] = [
    (["music pause", "music stops", "silence"],               0.0,  False, False),
    (["music murmur", "very soft", "gently returns"],         0.08, False, False),
    (["music fades to silence", "fade out", "wrap-up"],       0.0,  False, True),
    (["strings single note", "music fades in", "fade in"],    0.25, True,  False),
    (["strings gentle sustain", "gentle sustain"],            0.25, False, False),
    (["background music continues", "warm reverb"],           0.30, False, False),
    (["theme music warming up", "warming up"],                0.45, False, False),
    (["music rises to peak", "orchestral burst", "climax"],   0.70, False, False),
]

DEFAULT_VOLUME = 0.30


# ---------- Intelligent track scoring rules ----------
# Each rule: (trigger keyword list, preferred JSON label keyword list, score, reason label)
# Trigger keywords are searched in storyboard text (title + sound_design).
# Preferred label keywords are matched against the music library JSON's label field (e.g., "upbeat,soft,fashion").
SCORING_RULES: list[tuple[list[str], list[str], float, str]] = [
    # Luxury / high-end brands → fashion, elegant, soft
    (["CHANEL", "Chanel", "chanel", "Dior", "dior", "LV", "Gucci", "gucci",
      "luxury", "high-end", "premium"],
     ["fashion", "elegant", "soft"],
     3.0, "luxury brand"),

    # Cosmetics / skincare / makeup → fashion, soft, elegant, romantic
    (["lipstick", "skincare", "serum", "foundation", "perfume",
      "eyeshadow", "moisturizer", "blush", "concealer", "toner",
      "nail polish", "mascara", "beauty", "makeup"],
     ["fashion", "soft", "elegant", "romantic"],
     2.0, "beauty/skincare"),

    # FMCG / daily household / personal care → upbeat, relaxed
    (["shampoo", "body wash", "toothpaste", "cleanser", "lotion",
      "conditioner", "soap", "detergent"],
     ["upbeat", "relaxed"],
     2.0, "daily personal care"),

    # Tech / digital products → dynamic, uplifting, sci-fi
    (["phone", "laptop", "earbuds", "smart", "tech", "digital",
      "AI", "app", "software", "gadget", "device", "wearable"],
     ["dynamic", "uplifting", "sci-fi"],
     2.0, "tech/digital"),

    # Business / workplace → fashion, dynamic
    (["B2B", "business", "corporate", "professional", "enterprise"],
     ["fashion", "dynamic"],
     2.0, "business style"),

    # Travel / outdoor / nature → upbeat, relaxed, uplifting
    (["travel", "outdoor", "nature", "adventure", "vacation", "hiking",
      "camping", "explore"],
     ["upbeat", "relaxed", "uplifting"],
     2.0, "travel/outdoor"),

    # Summer / fresh → upbeat, relaxed
    (["summer", "fresh", "beach", "sunshine", "refreshing",
      "tropical", "breezy"],
     ["upbeat", "relaxed"],
     1.5, "summer/fresh"),

    # Strings / quiet / elegant → soft, elegant
    (["strings", "minimal", "gentle", "slow life", "ambient",
      "quiet", "peaceful"],
     ["soft", "elegant"],
     2.0, "strings/ambient"),

    # Upbeat / energetic → upbeat, uplifting, dynamic
    (["upbeat", "lively", "energetic", "dynamic", "vibrant",
      "exciting", "powerful"],
     ["upbeat", "uplifting", "dynamic"],
     1.5, "upbeat/energetic"),

    # Warm / emotional → soft, romantic
    (["warm", "emotional", "story", "touching", "family",
      "heartfelt", "nostalgic"],
     ["soft", "romantic"],
     1.5, "warm/emotional"),

    # Unboxing / product review / seeding → upbeat, relaxed, fashion
    (["unboxing", "haul", "product review", "seeding", "lifestyle",
      "everyday", "authentic", "relatable"],
     ["upbeat", "relaxed", "fashion"],
     3.0, "unboxing/seeding"),
]


def parse_duration(dur_str: str) -> float:
    """Convert '3s', '2.5s', or plain number string to float seconds."""
    if not dur_str:
        return 3.0
    s = str(dur_str).strip().rstrip("s").strip()
    try:
        return float(s)
    except ValueError:
        return 3.0


def parse_sound_design(text: str) -> tuple[str, str, str]:
    """Split sound_design field by '·' into (lead SFX, music emotion, special processing)."""
    parts = [p.strip() for p in text.split("·")]
    while len(parts) < 3:
        parts.append("")
    return parts[0], parts[1], parts[2]


def get_mood_params(mood: str) -> tuple[float, bool, bool]:
    """Return (volume, fade_in, fade_out) based on music emotion text."""
    for keywords, vol, fade_in, fade_out in MOOD_RULES:
        if any(kw in mood for kw in keywords):
            return vol, fade_in, fade_out
    return DEFAULT_VOLUME, False, False


def build_volume_expression(segments: list[dict]) -> str:
    """
    Build a dynamic ffmpeg volume filter expression.
    Uses between(t, start, end) to set volume per shot time segment.
    Fade-in/fade-out use linear ramps.
    """
    if not segments:
        return str(DEFAULT_VOLUME)

    parts: list[str] = []
    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        vol = seg["volume"]
        dur = max(end - start, 0.001)

        if seg.get("fade_in"):
            ramp = f"min(1,max(0,(t-{start:.3f})/{dur:.3f}))*{vol:.4f}"
            parts.append(f"{ramp}*between(t,{start:.3f},{end:.3f})")
        elif seg.get("fade_out"):
            prev_vol = seg.get("prev_volume", DEFAULT_VOLUME)
            ramp = f"min(1,max(0,({end:.3f}-t)/{dur:.3f}))*{prev_vol:.4f}"
            parts.append(f"{ramp}*between(t,{start:.3f},{end:.3f})")
        else:
            parts.append(f"{vol:.4f}*between(t,{start:.3f},{end:.3f})")

    return "+".join(parts)


def has_audio_stream(video_path: Path) -> bool:
    """Check whether a video file has an audio stream."""
    if FFPROBE_BIN != FFMPEG_BIN:
        r = subprocess.run(
            [
                FFPROBE_BIN, "-v", "error",
                "-select_streams", "a",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0",
                str(video_path),
            ],
            capture_output=True, text=True,
        )
        return bool(r.stdout.strip())
    else:
        # Fallback: use ffmpeg -i to detect; check stderr for "Audio:"
        r = subprocess.run(
            [FFMPEG_BIN, "-hide_banner", "-i", str(video_path)],
            capture_output=True, text=True,
        )
        return "Audio:" in r.stderr


def check_ffmpeg() -> None:
    """FFMPEG_BIN is resolved at module load; this function only does a quick validation."""
    r = subprocess.run([FFMPEG_BIN, "-version"], capture_output=True)
    if r.returncode != 0:
        print(f"ERROR: ffmpeg not available ({FFMPEG_BIN}). Please install: brew install ffmpeg or pip install imageio-ffmpeg")
        sys.exit(1)


def load_bgm_catalog(json_path: Path = BGM_JSON_PATH) -> list[dict]:
    """Read track list from JSON music library; returns [{"url": ..., "label": ..., "tags": [...]}]."""
    if not json_path.exists():
        print(f"⚠️  Music library file not found: {json_path}")
        return []
    with open(json_path, encoding="utf-8") as f:
        raw = json.load(f)
    catalog = []
    for item in raw:
        url = item.get("url", "").strip()
        label = item.get("label") or ""
        tags = [t.strip() for t in label.split(",") if t.strip()]
        if url:
            catalog.append({"url": url, "label": label, "tags": tags})
    return catalog


def select_bgm_from_catalog(catalog: list[dict], data: dict,
                             video_total_dur: float = 0.0) -> tuple[str, str]:
    """
    Intelligently select a track from the music library based on storyboard JSON content.
    Returns (best track URL, selection reason).
    If no match, returns a random track.
    """
    if not catalog:
        return "", "Music library is empty"

    # Build search text: title + format + all sound_design fields
    title = data.get("title", "")
    fmt = data.get("format", "")
    all_sound = " ".join(
        shot.get("sound_design", "") for shot in data.get("shots", [])
    )
    search_text = f"{title} {fmt} {all_sound}"

    scores: dict[int, float] = {i: 0.0 for i in range(len(catalog))}
    matched_reasons: dict[int, list[str]] = {i: [] for i in range(len(catalog))}

    for trigger_kws, prefer_label_kws, score, rule_label in SCORING_RULES:
        triggered = any(kw in search_text for kw in trigger_kws)
        if not triggered:
            continue
        for i, entry in enumerate(catalog):
            if any(kw in entry["tags"] for kw in prefer_label_kws):
                scores[i] += score
                matched_reasons[i].append(rule_label)

    # If video duration > 35s, prefer tracks tagged "over-35-seconds" for extra points
    if video_total_dur > 35:
        for i, entry in enumerate(catalog):
            if "over-35-seconds" in entry["tags"]:
                scores[i] += 1.0

    best_idx = max(range(len(catalog)), key=lambda i: scores[i])
    reasons = matched_reasons[best_idx]

    if scores[best_idx] == 0:
        import random
        best_idx = random.randrange(len(catalog))
        reason_text = "No clear match, selected randomly"
    else:
        reason_text = " × ".join(dict.fromkeys(reasons))

    entry = catalog[best_idx]
    return entry["url"], f"{reason_text} (tags: {entry['label']})"


def download_bgm_url(url: str, tmp_dir: str) -> Path:
    """Download BGM URL to temp directory, return local path."""
    ext = os.path.splitext(url.split("?")[0])[-1] or ".mp3"
    out_path = Path(tmp_dir) / f"bgm_selected{ext}"
    encoded_url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=-._~")
    print(f"Downloading BGM: {encoded_url}")
    urllib.request.urlretrieve(encoded_url, str(out_path))
    print(f"BGM downloaded: {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Intelligently mix BGM into final_video.mp4")
    parser.add_argument("json_file", help="Path to storyboard_data.json")
    parser.add_argument("--batch-dir", required=True, help="Batch output directory")
    parser.add_argument("--bgm", help="Manually specify BGM (local file path or URL; omit for auto-selection from library)")
    args = parser.parse_args()

    check_ffmpeg()

    batch_dir = Path(args.batch_dir).resolve()
    json_path = Path(args.json_file).resolve()

    # Find input video:
    # Prefer final_video.mp4 (B-1 per-shot concat output);
    # fall back to final_video_coherent.mp4 (B-2 Seedance 2.0 coherent full-film output) if not found
    input_video = batch_dir / "final_video.mp4"
    if not input_video.exists():
        coherent_video = batch_dir / "final_video_coherent.mp4"
        if coherent_video.exists():
            print(f"Note: final_video.mp4 not found; using coherent film output {coherent_video.name} as mix input.")
            input_video = coherent_video
        else:
            print(f"ERROR: Neither {input_video} nor {coherent_video} found. "
                  f"Please generate the complete video first (per-shot concat or Seedance 2.0 coherent mode).")
            sys.exit(1)

    # Load storyboard data (must be loaded before track selection)
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    shots = data.get("shots", [])
    if not shots:
        print("ERROR: No shots data found in JSON.")
        sys.exit(1)

    # Calculate total video duration (for "over-35-seconds" tag filtering)
    video_total_dur = sum(
        parse_duration(s.get("duration", "3s")) for s in shots
    )

    # Track selection & temp directory management
    _tmp_dir_obj = tempfile.TemporaryDirectory()
    _tmp_dir = _tmp_dir_obj.name

    if args.bgm:
        raw_bgm = args.bgm.strip()
        if raw_bgm.startswith("http://") or raw_bgm.startswith("https://"):
            bgm_path = download_bgm_url(raw_bgm, _tmp_dir)
        else:
            bgm_path = Path(raw_bgm).resolve()
        bgm_reason = "Manually specified by user"
    else:
        catalog = load_bgm_catalog()
        if not catalog:
            print("Note: Music library is empty or unavailable. Skipping mix.")
            sys.exit(0)
        bgm_url, bgm_reason = select_bgm_from_catalog(catalog, data, video_total_dur)
        if not bgm_url:
            print("Note: Could not select a suitable track from the library. Skipping mix.")
            sys.exit(0)
        bgm_path = download_bgm_url(bgm_url, _tmp_dir)

    if not bgm_path.exists():
        print(f"ERROR: BGM file not found: {bgm_path}")
        sys.exit(1)

    print(f"\nTrack selected: {bgm_path.name}")
    print(f"Reason: {bgm_reason}\n")

    # Detect voiceover file (for product review / seeding videos)
    voiceover_path = batch_dir / "voiceover.mp3"
    has_voiceover = voiceover_path.exists()
    if has_voiceover:
        print(f"Voiceover file detected: {voiceover_path.name}")
        print(f"Mix strategy: voiceover at full volume (1.0) + BGM ducked to 20%\n")

    # Build timeline segments
    segments: list[dict] = []
    current_time = 0.0
    prev_vol = DEFAULT_VOLUME
    for shot in shots:
        dur = parse_duration(shot.get("duration", "3s"))
        sound = shot.get("sound_design", "")
        _, mood, _ = parse_sound_design(sound)
        vol, fade_in, fade_out = get_mood_params(mood)

        segments.append({
            "shot": shot.get("shot_num", shot.get("shot_number", "?")),
            "start": current_time,
            "end": current_time + dur,
            "volume": vol,
            "fade_in": fade_in,
            "fade_out": fade_out,
            "prev_volume": prev_vol,
            "mood": mood,
        })
        if not fade_out:
            prev_vol = vol
        current_time += dur

    total_dur = current_time

    # Print timeline preview
    print("=== BGM Volume Timeline ===")
    print(f"{'Shot':<10} {'Time Range':<16} {'Music Emotion':<22} {'Volume':>6}  {'Effect'}")
    print("─" * 65)
    for seg in segments:
        effect = "Fade In" if seg["fade_in"] else ("Fade Out" if seg["fade_out"] else "Constant")
        print(
            f"{str(seg['shot']):<10}"
            f" {seg['start']:.1f}s–{seg['end']:.1f}s   "
            f"{seg['mood'][:20]:<22}"
            f" {seg['volume']:>5.2f}  {effect}"
        )
    print(f"\nTotal duration: {total_dur:.1f}s\n")

    # Build volume expression
    vol_expr = build_volume_expression(segments)

    # Output path: derived from input filename to maintain naming consistency
    # final_video.mp4          → final_video_mixed.mp4
    # final_video_coherent.mp4 → final_video_coherent_mixed.mp4
    output_path = batch_dir / f"{input_video.stem}_mixed.mp4"

    # Check if final_video.mp4 has audio
    video_has_audio = has_audio_stream(input_video)

    if has_voiceover:
        # ── Voiceover + BGM mix mode (product review / seeding video) ──────────────
        # Strategy: BGM ducked to 20% throughout (overrides volume curve), voiceover at full volume (1.0)
        # Input indices: 0=video, 1=BGM(stream_loop), 2=voiceover
        bgm_ducked_filter = (
            f"[1:a]atrim=0:{total_dur:.3f},"
            f"asetpts=PTS-STARTPTS,"
            f"volume=0.20[bgm_ducked]"
        )
        vo_filter = (
            f"[2:a]atrim=0:{total_dur:.3f},"
            f"asetpts=PTS-STARTPTS,"
            f"volume=1.0[vo]"
        )
        # With voiceover present, only mix BGM + voiceover regardless of whether the video has audio,
        # to prevent Seedance 2.0 native SFX (at full volume) from drowning out the voiceover.
        filter_complex = (
            f"{bgm_ducked_filter};"
            f"{vo_filter};"
            f"[bgm_ducked][vo]amix=inputs=2:duration=shortest:normalize=0[aout]"
        )
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(input_video),
            "-stream_loop", "-1", "-i", str(bgm_path),
            "-i", str(voiceover_path),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total_dur:.3f}",
            str(output_path),
        ]
    else:
        # ── Standard BGM mix mode ─────────────────────────────────
        bgm_filter = (
            f"[1:a]atrim=0:{total_dur:.3f},"
            f"asetpts=PTS-STARTPTS,"
            f"volume='{vol_expr}':eval=frame[bgm]"
        )
        if video_has_audio:
            filter_complex = (
                f"{bgm_filter};"
                f"[0:a][bgm]amix=inputs=2:duration=shortest:normalize=0[aout]"
            )
        else:
            filter_complex = (
                f"{bgm_filter};"
                f"[bgm]anull[aout]"
            )
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(input_video),
            "-stream_loop", "-1", "-i", str(bgm_path),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total_dur:.3f}",
            str(output_path),
        ]

    print("Mixing audio, please wait...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR: ffmpeg execution failed")
        print(result.stderr[-3000:])
        sys.exit(1)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"\nMixing complete!")
    print(f"Output file: {output_path}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"BGM reason: {bgm_reason}")
    if has_voiceover:
        print(f"Audio track: voiceover (voiceover.mp3) + BGM (ducked to 20%) mixed")
    elif video_has_audio:
        print(f"Audio track: native SFX (from {input_video.name}) + BGM")
    else:
        print(f"Audio track: BGM only ({input_video.name} has no audio track)")

    # Clean up BGM temp download file
    _tmp_dir_obj.cleanup()

    # Auto-trigger Phase 7: Instagram-style subtitle burning
    subtitles_script = Path(__file__).parent / "add_subtitles.py"
    if subtitles_script.exists():
        print("\n── Auto-triggering Phase 7: Subtitle burning ──")
        subprocess.run(
            [sys.executable, str(subtitles_script), str(json_path), "--batch-dir", str(batch_dir)],
            check=False,
        )
    else:
        print(f"\nNote: Subtitle script {subtitles_script} not found. Skipping Phase 7.")


if __name__ == "__main__":
    main()
