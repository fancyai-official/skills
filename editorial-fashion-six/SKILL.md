---
name: editorial-fashion-six
description: "Generate 6 fixed editorial storyboard shots (fixed 3:4) from the user's multi-angle product images of the same SKU. Identify the brand first; optionally search the web for same-brand, same-category references to enrich background layering. Scenes (MLB types / taboos + foreground, midground, background / light / ground / depth of field; avoid flat empty walls) → reference-scenes. Styling must follow reference-outfit (generic bottoms / shoes & socks / color palette / layers + abstracted trend tags and formulas). Optional web search for global social UGC / editorial trend cues (Instagram / Pinterest / TikTok–style abstractions) and broader fashion trend reports. Extended-shot poses stand / sit / lean / walk → reference-pose-vocabulary; must stay consistent with outfit visibility. QA, triple-choice, hero-image anchoring, direct image generation via HTTP nano banana; every finished image must pass QC—if not, regenerate only that frame (see Image QC and regeneration). Lighting defaults to natural light / sunlight, airy, slightly higher saturation. Backgrounds by default avoid hotel lobbies / symmetrical office elevator halls (unless the client requests otherwise). Outputs must have complete limbs; guard against missing limbs / extra fingers; guard against floating extra shoes or hand–shoe fusion. Model and outfit should look good, cohesive, and not steal focus from the product. Extra accessories default to no bag, and no earrings, no necklaces (including chokers); other accessories have no third-party logos, must be cohesive as a set, must not block the product, and need not appear in every frame. Do not show full prompts in chat. Use when the user wants 6 editorial storyboard shots or nano banana image gen; for an 8-image e-commerce matrix, use ecommerce-fashion-workflow."
---

# White-background product → 6 editorial fashion shots

## Input: multi-angle product images

Users usually provide **multiple angles of the same SKU** (white-background or flat lay: front, side, back, etc.). Before running, **map angles**: from user notes or filenames, confirm which file is **front / side / back**; later frames use the matching reference. **Do not** separately ask “do you have a back image.” **Frame 4** in this Skill defaults to a **front variation** (see step-6 table) and **does not** require a back image. If an angle is **actually missing** (e.g. no side), substitute sensibly for that frame and **briefly** tell the user.

## When to use this Skill vs the 8-image e-commerce Skill

| Need | Use |
|------|-----|
| 6 images, magazine / mood / story; unified scene and light | **This Skill** (`editorial-fashion-six`) |
| **Global PDP 8-slot matrix** (Amazon / Shopify / DTC–style detail page: front / back / side / top–bottom detail / macro / flat lay / styling) | **`ecommerce-fashion-workflow`** |

Shared ideas: white-background reference, hero anchoring, de-gray and lift. This Skill is **6 fixed frames** (including frame 4 **front variation** and fabric close-up); it differs from the 8-slot matrix in count and shot mix.

## Do not show prompts to the user

- **Internally** still write `prompt` and run **nano-banana image generation** (same parameters as below); **do not paste** the full prompt in chat.
- Show the user: **triple-choice summary**, **which frame and shot type** (e.g. “Frame 3 · full-body mood”), **result URL or image**, **checkpoints**; give full prompts only if the user asks.

## Direct image generation (nano banana / HTTP)

1. **Implementation**: Use **nano-banana image generation** available in the current environment (Fancybos-style HTTP API or IDE-integrated tooling)—**no** scripts in this folder are required.
2. **Parameters (unified across the set)**:
   - `ratio` **fixed `"3:4"`** (all 6 the same).
   - `image_size` recommended **`"2K"`** (match production; keep consistent).
   - `app_model_type` default **`"nano-banana-2"`** unless user asks for pro.
   - Frame 1 may need longer runs—increase `timeout` (seconds); `poll_interval` ~2s is fine.
3. **Optional env**: `NANO_BANANA_BASE_URL` overrides default `http://ai-api.fancybos.com` (test/prod).
4. **Frame 1**: `img_urls` = user’s **front product image** (URL or local path).
5. **Frames 2–6**: **frame 1 output URL** as hero anchor; per shot, combine **matching-angle product refs** (side, front, etc.) with anchor in `img_urls` (e.g. `[frame1_URL, side product image]`); count per API limit. **Frame 4** is **front** framing (see table): `img_urls` = **front product** + frame 1 anchor; **not** default back view; **no** back asset required.

