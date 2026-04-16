<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Scene Plan Guide — Field-by-Field Reference

Reference file for Phase 3. Read this before writing the scene plan JSON.

---

## Aspect Ratio

Use the ratio selected by the user at Gate 1.1. This value goes into the scene plan's `ratio` field and is passed to both nano-banana and Seedance 2.0.

Ratio affects composition guidance in the `comp` field:
- **9:16 (vertical)**: Favor centered product, close-ups, and vertical stacking of illustrated elements above/below the product
- **1:1 (square)**: Balanced compositions, product can sit center or rule-of-thirds
- **16:9 / 21:9 (landscape)**: Wide illustrated worlds, product can be smaller in frame, more environmental storytelling

---

## Beat-to-Scene Mapping

The concept card's 4 beats expand into 9 shots. Each beat maps to a cluster of shots in the 9-shot cinematic structure:

- Beat 1 (opening) → Shots 1-2 (establishing + detail)
- Beat 2 (development) → Shots 3-4 (reveal + interaction)
- Beat 3 (pivot/climax) → Shots 5-6 (acceleration + climax — the concept card's "key moment" maps here)
- Beat 4 (resolution) → Shots 7-9 (aftermath + hero + signature)

---

## Narrative Progression (Critical — The Story Behind the Scenes)

The concept card defines the story. The scene plan must CARRY that story into every field. Without these rules, the agent defaults to writing 9 variations of the same setting with different colors — a poster series, not a story.

### The "Because" Chain

Each shot after shot 1 must describe a state that exists BECAUSE of what happened in the previous shot. The `scene_because` field captures this causality explicitly.

Test: read the 9 shots using "because" between them. If you have to use "and then" instead, the shots are parallel posters, not story chapters.

- "The archway stands empty at dawn" → "BECAUSE dawn arrived, a crack appears in the stone" → "BECAUSE the crack formed, the product now sits on the stone" → "BECAUSE the product is present, a vine tendril erupts" → ... ← this is a story
- "Empty archway" → "AND THEN close-up of stone" → "AND THEN product appears" → "AND THEN vines grow" ← this is a slideshow

### Emotional Arc

The viewer's feeling must change across the 9 shots. The 9-shot structure naturally creates a cinematic energy arc:

```
Shot:    1          2        3       4           5            6       7         8      9
Feel:    stillness  tension  wonder  engagement  excitement   awe     breathing earned  peace
Energy:  ▁▁        ▁▂       ▃▃      ▅▅          ▆▇           ██      ▅▃        ▆▅     ▃▂
```

If all 9 shots evoke the same feeling, there's no journey.

### State Progression

Shared visual elements (from `shared_elements`) must evolve across shots — they tell part of the story through their own transformation:

- Shot 1 (establishing): "faint pencil-sketch vine border, barely visible"
- Shot 3 (reveal): "vine border starting to fill with green ink"
- Shot 5 (acceleration): "vine border growing rapidly, tendrils extending"
- Shot 6 (climax): "vine border dense and lush, every curve alive"
- Shot 8 (hero): "vine border complete and luminous, gilt accents glowing"

Same element, progressive states. Copying a static description across all 9 shots produces 9 identical images.

---

## 9-Shot Structure (Standard)

The scene plan uses 9 shots arranged as a cinematic sequence. Each shot has a specific dramatic function (`shot_type`). The product does NOT appear in every shot — its absence builds anticipation, and its presence earns impact.

| Panel | Shot Type | Product | Purpose |
|-------|-----------|---------|---------|
| 1 | establishing | absent | Wide world, atmosphere, sets the universe |
| 2 | detail | absent | Close-up foreshadowing, something stirs |
| 3 | reveal | enters | Product's first appearance |
| 4 | interaction | present | Product and world react to each other |
| 5 | acceleration | present | Transformation builds speed |
| 6 | climax | present/obscured | Peak energy, product may be overwhelmed by its own power |
| 7 | aftermath | absent/small | Wide pull-back showing the transformed world |
| 8 | hero | hero | Product centered, crowned — the money shot |
| 9 | signature | present | Closing frame, brand moment |

---

## Character-Driven 9-Shot Structure (Cinematic tier)

The 9-shot structure varies by story shape. Panels 1-2 (setup) and 8-9 (hero + signature) are consistent across shapes; panels 3-7 differ based on the story engine.

**Quest shape** — character searches through spaces:

| Panel | Shot Type       | Character    | Product | Purpose                                                  |
| ----- | --------------- | ------------ | ------- | -------------------------------------------------------- |
| 1     | world_intro     | absent       | absent  | The illustrated world exists — atmosphere, scale         |
| 2     | character_intro | enters       | absent  | Who is this person? Distinctive silhouette, first action |
| 3     | desire          | present      | absent  | What do they want? The search begins                     |
| 4     | journey         | present      | absent  | First step — new space, obstacles, wonders               |
| 5     | deepening       | present      | absent  | Journey intensifies — deeper into the world              |
| 6     | discovery       | present      | enters  | Character finds the product                              |
| 7     | union           | present      | present | Character and product together — the earned moment       |
| 8     | hero            | small/absent | hero    | Product centered, crowned                                |
| 9     | signature       | present      | present | Brand close — character at peace with the product        |

**Creation shape** — character builds toward the product:

| Panel | Shot Type       | Character    | Product | Purpose                                                  |
| ----- | --------------- | ------------ | ------- | -------------------------------------------------------- |
| 1     | workshop        | absent       | absent  | The workspace/atelier — tools, materials, atmosphere     |
| 2     | maker_enters    | enters       | absent  | The maker arrives — hands, intent, first gesture         |
| 3     | vision          | present      | absent  | What they want to create — a sketch, a glance, a plan   |
| 4     | craft           | present      | absent  | Hands at work — mixing, shaping, assembling              |
| 5     | refine          | present      | absent  | Almost there — adjustment, precision, near-miss          |
| 6     | complete        | present      | enters  | The creation is finished — the product emerges           |
| 7     | unite           | present      | present | Maker beholds the completed work — pride, satisfaction   |
| 8     | hero            | small/absent | hero    | Product centered, the masterwork crowned                 |
| 9     | signature       | present      | present | Brand close — maker at peace with the creation           |

**Transformation shape** — character is changed by the product:

| Panel | Shot Type       | Character    | Product  | Purpose                                                 |
| ----- | --------------- | ------------ | -------- | ------------------------------------------------------- |
| 1     | before_world    | absent       | absent   | The world BEFORE — muted, constrained, waiting          |
| 2     | character_static| enters       | absent   | Character in their before-state — longing, stasis       |
| 3     | catalyst        | present      | **enters** | Character encounters the product — the trigger          |
| 4     | first_change    | present      | optional | First visible change — color bleeds, texture shifts     |
| 5     | accelerate      | present      | absent   | Change cascades — character and world transforming fast  |
| 6     | peak_change     | present      | optional | Peak metamorphosis — maximum visual difference          |
| 7     | new_self        | present      | present  | Transformed character with product — the "after"        |
| 8     | hero            | small/absent | hero     | Product centered — cause of the transformation          |
| 9     | signature       | present      | present  | Brand close — new self at peace in the new world        |

Note: This is the ONLY shape where product appears before panel 6 (panel 3 as catalyst). Panels 4-5 may show the product faintly or not at all — the focus is the CHANGE.

**Performance shape** — character expresses, product revealed late:

| Panel | Shot Type       | Character    | Product | Purpose                                                  |
| ----- | --------------- | ------------ | ------- | -------------------------------------------------------- |
| 1     | stage_set       | absent       | absent  | The setting/stage — atmosphere, anticipation             |
| 2     | performer_still | enters       | absent  | Character in stillness — tension before the first move   |
| 3     | first_move      | present      | absent  | The opening gesture — restrained, deliberate             |
| 4     | build           | present      | absent  | Movement grows — rhythm established, energy building     |
| 5     | crescendo       | present      | absent  | Peak expression — maximum movement, energy, drama        |
| 6     | peak            | present      | absent  | The most extreme moment — freeze or explosion            |
| 7     | aftermath       | present      | enters  | Stillness returns — product revealed as the source       |
| 8     | hero            | small/absent | hero    | Product centered — what powered the performance          |
| 9     | signature       | present      | present | Brand close — performer at rest with the product         |

Note: Product appears in only 3 of 9 panels (7-9) — the latest reveal of all shapes. The performance itself IS the advertisement.

**Summary of product visibility by shape:**

| Shape | Product-absent panels | Product enters | Product hero panels | Total product panels |
|---|---|---|---|---|
| Quest | 1-5 | 6 | 6-9 | 4 |
| Creation | 1-5 | 6 | 6-9 | 4 |
| Transformation | 1-2, 4-5 | 3 (catalyst) | 3, 7-9 | 4-5 |
| Performance | 1-6 | 7 | 7-9 | 3 |

---

## Field-by-Field Translation

**`world`** — The core visual description for this scene's keyframe. Must be specific enough to serve as a nano-banana prompt AND must carry the story forward. This field is where the story lives or dies.

**Prompt structure (in this order — nano-banana weights early content most heavily):**

1. **The event/change (first 1-2 sentences, ~40% of words):** What's HAPPENING in this scene — the unique action, state, or revelation from `scene_event`. Start with the verb or the visual state. This is what makes this scene different from its neighbors.
2. **The environment context (1 sentence, ~20%):** Where we are in the shared world — briefly. NOT a full re-description.
3. **Shared elements in their CURRENT STATE (1 sentence, ~20%):** The visual thread elements described as they look RIGHT NOW in this story moment — not copy-pasted from a static description.
4. **Atmosphere/light (~20%):** Color, mood, light conditions.

**Wrong (shared elements dominate — produces identical images):**
"Art Nouveau vine border with flowing organic curves and gilt grape-leaf accents frames the stone archway. Trailing grapevine tendrils with purple grape clusters hang from the arch. The warm stone surfaces show carved grape-leaf reliefs. ...oh and also, a single tendril is starting to grow from the stone."

**Right (event leads — produces a distinct scene):**
"A single green tendril pushes through a crack in bare stone, unfurling its first tiny leaf near the base of the bottle. The stone surface is empty — dormant, expectant, no other growth visible. Above, a faint pencil-sketch vine border is barely visible along the archway, gilt accents catching the first hint of warm dawn light. Pale gold and muted stone, no green yet except the one emerging tendril."

In the wrong version, nano-banana reads "ornate border, grape clusters, tendrils" first and generates a lush poster. In the right version, it reads "single tendril, bare stone, empty" first and generates a sparse opening scene. The shared elements are still present — but in an early, dormant state that matches the story beat.

**Word budget:** The scene's unique event/state should occupy at least 40% of the `world` field. Shared elements should occupy at most 25%. If the ratio is inverted, the images converge.

**Text avoidance rule:** Never use the words "label", "text", "caption", "title", "typography", "lettering", "brand name", or "logo" in any `world` field. These words cause nano-banana to render visible text/captions in the panel. Describe the product by its physical features instead. Examples: "Close-up of the bottle label" → "Close-up of the bottle surface and golden cap"; "brand logo on the glass" → "embossed emblem on the glass"; "the product name is visible" → "the bottle's front face catches the light." The product's own printed label will remain visible naturally because the product photo is provided as a reference — you don't need to describe text for it to appear.

Layer on the chosen style's `visual` vocabulary from `prompt-library.json`. Test: could you picture the exact frame from this description alone? Would this frame look DIFFERENT from the other 8 shots at thumbnail size?

**`world_end`** *(per-shot Alternative 1 only)* — Describes the scene at its END — reflecting BOTH the completed environmental animation AND where the camera has arrived. Same camera angle (perspective), but the framing may have changed due to camera movement. This drives the end-keyframe (used as `last_img_url` in Seedance) so the video knows where to "arrive" — giving it a motion path to follow.

The end-keyframe is NOT a copy of the start with different paint. It's where the clip ENDS UP — tighter if the camera pushed in, shifted if it panned, wider if it pulled back. This difference between start and end keyframes is what creates visible camera motion in the video.

Example: if `world` says "wide watercolor plain with faint lavender reflections pooling from bottle base," `motion` says "reflections pool outward," and `camera` says "slow push-in":
- `world_end` should say "closer view of dark watercolor plain, lavender reflections fully spread from bottle base, pigment settled into layered washes" — the framing is tighter AND the animation has completed.

**`comp`** — Product placement and composition at the scene's START. Derive from the story's needs — these are common patterns, NOT hard rules:
- Wide establishing shot (product at 15-20%) — when the illustrated world is the star
- Medium shot (product at 25-35%) — balanced view of product and environment
- Close-up (product at 40%+) — product dominance, detail emphasis
- Any scale is valid if the story calls for it. A visionary concept might open with a tiny product in a vast world (10%) and end in extreme close-up (50%).

**`comp_end`** *(per-shot Alternative 1 only)* — Product placement and composition at the scene's END — after the camera movement has completed. This is what makes the video feel alive instead of a static animated painting.

Derive from `comp` + `camera`:
- If `camera` = "slow push-in" → `comp_end` is tighter than `comp` (product grows ~5-10% larger in frame, more detail visible, less background)
- If `camera` = "gentle pan right" → `comp_end` shifts the scene rightward (product may move from center to left-third, new environment revealed on right)
- If `camera` = "slow pull-back" → `comp_end` is wider (product shrinks, more environment visible)
- If `camera` = "static" → `comp_end` matches `comp` (no change in framing, only environmental animation creates motion)

Example: `comp` = "Product centered at 25% of frame on dark watercolor plain" with `camera` = "slow push-in" → `comp_end` = "Product centered at 35% of frame, tighter view, watercolor ground fills more of the frame edges"

**`camera_angle`** — Explicit label for the camera perspective. Extracted from `comp`. Must be one of these proven-to-transfer labels:
- `eye-level frontal` (default, highest I2V fidelity)
- `slight high-angle` (30-40 degrees down — good I2V fidelity)
- `slight low-angle` (looking slightly up — moderate I2V fidelity)
- `three-quarter view` (moderate I2V fidelity)
- `high-angle overhead` (LOW I2V fidelity — use with caution, see Executability Notes)
- `extreme low-angle` (LOW I2V fidelity — use with caution)

This value is injected directly into the video prompt to reinforce camera direction throughout the clip.

**`product_scale`** — Approximate percentage of frame the product occupies (e.g., "15%", "35%", "45%"). Driven by the story — a vast illustrated world might call for a small product, a product-hero moment might call for 50%. Injected into the video prompt to reinforce the intended composition against Seedance's tendency to normalize everything to ~35%.

**`product_position`** — Where the product sits in frame (e.g., "centered", "lower-third centered", "bottom-center rising upward"). Injected into the video prompt.

**`color`** — 3-4 specific colors. At least one echoes the product's actual color. Pull the style's recommended palette from `references/illustration-styles.md` and adapt to the concept's world.

**`color_constraint`** — Negative color direction: what tones/hues to AVOID. Prevents Seedance's tendency to lighten palettes or introduce unwanted colors. Examples: "no blue-white tones, maintain deep indigo-violet", "no rainbow colors, stay within lavender-gold palette", "no pastel softening, keep saturated dark tones." Injected directly into the video prompt.

**`product_motion`** — What the product DOES in this shot. Depends on direction tier:

*Safe:* `"static"` — product doesn't move. The world tells the story around it.

*Bold:* Product participates in the story. Choose from:
- `"float"` / `"levitate"` — rises from surface, hovers (Dior J'adore ascending)
- `"tilt 15 degrees toward the vine"` — leans toward a world element, as if responding
- `"rise from the mist"` / `"emerge from flowers"` — surfaces from an element
- `"drift left to right, trailing golden wake"` — moves laterally through the world
- `"spray activates, visible mist cloud"` — product dispenses (the moment of use)
- `"descend into frame and land on stone"` — arrives with weight and impact
- `"rotate 30 degrees revealing side label"` — turns to show another angle
- Product maintains photographic quality throughout.

*Visionary:* All Bold motions, plus:
- `"shatter into fragments revealing ingredients inside"` — temporary destruction for revelation
- `"grow monumental, towering over the landscape"` — Alice-in-Wonderland scale shift
- `"dissolve into golden particles that seed the illustrated world"` — product becomes the story
- `"assemble from swirling ingredients"` — origin story in reverse
- Photographic quality may flux during transformation. HERO shot (panel 8) always restores it.

**Seedance executability:** position changes, slight tilts, emergence, spray = reliable. Rotation > 30deg, scale shift = moderate. Shatter, morph, full rotation = unreliable (Visionary accepts this).

If `product_in_frame` is false, omit this field.

**`motion`** — What animates in the illustrated world: flowers bloom, vines grow, mist drifts, light shifts. Select from the chosen style's `motions` list in `prompt-library.json`. For product-visible shots, this field describes WORLD motion only — product motion goes in `product_motion`. For product-absent shots (establishing, detail, aftermath), this is the sole motion description.

**`camera`** — Choose from the proven set: static, slow push-in, gentle pan, slow drift, slow pull-back. Seedance 2.0 handles these well. Avoid complex choreography. No two adjacent shots share the same camera movement.

**`moment`** — Cinematic animation direction for the video model. 1-2 sentences (~15-20 words) describing the CHARACTER of this scene's motion: energy level, pacing, and motion density. This field goes directly into the Seedance I2V prompt alongside `motion` and `camera`, telling the model HOW to animate, not what the scene looks like.

Write `moment` using Seedance-executable language:
- **Motion energy**: "nearly still" / "slow, deliberate" / "rapid, explosive" / "settling, decelerating"
- **Motion density**: "single point of change" / "spreading, multiplying" / "everything moving simultaneously" / "minimal ambient"
- **Motion quality**: "tentative, careful" / "steady, building" / "cascading, overwhelming" / "gentle, resting"
- **Pacing**: "patient, held" / "gradually accelerating" / "climactic peak" / "slow resolution"

Do NOT use:
- Metaphors ("the world holds its breath")
- Abstract narrative ("the journey is fulfilled")
- Literary judgments ("tentative but unstoppable")
- Viewer emotions ("the viewer feels anticipation")
- Visual descriptions (that's `world`) or mechanical animation lists (that's `motion`)

Test: could an animator read this and know the ENERGY of the scene without seeing any images? The `moment` fields together should form an energy arc across the 9 shots (e.g., still → tense → rising → building → accelerating → peak → settling → earned → gentle). If they all say "gentle" or "slowly," the video will feel monotone.

Examples:
- Opening: "Nearly still — barely any movement, one faint atmospheric drift across empty sparse space"
- Development: "Slow deliberate emergence — a single element growing upward with careful energy, just the beginning of spreading growth"
- Climax: "Rapid simultaneous growth — everything expanding in all directions at once, maximum motion density, cascading and overwhelming"
- Resolution: "Settling to warm stillness — minimal gentle movement, everything at rest, slow ambient glow"

**`duration`** — 4-8 seconds per scene (per-shot alternative only — the primary storyboard-guided path always uses 15s total). For per-shot, allocate proportionally within 32-41s total. The climax beat typically gets the longest duration.

---

## Visual Continuity (Critical — Read Before Writing Any `world` Field)

The biggest risk in this pipeline is generating 9 beautiful but disconnected illustrations that look like separate posters, not frames from one continuous story. Even though the storyboard is generated in a single nano-banana call (inherently better for continuity), the scene plan's `world` fields still drive what each panel looks like. Continuity must be **designed into the scene plan**, not hoped for at generation time.

### Rule 1: One World, Not Four

All scenes exist within a SINGLE recognizable spatial environment. The camera moves through different areas of the same world — it does NOT teleport between different worlds.

Before writing individual scene `world` fields, define the shared environment in one sentence. Then each scene's `world` describes a different VIEW or MOMENT within that environment.

**Wrong approach** (4 separate worlds):
- Scene 1: "Golden cathedral with stained glass prisms"
- Scene 2: "Cream-colored botanical laboratory with copper vessels"
- Scene 3: "Purple crystal cave with glowing violet drops"
- Scene 4: "Dark indigo night garden with fireflies"

**Right approach** (one world, 4 moments):
- Shared environment: "An Art Nouveau distillation tower — ornate gilt metalwork with vine motifs rising vertically through a dark emerald space"
- Scene 1: "Upper section of the tower — golden light enters through ornate prism at the top, illuminating the gilt vine framework"
- Scene 2: "Mid-section of the tower — the light-liquid flows through vine-like tubing, the gilt metalwork now catching rose tones as the liquid shifts color"
- Scene 3: "Lower section near the bottle — violet essence drips from the final vessel, the gilt vine framework now suffused with violet, the same metalwork framing the product"
- Scene 4: "The completed tower at rest — the full gilt vine framework visible from base to top, now glowing deep indigo-violet"

The viewer should feel like the camera is traveling through ONE space, not cutting between postcards.

**Important:** One world does NOT mean one composition or one camera position. It means one SPATIAL UNIVERSE that the story moves through. The KENZO Flower reference shows one world (Paris at night) with completely different views — city panorama, rooftop, apartment interior, snowy window, street-level monument. The continuity is in the world, not in the frame.

### Rule 2: Visual Thread

Identify 2-3 illustrated elements that appear in EVERY scene's `world` field. These are the viewer's visual anchor — they recognize these elements across cuts, making the sequence feel connected.

Good visual threads:
- The same ornamental border style (e.g., "Art Nouveau vine borders with flowing organic curves and gilt accents")
- The same type of flora/motif (e.g., "grape vine spirals" or "fern fronds" — not "grape vines" in Scene 1 and "lilies" in Scene 3)
- The same architectural framework (e.g., "ornate gilt metalwork arches" — not "prism" in Scene 1 and "alembic" in Scene 3 with no visual link)
- The same background texture (e.g., "dark emerald with visible paper grain" — consistent across all scenes)

Write the chosen visual thread into the top-level `shared_elements` field, then ensure each scene's `world` description includes these elements.

**Critical: persist does NOT mean repeat verbatim.** Shared elements should appear across shots in EVOLVING STATES that reflect the story's progression. The state of the shared elements IS part of the story — a faint sketch border becoming a dense ornate border tells a creation story through the border itself. Copying the same description across all `world` fields produces identical images. See "Narrative Progression: State Progression" for how to write shared elements in their shot-specific state.

### Rule 3: Color Overlap at Boundaries

Define the overall color arc in the top-level `color_arc` field first. Then ensure adjacent scenes share 1-2 colors at their boundary.

**Wrong** (abrupt jumps):
- Scene 1: gold, amber, dark emerald
- Scene 2: copper, cream, beige ← where did the emerald go? where did cream come from?
- Scene 3: bright violet, purple ← no connection to previous scene

**Right** (overlapping transitions):
- Scene 1: gold, amber, dark emerald
- Scene 2: amber, rose, dark emerald deepening ← amber carries from Scene 1, emerald persists
- Scene 3: deep rose, violet, dark emerald-to-indigo ← rose carries from Scene 2, emerald transitions to indigo
- Scene 4: violet, deep indigo, soft gilt ← violet carries from Scene 3, gilt echoes Scene 1 for closure

Each scene's palette includes at least one color from its neighbor. The background tone evolves gradually rather than jumping.

### Rule 4: Background Continuity

The background color/texture is the most visible element across scenes. If it changes abruptly (dark emerald → cream → bright purple → dark indigo), the viewer perceives 4 different places regardless of other continuity cues.

The background should EVOLVE:
- If the story goes from warm to cool, the background should shift gradually — dark emerald with golden glow → dark emerald with rose tinge → dark emerald deepening to indigo → deep indigo
- Avoid introducing background colors that have no relationship to adjacent scenes (cream or white backgrounds are especially jarring between dark scenes)

---

## Quality Checks (Internal)

Before proceeding to storyboard generation, verify:

- All 9 shots are present with valid `shot_type` values
- Every `world` field is concrete enough to picture the exact frame (no abstract language)
- For product-visible shots: `product_scale`, `product_position` are filled. `world_end` and `comp_end` are needed only for the per-shot alternative
- For product-absent shots: product-specific fields can be omitted or set to "n/a"
- Every `camera_angle` is set and matches the perspective described in `comp`
- Every `color_constraint` includes at least one negative directive
- Every `motion` uses motion types from the chosen style's `motions` list
- `product_motion` matches the chosen direction tier (Safe = static only; Bold = dynamic; Visionary = transformative; Cinematic = generally static since the character carries the motion, but Transformation shape may have a brief product glow/pulse at the catalyst moment)
- The HERO shot (panel 8) always has `product_motion: "static"` or minimal motion — this is the clean money shot
- No two adjacent shots share the same camera movement
- The concept card's "key moment" maps to the CLIMAX shot (panel 6)
- Product visibility matches the tier: Safe/Bold/Visionary ~5-6 of 9 panels; Cinematic ~3-5 panels depending on story shape (Quest/Creation: 4 panels; Transformation: 4-5 panels; Performance: 3 panels)
- Per-shot alternative: total duration 32-41 seconds. Primary path: duration is always 15s (Seedance maximum)
- Color palettes connect to the product's actual colors
- **Executability check**: Shots with `camera_angle` set to `high-angle overhead` or `extreme low-angle` have LOW I2V fidelity
- **Continuity checks:**
  - `shared_elements` is filled and lists 2-3 persistent visual elements
  - Every `world` field includes the shared visual thread elements — but in EVOLVING STATES, not copied verbatim
  - Adjacent shots share at least 1-2 palette colors
  - Background tone evolves gradually — no abrupt jumps
  - `color_arc` is filled and the per-shot `color` fields follow its progression
- **Story checks:**
  - **Because-chain test**: Read all 9 `scene_because` fields in sequence. Does each explain WHY this shot follows the previous?
  - **Transformation test**: Compare shot 1's `world` to shot 9's `world`. Has the world fundamentally changed?
  - **Emotional arc test**: Do the 9 shots evoke DIFFERENT feelings? The energy should arc: low → low → rising → rising → high → PEAK → settling → hero → close
  - **Thumbnail test**: Shrink each `world` to one sentence. Would a viewer see 9 DIFFERENT images?
  - **Prompt structure test**: Does each `world` field lead with its unique event/state (at least 40% of words)?
  - `narrative_engine` is filled
  - Every `scene_event` describes a DIFFERENT action/change
  - **Energy arc test**: Read the 9 `moment` fields in sequence — they should follow the energy arc above
  - Every `moment` uses Seedance-executable language (energy, pacing, density) — no metaphors, no abstract narrative
  - **Product motion arc test** (Bold/Visionary only): Product motion should build through the sequence — static or absent early, increasingly dynamic through interaction/acceleration/climax, settling to rest at hero/signature
- **Character checks** *(Cinematic tier only)*:
  - `character` top-level field is filled with `description`, `visual_markers`, `want`, `rendering`
  - Character description is consistent across all panels where `character_in_frame: true` — the same visual markers appear in every `world` field that includes the character
  - Character has at most 3 visual markers (more = inconsistency risk across panels)
  - Character design is simple enough to read at storyboard panel size (silhouette-driven, avoid detailed faces)
  - Character's `character_action` changes across panels (not static — the character DOES different things)
  - Character's `character_emotion` follows an arc appropriate to the story shape
  - Character appears in panels 2-9 (7 of 9 panels), absent only from panel 1
  - **Shape-specific product visibility** (must match the chosen story shape):
    - Quest: product panels 6-9 only. `shot_type` values: world_intro, character_intro, desire, journey, deepening, discovery, union, hero, signature
    - Creation: product panels 6-9 only. `shot_type` values: workshop, maker_enters, vision, craft, refine, complete, unite, hero, signature
    - Transformation: product panel 3 (catalyst) + 7-9. `shot_type` values: before_world, character_static, catalyst, first_change, accelerate, peak_change, new_self, hero, signature
    - Performance: product panels 7-9 only. `shot_type` values: stage_set, performer_still, first_move, build, crescendo, peak, aftermath, hero, signature
  - **Shape diversity check**: Is this concept actually a Quest in disguise? If visual variety comes from different SPACES (not stages, metamorphosis, or actions), it's a Quest regardless of what `shot_type` labels say

---

## Preview Prompts (Optional Debug Step)

To verify assembled prompts before running API calls, use the `assemble_prompts.py` script:

```bash
python3 {SKILL_DIR}/scripts/assemble_prompts.py \
  {PROJECT_DIR}/scene_plan.json
```

This prints the assembled storyboard prompt (primary), storyboard video prompt (primary), plus per-shot keyframe, motion, and multi-shot prompts for every scene, with word counts. Useful for catching prompt issues (too long, missing fields, wrong style vocabulary) before spending time on generation.
