#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fashion Campaign Director — Asset Generator
Builds campaign image prompts with locked Style Seed for visual cohesion.
This script does not call external image APIs, download generated assets, or upload to CDN.

Types: hero, editorial, campaign
Requires --reference (input garment/lookbook image) for Product Fidelity.
Supports product-only mode (no model) via --model_persona "PRODUCT-ONLY".

Output: prompt files only. Bring these prompts to a user-provided generation tool if needed.

Usage:
    # 批量导出 prompt：
    python generate_campaign_assets.py --batch_file projects/brand/shots.json

    # 单张导出 prompt：
    python generate_campaign_assets.py --type hero --reference input.png --photographer "Naturalist, 85mm, Portra 400" --location "Brutalist rooftop" --color_grade "Bleached Warmth"
    python generate_campaign_assets.py --type hero --reference input.png --model_persona "PRODUCT-ONLY" --location "..." --photographer "..."
"""

import argparse
import inspect
import json
import os
import sys

PRODUCT_FIDELITY_DIRECTIVE = """PRODUCT FIDELITY — ABSOLUTE REQUIREMENT (overrides all other instructions):
The product in the output MUST be IDENTICAL to the reference image the user provided. This is the primary constraint.
- MATERIAL & TEXTURE: Exact match. Same weave, sheen, weight, surface quality. Linen stays linen, corduroy stays corduroy.
- COLOR: Exact hue, saturation, and tone. Dusty rose stays dusty rose. Navy stays navy. No color drift whatsoever.
- SILHOUETTE & PROPORTIONS: Exact shape preserved. If oversized and boxy, it stays oversized and boxy. Sleeve length, hem line, shoulder drop, waist position — all unchanged.
- CONSTRUCTION DETAILS: Every button, zipper, stitch, pocket, collar, cuff, seam, and hardware element from the reference MUST appear in the output. Nothing added, nothing removed, nothing relocated.
- PRINT & PATTERN: If the garment has stripes, checks, logos, embroidery, or any surface pattern, reproduce it exactly as in the reference.
- FIT & DRAPE: The way the garment sits on the body must be consistent with its construction — an oversized coat stays oversized, a slim-fit dress stays slim-fit.
You are photographing THIS EXACT garment from the reference image — not designing a similar one, not interpreting it, not improving it. The reference IS the product."""

REALISM_DIRECTIVE = """HIGH-FASHION EDITORIAL + PHOTOGRAPHIC REALISM — CRITICAL:

EDITORIAL STANDARD — the specific magazine language is defined by the Photographer/Narrative fields above. Match THAT style:
- If Vogue/Bazaar: composed, aspirational, precise lighting, clean skin, art-directed perfection.
- If i-D/Dazed/032c: raw, direct, in-your-face. Direct flash, visible skin texture, imperfections celebrated. Snapshot energy with editorial intent. Anti-polish.
- If W Magazine/AnOther: cinematic, narrative-driven, story in every frame. Practicals, warm light, characters not models. Film-still quality.
- If Purple/Document Journal: anti-fashion or gallery-precision. Snapshot aesthetic OR sculptural object treatment. Could hang in a gallery.
- If Harper's Bazaar: graphic drama, bold silhouettes. Strong directional light for shape. Negative space as design. Fashion as form.
- If Arena Homme+/Numéro: hard directional light, body as architecture (Homme+) OR saturated warmth, sensuality (Numéro).

UNIVERSAL EDITORIAL RULES (apply regardless of magazine style):
- POSING: Follow the posing/movement direction from the Narrative field. Match the campaign's creative register. No catalog-stiff or stock-photo poses.
- COMPOSITION: Deliberate framing driven by the garment. The garment drives the crop — show what matters most.
- STYLING HIERARCHY: Garment is the protagonist. Hair/makeup/accessories support but never compete.
- COLOR & TONE: Must match the specified Color Grade. Skin tones accurate and flattering across all ethnicities.

