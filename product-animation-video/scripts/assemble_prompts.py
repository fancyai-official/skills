#!/usr/bin/env python3
# Copyright 2026 FancyAI
# SPDX-License-Identifier: Apache-2.0

"""
Assemble NL prompts from prompt-library.json + scene plan JSON.

Usage:
    python3 assemble_prompts.py scene_plan.json

Reads the scene plan, loads prompt-library.json from ../references/,
and prints the assembled prompts for each scene (keyframe + motion).
Useful for debugging prompt construction before running API calls.
"""

import json
import os
import re
import sys


def load_prompt_library():
    lib_path = os.path.join(
        os.path.dirname(__file__), "..", "references", "prompt-library.json"
    )
    with open(lib_path) as f:
        return json.load(f)


def _strip_trailing_period(s):
    return s.rstrip(". ")


def _truncate(text, max_words=25):
    words = text.split()
    truncated = " ".join(words[:max_words]) if len(words) > max_words else text
    return truncated.rstrip(" .—,;:-–")


def assemble_keyframe_prompt(lib, style_id, scene):
    style = lib["styles"][style_id]
    tpl = lib.get("keyframe_start_tpl", lib.get("keyframe_tpl", ""))
    return tpl.format(
        style=style["name"],
        world=_strip_trailing_period(scene["world"]),
        comp=_strip_trailing_period(scene["comp"]),
        color=_strip_trailing_period(scene["color"]),
        avoid=style["avoid"],
    )


def assemble_end_keyframe_prompt(lib, style_id, scene):
    style = lib["styles"][style_id]
    tpl = lib.get("keyframe_end_tpl", "")
    if not tpl:
        return None
    return tpl.format(
        style=style["name"],
        world_end=_strip_trailing_period(scene.get("world_end", scene["world"])),
        comp_end=_strip_trailing_period(scene.get("comp_end", scene["comp"])),
        color=_strip_trailing_period(scene["color"]),
        avoid=style["avoid"],
    )


def assemble_motion_prompt(lib, style_id, scene):
    style = lib["styles"][style_id]
    return lib["motion_tpl"].format(
        motion=_strip_trailing_period(scene["motion"]),
        camera=_strip_trailing_period(scene["camera"]),
        style=style["name"],
        video_reinforce=style.get("video_reinforce", ""),
        camera_angle=scene.get("camera_angle", "eye-level frontal"),
        product_scale=scene.get("product_scale", "30%"),
        product_position=scene.get("product_position", "centered"),
        color_constraint=scene.get("color_constraint", "maintain scene palette"),
    )


def _short_product_desc(product_desc, max_words=8):
    """Shorten product description for storyboard panels."""
    words = product_desc.split(",")[0].split()[:max_words]
    return " ".join(words)


_RATIO_LABELS = {
    "9:16": "9:16 vertical portrait",
    "16:9": "16:9 horizontal landscape",
    "1:1": "1:1 square",
    "4:3": "4:3 landscape",
    "3:4": "3:4 portrait",
    "21:9": "21:9 ultrawide",
}


def _short_character_tag(character):
    """Build a short character tag for storyboard panels (e.g. 'tiny illustrated vine spirit in green')."""
    if not character:
        return ""
    markers = character.get("visual_markers", "")
    desc = character.get("description", "")
    tag = markers if markers else desc
    words = tag.split()[:8]
    return " ".join(words)


def assemble_storyboard_prompt(lib, style_id, scenes, product_desc, ratio="9:16", character=None):
    """Assemble a single storyboard prompt from all scenes.

    Generates a 3x3 panel grid prompt. Only panels with
    product_in_frame=True mention the product (using a short name).
    When a character dict is provided (Cinematic tier), panels with
    character_in_frame=True include the character tag.
    """
    style = lib["styles"][style_id]
    short_product = _short_product_desc(product_desc)
    short_char = _short_character_tag(character) if character else ""
    panel_ratio = _RATIO_LABELS.get(ratio, ratio)
    panel_parts = []
    for i, scene in enumerate(scenes, 1):
        world_short = _truncate(scene["world"], max_words=25)
        if scene.get("product_in_frame", True):
            world_short += f", {short_product} photographic"
        if short_char and scene.get("character_in_frame", False):
            action = scene.get("character_action", "")
            char_tag = f", {short_char} {action}".rstrip()
            world_short += char_tag
        panel_parts.append(f"{i}: {world_short}")

    avoid = style["avoid"] + ". No panel titles, no captions, no decorative text overlays"
    return lib["storyboard_tpl"].format(
        style=style["name"],
        panel_ratio=panel_ratio,
        panel_descriptions=". ".join(panel_parts),
        avoid=avoid,
    )


