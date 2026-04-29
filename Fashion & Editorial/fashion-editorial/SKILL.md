---
name: editorial-fashion-six
description: "Six fixed 3:4 editorial fashion storyboard images from the same SKU's multi-angle white-background product photos. Covers brand ID, layered non-flat scenes (reference-scenes), styling (reference-outfit), poses (reference-pose-vocabulary), optional web research, triple-choice, hero-image anchoring, HTTP nano-banana generation, and per-frame QC with targeted regeneration only; bright natural daylight; do not paste full prompts in chat. Use for six editorial, magazine, or mood shots, lookbook storyboards, or nano-banana synced generation for one garment. Triggers include requests for six frames, six editorial images, storyboard six, magazine-style, nano banana image gen. Do not use for eight-slot global PDP or marketplace detail-page matrices—use ecommerce-fashion-workflow instead."
metadata:
  version: "1.2.0"
compatibility: "Network for optional web search and nano-banana image generation (HTTP or IDE-integrated); env NANO_BANANA_BASE_URL optional when using the HTTP API. No Python scripts in this skill package."
---

# White-background product → 6 editorial fashion shots

## Critical rules (read first)

- **Output count and ratio**: exactly **six** images, all **3:4**; same `image_size` across the set (recommended 2K).
- **Phased generation**: produce **frame 1 first**, user confirms URL, then frames 2–6 with frame 1 as hero anchor—never all six at once.
- **Scope**: this skill is **not** the eight-image Amazon/Shopify PDP workflow—route that to `ecommerce-fashion-workflow`.
- **Privacy / UX**: **do not** paste full generation prompts in chat unless the user explicitly asks; share triple-choice, frame labels, URLs, checkpoints.
- **SKU fidelity**: frame 1 must match the **exact** front flat; if QC fails, regenerate **that frame only** before continuing.
- **Bundled references**: depth and taboos—[reference-scenes.md](reference-scenes.md); outfit formulas—[reference-outfit.md](reference-outfit.md); pose vocabulary—[reference-pose-vocabulary.md](reference-pose-vocabulary.md); **model tiers, body/face density, composition scale**—[reference-model-presets.md](reference-model-presets.md) (load when executing Step 4 and QC 1/4/9).

## Input: multi-angle product images

Users usually supply **several angles of the same SKU** (white-background or flat lay: front, side, back, etc.). Before running, **map angles**: from filenames or user notes, label which image is **front / side / back**; later shots pick the matching product reference. **If client assets cannot reliably distinguish front vs back** from filename, notes, or image structure (symmetrical styles, only one image, conflicting labels, etc.), **ask the client first** which is front and which is back (or ask for relabeled assets)—**do not** guess front/back without confirmation. **Do not** ask by default whether a back view exists—**do not** ping the client only for “do you have a back image.” **Shot 4** in this skill is a **front variation** by default (see step-6 table) and **does not require** a back image. If an angle is **actually missing** (e.g. no side), substitute sensibly for that frame and **briefly** tell the user.

## When to use this skill vs the 8-image e-commerce skill

| Need | Use |
|------|-----|
| 6 images, magazine / mood / story feel; unified scene and light | **This skill** (`editorial-fashion-six`) |
| **Global PDP 8-slot matrix** (Amazon / Shopify / DTC–style detail page: front / back / side / top–bottom detail / macro / flat lay / styling) | **`ecommerce-fashion-workflow`** |

Shared ideas: white-bg reference, hero anchoring, de-gray and lift. This skill is **6 fixed frames** (including shot 4 **front variation** and fabric close-up); it differs from the 8-slot matrix in count and shot mix.

## Examples

**Example A — Magazine six-pack**

- **User**: “Same hoodie white-bg front/side—I need six magazine-style street editorial shots, nano banana.”
- **Agent**: Map angles; brand ID; source QA; triple-choice; frame 1 with front flat → confirm URL; frames 2–6 with anchor + angle refs; QC each frame; save to `outputs/editorial-six/…`.