PHOTOGRAPHIC REALISM — must look like a REAL photograph on a REAL set (non-negotiable regardless of magazine style):
- Natural depth of field with appropriate bokeh for the specified lens
- Real film grain matching the specified film stock — never clinically clean
- Natural light falloff, visible catch-lights in eyes, ambient fill from environment
- Real skin texture: visible pores, fine lines, natural asymmetry, no porcelain/waxy/plastic skin
- Correct hand anatomy: exactly 5 fingers, natural proportions, visible knuckles and tendons
- Natural body proportions — no elongated limbs or impossibly small waists
- Fabric obeys gravity: wrinkles at joints, natural drape, buttons pull slightly, collars sit on shoulders
- Environment has real-world wear: scuffs, dust, patina, natural ground contact with shadows
EXPLICITLY AVOID: overly symmetrical faces, waxy glowing skin, floating/stiff fabric, melted fingers, unnaturally perfect teeth, abstract dissolving backgrounds, HDR over-processing, stock-photo smiles, commercial/lifestyle energy, catalog poses"""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_product_only(model_persona: str) -> bool:
    """Check if this is a product-only campaign (no model)."""
    return bool(model_persona) and model_persona.strip().upper() == "PRODUCT-ONLY"


def _build_style_seed(photographer: str, color_grade: str, grain: str, fabric: str,
                      brand: str = "", season: str = "", anchor: str = "") -> str:
    """Build the shared Style Seed prefix for Red Thread consistency."""
    seed_parts = []
    if brand:
        seed_parts.append(f"Brand: {brand}")
    if season or anchor:
        seed_parts.append(f"Collection: {season or ''} | Creative anchor: {anchor or 'editorial'}")
    if photographer:
        seed_parts.append(f"Photographer style: {photographer}")
    if color_grade:
        seed_parts.append(f"Color grade: {color_grade}")
    if grain:
        seed_parts.append(f"Film grain & texture: {grain}")
    if fabric:
        seed_parts.append(f"Product: {fabric}. (Product Fidelity enforced via PRODUCT_FIDELITY_DIRECTIVE below.)")
    return "\n".join(seed_parts)


def _validate_references(reference_images: list, shot_type: str):
    """Ensure reference images are provided — product fidelity depends on them."""
    if not reference_images or len(reference_images) == 0:
        raise ValueError(
            f"[{shot_type}] --reference is required. Product Fidelity cannot be enforced without input images. "
            f"Pass the garment/lookbook image(s) that define the product."
        )


def _save_prompt(prompt: str, output_path: str):
    """Save a generated prompt to a local text file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)


# ---------------------------------------------------------------------------
# Prompt builders (pure — no side effects, no generation)
# ---------------------------------------------------------------------------

def _build_hero_prompt(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    hmu: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
) -> str:
    """Build the hero image prompt string without generating anything."""
    _validate_references(reference_images, "hero")
    style_seed = _build_style_seed(photographer, color_grade, grain, fabric, brand, season, anchor)

    if _is_product_only(model_persona):
        return f"""Product-only fashion campaign hero image. NO MODEL — the garment is the sole protagonist.

{style_seed}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Narrative: {narrative or 'The garment exists in its intended world — still life with editorial gravity.'}

Location/Setting: {location or 'Contemporary editorial environment'}

Shot requirements:
- The garment must be IDENTICAL to the reference image — same fabric, color, silhouette, construction, hardware, prints. This is a photograph of THIS EXACT garment.
- NO human body, hands, or silhouette in the frame — garment only
- Full garment visible — shown as still life, suspended, draped on a form, or artfully laid/hung
- Environment supports the garment, never competes with it — lighting and space do the storytelling
- Each hero shot shows the same garment from a DIFFERENT angle or composition (front, side, back, 3/4, detail-in-context)
- Magazine-cover quality, high-fashion editorial still life — Vogue product pages, not e-commerce
- The garment should feel inevitable in this space, as if it belongs there

Vogue editorial quality. Shot on real film. Natural imperfections. Product-only, no model. Product identical to reference."""

    multi_piece = reference_images and len(reference_images) > 1
    outfit_instruction = ""
    if multi_piece:
        outfit_instruction = f"""
MULTI-PIECE LOOK: The reference images contain {len(reference_images)} separate garments that form ONE complete outfit.
- Combine ALL reference garments into a single styled look on the model
- Each piece must match its reference image EXACTLY (material, color, silhouette, construction details, prints)
- Style them together as a cohesive outfit — natural layering, proportions, and fit
- This is ONE look in a multi-look campaign — the model wears a DIFFERENT outfit in each hero shot"""

    return f"""Fashion campaign hero image.

{style_seed}
{outfit_instruction}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Narrative: {narrative or 'High-fashion editorial moment capturing the garment in its intended world.'}

Location/Setting: {location or 'Contemporary editorial environment'}
Styling & HMU: {hmu or 'Minimal, letting the garment speak'}
Model persona: {model_persona or 'Confident editorial presence, direct gaze'}

Shot requirements:
- Full-body or 3/4 editorial framing showing the COMPLETE outfit
- Every garment in the reference images must appear on the model — styled as one look
- POSING: Follow the posing direction described in the Narrative above. The pose must match the campaign's creative register — if theatrical/sculptural, the body must be dramatic and architectural, not standing neutrally. Posing IS the performance.
- Environment supports the garment, never competes with it
- Magazine-cover quality, high-fashion editorial — must be indistinguishable from a real photo shoot
- The model persona describes THIS specific model — maintain their exact identity across all their shots, but each shot shows a DIFFERENT outfit
- If the campaign has multiple models, each model has their own distinct persona passed via this field

Vogue editorial quality. Shot on real film. Natural imperfections. High-fashion, not commercial. Product identical to reference."""


