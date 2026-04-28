---
name: ecom-shoe-image-shotlist
description: Footwear e-commerce photography expert. Given a white-background shoe image, automatically analyzes product (compress_product_img.py → Read tool → LLM vision) → selects scene from professional scene library → generates 6 advertising-quality hero images in 2-batch parallel pipeline (batch 1 baseline model → batch 2 remaining 5 images) using three-step pattern (submit → poll → download/upload to CDN) covering on-feet full-body shots, on-feet close-ups, and lifestyle still-life shots → optional video generation for 5 images with highlight reel. Use when the user mentions "shoe photography", "e-commerce hero image", "product shot", or uploads a shoe product image.
---

# Footwear E-Commerce Hero Image + Video One-Stop AIGC Generation

Input a white-background shoe image to automatically generate a set of 6 advertising-quality hero images (on-feet full-body shots, close-up shots, lifestyle still-life shots), and optionally generate short videos compiled into a highlight reel with background music. Supports athletic shoes, fashion shoes, and children's shoes; Asian and Western models.

> **Load sub-files on demand (do not load all at once)**:
> - When selecting scenes → read `SCENE-LIBRARY.md`
> - When referencing complete prompt formats → read `PROMPT-EXAMPLES.md`

---

## Overall Style Tone

- **Quality positioning**: E-commerce fashion advertising campaign level, referencing Nike / Adidas / Zara / Massimo Dutti
- **Lighting**: Natural light preferred (morning light / evening soft light / indoor window light), avoid flat lighting, pursue three-dimensionality
- **Color tone**: Fashion shoes → premium minimalist cool/warm tone; Athletic shoes → energetic tone; Children's shoes → bright and fresh tone; natural and moderate color, no heavy filters
- **Texture**: Subtle film grain, close to fine film photography feel

---

## Input Collection (Must Confirm Before Starting)

**Required**:
- White-background product image path
- Shoe type: athletic shoes / fashion shoes / children's shoes
- Model type: Asian/Western + male adult / female adult / boy / girl

**Optional**:
- Project name (if not provided, auto-use timestamp `YYYYMMDD_HHMMSS`)
- Scene requirements (user-specified takes priority; otherwise read `SCENE-LIBRARY.md` for auto-selection)

> ⚠️ **When shoe type and model type are already provided in the resume prompt** (via static intro follow-up events), parse the values directly and proceed — **do NOT ask these questions again**. Only use `AskUserQuestion` when inputs are genuinely missing (e.g., user uploaded a photo mid-conversation without going through the intro flow). See CLAUDE.md "Input Collection Rules" for the exact template.
>
> 🚨 **After calling `AskUserQuestion` for shoe type / model type, you MUST end your turn and wait for the user's actual selection. NEVER auto-select or proceed to product analysis before the user responds.**

---

## Standard Image Set (Fixed 6 Images)

| # | Type | Key Specs |
|---|---|---|
| 01-02 | On-feet full-body shots | With face, medium/3-4 composition, 35-50mm, f/2.8-4, face must be visible |
| 03-04 | On-feet close-up shots | Below-knee close-up, 85-105mm, f/1.8-2.8, strong background blur; 03/04 must clearly differ in angle/foot pose |
| 05-06 | Lifestyle still-life | Product only, no people; same scene style, 05/06 must clearly differ in position/angle/perspective/shoe placement, no switching to completely different scene type |

**Global Consistency Constraints**:
- 01-04: Same model appearance, same outfit (including sock color and style), same scene tone
- 03-04 blurred background color tone must match 01-02 scene
- **Lifestyle shots (05-06) MUST use the exact same scene location as on-feet shots (01-04)** — same background, same surface material, same lighting environment; this is a hard constraint, not optional
- Image 02: Only reference the **model appearance** from image 01, must simultaneously satisfy:
  - **Pose/action must be clearly different** (01 standing → 02 walking/turning; 01 frontal → 02 side/back; never reuse similar poses)
  - **Scene makes minor variations within the same style** (no switching to completely different scene type; e.g., if 01 is outdoor street, 02 cannot be indoor studio; differences should be in: angle/position/lighting direction/background local elements, at least 3 must differ)
- Lifestyle shot hard constraint: No people, hands, feet, or pets in frame
- Full-body shot hard constraint: No other people in background

**Object Scale** (must declare in lifestyle shot prompts):
- Adult shoes approx. 25-30cm, children's shoes approx. 15-20cm
- Shoe-to-surrounding-object size ratio must be realistic

---

## Tool Paths

All scripts are located in the production base directory:
```
/home/bun/.claude/apps/app-ecom_shoe_image_shotlist/.claude/skills/ecom_shoe_image_shotlist/scripts/
```

**Product analysis**:
Use your visual capabilities (`ViewImage`) to perform structured analysis on the provided image.

**Image generation**:
Use `GenerateImage` tool to concurrently generate all 6 images.

