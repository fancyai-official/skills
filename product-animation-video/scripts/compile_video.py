#!/usr/bin/env python3
# Copyright 2026 FancyAI
# SPDX-License-Identifier: Apache-2.0

"""
Compile video clips into a final commercial using ffmpeg.

Supports:
- Cross-dissolve transitions between clips (xfade filter)
- Fade-in from black / fade-out to black
- Optional background music overlay
- Optional keyframe still prepend (show the keyframe image briefly before each clip)

Usage:
    python3 compile_video.py \
        --clips hero_shot.mp4 narrative.mp4 \
        --fade-in 0.5 --fade-out 1.0 \
        --output final_commercial.mp4

    python3 compile_video.py \
        --clips hero.mp4 narrative.mp4 hero.mp4 \
        --transition-duration 1.0 \
        --music bg_track.mp3 \
        --output final.mp4

    python3 compile_video.py \
        --clips scene_1.mp4 scene_2.mp4 \
        --keyframes kf_1.png kf_2.png \
        --keyframe-hold 0.8 \
        --transition-duration 1.0 \
        --output final.mp4
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from typing import List, Optional


def check_ffmpeg() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def get_video_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True,
        text=True,
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def get_video_resolution(path: str) -> tuple:
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_streams", "-select_streams", "v:0", path
        ],
        capture_output=True,
        text=True,
    )
    info = json.loads(result.stdout)
    stream = info["streams"][0]
    return int(stream["width"]), int(stream["height"])


def _create_keyframe_clip(
    image_path: str,
    duration: float,
    output_path: str,
    width: int,
    height: int,
    fps: float = 24.0,
) -> None:
    """Create a short video clip from a still keyframe image."""
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration),
        "-r", str(fps),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Keyframe clip creation failed: {result.stderr[:500]}", file=sys.stderr)
        raise RuntimeError(f"Failed to create keyframe clip from {image_path}")


def compile_video(
    clips: List[str],
    output: str,
    fade_in: float = 0.5,
    fade_out: float = 1.0,
    transition_duration: float = 0.0,
    music: Optional[str] = None,
    keyframes: Optional[List[str]] = None,
    keyframe_hold: float = 0.8,
) -> None:
    """Concatenate clips with cross-dissolve transitions, fade-in/out, and optional music."""

    if len(clips) == 1 and not keyframes and transition_duration <= 0:
        _compile_single(clips[0], output, fade_in, fade_out, music)
        return

    working_clips = list(clips)
    temp_kf_clips = []

    if keyframes:
        if len(keyframes) != len(clips):
            print(
                f"Warning: {len(keyframes)} keyframes for {len(clips)} clips. "
                "Keyframes will be matched to clips by position; extras ignored.",
                file=sys.stderr,
            )

        w, h = get_video_resolution(clips[0])

        expanded = []
        for i, clip in enumerate(clips):
            if i < len(keyframes) and keyframes[i] and os.path.exists(keyframes[i]):
                kf_clip_path = os.path.join(
                    tempfile.gettempdir(), f"kf_still_{i}.mp4"
                )
                _create_keyframe_clip(
                    keyframes[i], keyframe_hold, kf_clip_path, w, h
                )
                temp_kf_clips.append(kf_clip_path)
                expanded.append(kf_clip_path)
            expanded.append(clip)
        working_clips = expanded

    try:
        if transition_duration > 0 and len(working_clips) > 1:
            _compile_with_xfade(
                working_clips, output, fade_in, fade_out, transition_duration, music
            )
        else:
            _compile_with_concat(working_clips, output, fade_in, fade_out, music)
    finally:
        for tmp in temp_kf_clips:
            if os.path.exists(tmp):
                os.remove(tmp)


def _compile_with_xfade(
    clips: List[str],
    output: str,
    fade_in: float,
    fade_out: float,
    transition_duration: float,
    music: Optional[str],
) -> None:
    """Compile clips using FFmpeg xfade filter for cross-dissolve transitions."""

    durations = [get_video_duration(c) for c in clips]
    n = len(clips)

    input_args = []
    for clip in clips:
        input_args.extend(["-i", clip])

    offsets = []
    cumulative = 0.0
    for i in range(n - 1):
        offset = cumulative + durations[i] - transition_duration
        offsets.append(offset)
        cumulative = offset

    total_duration = cumulative + durations[-1]

    vf_parts = []
    af_parts = []

    if n == 2:
        vf_parts.append(
            f"[0:v][1:v]xfade=transition=fade:duration={transition_duration}:offset={offsets[0]}[vout]"
        )
        af_parts.append(
            f"[0:a][1:a]acrossfade=d={transition_duration}[aout]"
        )
        final_v = "[vout]"
        final_a = "[aout]"
    else:
        prev_v = "[0:v]"
        prev_a = "[0:a]"
        for i in range(1, n):
            out_v = "[vout]" if i == n - 1 else f"[v{i}]"
            out_a = "[aout]" if i == n - 1 else f"[a{i}]"
            vf_parts.append(
                f"{prev_v}[{i}:v]xfade=transition=fade:duration={transition_duration}:offset={offsets[i-1]}{out_v}"
            )
            af_parts.append(
                f"{prev_a}[{i}:a]acrossfade=d={transition_duration}{out_a}"
            )
            prev_v = out_v
            prev_a = out_a
        final_v = "[vout]"
        final_a = "[aout]"

    envelope_v = []
    envelope_a = []
    if fade_in > 0:
        envelope_v.append(f"fade=t=in:st=0:d={fade_in}")
        envelope_a.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        envelope_v.append(f"fade=t=out:st={total_duration - fade_out:.3f}:d={fade_out}")
        envelope_a.append(f"afade=t=out:st={total_duration - fade_out:.3f}:d={fade_out}")

    if envelope_v:
        vf_chain = ";".join(vf_parts) + f";{final_v}" + ",".join(envelope_v) + "[vfinal]"
        final_v = "[vfinal]"
    else:
        vf_chain = ";".join(vf_parts)

    if envelope_a:
        af_chain = ";".join(af_parts) + f";{final_a}" + ",".join(envelope_a) + "[afinal]"
        final_a = "[afinal]"
    else:
        af_chain = ";".join(af_parts)

    cmd = ["ffmpeg", "-y"]
    cmd.extend(input_args)
    if music:
        cmd.extend(["-i", music])
    cmd.extend(["-filter_complex", vf_chain + ";" + af_chain])
    cmd.extend(["-map", final_v, "-map", final_a])
    if music:
        cmd.extend(["-shortest"])
    cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "18"])
    cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd.extend(["-movflags", "+faststart"])
    cmd.append(output)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"xfade compilation failed: {result.stderr[:800]}", file=sys.stderr)
        print("Falling back to concat demuxer...", file=sys.stderr)
        _compile_with_concat(clips, output, fade_in, fade_out, music)
        return

    print(f"Compiled: {output} ({total_duration:.1f}s, {len(clips)} clips, {transition_duration}s cross-dissolve)")


def _compile_with_concat(
    clips: List[str],
    output: str,
    fade_in: float,
    fade_out: float,
    music: Optional[str],
) -> None:
    """Compile clips using concat demuxer (hard cuts, no transitions)."""

    durations = [get_video_duration(c) for c in clips]
    total_duration = sum(durations)

    list_path = os.path.join(tempfile.gettempdir(), "ffmpeg_concat.txt")
    with open(list_path, "w") as f:
        for clip in clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    vf_filters = []
    af_filters = []
    if fade_in > 0:
        vf_filters.append(f"fade=t=in:st=0:d={fade_in}")
        af_filters.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        vf_filters.append(
            f"fade=t=out:st={total_duration - fade_out:.3f}:d={fade_out}"
        )
        af_filters.append(
            f"afade=t=out:st={total_duration - fade_out:.3f}:d={fade_out}"
        )

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path]
    if music:
        cmd.extend(["-i", music])
    if vf_filters:
        cmd.extend(["-vf", ",".join(vf_filters)])
    if af_filters:
        cmd.extend(["-af", ",".join(af_filters)])
    if music:
        cmd.extend(["-map", "0:v", "-map", "1:a", "-shortest"])
    cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "18"])
    cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd.extend(["-movflags", "+faststart"])
    cmd.append(output)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Compilation failed: {result.stderr[:500]}", file=sys.stderr)
        sys.exit(1)

    print(f"Compiled: {output} ({total_duration:.1f}s, {len(clips)} clips)")
    os.remove(list_path)


def _compile_single(
    clip: str,
    output: str,
    fade_in: float,
    fade_out: float,
    music: Optional[str],
) -> None:
    duration = get_video_duration(clip)
    vf_filters = []
    af_filters = []
    if fade_in > 0:
        vf_filters.append(f"fade=t=in:st=0:d={fade_in}")
        af_filters.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        vf_filters.append(f"fade=t=out:st={duration - fade_out:.3f}:d={fade_out}")
        af_filters.append(f"afade=t=out:st={duration - fade_out:.3f}:d={fade_out}")

    cmd = ["ffmpeg", "-y", "-i", clip]
    if music:
        cmd.extend(["-i", music])
    if vf_filters:
        cmd.extend(["-vf", ",".join(vf_filters)])
    if af_filters:
        cmd.extend(["-af", ",".join(af_filters)])
    if music:
        cmd.extend(["-map", "0:v", "-map", "1:a", "-shortest"])
    cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "18"])
    cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd.extend(["-movflags", "+faststart"])
    cmd.append(output)

    subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(f"Compiled single clip: {output} ({duration:.1f}s)")


def main():
    parser = argparse.ArgumentParser(
        description="Compile video clips into a final commercial"
    )
    parser.add_argument(
        "--clips", nargs="+", required=True, help="Video clip paths in story order"
    )
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument(
        "--fade-in",
        type=float,
        default=0.5,
        help="Fade-in from black duration (default: 0.5s)",
    )
    parser.add_argument(
        "--fade-out",
        type=float,
        default=1.0,
        help="Fade-out to black duration (default: 1.0s)",
    )
    parser.add_argument(
        "--transition-duration",
        type=float,
        default=1.0,
        help="Cross-dissolve duration between clips (default: 1.0s, set 0 to disable)",
    )
    parser.add_argument(
        "--music", type=str, default=None, help="Optional background music file path"
    )
    parser.add_argument(
        "--keyframes",
        nargs="+",
        default=None,
        help="Optional keyframe image paths (one per clip) to prepend as stills",
    )
    parser.add_argument(
        "--keyframe-hold",
        type=float,
        default=0.8,
        help="Duration to hold each keyframe still before its clip (default: 0.8s)",
    )

    args = parser.parse_args()

    if not check_ffmpeg():
        print(
            "Error: ffmpeg not found. Install with: brew install ffmpeg",
            file=sys.stderr,
        )
        sys.exit(1)

    for clip in args.clips:
        if not os.path.exists(clip):
            print(f"Error: clip not found: {clip}", file=sys.stderr)
            sys.exit(1)

    if args.keyframes:
        for kf in args.keyframes:
            if kf and not os.path.exists(kf):
                print(f"Error: keyframe not found: {kf}", file=sys.stderr)
                sys.exit(1)

    if args.music and not os.path.exists(args.music):
        print(f"Error: music file not found: {args.music}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    compile_video(
        clips=args.clips,
        output=args.output,
        fade_in=args.fade_in,
        fade_out=args.fade_out,
        transition_duration=args.transition_duration,
        music=args.music,
        keyframes=args.keyframes,
        keyframe_hold=args.keyframe_hold,
    )


if __name__ == "__main__":
    main()