def _build_editorial_prompt(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    hmu: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
    styling_notes: str = "",
) -> str:
    """Build the editorial shot prompt string without generating anything."""
    _validate_references(reference_images, "editorial")
    style_seed = _build_style_seed(photographer, color_grade, grain, fabric, brand, season, anchor)

    if _is_product_only(model_persona):
        return f"""Product-only editorial fashion photography — detail and texture close-up. NO MODEL.

{style_seed}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Story: {narrative or 'The craftsmanship speaks — stitching, hardware, fabric weave tell the story.'}

Location: {location or 'Environment matching the campaign world'}

Shot requirements:
- DETAIL/TEXTURE CLOSE-UP — this shot proves the garment craftsmanship and authenticity
- The garment must be IDENTICAL to the reference — same fabric, color, construction, hardware
- NO human body, hands, or silhouette — garment details only
- Focus on: stitching quality, hardware (buttons, zippers, buckles), fabric weave/texture, collar construction, hem finishing
- Macro or close-range photography — show what the eye misses at full scale
- Same lighting, grade, grain as entire campaign (Red Thread rule)
- The detail shown must be VISIBLE in the reference image — do not invent construction details

Vogue editorial quality. Shot on real film. Natural imperfections. Product-only detail shot. Product identical to reference."""

    multi_piece = reference_images and len(reference_images) > 1
    outfit_instruction = ""
    if multi_piece:
        outfit_instruction = f"""
MULTI-PIECE LOOK: {len(reference_images)} garments form one styled outfit. Combine them naturally on the model."""

    return f"""Editorial fashion photography — narrative collection shot.

{style_seed}
{outfit_instruction}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Story: {narrative or 'A moment within the collection narrative — movement, attitude, context.'}

Location: {location or 'Environment matching the campaign world'}
Styling: {styling_notes or 'Full look styled with editorial layering and proportions'}
HMU: {hmu or 'Supporting the narrative — not competing with garments'}
Model: {model_persona or 'Editorial model — consistent with the cast persona assigned to this shot'}

Shot requirements:
- Editorial storytelling — model in environment, mid-action or contemplative
- ALL reference garments must appear on the model as one complete look
- POSING: Follow the posing/movement direction from the Story field. Match the campaign's creative energy — bolder treatments demand more theatrical, sculptural, or kinetic body positions. The pose tells the story.
- The model described in the persona field is the specific model for THIS shot — keep their identity locked
- Same lighting, grade, grain as entire campaign (Red Thread rule)
- Vogue / Net-a-Porter editorial quality — must look like a real photograph, not AI-generated

Vogue editorial quality. Shot on real film. Natural imperfections. High-fashion, not commercial. Product identical to reference."""