## Step 1: Brand ID and scene recommendation

1. **Identify brand**: from user copy, product logo/hang tag, filenames, or client sheet—**brand** (or line) when possible.
2. **If brand is clear**: recommend scene and light in that brand’s usual **visual tone** (e.g. American street, Korean fresh, outdoor tech, quiet luxury minimal) and why it fits the silhouette; you may mirror **public campaign** location types (stadium edge, café crawl, coastline)—**do not** invent off-brand mood. Summarize typical **model hair/makeup mood** from that brand’s campaigns (influencer-polished, outdoor natural, sporty clean, etc.) for step 4.
3. **Background reference (avoid flatness)**: if word lists alone yield **empty, flat, single-plane** backgrounds, **web-search** same-brand, same category/season campaigns, lookbooks, official social, street snaps—**abstract** richer layered elements into internal prompt; **do not** copy whole copyrighted frames—only **reproducible descriptions**. Without brand, search **category** benchmark brands’ public visuals. When **locking location**, follow [reference-scenes.md](reference-scenes.md) **“Scene diagram: layering and light vocabulary” · §1 How to use**: **(1)** Lock scene family from triple-choice and [reference-scenes.md](reference-scenes.md) **MLB quick reference**; **(2)** **Foreground / midground / background** each at least one clear element (not only `blur background` or blank wall); **(3)** add **light** (direction, hardness, time feel—see §3 there); **(4)** **ground and footing** (§4 there) to avoid floating subject; **(5)** taboos per MLB and main Skill (no European classical, no garbled signage, etc.). Combine **layering, light direction, ground, DoF** phrases so the “scene type” becomes **depth + light + ground**. Still obey MLB taboos. **Background defaults to avoid (this Skill)**: do not default **luxury hotel lobby**, **office elevator hall**—symmetrical elevator banks, glass hoist shafts, polished marble/granite, cold ceiling light, strong-perspective “HQ” corridors—**cold corporate** compositions; **prefer** outdoor natural (street, seaside boardwalk, stadium edge, terrace) or **lifestyle interior** (coffee/dessert in/out, window-lit casual space). Optionally add `avoid hotel lobby, office elevator hall, symmetrical elevator doors, marble corporate corridor` (don’t stack); if user or client Excel **explicitly** wants such interiors, follow that job.
4. **No brand or unclear**: recommend from **category and experience** (sport casual / denim / down fit different worlds) and layer [reference-scenes.md](reference-scenes.md) **MLB** quick scenes and taboos; if client Excel has a **required scene** column, that row wins. Hair/makeup from triple-choice + category—don’t force a fixed “influencer” template.
5. For the user, **short takeaway** only (brand read + 2–3 scene keywords)—**no** long essay.

## Step 2: Source image QA (avoid failure)

On each new garment batch check: light too dark, creases/shadows crushed black, harsh glare, garment heavily cropped, messy background.

- If risky: say it may inherit hard creases, dirty shadows, or crop issues; ask to **swap for cleaner white-background / flat** or confirm proceed anyway.
- If acceptable, go to style triple-choice.

## Step 3: Style and narrative (triple-choice)

From silhouette, fabric, audience, and **step 1** brand/scene (including **web** layering), give **3 differentiated** directions; each includes **scene setup**, **light mood**, **emotional tone** (2–4 sentences each); scene setup must show **background richness and depth** (avoid “one blank wall / solid cyclorama” flatness). Default **bright natural light** (sun, airy, slightly higher saturation); avoid gray murk; if brand wants low-key, say so separately. After user picks one, internal prompts stay on that rail so all 6 match.

