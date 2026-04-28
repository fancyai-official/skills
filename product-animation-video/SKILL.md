<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

---
name: product-animation-video
description: Use this skill whenever the user uploads a product photo and wants to create an animated story video where the product stays photographic while the surrounding world is illustrated and animated -- like a comic or storybook come to life. Covers the full pipeline from product analysis through 9-panel storyboard generation (nano-banana) to a single animated video (Seedance 2.0). Make sure to use this skill whenever the user mentions product animation, animated product video, illustrated product story, comic-style product video, storybook animation, or wants to place a real product into an animated illustrated world -- even if they just say "animate this product" or "make this into an illustrated video." Works for any product category and supports Chinese and English user requests.
---

# Product Animation Video

Transform a real product photo into a cinematic animated story video. A 9-panel illustrated storyboard is generated in a single image, then Seedance 2.0 animates it into a continuous 15-second video. The product is a character — it enters, interacts, and earns its hero moment. Not every panel shows the product; its absence builds anticipation, and its presence earns impact.

---

## Path Convention

All code blocks use two path variables. Set these once per session:

- **`SKILL_DIR`** — root directory of this skill (where this file lives). All scripts are at `{SKILL_DIR}/scripts/`.
- **`PROJECT_DIR`** — output root for the current product, e.g. `~/Desktop/ProductAnimation/{Brand}_{Product}`. Created per run.

---

## Language Handling

Detect the user's language from their input. If Chinese, respond in Chinese. If English, respond in English. All prompts sent to nano-banana and Seedance 2.0 APIs are always constructed in English regardless of user language.

---

## Core Concept: Dual Rendering (Tier-Dependent)

The defining visual identity: a photographic product inside an illustrated world. How strictly this applies depends on the direction tier:

- **Safe** — Product photographic and still. World animates around it.
- **Bold** — Product photographic and dynamic (floats, tilts, sprays) but maintains material quality.
- **Visionary** — Product photographic at rest, may transform at peak moments. HERO shot (panel 8) always restores photographic quality.
- **Cinematic** — An illustrated character drives the story. Three rendering layers: product (photographic), character (illustrated, NEVER photographic, simple iconic design), world (illustrated). Four story shapes available: Quest, Creation, Transformation, Performance — each with different product visibility patterns.

**Prompt templates:**
- `storyboard_tpl`: 3x3 panel grid via nano-banana
- `storyboard_video_tpl`: Primary I2V prompt for single-video generation
- `keyframe_start_tpl` / `keyframe_end_tpl`: Per-shot alternative only
- `motion_i2v_tpl`: Per-shot alternative only

---

## Interaction Progress

The skill has 3 user gates plus a quick platform question (Gate 1.1), followed by automatic execution with one quality checkpoint.