def _build_campaign_prompt(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
) -> str:
    """Build the wide campaign hero prompt string without generating anything."""
    _validate_references(reference_images, "campaign")
    style_seed = _build_style_seed(photographer, color_grade, grain, fabric, brand, season, anchor)

    if _is_product_only(model_persona):
        return f"""Wide-format product-only campaign hero image for fashion brand. NO MODEL.

{style_seed}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Campaign narrative: {narrative or 'The garment placed in its campaign world — cinematic, aspirational, environmental.'}

Location: {location or 'Campaign environment — wide establishing shot'}

Shot requirements:
- Wide 16:9 composition — suitable for OOH billboards, web hero, press
- The garment must be IDENTICAL to the reference image — same fabric, color, silhouette, construction, hardware, prints
- NO human body, hands, or silhouette — garment in environment only
- Garment placed within the environment (on a chair, hanging in doorway, draped over furniture, suspended in space)
- Cinematic framing with breathing room for text overlay
- Same lighting, same grade across all campaign shots (Red Thread)
- The garment should feel like the protagonist of a film still — inevitable in this space

Vogue editorial quality. Shot on real film. Natural imperfections. Product-only, cinematic. Product identical to reference."""

    multi_piece = reference_images and len(reference_images) > 1
    outfit_instruction = ""
    if multi_piece:
        outfit_instruction = f"""
MULTI-PIECE LOOK: {len(reference_images)} garments form one complete outfit on the model."""

    return f"""Wide-format campaign hero image for fashion brand.

{style_seed}
{outfit_instruction}

{PRODUCT_FIDELITY_DIRECTIVE}

{REALISM_DIRECTIVE}

Campaign narrative: {narrative or 'The definitive campaign moment — cinematic, aspirational.'}

Location: {location or 'Campaign environment — wide establishing shot'}
Model: {model_persona or 'Campaign talent in environment — the specific model cast for this shot'}

Shot requirements:
- Wide 16:9 composition — suitable for OOH billboards, web hero, press
- Cinematic framing with breathing room for text overlay
- POSING: Follow the posing direction from the Campaign narrative. The model's body language must match the treatment's ambition — sculptural, theatrical, or kinetic as directed. The pose is the headline.
- All reference garments visible on model as one styled look (Product Fidelity enforced)
- The model in this shot matches the persona described above — locked identity
- Same lighting, same grade across all campaign shots (Red Thread)
- Campaign-grade production value — Vogue / Net-a-Porter tier, not commercial or lifestyle

Vogue editorial quality. Shot on real film. Natural imperfections. High-fashion, cinematic. Product identical to reference."""


# ---------------------------------------------------------------------------
# Prompt builder registry & defaults
# ---------------------------------------------------------------------------

_PROMPT_BUILDERS = {
    "hero":      _build_hero_prompt,
    "editorial": _build_editorial_prompt,
    "campaign":  _build_campaign_prompt,
}

_DEFAULT_RATIOS = {"hero": "3:4", "editorial": "3:4", "campaign": "16:9"}


# ---------------------------------------------------------------------------
# Single-shot convenience functions (kept for backward compatibility)
# ---------------------------------------------------------------------------

def generate_hero(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    hmu: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
    ratio: str = "3:4",
    resolution: str = "2K"
) -> str:
    """Build the hero editorial prompt without calling an image API."""
    prompt = _build_hero_prompt(
        reference_images, photographer, location, color_grade, grain,
        hmu, narrative, fabric, brand, season, anchor, model_persona,
    )
    print(f"[PROMPT_ONLY] hero ratio={ratio} resolution={resolution}")
    return prompt


def generate_editorial(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    hmu: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
    styling_notes: str = "",
    ratio: str = "3:4",
    resolution: str = "2K"
) -> str:
    """Build the editorial shot prompt without calling an image API."""
    prompt = _build_editorial_prompt(
        reference_images, photographer, location, color_grade, grain,
        hmu, narrative, fabric, brand, season, anchor, model_persona, styling_notes,
    )
    print(f"[PROMPT_ONLY] editorial ratio={ratio} resolution={resolution}")
    return prompt


def generate_campaign(
    reference_images: list,
    photographer: str = "",
    location: str = "",
    color_grade: str = "",
    grain: str = "",
    narrative: str = "",
    fabric: str = "",
    brand: str = "",
    season: str = "",
    anchor: str = "",
    model_persona: str = "",
    ratio: str = "16:9",
    resolution: str = "2K"
) -> str:
    """Build the wide campaign prompt without calling an image API."""
    prompt = _build_campaign_prompt(
        reference_images, photographer, location, color_grade, grain,
        narrative, fabric, brand, season, anchor, model_persona,
    )
    print(f"[PROMPT_ONLY] campaign ratio={ratio} resolution={resolution}")
    return prompt