- **No lazy templates (hard rule)**
  - **What’s forbidden**: no reasoning, only rotating **place nouns** for A/B/C while all three are the same in **light, story, depth**; **do not** treat “terrace / seaside or boardwalk / café (or dessert shop) window seat” as the **default opener** every time.
  - **Not forbidden**: seaside, terrace, café/dessert window, florist door, waterfront boardwalk—often valid; **allowed** in triple-choice if **thinking checklist** below is satisfied, not autopilot.
  - **Triple-choice checklist** (internal must-check; for user, 1–2 sentences each on why this SKU and how it differs):
    1. **Hook / story**: one-line mood for this SKU (e.g. energetic sweet, vacation ease, urban polished sweet).
    2. **Light and time**: fits scene type; three options differ in grade or time (even if all “seaside,” differ in **space type** or **emotion**).
    3. **Layers and footing**: per [reference-scenes.md](reference-scenes.md) **Scene diagram** section—foreground / midground / background + **ground**; e.g. florist door = plant rack foreground + glass storefront mid + street depth back.
    4. **Brand and category**: compatible with step 1 brand and category.
    5. **Differentiation**: at least **two** of {scene type, light/time, emotion} clearly differ across the three.
  - **User named vs not**: if user **writes** a type (“must be seaside”), that option must be fully layered and lit—not one word. **If not named**, seaside/terrace/café/florist highs still need the checklist.
  - Truly separate the three using [reference-scenes.md](reference-scenes.md) **MLB high-frequency scenes** (street/urban, parking, bridge/stairs, stadium/music, travel/airport/cabin, record store, **rotate**), **grade and time** (overcast soft, golden hour, blue hour, low indoor, film cast—when brand fits), **story mood**, and [reference-outfit.md](reference-outfit.md) **social UGC & trend tags** so two dimensions differ.

**Scene library (MLB)**: quick ref and expansion in [reference-scenes.md](reference-scenes.md) **MLB**; client Excel **required scene** column wins per row.

## Styling vocabulary and formulas (required)

When user/client **has not** specified bottoms, shoes, socks, inner layers, before internal prompt **run** [reference-outfit.md](reference-outfit.md) **General vocabulary · §1 Decision order** → from **§2–§5** by hero category **pick** bottoms direction, shoe family, palette, at least one inner/layer. Then from **“Social UGC & trend styling”** in the same file pick **one** trend tag or formula compatible with brand and step 3, **abstract to English phrases** (**no** web required). **Rich ≠ more items**—same mood, **more visible detail**. Then check [reference-outfit.md](reference-outfit.md) **§8 Pre-prompt checklist (richness)**.

- **Outfit information density (hard rule)**: internal prompt must **state** (user overrides if written): **bottom silhouette**, **shoe family**, **sock logic** (ankle / crew / tonal with pant or shoe), **at least one visible layer** (inner neck or hem, jacket openness, waist/tuck). Do not replace with only `stylish outfit`.

## Trend search (global social & editorial, optional)

After **styling vocabulary (required)** is done, if you need extra keywords closer to current **global social / editorial “seed”** imagery, **web search** (Agent **cannot** browse gated logged-in social apps as the end user). **Abstract** to short prompt phrases—**no** stealing influencer finals, **no** swapping hero SKU.

- **When**: client/user **did not** specify outfit and wants trend boost; after step 1 **brand** and step 3 **triple-choice** are locked—avoid style clash.
- **How to search (examples)**: `street style outfit` or `OOTD` + category + mood (e.g. `hoodie street`, `dress vacation`, `shell jacket outdoor`); or fashion trend / seasonal launch articles. More tags in [reference-outfit.md](reference-outfit.md) **“Social UGC & trend styling”**.
- **What to abstract**: same as required section—**silhouette**, **palette**, **layer**, **shoes/socks**; **phrases** in prompt, not pasted paragraphs.
- **Forbidden**: use search to **replace hero**; stack styles that **fight brand / triple-choice**; when abstracting **default no bag**, **default no earrings/necklace** (same as this Skill); readable signage taboos still [reference-scenes.md](reference-scenes.md) **MLB**.

## Step 4: Model and mood (editorial)

Ask model type (Asian/Western, gender, plus-size, etc.). For **internal** prompts: **eyes default to camera** (hard default for set)—write `looking at camera, eye contact` or equivalent:

- **Face and mood**: model should **look good**, alive, balanced memorable features. **Makeup and mood follow “brand style”** (step 1): with brand, mirror campaign hair/makeup (may be **influencer** polished, Korean clean, outdoor healthy—**no** mixing clashing styles); without brand, match step 3 and category. **Makeup allowed**; if brand fits influencer look, polished base/eyes/lips and styled hair (`influencer makeup` etc. but aligned with brand keywords). **Do not** make “bare no-makeup” the only goal. Even heavier makeup keeps **garment as hero**; model **does not** steal scene. Avoid greasy skin, bug eyes, duck lips.
- **Body and eyes**: natural walk, shifted weight; hands may interact with **extra accessories** (sunglasses, coffee, hem/collar) or neutral poses; **by default no** handheld, shoulder, or crossbody **bags**. **Pose variety**: frames 2–6 may differ from frame 1—rotate **stand / sit / lean / slow walk** under one mood; short English phrases. **Stand/sit/lean/walk, hand micro-gestures, scale pairing, frame rotation** see [reference-pose-vocabulary.md](reference-pose-vocabulary.md) (**Usage principles**, **§6 Shot scale and pose pairing**). Poses must **match framing**: full / three-quarter / chest each get fitting motion—avoid crop vs pose conflict. **Outfit visibility**: seated, full body, lean shots must keep **inseam, hem, shoes/socks** visible and consistent—[reference-outfit.md](reference-outfit.md) **§7**—avoid “pose changed, shoes/pants not written.” **Eyes**: **every frame mainly to lens**—connection, alive; avoid dead stare, eye-roll, floor/off-camera blank drift. **Side / three-quarter** body may turn; **eyes still toward camera** (look back, over-shoulder, side face with pupils toward lens)—avoid “pure profile, never to camera.” **Frame 4** is front variation—**direct or natural to camera**; same facing as frame 1 but pose/scale must differ.
- **Limbs and anatomy (no missing arms/legs)**: full / three-quarter / side frames—visible **limbs complete and plausible**; no extra arms, missing hands, backwards joints, **amputation** feel; hands **five natural fingers** (not blobs or six fingers). Crop at waist/thigh **reasonably**—**avoid** cutting at elbow/knee. **Shoes on feet only**: no **extra pair floating**, **single floating shoe**, **hand fused to shoe**; internal prompt **do not** add `holding shoe, floating sneaker, extra shoes` **unless** user/client asks “holding shoe” styling. Optionally `complete visible limbs, anatomically correct, natural pose, five fingers per hand`; avoid semantics of `missing arm`, `extra limbs`, fused fingers, hand–shoe glue, extra shoes in frame (if no negative API, state in natural language).
- **Outfit (must look good)**: satisfy **“Styling vocabulary (required)”** and **“Outfit information density”**; without drifting hero, total look **finished**: inner/bottom/shoes/socks and **extras** (**default no bag**; **default no earrings/necklace**; hat, sunglasses, headphones) **same mood family** as **hero + pants/shoes** (street/sport/minimal/outdoor, etc.), **palette and material cues aligned** (e.g. all cool gray-black or all warm earth)—avoid “hat/sunglasses fight stiff hoodie vibe” patchwork. Accessories **simple and tasteful**. User/client **specified** shoe color, inner, handheld, **bag or not**, **earrings/necklace or not**—follow spec. If **trend search (optional)** used, still structural abstraction, **not** garment swap. Optionally `stylish outfit, cohesive styling, coordinated accessories...`; **default omit** `handbag, shoulder bag, crossbody bag` and `earrings, necklace, choker`.
- **Extra accessories (optional lift)**: **no** shoulder/crossbody/tote/waist **bags** by default (none in set); avoid those words **unless** user/client Excel **writes** bag—then still **no third-party luxury logo**, **don’t block** chest logo and key structure. **No earrings/necklace** (incl. choker) by default; avoid those tokens **unless** **written**. Other pieces: **no recognizable third-party** items (basic sunglasses, headphones, beanie) for depth; **one story**: hat/glasses/phones **same style/palette**—no random clash. **Don’t block product**: brim/hands **don’t hide** face and key top structure; chest logo, back graphic, waistband stay readable. Sunglasses on face vs head may alternate. **Not every frame**: some frames no handheld/no hat; when used, **limit count**—not every frame stacked. Coffee same. Kids or Excel extra bans—**follow sheet**.

## Composition and scale (apparel-first)