**Example B — Client sheet + Excel row**

- **User**: Uploads images + “SKU-A—the client sheet says coffee-shop window scene.”
- **Agent**: Required scene column wins over defaults; still layered foreground/mid/background per reference-scenes; execute same six-frame rhythm and QC.

## Prompt visibility (chat)

- **Internally** still write `prompt` and run **nano-banana image generation** (same parameters as below); **do not paste** the full prompt in the conversation (see Critical rules).
- Show the user: **triple-choice summary**, **frame + shot type**, **result URL or image**, **checkpoints**; full prompts only if the user asks.

## Direct image generation (nano banana / HTTP)

1. **Implementation**: Use **nano-banana image generation** available in the current environment (Fancybos-style HTTP API or IDE-integrated tooling). **No** Python scripts ship with this skill package.
2. **Parameters (unified across the set)**:
   - `ratio` **fixed `"3:4"`** (all 6 the same).
   - `image_size` recommended **`"2K"`** (match production; keep consistent).
   - `app_model_type` default **`"nano-banana-2"`** unless user specifies pro.
   - Frame 1 may need longer runs—increase `timeout` (seconds); `poll_interval` ~2s is fine.
3. **Optional env**: `NANO_BANANA_BASE_URL` overrides default `http://ai-api.fancybos.com` (test/prod).
4. **Frame 1**: `img_urls` = user’s **front product image** (URL or local path).
5. **Frames 2–6**: **frame 1 output URL** as hero anchor; per shot combine **matching-angle product refs** with anchor in `img_urls` (e.g. `[frame1_URL, side product]`); count per API limit. **Frame 4** is **front** framing (see table): `img_urls` = **front product** + frame 1 anchor; **not** default back view; **no** back asset required.

## Step 1: Brand ID and scene recommendation

1. **Identify brand**: from user copy, product logo/hang tag, filenames, or client sheet—**brand** (or line) when possible.
2. **If brand is clear**: recommend scene and light in that brand’s usual **visual tone** (e.g. American street, Korean fresh, outdoor tech, quiet luxury minimal) and why it fits the silhouette; mirror **public campaign** location types when appropriate—**do not** invent off-brand mood. Summarize typical **model hair/makeup mood** (influencer-polished, outdoor natural, sporty clean, etc.) for step 4.
3. **Background reference (avoid flatness)**: if word lists alone yield **empty, flat, single-plane** backgrounds, **web-search** same-brand, same category/season campaigns, lookbooks, official social—**abstract** richer layered elements into internal prompt; **do not** copy whole copyrighted frames. Without brand, search **category** benchmarks. When **locking location**, follow [reference-scenes.md](reference-scenes.md) **“Scene diagram: layering and light vocabulary” · §1 How to use**: **(1)** Lock scene family from triple-choice and **MLB quick reference**; **(2)** **Foreground / midground / background** each at least one clear element; **(3)** add **light** (§3 there); **(4)** **ground and footing** (§4); **(5)** taboos per MLB and main Skill. **Background defaults to avoid**: no default **luxury hotel lobby**, **office elevator hall** (symmetrical elevators, glass shafts, polished stone, cold top light, “HQ” corridor)—prefer outdoor natural or **lifestyle interior** (coffee/dessert, window-lit casual). Optionally `avoid hotel lobby, office elevator hall, symmetrical elevator doors, marble corporate corridor` (don’t stack); if client Excel **explicitly** wants such interiors, follow that job.
4. **No brand or unclear**: recommend from **category and experience**; layer [reference-scenes.md](reference-scenes.md) **MLB** quick scenes and taboos; if client Excel has **required scene**, that row wins.
5. For the user: **short takeaway** only—**no** long essay.

## Step 2: Source image QA

Check each new garment batch: light too dark, creases/shadows crushed, glare, heavy crop, messy background.