**Video prompt generation**:
Generate video prompts based on the templates in `PROMPT-EXAMPLES.md`.

**Video generation**:
Use `GenerateVideo` tool to concurrently generate all video clips.

**Highlight reel merge**: `merge_highlight_video.py`
Merges 5 video clips with xfade transitions + background music → uploads final video to CDN.
BGM auto-selected from music library based on shoe type.

**Background music library**:
```
/home/bun/.claude/apps/app-ecom_shoe_image_shotlist/.claude/skills/ecom_shoe_image_shotlist/assets/background-music.json
```

**Safety**: No hardcoded API Keys; all models are virtual/synthetic.

---

## Image Generation Workflow

**2-Batch Parallel Strategy**: Image 01 must be generated first (baseline model reference), then images 02-06 are generated in parallel as a single batch.

1. Create project folder: `mkdir -p projects/ecom-shoe/[project name]`
2. Confirm reference image + required info
3. Select scene (user-specified takes priority; otherwise read `SCENE-LIBRARY.md` for smart selection, avoid reusing recent scenes)
4. Write all 6 prompts, then generate in 2 batches:

   **Batch 1 — Image 01 (baseline model, must complete first)**:
   - **Image 01**: White-background product as reference, generate normally (serves as model appearance reference baseline for all subsequent images)

   **Batch 2 — Images 02-06 (5 tasks in parallel, after Batch 1 completes)**:
   - **Image 02**: `img_urls: [WHITE_BG_URL, IMAGE_01_CDN_URL]` dual reference, **only reference model appearance from image 01**; before writing prompt, clarify: ① different action/pose from image 01 (e.g., 01 standing → 02 walking; 01 frontal → 02 side), ② different specific position/angle/lighting within the same style, never switch to completely different scene type
   - **Images 03-04**: `img_urls: [WHITE_BG_URL, IMAGE_01_CDN_URL]` dual reference, ensure outfit/socks match image 01, strong background blur; 03/04 shooting angles must clearly differ (e.g., 03 side → 04 diagonal front; 03 static → 04 tiptoe/stepping), never reuse similar poses
   - **Images 05-06**: `img_urls: [WHITE_BG_URL]` single reference (no model), lifestyle shots; **the scene MUST be the exact same location as images 01-04** (same background, same surface/floor material, same props, same lighting direction) — only the shoe placement, angle, and composition differ between 05 and 06. Before writing prompt: ① explicitly state the same scene elements from 01-04 (e.g., "same wooden café steps, same grey wall, same window light from left"), ② 06 must clearly differ from 05 in placement/angle (e.g., 05 top-down flat → 06 eye-level 45° angled; 05 single front view → 06 pair combination). Never invent a new or different scene type.
   - If referencing complete prompt format → read `PROMPT-EXAMPLES.md`

   **Sequential per-image generation is strictly forbidden** — always use batch submission.

5. After generation, check file size; if over 3MB, compress (adjust JPG quality)

**Prompts must include**: Model description + shoe description + scene setting + action/pose + composition/angle + lens language + lighting texture + color tone + style reference

---

## Quality Checklist (Review Each Image)

**Advertising campaign quality (highest priority)**:
- ✓ Matches Nike/Zara/Massimo Dutti campaign quality, subtle film grain
- ✓ Rich light-shadow layering, no flat lighting; natural color tone, no heavy filters
- ✓ Natural model movement, professional poses, appropriate expressions (avoid stiff/wooden)

**Basic items**:
- ✓ Model appearance/outfit (including socks)/scene fully consistent across images 01-04
- ✓ Model face clearly visible in full-body shots
- ✓ Lifestyle shots have realistic object proportions, natural contact shadows, no floating effect
- ✓ **Images 05-06 scene is identical to images 01-04**: same background, same surface material, same lighting direction — if they look like a different location, reject and regenerate
- ✓ Image 06 and 05 have clearly different shoe placement/angle/composition (no reuse of similar framing)
- ✓ Image 02 and 01 **pose/action clearly different** (cannot reuse similar poses)
- ✓ Image 04 and 03 **shooting angle/foot pose clearly different** (cannot reuse similar angles)

**Video quality review** (manual confirmation required after generation):
- ✓ Shoes visible throughout the video, not out of frame
- ✓ No upward push causing shoes to disappear
- ✓ Full-body shots (01/02 videos) show from head to toe throughout
- ✓ Close-up shots (03/04 videos) lock onto lower leg + shoe area
- If failed → adjust prompt with stronger constraint words and regenerate that video
- ✓ Image 02 and 01 have same scene style, only minor differences in position/angle/lighting/background elements (no scene type switching)
- ✓ 1500×2000px, < 3MB, JPG

---

## User Quality Review & Feedback Loop

After all 6 images are generated, **proactively ask**:
> "Please review these 6 images. Are they up to standard? If any are not, please indicate the number and reason."