- **Subject scale**: **model large in frame**—medium-close, subject fills frame; avoid tiny person / empty environment unless frame needs distance.
- **Garment + upper body priority**: for **tops**, still center **upper body and garment**—but **not** every frame strict half-body; rotate chest-up, three-quarter, knee-up, full body as long as subject stays large—not distant speck.
- **Vs shot list**: frame 3 full body when pants/shoes matter; subject still **large** in frame.
- **“Half-body” means (frame 5, avoid unreadable product)**: **not** tight chest-only (cropped at chest hides bottoms). Prefer **American three-quarter / mid-thigh up / three-quarter (“cowboy”)**: lower frame edge around **mid-thigh**; show **full top** plus **waistband, pockets, crotch line / hem relationship**; dress/long coat at least **above knee or main hem silhouette**. Internal: `three-quarter shot, mid-thigh crop, outfit full visibility, waist and pockets visible`.

## Step 5: Consistency, light, expectations

1. **Photo and color (bright airy)**: background and overall **natural-light led**, **sunny feel** (`natural sunlight, bright daylight, soft golden hour`, avoid gloomy gray studio). **Layered background** (`layered background, environmental depth, rich scene details`)—not huge void, single plane, no-depth “flat studio”; reuse [reference-scenes.md](reference-scenes.md) **“Scene diagram” · §2–§7** (space, light, ground, recipes, materials, DoF). Elements from step 1 **same-brand/type** abstract search; subject still hero. **Slightly higher saturation**, clear color (`vibrant colors, high saturation, clear tones`)—**not** dark, gray, muddy (avoid `faded, dull, muddy, gray cast, low key, underexposed`). Face evenly lit, no split “yin-yang” face. Mix **medium / chest-up / three-quarter / knee-up / full body**, keep **large subject**; **frame 5** avoid **chest-up only** so outfit pairing reads. Full body: head room, try not to crop feet; background **rich but not competing**.
2. **Garment and styling consistency**: hero locked by multi-angle refs + frame 1 anchor—silhouette, main color, major structure stable; **styled pieces** follow outfit rules above; all 6 **one family**—no random shoe swap unless frame/client asks.
3. **Hero anchoring**: **call API for frame 1 only first**; after user OK, frames 2–6 `img_urls` lead with **frame 1 output URL** plus **per-angle product** (above).
4. **Frame 4 (front variation)**: **not** back view. **Front** camera; same facing as frame 1 but **different pose or scale** (sit/lean/walk freeze, slightly wider/tighter front framing)—avoid duplicate “same standing pose.” Product refs: **front product** + frame 1 anchor. If user **later** wants back, restore back logic for that job.
5. **Logo / small type**: complex prints may warp; note possible post PS for logo.
6. **Background and anatomy (delivery quality)**: same **background avoid** as step 1—no default hotel lobby / symmetrical elevator unless specified. Delivery meets step 4 **limbs and anatomy**; no missing/extra limbs, severe hand deformity; full/three-quarter relations sound; **no** extra floating shoes, hand–shoe fusion.

## Step 6: Six frames (ratio fixed 3:4)

**Output ratio only `ratio="3:4"`**—no other ratios mixed in.

| # | Framing | Notes | Internal prompt focus (do not show full text to user) |
|---|---------|-------|--------------------------------------------------------|
| **1** | **Front** | Show top block; **upper body large**; **to camera** | front view, chest-up or waist-up, large subject scale, looking at camera |
| **2** | **Side** | Profile; **upper dominant, subject large**; **eyes still toward camera** (over-shoulder, etc.) | side profile, upper body, tight framing, eyes toward camera |
| **3** | **Full body** | When pants/ratio matter; subject still **large**—not distant speck; **to camera** | full body but subject large in frame, minimal distant framing, looking at camera |
| **4** | **Front (variation)** | **Not back**: still **front-facing**, differ from frame 1—rotate **stand/sit/lean/walk** or **medium-close change**; **upper emphasis**, large subject; **to camera** | front view, alternate pose vs shot 1, upper body or medium framing, large subject scale, looking at camera, not back view |
| **5** | **Half-body (product three-quarter)** | **Readable full outfit structure**: prefer **mid-thigh crop / American three-quarter**; top + waist/pockets visible; **avoid** tight chest-only; subject large; **to camera** | three-quarter shot, mid-thigh crop, waist and pockets visible, full outfit readability, looking at camera |
| **6** | **Fabric macro** | Material close-up, chest/shoulder local, **large in frame**; if face in frame **to camera** | fabric macro, large detail fill; face visible → looking at camera |

## Execution rhythm (two phases)