- If risky: note possible inherited creases/shadows/crop; ask for **cleaner white-bg / flat** or confirm proceed.
- If OK, go to triple-choice.

## Step 3: Style and narrative (triple-choice)

From silhouette, fabric, audience, and step 1 (including **web** layering), give **3 differentiated** directions; each has **scene**, **light mood**, **emotional tone** (2–4 sentences); scene must show **depth** (avoid one blank wall / solid cyclorama). Default **bright natural light (clear white daylight)**—airy, clean, slightly higher saturation; **avoid** gray murk and dirty shadows; if brand/user wants **warm / golden hour / film cast**, state in triple-choice or that option; if brand wants low-key, state separately. After pick, internal prompts stay on that rail.

- **No lazy templates (hard rule)**: same as root Skill—no rotating place nouns with identical light/story/depth; don’t default to terrace/seaside/café window every time; **checklist** for differentiation (hook, light/time, layers/footing, brand/category, two dimensions differ); pull from MLB high-frequency scenes, grade/time, and [reference-outfit.md](reference-outfit.md) **social UGC & trend tags**.

**Scene library (MLB)**: [reference-scenes.md](reference-scenes.md) **MLB**; client **required scene** column wins per row.

## Styling vocabulary and formulas (required)

When user/client **has not** specified bottoms/shoes/socks/inners: run [reference-outfit.md](reference-outfit.md) **§1 Decision order** → **§2–§5** picks; then **“Social UGC & trend styling”** in the same file for one compatible trend tag—**abstract to English** (**no** web required). **Rich ≠ more items**. Check **§8 Pre-prompt checklist**.

- **Outfit information density (hard rule)**: state **bottom silhouette**, **shoe family**, **sock logic**, **at least one visible layer**; don’t use only `stylish outfit`.

## Trend search (global social & editorial, optional)

After required styling block: optional **web search** for global social / editorial and trend keywords (Agent **cannot** browse gated logged-in social apps as the end user). **Abstract** to phrases—no stealing finals, no hero swap. **When/How/What/Forbidden** same as root Skill; signage taboos [reference-scenes.md](reference-scenes.md) **MLB**.

## Step 4: Model and mood (editorial)

**Full detail lives in** [reference-model-presets.md](reference-model-presets.md) (tiers, sweet-clear addendum, body/face density, limbs, accessories, composition scale). **Open that file** when drafting internal prompts or fixing QC for frames 1–6.

**In SKILL, keep these hard rules:**

1. **Pick one** model tier (default female-leaning) or user/custom tier; phrases **in English, pick don’t stack**—see reference Sections 1–3.
2. **Priority**: user/client model preference **>** step 1 brand hair/makeup **>** step 3 emotion; **user wins** on conflict. If ethnicity/tier unstated: infer + **one-sentence** confirmation. Male / plus-size / outside table: follow user + brand; still use reference for proportions and QC vocabulary.
3. **Eyes** default to camera; **pose variety** (stand/sit/lean/walk) and **outfit visibility** per [reference-pose-vocabulary.md](reference-pose-vocabulary.md) and [reference-outfit.md](reference-outfit.md) (reference-model-presets Section 8 points to the same).
4. **Every** prompt must satisfy **body proportion lines** and **facial detail density** in the reference—else **Image QC** will fail; sweet-clear tier also uses **Section 3** addendum and QC item 9.

## Step 5: Consistency, light, expectations