# ---------------------------------------------------------------------------
# Batch prompt export
# ---------------------------------------------------------------------------

def _build_batch_tasks(shots: list) -> tuple:
    """
    从 shots 规格列表构建任务列表和元数据。纯函数，无 I/O。

    Returns:
        (tasks, shot_meta) 元组
        tasks:     prompt task dictionaries
        shot_meta: 保存 output 路径等信息的元数据列表（与 tasks 等长且顺序一致）
    """
    if not shots:
        raise ValueError("shots list is empty — nothing to generate.")

    tasks = []
    shot_meta = []

    for i, shot in enumerate(shots):
        shot_type = shot.get("type")
        builder = _PROMPT_BUILDERS.get(shot_type)
        if not builder:
            raise ValueError(
                f"[shot {i + 1}] Unknown type: {shot_type!r}. Must be 'hero', 'editorial', or 'campaign'."
            )

        # Filter to only the params the builder actually accepts (avoid TypeError
        # if the JSON has extra keys, e.g. styling_notes on a campaign shot).
        # "reference" in JSON maps to "reference_images" in builder signatures.
        _skip = {"type", "output", "ratio", "resolution", "reference"}
        valid_params = set(inspect.signature(builder).parameters)
        builder_kwargs = {k: v for k, v in shot.items() if k not in _skip and k in valid_params}
        builder_kwargs["reference_images"] = shot.get("reference", [])
        prompt = builder(**builder_kwargs)

        ratio = shot.get("ratio") or _DEFAULT_RATIOS[shot_type]
        task_name = f"{shot_type}_{i + 1}"
        tasks.append({
            "task_name": task_name,
            "reference": shot["reference"],
            "prompt":    prompt,
            "ratio":     ratio,
            "resolution": shot.get("resolution", "2K"),
        })
        shot_meta.append({
            "output":    shot.get("output"),
            "type":      shot_type,
            "index":     i + 1,
            "task_name": task_name,
        })

    return tasks, shot_meta


def _save_batch_outputs(shot_meta: list, tasks: list) -> dict:
    """
    将 prompt 保存到输出路径并返回结果字典。

    Args:
        shot_meta:     _build_batch_tasks 返回的元数据列表
        tasks:         _build_batch_tasks 返回的 prompt 任务列表

    Returns:
        dict: 以 output 路径（或 "type_N"）为键，prompt 文件路径或 prompt 文本为值

    输出标记（供 Claude 解析图片 URL）：
        [CAMPAIGN_PROMPT] shot_name path     — 每个导出的 prompt
    """
    results = {}
    for meta, task in zip(shot_meta, tasks):
        shot_name = meta["task_name"]
        key = meta["output"] or f"{meta['type']}_{meta['index']}.prompt.txt"
        prompt = task["prompt"]

        if meta["output"]:
            out_path = meta["output"]
            if not out_path.endswith(".txt"):
                out_path = f"{out_path}.prompt.txt"
            _save_prompt(prompt, out_path)
            results[key] = out_path
            print(f"[CAMPAIGN_PROMPT] {shot_name} {out_path}")
        else:
            results[key] = prompt
            print(f"[CAMPAIGN_PROMPT] {shot_name}")

    return results


