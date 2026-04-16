<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Per-Shot & Multi-Shot Alternative Paths

Reference file for alternative video generation. Read this only when the user explicitly requests a longer video (30-40s), per-shot control, or multi-shot transitions.

**NEVER use these manual Seedance calls as a workaround when `generate_video.py` fails — fix the script issue and re-run instead.**

---

## Alternative 1: Per-Shot I2V (for longer videos or precise control)

When the user needs a **longer video** (30-40s) or **precise control** over individual shots (specific camera movements, product motion per shot, variable pacing), fall back to per-shot I2V generation. Each shot becomes its own video clip, compiled at the end.

### End-Keyframes (per-shot only)

For product-visible panels with camera or product motion, generate individual end-keyframes:

```bash
python3 -c "
import sys, os, requests as req
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from nano_banana import nano_banana_image_gen_sync

save_dir = os.path.expanduser('{PROJECT_DIR}/keyframes')

urls = nano_banana_image_gen_sync(
    prompt='''ASSEMBLED_END_KEYFRAME_PROMPT''',
    img_urls=['PRODUCT_PHOTO_PATH_OR_URL', 'CROPPED_PANEL_PATH'],
    app_model_type='nano-banana-2',
    ratio='RATIO',
    image_size='2K',
    pic_num=1,
)
for i, u in enumerate(urls):
    ext = u.rsplit('.', 1)[-1].split('?')[0] or 'png'
    path = os.path.join(save_dir, f'panel_NUM_end.{ext}')
    with open(path, 'wb') as f:
        f.write(req.get(u).content)
    print(f'Saved: {path}')
"
```

**Which panels need end-keyframes:**
- Product-visible panels with camera movement or product motion → YES
- Product-absent panels (establishing, detail, aftermath) → NO
- Panels with `camera: "static"` and `product_motion: "static"` → OPTIONAL

### Per-Shot I2V Prompt

In I2V mode, the keyframe IS the scene description. The prompt describes ONLY what moves. Use `motion_i2v_tpl`:

```
"{moment}. Animate the scene shown in the input image. {motion}. {product_directive}. {camera}."
```

Use `assemble_i2v_motion_prompt(lib, scene, direction)` from `scripts/assemble_prompts.py`.

- `first_img_url`: Cropped storyboard panel (720p from `crop_storyboard.py`)
- `last_img_url`: End-keyframe for product-visible shots with motion; omit for product-absent or static shots
- Do NOT pass `reference_image_urls` in per-shot mode — product identity comes from the panels
- Launch all 9 shots in parallel

```bash
python3 -c "
import sys, os, requests as req
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from seedance20_video import seedance20_video_gen_sync

save_dir = os.path.expanduser('{PROJECT_DIR}/videos')
os.makedirs(save_dir, exist_ok=True)

urls = seedance20_video_gen_sync(
    prompt='''ASSEMBLED_I2V_MOTION_PROMPT''',
    first_img_url='PANEL_URL',
    duration=DURATION,
    ratio='RATIO',
    resolution='720p',
    generate_audio=True,
)
for i, u in enumerate(urls):
    path = os.path.join(save_dir, f'shot_NUM_{i+1}.mp4')
    with open(path, 'wb') as f:
        f.write(req.get(u).content)
    print(f'Saved: {path}')
"
```

Per-shot clips are compiled using `compile_video.py` (see below).

---

## Alternative 2: T2V Multi-Shot (optional, user can request)

If the user specifically wants fluid "lens switch" transitions between scenes and accepts a softer illustration style, T2V multi-shot is available:

```
multishot_tpl: "{scenes_joined_by_lens_switch}. {style} animated illustration, cinematic."
```

Assemble by joining each scene's shortened summary with "Lens switch." between them.

```bash
python3 -c "
import sys, os, requests as req
sys.path.insert(0, os.path.expanduser('{SKILL_DIR}/scripts'))
from seedance20_video import seedance20_video_gen_sync

save_dir = os.path.expanduser('{PROJECT_DIR}/videos')
os.makedirs(save_dir, exist_ok=True)

urls = seedance20_video_gen_sync(
    prompt='''ASSEMBLED_MULTISHOT_PROMPT''',
    reference_image_urls=['PRODUCT_PHOTO_URL'],
    duration=TOTAL_DURATION,
    ratio='RATIO',
    resolution='720p',
    generate_audio=True,
    vid_num=1,
)
for i, u in enumerate(urls):
    fname = f'multishot_{i+1}.mp4'
    path = os.path.join(save_dir, fname)
    with open(path, 'wb') as f:
        f.write(req.get(u).content)
    print(f'Saved: {path}')
"
```

**T2V trade-offs:**
- Better scene transitions (real "lens switch" cuts)
- Weaker illustration style (tends toward semi-photorealistic)
- Approximate product identity (label text may drift)
- Do NOT use `first_img_url` -- it locks composition and prevents shot transitions
- Uses the verbose `motion_tpl` (not `motion_i2v_tpl`) since there are no keyframes to anchor visuals
- Uses `reference_image_urls` with product photo since there are no keyframes carrying product identity
- Keep total prompt under 80 words

After generation, present the video to the user. They can request regeneration or switch to a different approach.

---

## Per-Shot Compilation (Phase 6)

If the per-shot alternative (Alternative 1) was used, compile all 9 clips into one video with cross-dissolve transitions:

**Script**: `scripts/compile_video.py`

```bash
python3 {SKILL_DIR}/scripts/compile_video.py \
  --clips {PROJECT_DIR}/videos/shot_1_1.mp4 \
          {PROJECT_DIR}/videos/shot_2_1.mp4 \
          {PROJECT_DIR}/videos/shot_3_1.mp4 \
          {PROJECT_DIR}/videos/shot_4_1.mp4 \
          {PROJECT_DIR}/videos/shot_5_1.mp4 \
          {PROJECT_DIR}/videos/shot_6_1.mp4 \
          {PROJECT_DIR}/videos/shot_7_1.mp4 \
          {PROJECT_DIR}/videos/shot_8_1.mp4 \
          {PROJECT_DIR}/videos/shot_9_1.mp4 \
  --transition-duration 0.6 \
  --fade-in 0.5 --fade-out 1.0 \
  --output {PROJECT_DIR}/final/animation.mp4
```

**Execution notes:**
- Set `block_until_ms` to at least 90000 (9 clips take longer to compile)
- Requires `ffmpeg` installed (`brew install ffmpeg` if missing)
- `--transition-duration 0.6`: Short transitions — storyboard continuity reduces visual jumps
- Variable clip durations are handled automatically
- Total runtime: ~32-41s minus transition overlaps ≈ ~28-37s final video
- Optional `--music AUDIO_FILE`: Add background music