1. **Photo and color**: **natural-light led**; default **bright natural, clear white daylight**—`clean bright daylight`, `airy natural light`, `clear white-balanced daylight`; also `natural sunlight`, `bright daylight`. **Do not confuse** with step 1 taboo “cold office elevator top light”—here means **outdoor/window** clear daylight, not that scene type. `soft golden hour` **only** if step 3/emotion **asks warm**—not every frame yellow. **Layered background**; reuse [reference-scenes.md](reference-scenes.md) **Scene diagram · §2–§7**. **Slightly higher saturation**, clear tones—avoid muddy gray. Even face light. **Frame 5** not chest-up only. Full body: head room, feet mostly in frame; background rich, secondary.

   - **Delivery look reference (clear street lifestyle)**: under default **bright natural (clear white)**, prefer **even highlight, soft shadow**—**bright overcast** or **open shade diffused sun** (don’t default whole frame **golden hour / strong warm skin** unless step 3 says so). **Neutral, slightly cool-clean** WB; may add `soft even lighting`, `diffused daylight`, `neutral white balance`, `minimal warm color cast`. For **full body or line emphasis**, **slightly low angle** (`slightly low angle`) aligns with body rules; if still big-head/short-leg, reduce tight face crop, reinforce `balanced head-to-body ratio` + `elongated legs`—avoid wide-angle face + bad crop **chibi** proportions. Street lifestyle: façade (warm gray plaster/brick) + **glass doors** + **distant trees/street depth**; foreground light **terrace table corner, cup, chair back**; mid/back **shallow DoF**; subject dominant. **Clear garment colors** vs **warm env, white, green**—**airy, not gray or mushy**.

2. **Garment + styling consistency**: hero locked; styled pieces one family all 6.
3. **Hero anchoring**: **frame 1 only first**; then 2–6 use **frame 1 URL** + angle refs.
4. **Frame 4 (front variation)**: **not** back; **front**; different pose/scale vs frame 1; front product + anchor; if user **later** wants back, restore back logic.
5. **Logo / small type**: may warp—note PS path.
6. **Background + anatomy**: same defaults as step 1; limbs/shoes rules satisfied.

## Step 6: Six frames (ratio 3:4 only)

| # | Framing | Notes | Internal focus (don’t show full text to user) |
|---|---------|-------|-----------------------------------------------|
| **1** | **Front** | Upper large; **to camera**; **same SKU as white-bg ref** | front view, chest-up or waist-up, large scale, looking at camera; **exact garment from reference product image**, faithful details, no substitute |
| **2** | **Side** | Upper dominant, large; eyes toward camera | side profile, upper body, tight framing, eyes toward camera |
| **3** | **Full** | Large in frame; **long legs, normal head-to-body** | full body, large subject, looking at camera; elongated legs, balanced head-to-body ratio |
| **4** | **Front variation** | **Not back**; alternate pose/scale vs 1 | front view, alternate pose vs shot 1, upper or medium framing, looking at camera, not back view |
| **5** | **Three-quarter outfit** | Mid-thigh, waist/pockets readable | three-quarter, mid-thigh crop, waist and pockets visible, looking at camera |
| **6** | **Fabric macro** | Large detail; face in frame → to camera | fabric macro, large detail fill; face → looking at camera |

## Execution rhythm (two phases)

1. **Phase A**: frame 1 only, white-bg in `img_urls`, `ratio="3:4"`, user confirms URL.
2. **Phase B**: frames 2–6 with frame 1 URL anchor + angle refs; `ratio="3:4"`.

Don’t generate all 6 at once.

## Frame 1 must match white-background product (hard rule)

Common failure: model’s top **is not the same SKU** as client flat (wrong or “similar” piece). Frame 1 **must pass SKU fidelity** before 2–6.

- Internal prompt must stress (pick): **exact same garment as reference flat**—`exact garment from reference product image`, `faithful reproduction`, `match reference SKU`, same neckline/sleeves/hem/pockets/print placement, `no alternate design`, `no generic similar item`. Styled bottoms/shoes still per [reference-outfit.md](reference-outfit.md)—**never** replace hero.
- **img_urls**: user-confirmed **front white-background product**; if multiple refs, state which is hero internally.
- **Before delivery**: **Image QC · frame 1** vs flat; fail → **rerun frame 1 only**—**do not** proceed to 2–6 if frame 1 is wrong garment.

