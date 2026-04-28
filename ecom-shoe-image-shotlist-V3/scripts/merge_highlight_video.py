"""
Highlight Reel Merge Tool for Footwear E-Commerce Photography

Merges individual shoe video clips into a single highlight reel with
xfade crossfade transitions and background music overlay.
Uploads the final video to CDN and prints a structured result.

Core ffmpeg / download / probe logic is modeled on the stable
merge_multi_video_safe.py in the same directory.

Usage:
    python3 merge_highlight_video.py \
        --videos clip1.mp4 clip2.mp4 clip3.mp4 clip4.mp4 clip5.mp4 \
        --shoe-type athletic \
        --output-dir projects/ecom-shoe/outputs

    python3 merge_highlight_video.py \
        --videos clip1.mp4 clip2.mp4 ... \
        --shoe-type fashion \
        --output-dir projects/ecom-shoe/outputs \
        --clip-duration 4.0 \
        --xfade-duration 0.6 \
        --bgm /path/to/custom_bgm.mov

Dependencies:
    ffmpeg / ffprobe (must be on PATH)
    pip install requests
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import uuid
from pathlib import Path
from typing import Optional

import requests

# --- secrets loader (for CDN upload) ---
_apps_dir = str(Path(__file__).resolve().parents[5])
if _apps_dir not in sys.path:
    sys.path.insert(0, _apps_dir)
try:
    from secrets_loader import load_secrets
    load_secrets()
except ImportError:
    pass
# --- end secrets loader ---

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

SHOE_KEYWORDS_EN = {
    "athletic":  {"primary": ["energetic", "uplifting", "passionate"], "secondary": ["upbeat", "stylish"]},
    "fashion":   {"primary": ["stylish", "elegant", "soft"],          "secondary": ["romantic", "relaxing"]},
    "children":  {"primary": ["upbeat", "relaxing"],                  "secondary": ["stylish", "energetic"]},
}



LONG_TRACK_TAG_EN = "over-35s"


# ── Download (from merge_multi_video_safe.py) ────────────────────────

def _download_file(url: str, max_retries: int = 3, wait_time: int = 2,
                   timeout: int = 1200) -> bytes:
    """Download a file with retries, matching merge_multi_video_safe.py logic."""
    url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=-._~")
    print(f"  Downloading: {url[:100]}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                       "(KHTML, Gecko) Chrome/56.0.2924.76 Safari/537.36",
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=timeout)
            if response.status_code == 200:
                print(f"  Download complete: {url[:60]}...")
                return response.content
            raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            retries += 1
            print(f"  Download failed ({retries}/{max_retries}): {e}")
            if retries < max_retries:
                print(f"  {wait_time}s s retrying...")
                time.sleep(wait_time)
    raise Exception(f"Download failed (retried{max_retries}times): {url}")


def _is_url(path: str) -> bool:
    return path.startswith(("http://", "https://"))


def _resolve_input(path_or_url: str, work_dir: str) -> str:
    """If URL, download to work_dir and return local path; otherwise return as-is."""
    if not _is_url(path_or_url):
        return path_or_url
    data = _download_file(path_or_url)
    ext = os.path.splitext(path_or_url.split("?")[0])[1] or ".mp4"
    local_path = os.path.join(work_dir, f"dl_{uuid.uuid4().hex}{ext}")
    with open(local_path, "wb") as f:
        f.write(data)
    size_kb = len(data) // 1024
    print(f"  Saved: {local_path} ({size_kb} KB)")
    return local_path


# ── ffprobe helpers (from merge_multi_video_safe.py) ─────────────────

def _probe_has_audio(video_path: str) -> bool:
    """Detect whether a video contains an audio stream (ffprobe JSON)."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        video_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        return any(s.get("codec_type") == "audio" for s in info.get("streams", []))
    except Exception:
        return False