1. **Phase A**: generate **frame 1** only (white-background in `img_urls`, `ratio="3:4"`), give user **result URL** for approval.
2. **Phase B**: after OK, generate **frames 2–6** in order, each with **frame 1 URL** as **first anchor** plus **matching-angle product ref** in `img_urls` (e.g. `[frame1_URL, side product]`, order per API); count per API cap; **ratio still `"3:4"`**.

Avoid generating all 6 at once—wastes retries.

## Image QC and regeneration (before each delivery)

Every frame (**1** and **2–6**) before handoff or next frame: Agent **views output** (image at result URL), quick-check below. If any fail clearly, **regenerate that frame only** with the same nano-banana call path, **strengthen** internal prompt (e.g. `complete visible limbs`, `looking at camera`, shoes on feet only, layering phrases)—**do not** rerun all 6 for one bad frame.

1. **Anatomy and limbs**: missing/extra limbs, bad hands, backwards joints; crop at elbow/knee “amputation.”
2. **Shoes and hands**: extra shoes, floating shoes, hand–shoe fusion (unless client asked hold-shoe).
3. **Eyes and framing**: matches shot (side still toward lens; frame 4 front variation and to camera).
4. **Garment vs hero**: silhouette/main color/structure drift; chest logo unreadable (note post fix).
5. **Background and grade**: empty wall, flat muddy gray; default taboo slipped (hotel lobby, symmetrical elevator) unless job asked.
6. **Outfit info**: if this frame should show bottoms/shoes, visible and consistent with set.

**Retry policy**: **~2–3 tries max** per frame (including first); if still bad, explain and ask swap flat / relax rule / accept.  
**Frame 1 special**: if frame 1 reruns, tell user **“hero frame regenerated”**; frames 2–6 still anchor to **final frame 1 URL**.  
**User relationship**: may auto-retry before delivery; if user signed off a frame, don’t auto-rerun that frame.

## Self-check list (before each delivery)

- [ ] Brand ID (or noted unknown) + scene rec (brand- or experience-based).
- [ ] Source QA done + user confirmation.
- [ ] Triple-choice locked; all 6 on one rail.
- [ ] Step 3 **not lazy**: if seaside/terrace/café/florist appear, each has **story or light basis** and clear **diff vs other two** (see checklist).
- [ ] Frame 1 approved before 2–6; anchor = frame 1 URL; per frame correct product angle.
- [ ] Set `ratio="3:4"`, same `image_size`.
- [ ] **Natural / sunny**, saturation and clarity OK—**no** gray murk (unless brand/user asked low-key).
- [ ] **Background** layered—not blank mono wall; [reference-scenes.md](reference-scenes.md) **Scene diagram**: **foreground/midground/background** + **footing**, clear light; abstracted from **same-brand/type** public refs; [reference-scenes.md](reference-scenes.md) **MLB** taboos; **not** default hotel/symmetrical elevator unless written.
- [ ] Composition **large subject**; **frame 5** product three-quarter **not** tight chest; frame 3 still large enough.
- [ ] Model **to camera** (`looking at camera`): front/side/full/three-quarter; side may over-shoulder—**avoid** never to lens; **frame 4** front variation, to camera.
- [ ] Model **looks good**, healthy color; hair/makeup matches **brand / triple-choice** (influencer OK **per brand**); **does not** outshine clothes.
- [ ] **Outfit** coherent; internal prompt has **bottoms + shoes + socks + one layer** (if user silent, ran [reference-outfit.md](reference-outfit.md) required flow + social section pick); **default no bag** (unless written); **default no earrings/necklace** (unless written); **extras** one story with hero/pants—no competitor logos; **don’t block** logo; **not** every frame max accessories (kids/Excel from sheet).
- [ ] **Poses** match shot and scale ([reference-pose-vocabulary.md](reference-pose-vocabulary.md)); full/sit/lean **shoes/pants/socks** visible, consistent.
- [ ] If **trend search** used: still **brand + hero**; **abstract structure** only—**no** swap, **no** clashing stack.
- [ ] **No** missing/extra limbs / bad hands; **no** floating shoes / hand–shoe fusion (unless hold-shoe requested).
- [ ] Each frame **QC passed**; failures **single-frame regen** (or user agreed), within retry budget.
- [ ] Did not default-show full prompts to user.
- [ ] If user wants 8-slot e-com, pointed to `ecommerce-fashion-workflow`.