def generate_all_campaign_assets(shots: list) -> dict:
    """
    导出所有 campaign 素材 prompt（hero + editorial + campaign wide）。

    Args:
        shots: 镜头规格列表，每项为包含以下字段的字典：
            type        (str):        "hero" | "editorial" | "campaign"
            reference   (list):       参考图片路径或 URL 列表（必填）
            output      (str, 可选):  本地 prompt 输出路径
            ratio       (str, 可选):  宽高比，默认按 type 自动选择
            resolution  (str, 可选):  "2K" | "4K"，默认 "2K"
            photographer, location, color_grade, grain, hmu,
            narrative, fabric, brand, season, anchor, model_persona,
            styling_notes (hero/editorial only)

    Returns:
        dict: 以 output 路径（或 "type_N"）为键，prompt 文件路径或 prompt 文本为值。

    JSON 示例 (shots.json):
    [
      {
        "type": "hero",
        "reference": ["projects/brand/inputs/look1.png"],
        "photographer": "Soft Naturalist, 85mm f/1.4, Kodak Portra 400",
        "location": "Brutalist rooftop, late afternoon raking light",
        "color_grade": "Bleached Warmth — lifted shadows, amber highlight roll-off",
        "grain": "Medium Portra grain, slightly soft",
        "hmu": "Undone tousled hair, bare skin, no foundation",
        "narrative": "Model turns mid-step, coat caught in wind, full-body 3/4 shot",
        "fabric": "Heavyweight charcoal wool overcoat, notched lapel, single-breasted",
        "model_persona": "East Asian, late 20s, angular jawline, stoic energy",
        "brand": "BRAND",
        "season": "AW26",
        "anchor": "Volcanic Stillness",
        "ratio": "3:4",
        "output": "projects/brand/outputs/hero_1.png"
      }
    ]
    """
    tasks, shot_meta = _build_batch_tasks(shots)

    print(f"[CAMPAIGN PROMPTS] Exporting {len(tasks)} prompts "
          f"({sum(1 for s in shots if s.get('type') == 'hero')} hero · "
          f"{sum(1 for s in shots if s.get('type') == 'editorial')} editorial · "
          f"{sum(1 for s in shots if s.get('type') == 'campaign')} campaign wide) ...")

    results = _save_batch_outputs(shot_meta, tasks)
    print(f"[CAMPAIGN PROMPTS DONE] {len(results)}/{len(tasks)} prompts exported.")
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

GENERATORS = {
    "hero":      generate_hero,
    "editorial": generate_editorial,
    "campaign":  generate_campaign,
}