## Save finals to disk (after approval)

When user/client **finalizes all 6** (or each frame), Agent **must** **download** each **http(s) result URL** to a **local folder**—not only chat links.

- **Suggested path**: `outputs/editorial-six/<SKU_or_date_summary>/` (or user absolute path); **one subfolder per SKU**.
- **Filenames** (match step 6): `01_front.jpg`, `02_side.jpg`, `03_full_body.jpg`, `04_front_variation.jpg`, `05_three_quarter_outfit.jpg`, `06_fabric_macro.jpg` (or `.png`, consistent).
- **How**: Download each result with whatever the environment allows (browser save-as, terminal `curl`, Agent/IDE file tools); save under the filenames above. No Python batch script required.
- **Optional**: `urls.txt` one URL per line; **hero anchor** archive: `00_hero_anchor_url.txt` with final frame 1 URL.

## Image QC and regeneration (before each delivery)

Before handoff or next frame, **view** output; if any item fails, **regenerate that frame only** with targeted strengthening (frame 1: **exact garment**; sweet-clear tier: expression; Step 4 **body** + **facial density** + Avoid per [reference-model-presets.md](reference-model-presets.md); `complete visible limbs`, `looking at camera`, shoes on feet, layering)—**don’t** rerun all 6.

1. **Body proportion**: oversized head, giraffe neck, short legs, stubby/chibi proportions → **rerun**; reinforce required + Avoid phrases; if big head + short legs, **don’t** only tweak face.
2. **Anatomy and limbs**: missing/extra limbs, bad hands, bad joints; bad elbow/knee crops.
3. **Shoes and hands**: extra/floating shoes, hand–shoe fusion (unless hold-shoe requested).
4. **Face and features**: output **face shape, hair, eyes/nose/lips** **clearly off** prompt (identity drift, hair vs ban)—**rerun**; common: **moon face, too round-flat, chubby cheeks, wide jaw** vs **oval/V-line/small face, large eyes, high bridge**; **unfounded light brown hair**; **bare lifestyle / blunt features** vs sweet-influencer target. Retry: **facial density** + **Avoid** (`round face`, `wide jaw`, `light hair`, etc.).
5. **Eyes and framing**: side still toward lens; frame 4 front + to camera.
6. **Garment vs hero**: drift; unreadable logo (note post). **Frame 1 strict**: top vs **front flat** same SKU—neckline, placket, sleeves, pockets, hem length, main color, print placement **clearly different** (“another piece”) → **rerun frame 1**; don’t enter 2–6 until aligned.
7. **Background and grade**: empty wall, flat gray; default taboo locations unless job asked.
8. **Outfit**: if bottoms/shoes should show, visible and consistent.
9. **Sweet-clear (strict, only if tier = Asian female sweet-clear or equivalent written)**:**(a)** Expression **cold, distant, “over-it,” zero warmth**, or **pink blush but still cold editorial / mature face**; **(b)** face **too large, wide jaw, moon/round, wide square, overly mature bone** vs **oval, petite face, large eyes, high bridge**; **(c)** hair **middle part + big curl / heavy wave**; **(d)** hair **unfounded light gold/brown/bleach** (no client write)—any clear miss → **rerun**; reinforce [reference-model-presets.md](reference-model-presets.md) Sections **1 and 3**: expression, Asian makeup, small face, young hair, dark brown-black hair (`dark brown-black hair`, `influencer-style petite face`, `Asian beauty makeup`, `youthful hairstyle, no middle-part big curls`, etc.)—don’t fight garment/body hard rules.

**Retry policy**: ~2–3 tries per frame; then explain and ask flat swap / relax rule / accept.  
**Frame 1**: if rerun (including **mismatch flat**), tell user **“hero frame regenerated”** + reason; 2–6 anchor **final frame 1 URL**.  
**User**: may auto-retry; if user approved a frame, don’t auto-rerun it.