- All pass → proceed to video generation workflow
- Some fail → only regenerate failing images (keep passing ones), adjust prompts targeting the issues, ask again
- Same image fails 2 consecutive times → analyze root cause, adjust more elements like scene/angle/lighting

---

## Video Generation Workflow (Optional After Images Pass)

Ask user if they want to generate videos. **Only generate videos for images 01-05, skip image 06.**

**Step 1: Generate Video Prompts**

Generate video prompts based on the templates in `PROMPT-EXAMPLES.md`.

Core principles:
- Models must have **natural movement** (turning/weight shift/arm swing/leg micro-movement), cannot be static
- Shoes **must not deform**, can rotate slightly and slowly (≤30 degrees, slow and steady)
- **Shoes must be visible throughout the video**, this is a hard constraint, non-negotiable
- Camera movement strict restrictions:
  - **Prohibited**: pushing upward past waist (causes shoes to leave frame)
  - **Prohibited**: large push-pull (over 10% of frame range)
  - Allowed: slight pan (left-right ≤5%), slight downward push (toward shoe area), slow pull-back
  - Full-body shots (01/02): camera stays at medium shot, ensuring head to toe visible throughout
  - Close-up shots (03/04): camera locks on lower leg + shoe area, no upward drift
- Prompts **must explicitly include**: `camera stays on shoes throughout`, `shoes always visible in frame`, `no upward pan`

After showing 5 prompts, **review each one**: does each prompt include shoes-always-visible constraint words (`shoes always visible`, `no upward pan`), then ask user to confirm before starting generation.

**Step 2: Create Prompt Text Files**

Create inside project folder (same filename as image, with `.txt` extension):
`01-onfeet-full-01.txt` / `02-onfeet-full-02.txt` / `03-onfeet-closeup-01.txt` / `04-onfeet-closeup-02.txt` / `05-lifestyle-scene-01.txt`

**Step 3: Generate Videos One by One**

Use `GenerateVideo` tool to concurrently generate all video clips:
- `prompt`: corresponding video prompt
- `first_img_url`: the URL returned when that image was generated (if only local file available, first upload using `file_upload_to_obs_sync` to get URL)
- Fixed parameters: `duration=5`, `ratio="3:4"`, `resolution="1080p"`

Download each video immediately after completion, output: `01-onfeet-full-01.mp4` … `05-lifestyle-scene-01.mp4`

**Step 4: Ask if Merging Highlight Video (use AskUserQuestion)**

Use `AskUserQuestion` to ask whether to merge — do NOT use plain text. One question, two options:
- Option 1: "Yes, merge with BGM" — merge 5 clips into a ~15s highlight reel with background music
- Option 2: "No thanks" — skip merge

If the user selects yes, call the `merge_highlight_video.py` script:

```
cd /home/bun/.claude/apps/app-ecom_shoe_image_shotlist/.claude/skills/ecom_shoe_image_shotlist/scripts && python3 merge_highlight_video.py \
  --videos "VIDEO_01_PATH" "VIDEO_02_PATH" "VIDEO_03_PATH" "VIDEO_04_PATH" "VIDEO_05_PATH" \
  --shoe-type SHOE_TYPE \
  --output-dir "PROJECT_OUTPUT_DIR"
```

- Replace `VIDEO_XX_PATH` with the local file paths from Video Step 3 (e.g., `projects/ecom-shoe/outputs/01_video.mp4`)
- Replace `SHOE_TYPE` with one of: `athletic`, `fashion`, `children`
- Replace `PROJECT_OUTPUT_DIR` with the project output directory
- The script automatically:
  1. Trims each clip to 3.5 seconds
  2. Applies fade crossfade transitions (0.5s) between clips
  3. Selects background music from the library matching the shoe type
  4. Mixes BGM with original audio (BGM fades out at the end)
  5. Uploads the final highlight reel to CDN
- On success: prints `[MERGE_RESULT]` followed by a JSON object with `r2_url` (CDN URL), `duration`, `bgm_label`, `file_size_mb`
- Final duration ≈ 5×3.5 − 4×0.5 = 15.5 seconds
- Optional parameters: `--clip-duration 3.5`, `--xfade-duration 0.5`, `--bgm <path_or_url>`

---

## Naming Convention

**Project folder**: `projects/ecom-shoe/[project name or timestamp]/`

**Images**:
```
01-onfeet-full-01.jpg    02-onfeet-full-02.jpg
03-onfeet-closeup-01.jpg 04-onfeet-closeup-02.jpg
05-lifestyle-scene-01.jpg 06-lifestyle-scene-02.jpg
```

**Videos** (inside project folder):
```
01-onfeet-full-01.mp4 … 05-lifestyle-scene-01.mp4
01-onfeet-full-01.txt … 05-lifestyle-scene-01.txt  (prompt files)
background_music.mov
final_video_with_music.mp4
```