def main():
    parser = argparse.ArgumentParser(
        description="Fashion Campaign Director — export campaign prompts with locked Style Seed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Batch prompt export:
  python generate_campaign_assets.py --batch_file projects/brand/shots.json

  # Single hero prompt:
  python generate_campaign_assets.py --type hero --reference input.png \\
    --photographer "Soft Naturalist, 85mm, Portra 400" --location "Brutalist rooftop" \\
    --color_grade "Bleached Warmth" --fabric "heavyweight brushed cotton twill" \\
    --output outputs/hero_1.png

  # Product-only hero (no model)
  python generate_campaign_assets.py --type hero --reference input.png \\
    --model_persona "PRODUCT-ONLY" --photographer "Studio Minimalist, 50mm" \\
    --location "Polished concrete, single shaft of light" --output outputs/hero_1.png
        """
    )

    # Batch mode
    parser.add_argument(
        "--batch_file",
        help="JSON file with all shot specs for batch prompt export. "
             "See generate_all_campaign_assets() docstring for the JSON format.",
    )
    # Single-shot mode
    parser.add_argument("--type", choices=list(GENERATORS.keys()),
                        help="Asset type to generate (single-shot mode)")
    parser.add_argument("--reference", nargs="+",
                        help="Reference image paths — REQUIRED for Product Fidelity. Pass all pieces of a look.")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--ratio", default=None,
                        help="Aspect ratio: 1:1, 16:9, 9:16, 3:4, 4:3")
    parser.add_argument("--resolution", default="2K", help="2K or 4K")

    # Style Seed parameters (shared across all types for Red Thread)
    parser.add_argument("--brand", default="", help="Brand name")
    parser.add_argument("--photographer", default="", help="Photographer style, lens, film stock")
    parser.add_argument("--color_grade", default="", help="Color grade name and description")
    parser.add_argument("--grain", default="", help="Film grain and texture description")
    parser.add_argument("--fabric", default="",
                        help="Full product description for fidelity: material + color + silhouette + construction. Not just fabric — include all identifying details.")
    parser.add_argument("--season", default="", help="Season tag (e.g., AW26)")
    parser.add_argument("--anchor", default="", help="Creative anchor word")

    # Type-specific parameters
    parser.add_argument("--location", default="", help="Setting/environment")
    parser.add_argument("--hmu", default="", help="Hair, makeup, styling direction")
    parser.add_argument("--narrative", default="", help="Campaign narrative hook")
    parser.add_argument("--model_persona", default="",
                        help='Model persona, or "PRODUCT-ONLY" for no-model campaigns')
    parser.add_argument("--styling_notes", default="", help="Styling notes for editorial shots")

    # Reject legacy / hallucinated arguments immediately with a clear error message.
    # Using parse_known_args to intercept unknown args before acting on them.
    args, unknown = parser.parse_known_args()
    if unknown:
        legacy_flags = {"--action", "--batch_config", "--batch_tasks", "--max_workers", "--batch_urls"}
        matched = [u for u in unknown if u in legacy_flags or u.startswith("--action")]
        if matched:
            parser.error(
                f"FORBIDDEN LEGACY ARGUMENTS DETECTED: {matched}\n"
                "These parameters no longer exist. This script only exports prompts:\n"
                "  python3 generate_campaign_assets.py --batch_file shots.json\n"
                "NEVER use --action, --batch_config, --batch_tasks, or stdin injection."
            )
        parser.error(f"Unrecognized arguments: {unknown}")

    # ---- Batch mode ----
    if args.batch_file:
        with open(args.batch_file, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # Validate top-level structure — must be a plain list, not a wrapped object.
        # ⚠️ DEFENSIVE ONLY — the CORRECT format is a plain JSON array [...].
        # The auto-unwrap below is a SAFETY NET for when LLMs write the wrong
        # format. It does NOT mean the script "expects" a wrapped object.
        if isinstance(raw, dict):
            # Common LLM hallucinations: {"style_seed": ..., "shots": [...]},
            # {"shots": [...]}, {"data": [...]}, {"tasks": [...]}
            for wrapper_key in ("shots", "data", "tasks", "items", "images"):
                if wrapper_key in raw and isinstance(raw[wrapper_key], list):
                    print(
                        f"[JSON FORMAT ERROR] shots file is wrapped in an object with key "
                        f'"{wrapper_key}". The file must be a plain JSON array [...], not an '
                        f"object {{...}}. Attempting auto-unwrap..."
                    )
                    raw = raw[wrapper_key]
                    break
            else:
                print(
                    f"[JSON FORMAT ERROR] shots file top-level must be a JSON array [...], "
                    f"but got an object with keys: {list(raw.keys())}. "
                    f"Fix the shots file and re-run."
                )
                sys.exit(1)

        if not isinstance(raw, list):
            print(
                f"[JSON FORMAT ERROR] shots file must be a JSON array [...], "
                f"got {type(raw).__name__}. Fix the shots file and re-run."
            )
            sys.exit(1)

        shots = raw

        # Validate each shot's reference field is a list (not a bare string)
        for i, shot in enumerate(shots):
            if isinstance(shot.get("reference"), str):
                print(
                    f"[JSON FORMAT WARNING] shot {i+1} has \"reference\" as a string — "
                    f"auto-converting to list. Fix the shots file to use an array: "
                    f'["URL"] instead of "URL".'
                )
                shot["reference"] = [shot["reference"]]

        results = generate_all_campaign_assets(shots)
        failed = [k for k, v in results.items() if not v]
        if failed:
            print(f"Failed shots: {failed}")
            sys.exit(1)
        print(f"\nSuccess: {len(results)} prompts exported")
        return

    # ---- Single-shot mode ----
    if not args.type:
        parser.error("Either --batch_file or --type is required.")
    if not args.reference:
        parser.error("--reference is required in single-shot mode.")

    default_ratios = {"hero": "3:4", "editorial": "3:4", "campaign": "16:9"}
    ratio = args.ratio or default_ratios[args.type]

    kwargs = {
        "reference_images": args.reference,
        "brand":       args.brand,
        "photographer": args.photographer,
        "color_grade": args.color_grade,
        "grain":       args.grain,
        "fabric":      args.fabric,
        "season":      args.season,
        "anchor":      args.anchor,
        "ratio":       ratio,
        "resolution":  args.resolution,
    }

    type_specific = {
        "hero":      ["location", "hmu", "narrative", "model_persona"],
        "editorial": ["location", "hmu", "narrative", "model_persona", "styling_notes"],
        "campaign":  ["location", "narrative", "model_persona"],
    }

    for param in type_specific.get(args.type, []):
        kwargs[param] = getattr(args, param, "")

    try:
        generator = GENERATORS[args.type]
        result = generator(**kwargs)

        if result and args.output:
            _save_prompt(result, args.output)
            print(f"Saved to: {args.output}")
            result = args.output

        if not result:
            print("Error: Prompt export failed")
            sys.exit(1)

        print(f"\nSuccess: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