## Troubleshooting

| Symptom | Likely cause | What to do |
|--------|----------------|------------|
| User wanted **8 PDP slots** (front/back/side/detail/flat lay…) | Wrong skill | Switch to **`ecommerce-fashion-workflow`**; do not force six editorial frames. |
| Skill should trigger but does not | `description` mismatch | User query should mention six frames, editorial/magazine/storyboard, same-SKU multi-angle, or nano-banana; re-read frontmatter triggers. |
| Skill triggers for **unrelated** tasks | Over-broad wording in chat | Confirm user actually wants **six** 3:4 **editorial** shots—not a generic “help me generate some images” request. |
| **Frame 1** wrong garment vs flat | Prompt or ref order | Rerun frame 1 only; strengthen SKU-fidelity phrases; verify `img_urls` uses correct **front** flat. |
| **HTTP / timeout** errors | API or network | Check `NANO_BANANA_BASE_URL`, increase timeout on frame 1, verify network; retry; surface error once with next step. |
| **Big head / short legs / moon face** (sweet tier) | Model block too thin | Apply Image QC items 1, 4, 9; rerun **that frame** with density + Avoid lines from [reference-model-presets.md](reference-model-presets.md)—not the whole set. |
| Instructions feel **too long to follow** | Context load | Use **Critical rules** + step headers first; load [reference-scenes.md](reference-scenes.md) / [reference-outfit.md](reference-outfit.md) for scene/styling; load [reference-model-presets.md](reference-model-presets.md) for Step 4 and QC face/body fixes. |

## Self-check list (each delivery)

- [ ] Brand + scene done; angles mapped; if front/back was unclear, **client confirmed** (see Input).
- [ ] Source QA + triple-choice; not lazy template; frame 1 approved; anchor + angle refs; frame 1 **SKU vs flat** checked.
- [ ] `ratio="3:4"`, same `image_size`.
- [ ] **Bright natural (clear white)**; no gray murk unless asked; no default golden cast unless step 3 wants warm—matches step 5 delivery reference.
- [ ] Layered background; [reference-scenes.md](reference-scenes.md) **Scene diagram** + **MLB**; not default hotel/sym elevator unless written.
- [ ] Large subject; frame 5 three-quarter not tight chest; frame 3 large enough.
- [ ] **Looking at camera**; frame 4 front variation.
- [ ] **Model preference** confirmed or inferred with user; no unresolved conflict with brand/triple-choice.
- [ ] If **Asian female sweet-clear**: oval/V-line, large eyes, high bridge, petite face, Asian makeup; **not** middle-part big curl; **dark brown-black** hair, no unfounded light/bleach unless written; **warm** expression; [reference-model-presets.md](reference-model-presets.md) Sections 1 + 3 in prompt; QC 9 if needed.
- [ ] **Body proportions**: no big head / stubby legs; reference-model-presets Sections 5 + Avoid lines; QC 1 if needed.
- [ ] Model looks good; brand/triple-choice; garment hero.
- [ ] **Facial density**: all five bullets; not generic pretty-only; moon-face Avoid (**unless user wants plus/round**); QC 4 checked.
- [ ] **Outfit**: bottoms + shoes + socks + layer; [reference-outfit.md](reference-outfit.md) flow + social pick; default no bag/jewelry unless written; extras cohesive; don’t block logo.
- [ ] **Poses** match [reference-pose-vocabulary.md](reference-pose-vocabulary.md); pants/shoes/socks visible where needed.
- [ ] If **trend search**: abstract only; brand + hero; no swap/clash.
- [ ] Limbs/shoes QC; per-frame regen within budget.
- [ ] **Finals saved** to disk (`01_front`–`06_fabric_macro` or user naming)—not links only.
- [ ] No default full prompt paste to user.
- [ ] 8-slot e-com → `ecommerce-fashion-workflow`.