```
┌─────────────────────────────────────────────────────┐
│  Gate 1: PRODUCT CONFIRMATION                       │
│  User uploads photo → AI analyzes → presents card   │
│  with product facts + creative reads                 │
│  → User confirms or corrects                        │
├─────────────────────────────────────────────────────┤
│  Gate 1.1: PLATFORM / ASPECT RATIO                  │
│  AI asks intended platform → User picks             │
│  (or defaults to 9:16 vertical)                     │
├─────────────────────────────────────────────────────┤
│  Gate 2: CREATIVE DIRECTION                         │
│  AI presents 4 concepts:                            │
│  Safe / Bold / Visionary / Cinematic                │
│  → User picks one                                   │
├─────────────────────────────────────────────────────┤
│  Gate 3: ILLUSTRATION STYLE                         │
│  AI recommends top 3 styles for this concept        │
│  → User picks one                                   │
├─────────────────────────────────────────────────────┤
│  EXECUTION (automatic after Gate 3)                 │
│                                                     │
│  Scene Plan Translation (internal, no user gate)    │
│  → Storyboard Generation (nano-banana 3x3 grid)     │
│  → ✓ Storyboard Review (user picks variant)         │
│  → Video Generation (Seedance 2.0 — single video)   │
│  → Present final video + offer iteration            │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- Never skip a gate. Never generate images or video before the user has confirmed all 3 gates.
- Present each gate using AskQuestion for structured selection (directions, styles) and markdown for review (product card, concept cards).
- If the user says "just do it" or "surprise me," pick Bold direction + the most fitting style and proceed directly to execution.

---

## Phase 1: Product Analysis (Brand Strategist Role)

Analyze the uploaded product photo. The agent acts as a **Brand Strategist** -- not just identifying the product but understanding what stories it can tell. Gate 1 presents both the facts AND the creative interpretation, so the user can correct the agent's understanding before it drives the entire video.

### 1.1 Product Facts

Quick identification from the photo. Keep this to 3 lines -- just enough to confirm the agent has the right product:

```
**Product**: [Brand] [Product Name] — [what it is in plain language]
**Ingredients**: [key ingredients, especially those with visual/story potential]
**Origin**: [brand's country/region + any specific heritage or founding story]
```

Example:
```
**Product**: Caudalie Beauty Elixir — grape-water facial mist
**Ingredients**: grape water, grape seed polyphenols, rosemary, rose, myrrh essential oils
**Origin**: Bordeaux, France — founded at Château Smith Haut Lafitte vineyard
```

If the agent cannot identify the brand or ingredients from the photo alone, it should say so and ask the user to provide this information. Wrong ingredients are worse than missing ingredients -- do not guess.

**Product string** (1 line, used in all downstream prompts):
```
"{Brand} {Product Name}, {material description}, {key visual features}"
```

### 1.2 Creative Reads

This is the critical output of Phase 1. The agent interprets the product's **creative meaning** -- what metaphors, narratives, and visual worlds does this product suggest? These reads directly fuel the 4 creative directions in Phase 2.

Present 4-6 creative reads, each a single bullet. Each read extracts a story seed from the product's name, ingredients, usage, appearance, or brand heritage.

```markdown
**Creative reads I see:**
- [Product name as metaphor] — e.g. "Elixir" = alchemy, a magical potion, transformation
- [Usage moment as story trigger] — e.g. Spray mist = a moment of transformation, the mist changes the illustrated world
- [Ingredient as illustrated world] — e.g. Grape vine → growth, harvest cycle, seasons, vineyard landscape
- [Origin as setting] — e.g. Bordeaux wine country → specific light, stone architecture, terroir culture
- [Visual feature as design echo] — e.g. Frosted pink glass → dawn light, petal translucency, soft warmth
- [Brand story as narrative] — e.g. Founded when researchers discovered grape seed antioxidants → a discovery story
```

**Rules for creative reads:**
- Each read must trace back to a specific product attribute (name, ingredient, usage, appearance, or origin). No free-floating "ideas."
- Include at least 1 read based on the **product name** (names carry metaphors: "Elixir," "Glow," "Silk," "Noir" all suggest different stories)
- Include at least 1 read based on **ingredients** (these drive the Bold direction)
- Include at least 1 read based on **usage or form factor** (spray → mist → transformation; lipstick → color reveal; cream → smoothness → water)
- Include at least 1 read based on **character potential** — what kind of protagonist AND what kind of story does this product suggest? The character must derive from a specific product attribute, not be a generic "a woman in a dress." Consider both WHO the character is and WHAT they do: searching (Quest), making (Creation), being changed (Transformation), or expressing (Performance). Examples: a perfume named "EVES" → Eve in a primordial garden (Quest: searching for the forbidden fruit, OR Transformation: the garden changes when she arrives); a grape-based elixir → a vintner's daughter (Creation: blending the formula); a luxury shoe → a tiny explorer in a world of giant shoes (Quest: finding THE one); a lipstick called "Rouge" → a dancer trailing color (Performance: each movement leaves a color trail). This read fuels the Cinematic direction — push for the story shape that is most visually distinct from Safe/Bold/Visionary.
- Reads should be SPECIFIC to this product. "Luxury and elegance" is too generic -- it could describe any product. "The spray mist as a magical veil that transforms the world" is specific to a spray product.

**Why this matters:** The creative reads are the raw material for all 4 directions. If the reads are generic ("luxury, nature, beauty"), the directions will be generic. If the reads are specific ("Elixir = alchemy, mist = transformation trigger, grape vine = growth cycle, a vine-spirit character"), the directions will be compelling and distinct.

### Gate 1: Confirm Product + Creative Reads

Present the Product Facts AND Creative Reads together. Ask the user:

> "Here's what I see in this product — the facts and the creative angles I'd use to build the story. Does this match your product? Anything to add, correct, or steer?"

The user might:
- Correct a fact: "It's actually made with grape seed oil, not grape water"
- Add a story angle: "The brand founder was actually a winemaker's daughter"
- Remove a read: "Don't use the alchemy angle, keep it natural and clean"
- Redirect: "Focus more on the morning routine feel, less on the heritage"

These corrections directly improve the quality of all downstream creative decisions. Only proceed after the user confirms.

### Gate 1.1: Platform / Aspect Ratio

Immediately after Gate 1 confirmation, ask the user where the video will be used. Use AskQuestion with these options:

- **TikTok / Reels / Shorts** (9:16 vertical)
- **Instagram Feed** (1:1 square)
- **YouTube / Landscape** (16:9 horizontal)
- **Cinematic Widescreen** (21:9)
- **Not sure — default vertical**

Store the selected ratio. It flows into the scene plan's `ratio` field and is used for both keyframe generation (nano-banana) and video generation (Seedance 2.0). Aspect ratio affects composition — vertical frames favor close-ups and centered product placement, while landscape frames allow wider illustrated worlds.

If the user picks "Not sure," default to `9:16`.

### Upload Product Photo

Before proceeding to Phase 2, upload the product photo to get a persistent remote URL. This URL is reused across all API calls — nano-banana can handle local paths automatically, but Seedance 2.0 requires URLs for `reference_image_urls`.

```bash
python3 -c "
import sys, os
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from nano_banana import file_upload_to_obs_sync
import base64

photo_path = 'LOCAL_PRODUCT_PHOTO_PATH'
ext = os.path.splitext(photo_path)[1].lstrip('.')
with open(photo_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
url = file_upload_to_obs_sync(file_bytes_or_base64=b64, file_extension=ext)
print(f'Product photo URL: {url}')
"
```

Store this URL as `product_photo_url`. Use it for:
- `img_urls` in nano-banana keyframe calls
- `reference_image_urls` in Seedance 2.0 video calls
- `product_photo` field in the scene plan JSON

Replace `LOCAL_PRODUCT_PHOTO_PATH` with the actual local file path from the user's upload. Set `required_permissions: ["full_network"]`.

---

## Phase 2: Creative Direction (Gate 2) — Creative Director Role

You are the Creative Director. Your job is to take the creative reads from Gate 1 and transform them into 4 specific, compelling, EXECUTABLE concepts at different levels of narrative ambition (Safe, Bold, Visionary, Cinematic). The user is your client — present options with confidence and a recommendation.

The concepts must be more than narratively interesting — they must translate directly to illustrated keyframes (nano-banana) and animated video (Seedance 2.0). Every creative choice you make should be specific enough to prompt an image model.

> **Before starting this phase, read `references/creative-direction.md` for the full creative methodology** — Steps 1-6 (tension mapping, reference mining, emotional targets, concept development, visual translation, self-critique), all narrative structure definitions, the 4 direction tier details, anti-patterns, concept card formats, and arc validation rules.

**What you must produce:** 4 concept cards developed internally with full detail (world, story pattern, narrative engine, 4-beat arc, why it works — Cinematic adds character, want, story shape). **Present to the user only:** the concept name, the pitch, and the key moment. Cinematic adds a one-line character description. Retain the full internal card for Phase 3.

**Creative Director's Recommendation:** After presenting all 4 concepts, recommend one with a specific reason tied to the product's strengths. Don't be neutral.

### Gate 2: User Selection

Use AskQuestion with 4 options (the 4 concept titles, not just "Safe/Bold/Visionary/Cinematic"). Include a "Let me describe what I want" option for users who want to steer or combine.

If the user steers ("I like the vine-growth idea from Bold but want it to feel more magical like Visionary"), synthesize a new concept from their direction. Run the new concept through visual translation + self-critique before presenting the revised concept card for confirmation.

---

## Phase 2b: Illustration Style Selection (Gate 3)

Gate 2 defined the creative direction and concept. Gate 3 is about visual presentation: which illustration style should the concept be rendered in? Any concept can work with any style — this is the user's aesthetic preference.

### Available Styles (Internal Reference)

The full style library below is for YOUR reference when making recommendations — do NOT present the full table to the user. For deeper details on each style, consult `references/illustration-styles.md`.

| Style | Visual Signature |
|---|---|
| **Art Nouveau Botanical** | Ornamental vine borders, flowing organic curves, flat fills with ink linework, gilt accents (Mucha) |
| **Impressionist Painterly** | Visible brushstrokes, soft color blending, impasto texture, light-defined forms (Monet) |
| **Line-Art Botanical / Ghibli** | Clean ink outlines, flat color fills, botanical precision, hand-drawn warmth (Studio Ghibli) |
| **Comic Panel / Storybook** | Bold outlines, flat color blocks, sequential panel layout, storybook narrative |
| **Watercolor** | Soft wet edges, color bleeding into paper texture, translucent washes, organic spreading |
| **Art Deco** | Geometric patterns, bold symmetry, metallic accents, angular forms, 1920s glamour (Erté) |
| **Ukiyo-e (Japanese Woodblock)** | Flat color planes, bold flowing outlines, nature motifs, limited palette (Hokusai) |
| **Chinese Ink Wash (Shanshui)** | Ink gradients, calligraphic brushstrokes, mountain-water landscapes, intentional negative space |
| **Pop Art** | Bold primary colors, Ben-Day dots, high contrast, graphic impact (Warhol/Lichtenstein) |
| **Paper Cut / Collage** | Layered paper textures, visible cut edges, shadows between layers, craft aesthetic (Matisse) |

### Recommendation (internal)

Pick the **top 3 styles** that best fit this specific product + chosen concept. Base the selection on:
- The product's category and visual identity (use "Best for" in `references/illustration-styles.md`)
- The chosen concept's visual direction (which style best renders "The world" described in the concept card?)
- Technical video strength (styles with strong outlines hold better in Seedance 2.0)

Lead with your top recommendation. Keep the reasoning internal — do not explain why each style fits unless the user asks.

### Gate 3: User Selection

**User-facing:** Present only the style names. Use AskQuestion with your top 3 style names as options (e.g. "Art Deco", "Line-Art Botanical", "Art Nouveau"), plus a **"Something else"** option. No descriptions needed — the names are evocative enough for the user to choose.

If the user picks "Something else," present the remaining styles or let them describe a custom style. For custom styles, create an ad-hoc entry following the `prompt-library.json` structure (visual, video_reinforce, motions, avoid) and proceed.

---

## Phase 3: Scene Plan Translation (Internal — No User Gate)

This is the critical bridge between creative direction and execution. The concept card (Gate 2) + style (Gate 3) are translated into a Scene Plan JSON that drives keyframe and video generation. No user review — the user already approved the concept's 4 beats and the illustration style.

> **Before starting this phase, read `references/scene-plan-guide.md` for the full field-by-field reference** — beat-to-scene mapping, narrative progression rules, 9-shot structure tables (standard + all 4 character-driven shapes), field translation guide (`world`, `comp`, `camera_angle`, `color`, `moment`, `motion`, etc.), visual continuity rules, and quality checks.

**The `world` field is the single most important field in the JSON.** It becomes the core of the nano-banana keyframe prompt. Write `world` as if you're writing a nano-banana prompt — specific, visual, concrete.

### Scene Plan JSON Structure

```json
{
  "product": "[product string from Phase 1]",
  "product_photo": "[path or URL to product photo]",
  "direction": "[safe / bold / visionary / cinematic]",
  "style_id": "[chosen style from Gate 3]",
  "ratio": "[aspect ratio]",
  "shared_elements": "[2-3 visual elements that persist across shots]",
  "color_arc": "[overall color journey]",
  "narrative_engine": "[the question or desire that pulls the viewer through]",
  "story_pattern": "[Quest / Reveal / Genesis / Day / Transformation / Character Quest / Character Creation / Character Transformation / Character Performance]",
  "character": {
    "description": "[Cinematic only — illustrated figure description]",
    "visual_markers": "[3 max distinctive features]",
    "want": "[the character's desire]",
    "rendering": "[illustrated in {style} style — NEVER photographic]"
  },
  "shots": [
    {
      "panel": 1,
      "shot_type": "[see scene-plan-guide.md for valid values per structure]",
      "product_in_frame": false,
      "product_motion": "[static / float / tilt / rise / drift / spray / etc.]",
      "character_in_frame": false,
      "character_action": "[Cinematic only]",
      "character_position": "[Cinematic only]",
      "character_scale": "[Cinematic only]",
      "character_emotion": "[Cinematic only]",
      "title": "[shot name]",
      "scene_event": "[what HAPPENS in this shot]",
      "scene_because": "[cause-effect link to previous shot]",
      "world": "[illustrated world description — prompt-quality, ~40-60 words]",
      "world_end": "[per-shot alternative only]",
      "comp": "[composition description]",
      "comp_end": "[per-shot alternative only]",
      "camera_angle": "[eye-level frontal / slight high-angle / slight low-angle / three-quarter view]",
      "color": "[color palette for this shot]",
      "color_constraint": "[negative constraint]",
      "product_scale": "[percentage or n/a]",
      "product_position": "[position or n/a]",
      "moment": "[cinematic animation direction — energy, pacing, density]",
      "motion": "[what animates]",
      "camera": "[camera movement]",
      "duration": 4
    }
  ]
}
```

**Duration by shot type** (per-shot Alternative 1 only — primary path uses fixed 15s):
- establishing: 4-5s, detail: 2-3s, reveal: 4-5s, interaction: 4-5s, acceleration: 3-4s, climax: 5-6s, aftermath: 3-4s, hero: 4-5s, signature: 3-4s
- Total: ~32-41 seconds (per-shot path only)

### Save Scene Plan

After quality checks pass, save the scene plan JSON to disk:

```bash
python3 -c "
import json, os
plan = SCENE_PLAN_DICT
save_dir = os.path.expanduser('{PROJECT_DIR}')
os.makedirs(save_dir, exist_ok=True)
path = os.path.join(save_dir, 'scene_plan.json')
with open(path, 'w') as f:
    json.dump(plan, f, indent=2)
print(f'Saved: {path}')
"
```

Replace `SCENE_PLAN_DICT` with the actual Python dict.

### Preview Prompts (Optional Debug Step)

```bash
python3 {SKILL_DIR}/scripts/assemble_prompts.py \
  {PROJECT_DIR}/scene_plan.json
```

Prints assembled prompts with word counts. Useful for catching prompt issues before generation.

---

## Phase 4: Storyboard Generation + Review Checkpoint

**This is the critical visual quality gate.** The storyboard is the first time the user sees what their concept actually looks like as a STORY. All 9 panels are generated in a single nano-banana call, ensuring inherent visual continuity across the sequence.

### Storyboard Generation (nano-banana — single image)

Generate a **single 3x3 storyboard image** containing all 9 shots. nano-banana sees the entire story at once, producing consistent style, palette, and spatial continuity that per-frame generation cannot achieve.

#### Step 1: Assemble the storyboard prompt

Use `assemble_storyboard_prompt()` from `scripts/assemble_prompts.py`. This:
- Truncates each shot's `world` to ~25 words (keeping total prompt under ~280 words)
- Appends "the [product description] appears photographic" ONLY to panels where `product_in_frame: true`
- Fills the `storyboard_tpl` template

#### Step 2: Generate the storyboard

```bash
python3 -c "
import sys, os, json, requests as req
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from nano_banana import nano_banana_image_gen_sync
from assemble_prompts import load_prompt_library, assemble_storyboard_prompt

plan_path = os.path.expanduser('{PROJECT_DIR}/scene_plan.json')
with open(plan_path) as f:
    plan = json.load(f)

lib = load_prompt_library()
prompt = assemble_storyboard_prompt(lib, plan['style_id'], plan['shots'], plan['product'], plan['ratio'])
print(f'Storyboard prompt ({len(prompt.split())} words):')
print(prompt)

save_dir = os.path.expanduser('{PROJECT_DIR}/storyboard')
os.makedirs(save_dir, exist_ok=True)

urls = nano_banana_image_gen_sync(
    prompt=prompt,
    img_urls=['PRODUCT_PHOTO_PATH_OR_URL'],
    app_model_type='nano-banana-2',
    ratio=plan['ratio'],
    image_size='4K',
    pic_num=2,
)
for i, u in enumerate(urls):
    ext = u.rsplit('.', 1)[-1].split('?')[0] or 'png'
    path = os.path.join(save_dir, f'storyboard_v{i+1}.{ext}')
    with open(path, 'wb') as f:
        f.write(req.get(u).content)
    print(f'Saved: {path}')
"
```

**Key settings:**
- The script prints the assembled prompt to the terminal for debugging — **do not paste that prompt into the user-visible chat** at storyboard review; the user should only see the two storyboard images.
- `image_size='4K'` — required. At 4K with 9:16 ratio (~2304x4096), each panel is ~768x1365, exceeding the 720p Seedance input requirement
- `pic_num=2` — generates 2 storyboard variants for the user to choose between
- `img_urls` includes the product photo so nano-banana knows what the product looks like (even though not every panel shows it)
- Set `block_until_ms` to at least 300000 and `required_permissions: ["full_network"]` — 4K generation takes longer

#### Step 3: Crop panels

After the user approves a storyboard variant, crop it into 9 individual panels at video resolution:

```bash
python3 -c "
import sys, os
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from crop_storyboard import crop_storyboard

# Adjust width/height to match the ratio: 9:16 → 720x1280, 16:9 → 1280x720, 1:1 → 720x720
paths = crop_storyboard(
    'SELECTED_STORYBOARD_PATH',
    os.path.expanduser('{PROJECT_DIR}/keyframes'),
    target_width=720,
    target_height=1280,
    border_trim_px=8,
)
for p in paths:
    print(p)
"
```

This outputs `panel_1.png` through `panel_9.png` in the keyframes directory, each at 720p. These are useful for:
- **User review** — individual panels are easier to evaluate than the full grid
- **Per-shot I2V** (Alternative 1) — each panel becomes the `first_img_url` for its shot
- **Note**: The primary pipeline (`generate_video.py`) does NOT use these files — it auto-crops Panel 1 and 9 from the storyboard directly, guaranteeing panel/storyboard match.

#### Step 4: Ready for Video Generation

After the user approves a storyboard, proceed directly to Phase 5. The `generate_video.py` script only needs the storyboard image and scene plan — it handles panel cropping, upload, and video generation internally.

### Storyboard Review Checkpoint

**User-facing (minimal UI):** Show only the storyboard images. Do not paste the assembled prompt, panel-by-panel summaries, or long narrative descriptions — the user decides from the visuals alone.

1. **Display both full storyboard variants inline** (the two 3x3 images only — not cropped panels).

2. **Choice** — use AskQuestion with a short label only, e.g. options "Variant 1", "Variant 2", "Regenerate both". No need for a long question body beyond what the UI requires. If the user picks Regenerate both, adjust the scene plan's `world` fields and re-run storyboard generation.

**Internal checks (agent only — do not list or explain these to the user unless the user asks):** Before showing images, verify story continuity, product panel placement vs. scene plan, style consistency, color arc, and product identity. If one panel is weak but the grid reads as a story, acceptable for the primary path (Seedance blends across panels). Do not proceed to video until the user has chosen a variant (or confirmed after regenerate).

### Executability Assessment (before proceeding to video)

After the storyboard is approved and panels cropped, assess each shot for I2V translation risk using the table below — **internally**. For the storyboard-guided primary path, risks are usually mitigated; this matters most for per-shot Alternative 1.

| Risk Factor | Detection | Impact | Mitigation |
|---|---|---|---|
| Non-standard camera angle | Check `camera_angle` field | Seedance normalizes to frontal | Suggest `slight high-angle` or `slight low-angle` instead |
| Complex product-environment overlap | Check `world` for "dissolves into", "merges with" | I2V can't composite | Simplify to product NEAR the element, not blending into it |
| Fine texture detail | Check `world` for micro-level descriptions | Video model smooths detail | Keep in keyframe prompt but don't expect survival in video |
| Product text legibility required | Check if design relies on readable text | All I2V models garble text | Plan for post-production text overlay instead |
| Ambitious product motion (Bold/Visionary) | Check `product_motion` for "shatter", "grow", "dissolve" | Unreliable I2V interpolation | Accept artistic imperfection or simplify to reliable motion |

If something is critically wrong for video (e.g. unreadable label is essential), one short optional line to the user is enough — no table, no lecture. Otherwise proceed to Phase 5.

---

## Phase 5: Video Generation (Seedance 2.0)

### Primary: Storyboard-Guided Single Video

Generate a **single continuous video** from the storyboard using the `generate_video.py` script. The script handles everything in one command: auto-crops Panel 1 and Panel 9 from the storyboard, uploads all assets, assembles the prompt, calls Seedance, downloads, auto-trims grid endings, and verifies frames.

**How it works internally:**
- **Auto-crop**: Panel 1 (top-left cell) and Panel 9 (bottom-right cell) are cropped directly from the storyboard image. This eliminates panel/storyboard mismatch — the panels always come from the exact storyboard being used as reference.
- `first_img_url`: Auto-cropped **Panel 1** — anchors the opening frame with high fidelity
- `last_img_url`: Auto-cropped **Panel 9** — attempts to anchor the ending frame
- `reference_image_urls`: The **full 3x3 storyboard grid** — guides Seedance through the narrative sequence left-to-right, top-to-bottom
- Duration: **15s** (Seedance maximum)
- **Auto-trim**: Seedance sometimes ends the video by pulling back to show the full 3x3 storyboard grid (last 1-2 seconds). The script detects this by scanning frames backward from the end, then auto-trims the video to the last clean frame, producing a ~13-14s video with a clean ending
- **Minimum duration guard**: If the grid appears too early (before 8s), the trim is skipped and a warning is printed — a 3s video is worse than a 15s video with a grid ending. Re-generate with a different storyboard variant instead.

**Why this works:** Seedance treats `first_img_url` literally as the opening frame (ensuring first-frame fidelity) while using `reference_image_urls` to understand the full narrative arc and visual style. The model follows the storyboard grid reading order, producing smooth transitions between scenes without manual compilation.

#### Generate the video

```bash
python3 {SKILL_DIR}/scripts/generate_video.py \
  --storyboard {PROJECT_DIR}/storyboard/SELECTED_STORYBOARD.png \
  --plan {PROJECT_DIR}/scene_plan.json \
  --output-dir {PROJECT_DIR}/final
```

Replace `SELECTED_STORYBOARD` with the user's chosen storyboard variant (e.g., `storyboard_v1.png`).

**Execution notes:**
- Set `block_until_ms: 0` — runs in background, typically 5-10 minutes for 15s video
- Set `required_permissions: ["full_network"]`
- The script automatically: crops Panel 1 & 9 from the storyboard, uploads all three assets, assembles the prompt, calls Seedance, downloads the video, auto-trims any grid ending, and verifies both first and last frames
- Add `--prefix animation_deco` to customize the output filename prefix
- Add `--border-trim 12` if grid lines are still visible in panels (default: 8px)

**Built-in safety checks:**
1. **Panel/storyboard match guarantee**: Panels are auto-cropped from the storyboard — never from a separate file, never from a different variant. Mismatch is structurally impossible.
2. **Post-generation grid trim**: Scans backwards from the last frame to detect grid onset, then trims the video to the last clean frame (typically removes the last 1-2 seconds where Seedance pulls back to show the full storyboard). Final video is ~13-14s
3. **Minimum duration guard**: If trim would produce a video under 8s, keeps the full video and warns instead — a short video is worse than a grid ending
4. **Post-trim verification**: Both first and last frames are checked for grid patterns

Present the generated video to the user. The single 15s video is the final output — no compilation needed.

**If `generate_video.py` fails or errors out:**
- **DO NOT** fall back to calling `seedance20_video_gen_sync` directly. Manual Seedance calls bypass auto-crop, auto-trim, and frame verification — this is how grid bugs reappear.
- Instead: read the error message, fix the root cause (missing file, wrong path, network timeout), and re-run `generate_video.py`.
- Common failures and fixes:
  - `Task timed out` → Seedance was slow. Re-run the same command — the script generates a new task.
  - `Task failed with status=FAILURE` → Seedance rejected the input. Check that the storyboard exists and is a valid image.
  - `WARNING: frame appears to show a storyboard grid` → the auto-trim should have handled this. If the warning persists after trim, re-run with a different storyboard variant.
  - `WARNING: Grid detected at X.Xs ... below 8.0s minimum` → the grid appeared too early. Re-run the command, or try a different storyboard.

### Alternatives

For per-shot I2V (longer 30-40s videos, precise shot control) or T2V multi-shot, read `references/per-shot-alternative.md`. **Only use these when the user explicitly requests a longer video or per-shot control — never as a workaround for `generate_video.py` failures.**

---

## Phase 6: Output + Delivery

### Primary Path (Storyboard-Guided Single Video)

The single 15s video from Phase 5 is already saved in `final/` — no copy or compilation needed. Present the final animation to the user.

### Per-Shot Path

If the per-shot alternative was used, see `references/per-shot-alternative.md` for compilation instructions using `compile_video.py`. The per-shot path uses `videos/` for individual shot clips and compiles into `final/`.

---

## Output File Structure

```
{PROJECT_DIR}/
├── scene_plan.json               (the scene plan JSON from Phase 3 — 9 shots)
├── storyboard/
│   ├── storyboard_v1.png         (full 3x3 storyboard variant 1)
│   └── storyboard_v2.png         (full 3x3 storyboard variant 2)
├── keyframes/                    (for review and per-shot alternative; primary path auto-crops from storyboard)
│   ├── panel_1.png … panel_9.png
├── final/
│   └── animation_1.mp4           (primary: single storyboard-guided video, 15s)
└── videos/                       (per-shot alternative only — not created for primary path)
    # ├── shot_1_1.mp4
    # ├── shot_2_1.mp4
    # └── ...
```

---

## Iteration

After presenting the final video, ask if changes are needed. Use AskQuestion with these options:

- **Love it — done**
- **Tweak a scene** (targeted fix)
- **Try a different style** (loop back to Gate 3)
- **Try a different concept** (loop back to Gate 2)
- **Start over with a different product**

### Targeted Fixes (no gate reset)

For issues with the output, only regenerate what's affected:

- **Storyboard issue** → revise the shot's `world` field, regenerate the full storyboard (1 nano-banana call), and re-run `generate_video.py` with the new storyboard
- **Single panel weak** → generate an individual keyframe for that panel using `keyframe_start_tpl`, regenerate storyboard if the weak panel is Panel 1 or 9
- **Animation doesn't follow narrative** → revise the `scene_event` fields to be more descriptive, regenerate the storyboard video prompt, and re-run `generate_video.py`
- **Product identity weak in a panel** → increase product description specificity in that panel's `world` field, regenerate storyboard
- **Video too short** → switch to per-shot alternative for a 30-40s video (read `references/per-shot-alternative.md`)
- **Need precise shot control** → switch to per-shot alternative for individual shot regeneration
- **First frame doesn't match Panel 1** → try `--border-trim 12` (trims more grid border from cropped panel), re-run `generate_video.py`
- **Grid ending persists** → re-run `generate_video.py`, or try a different storyboard

The scene plan JSON makes targeted fixes easy — change one field without touching others.

### Loop-Back to Gate 3 (new style, same concept)

If the concept is right but the visual style doesn't land, loop back to Gate 3. The user picks a new illustration style, and execution restarts from Phase 3 (scene plan translation). Gate 1 and Gate 2 outputs are preserved — no need to re-analyze the product or re-generate concepts.

### Loop-Back to Gate 2 (new concept)

If the concept itself missed the mark, loop back to Gate 2. Present the original 4 concepts again (or generate fresh ones if the user wants). Gate 1 output is preserved — no need to re-analyze the product. After the user picks a new concept, proceed through Gate 3 and execution as normal.

### Full Restart

Only if the user wants to try a completely different product. Start from Gate 1.