def _probe_resolution(video_path: str) -> tuple[int, int]:
    """Get video resolution via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-select_streams", "v:0",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    vs = info["streams"][0]
    return int(vs["width"]), int(vs["height"])


# ── BGM selection ────────────────────────────────────────────────────

def _get_music_json_path() -> Path:
    return ASSETS_DIR / "background-music.json"


def _load_music_catalog(json_path: Path) -> list[dict]:
    if not json_path.exists():
        print(f"WARNING: Music library file not found: {json_path}")
        return []
    with open(json_path, encoding="utf-8") as f:
        raw = json.load(f)
    catalog = []
    for item in raw:
        url = item.get("url", "").strip()
        label = item.get("label", "") or ""
        tags = [t.strip() for t in label.split(",") if t.strip()]
        if url:
            catalog.append({"url": url, "label": label, "tags": tags})
    return catalog


def select_music(shoe_type: str, total_duration: float) -> tuple[str, str]:
    """Select a background music track based on shoe type and video duration."""
    json_path = _get_music_json_path()
    catalog = _load_music_catalog(json_path)
    if not catalog:
        return "", ""

    kw_map = SHOE_KEYWORDS_EN
    lookup_type = shoe_type.lower()
    long_tag = LONG_TRACK_TAG_EN

    kw = kw_map.get(lookup_type, list(kw_map.values())[1])

    def _match(tags: list[str], keywords: list[str]) -> bool:
        return any(k in t for t in tags for k in keywords)

    pool = [m for m in catalog if _match(m["tags"], kw["primary"]) and long_tag in m["tags"]]
    if not pool:
        pool = [m for m in catalog if _match(m["tags"], kw["primary"])]
    if not pool:
        pool = [m for m in catalog if _match(m["tags"], kw["secondary"])]
    if not pool:
        pool = catalog

    sel = random.choice(pool)
    return sel["url"], sel["label"]


# ── ffmpeg merge core ────────────────────────────────────────────────

def build_ffmpeg_merge_cmd(
    video_files: list[str],
    bgm_path: str,
    output_path: str,
    clip_duration: float = 3.5,
    xfade_duration: float = 0.5,
    fade_out_duration: float = 2.5,
) -> tuple[list[str], float]:
    """Build ffmpeg command for xfade highlight reel with BGM overlay.

    Uses ffprobe-based audio detection and auto resolution from the first clip,
    matching the stable patterns in merge_multi_video_safe.py.
    """
    n = len(video_files)
    has_audio_flags = [_probe_has_audio(v) for v in video_files]

    width, height = _probe_resolution(video_files[0])
    print(f"  Auto-detected resolution: {width}x{height}")

    inputs = []
    for v in video_files:
        inputs += ["-i", v]
    inputs += ["-i", bgm_path]

    fp = []
    for i in range(n):
        fp.append(
            f"[{i}:v]trim=0:{clip_duration},setpts=PTS-STARTPTS,fps=24,"
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]"
        )
        if has_audio_flags[i]:
            fp.append(f"[{i}:a]atrim=0:{clip_duration},asetpts=PTS-STARTPTS[a{i}]")
        else:
            fp.append(f"anullsrc=r=44100:cl=stereo,atrim=0:{clip_duration}[a{i}]")

    offset = clip_duration - xfade_duration
    pv, pa = "v0", "a0"
    for i in range(1, n):
        nv, na = f"vx{i}", f"ax{i}"
        fp.append(
            f"[{pv}][v{i}]xfade=transition=fade:"
            f"duration={xfade_duration}:offset={offset:.3f}[{nv}]"
        )
        fp.append(f"[{pa}][a{i}]acrossfade=d={xfade_duration}[{na}]")
        offset += clip_duration - xfade_duration
        pv, pa = nv, na

    total_duration = n * clip_duration - (n - 1) * xfade_duration
    fade_start = total_duration - fade_out_duration
    fp.append(
        f"[{n}:a]atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.8,afade=t=out:st={fade_start:.3f}:d={fade_out_duration}[bgm]"
    )
    fp.append(f"[{pa}][bgm]amix=inputs=2:duration=shortest:normalize=0[aout]")

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", ";".join(fp),
        "-map", f"[{pv}]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path),
    ]
    return cmd, total_duration


# ── CDN upload ───────────────────────────────────────────────────────

def upload_to_cdn(file_path: str) -> Optional[str]:
    try:
        banana_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banana")
        if banana_dir not in sys.path:
            sys.path.insert(0, banana_dir)
        from uploader_factory import get_uploader

        uploader = get_uploader()
        with open(file_path, "rb") as f:
            data = f.read()
        cdn_url = uploader.upload_bytes(data, extension="mp4")
        return cdn_url
    except Exception as e:
        print(f"[ERROR] CDN upload failed: {e}")
        return None


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Merge shoe video clips into a highlight reel with BGM"
    )
    parser.add_argument(
        "--videos", nargs="+", required=True,
        help="Video file paths or CDN URLs (in playback order)",
    )
    parser.add_argument(
        "--shoe-type", required=True,
        choices=["athletic", "fashion", "children"],
        help="Shoe type for BGM selection",
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Directory to save the final highlight video",
    )
    parser.add_argument(
        "--clip-duration", type=float, default=3.5,
        help="Duration to keep from each clip (seconds, default 3.5)",
    )
    parser.add_argument(
        "--xfade-duration", type=float, default=0.5,
        help="Crossfade transition duration (seconds, default 0.5)",
    )
    parser.add_argument(
        "--bgm", default=None,
        help="Manual BGM path or URL (omit for auto-selection)",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    work_dir = tempfile.mkdtemp(prefix="shoe_merge_")
    temp_files: list[str] = []

    try:
        # ── 1. Prepare local video files ─────────────────────────────
        print("\n=== Preparing video clips ===")
        local_videos: list[str] = []
        for vp in args.videos:
            if _is_url(vp):
                local = _resolve_input(vp, work_dir)
                local_videos.append(local)
                temp_files.append(local)
            else:
                if not os.path.isfile(vp):
                    print(f"Error: File not found -> {vp}")
                    sys.exit(1)
                local_videos.append(vp)

        n = len(local_videos)
        print(f"Clips ready: {n}")

        total_duration = n * args.clip_duration - (n - 1) * args.xfade_duration

        # ── 2. Select or download BGM ────────────────────────────────
        print("\n=== Selecting BGM ===")
        if args.bgm:
            if _is_url(args.bgm):
                bgm_local = _resolve_input(args.bgm, work_dir)
                temp_files.append(bgm_local)
            else:
                bgm_local = args.bgm
            bgm_label = "user-specified"
        else:
            bgm_url, bgm_label = select_music(args.shoe_type, total_duration)
            if not bgm_url:
                print("[ERROR] No music available.")
                sys.exit(1)
            bgm_local = _resolve_input(bgm_url, work_dir)
            temp_files.append(bgm_local)

        print(f"BGM: {bgm_label}")

        # ── 3. Build and run ffmpeg ──────────────────────────────────
        print(f"\n=== Merging {n} clips (xfade={args.xfade_duration}s, clip={args.clip_duration}s) ===")
        output_path = os.path.join(args.output_dir, "highlight_reel.mp4")

        cmd, final_dur = build_ffmpeg_merge_cmd(
            local_videos, bgm_local, output_path,
            clip_duration=args.clip_duration,
            xfade_duration=args.xfade_duration,
        )

        print(f"[re] Executing merge ({n} clips)")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] ffmpeg failed (exit {result.returncode})")
            print(result.stderr[-2000:])
            sys.exit(1)

        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"Merge complete -> {output_path} ({size_mb:.1f} MB, {final_dur:.1f}s)")

        # ── 4. Upload to CDN ─────────────────────────────────────────
        print("\n=== Uploading to CDN ===")
        cdn_url = upload_to_cdn(output_path)

        merge_result = {
            "success": True,
            "local_path": output_path,
            "r2_url": cdn_url,
            "duration": round(final_dur, 1),
            "bgm_label": bgm_label,
            "file_size_mb": round(size_mb, 1),
        }
        print(f"\n[MERGE_RESULT] {json.dumps(merge_result, ensure_ascii=False)}")

    finally:
        for tf in temp_files:
            if os.path.exists(tf):
                os.unlink(tf)
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