def assemble_i2v_motion_prompt(lib, scene, direction="safe", character=None):
    """I2V prompt with animation direction + mechanical motion.

    The keyframe defines scene visuals. This prompt adds:
    - moment: animation character (energy, pacing, density)
    - motion: what physically moves
    - product_directive: tier-dependent product render instruction
    - character_directive: character action (Cinematic only)
    - camera: camera movement
    """
    product_in = scene.get("product_in_frame", True)
    product_motion = scene.get("product_motion", "static")

    if not product_in:
        directive = ""
    elif product_motion == "static" or direction == "safe":
        directive = "Product bottle stays photographic and stationary with sharp glass reflections"
    elif direction == "visionary" and any(
        w in product_motion
        for w in ["shatter", "dissolve", "fragment", "grow", "transform"]
    ):
        directive = f"Product bottle {_strip_trailing_period(product_motion)}"
    else:
        directive = f"Product bottle {_strip_trailing_period(product_motion)} while maintaining photographic glass quality"

    char_directive = ""
    if character and scene.get("character_in_frame", False):
        short_char = _short_character_tag(character)
        action = scene.get("character_action", "")
        emotion = scene.get("character_emotion", "")
        parts = [p for p in [short_char, action, emotion] if p]
        if parts:
            char_directive = f". {' '.join(parts)}"

    combined_directive = directive + char_directive

    raw = lib["motion_i2v_tpl"].format(
        moment=_strip_trailing_period(scene.get("moment", "")),
        motion=_strip_trailing_period(scene["motion"]),
        product_directive=combined_directive,
        camera=_strip_trailing_period(scene["camera"]),
    )
    raw = re.sub(r"\.\s*\.\s*\.", ". ", raw)
    raw = re.sub(r"\.\s*\.", ".", raw)
    return raw.strip()


def assemble_storyboard_video_prompt(lib, style_id, scenes, character=None):
    """Assemble a prompt for single-video storyboard animation (Test A approach).

    Used with first_img_url=cropped Panel 1, reference_image_urls=[full storyboard].
    Summarizes each scene's event so Seedance follows the storyboard sequence
    through all 9 panels in a single continuous video.

    When a character is present (Cinematic tier), character actions are woven
    into the narrative summaries alongside the scene events.
    Product identity comes from the images (Panel 1 + storyboard), not the prompt.
    """
    style = lib["styles"][style_id]
    short_char = _short_character_tag(character) if character else ""
    event_summaries = []
    for scene in scenes:
        summary = _truncate(
            scene.get("scene_event", scene.get("title", "")), max_words=18
        )
        if short_char and scene.get("character_in_frame", False):
            action = scene.get("character_action", "")
            if action:
                summary += f", {short_char} {action}"
        event_summaries.append(summary)

    narrative = ", ".join(event_summaries)
    motions = style.get("motions", [])
    ambient = ", ".join(motions[:3]) if motions else "gentle ambient motion"

    return lib["storyboard_video_tpl"].format(
        narrative=narrative,
        style=style["name"],
        ambient_motion=_strip_trailing_period(ambient),
    )


def _shorten_for_multishot(scene):
    """Extract a compact ~15 word summary per scene for multi-shot prompts."""
    words = scene["world"].split()[:8]
    world_short = " ".join(words)
    motion_words = scene["motion"].split()[:6]
    motion_short = " ".join(motion_words)
    return f"{_strip_trailing_period(world_short)}, {_strip_trailing_period(motion_short)}, {scene['camera']}"


def assemble_multishot_prompt(lib, style_id, scenes):
    style = lib["styles"][style_id]
    scene_strs = [_shorten_for_multishot(s) for s in scenes]
    joined = ". Lens switch. ".join(scene_strs)
    return lib["multishot_tpl"].format(
        scenes_joined_by_lens_switch=joined,
        style=style["name"],
    )


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <scene_plan.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        plan = json.load(f)

    lib = load_prompt_library()
    style_id = plan["style_id"]

    scenes = plan.get("shots", plan.get("scenes", []))
    direction = plan.get("direction", "safe")
    character = plan.get("character")

    print("=" * 60)
    print(f"Product:   {plan['product']}")
    print(f"Style:     {lib['styles'][style_id]['name']}")
    print(f"Direction: {direction}")
    print(f"Ratio:     {plan['ratio']}")
    print(f"Shots:     {len(scenes)}")
    if character:
        print(f"Character: {character.get('description', 'n/a')}")
    print("=" * 60)

    for i, scene in enumerate(scenes, 1):
        beat = scene.get("beat", scene.get("shot_type", ""))
        print(f"\n--- Scene {i}: {scene['title']} ({beat}) ---")
        in_frame = scene.get("product_in_frame", True)
        char_in = scene.get("character_in_frame", False)
        print(f"  product_in_frame: {in_frame}")
        if character:
            print(f"  character_in_frame: {char_in}")
        if in_frame:
            kf = assemble_keyframe_prompt(lib, style_id, scene)
            ekf = assemble_end_keyframe_prompt(lib, style_id, scene)
            print(f"\nStart-keyframe prompt ({len(kf.split())} words):")
            print(kf)
            if ekf:
                print(f"\nEnd-keyframe prompt ({len(ekf.split())} words):")
                print(ekf)
        i2v = assemble_i2v_motion_prompt(lib, scene, direction, character)
        print(f"\nMotion prompt [I2V] ({len(i2v.split())} words):")
        print(i2v)

    print(f"\n{'=' * 60}")
    print("Storyboard prompt (all panels):")
    sb = assemble_storyboard_prompt(lib, style_id, scenes, plan["product"], plan.get("ratio", "9:16"), character)
    print(f"({len(sb.split())} words):")
    print(sb)

    print(f"\n{'=' * 60}")
    print("Storyboard video prompt (Test A — single I2V):")
    sv = assemble_storyboard_video_prompt(lib, style_id, scenes, character)
    print(f"({len(sv.split())} words):")
    print(sv)

    print(f"\n{'=' * 60}")
    print("Multi-shot prompt (all scenes):")
    ms = assemble_multishot_prompt(lib, style_id, scenes)
    print(f"({len(ms.split())} words):")
    print(ms)


if __name__ == "__main__":
    main()
