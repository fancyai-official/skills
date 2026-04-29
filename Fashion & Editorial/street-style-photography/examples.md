# Mock Interaction — Full Walkthrough

> **DO NOT READ THIS FILE DURING REAL USER INTERACTIONS.**
> This file is for skill developers testing the flow. Reading 652 lines of mock data during a live session wastes tokens and context window. Everything you need is in SKILL.md.

Three complete mock sessions testing the skill flow, one for each input type:
- **Scenario A**: Type 3 — Model Wearing Garment (Womenswear, Paris) — the most common case
- **Scenario B**: Type 1 — Product Only (Menswear, Florence) — tests auto-cast logic
- **Scenario C**: Type 2 — Product + Model (Womenswear, Milan) — tests two-image input

---

## Scenario A: Type 3 — Model Wearing Garment (Womenswear, Paris)

### User Uploads

The user uploads a lookbook photo of a woman wearing a camel cotton trench coat set with a crossbody bag and Mary Jane shoes.

---

### Step 1a: Input Image Validation

> **AI (internal check — not shown to user unless fails):**
>
> | Check | Result |
> |-------|--------|
> | Image loads | Pass — valid PNG |
> | Resolution | Pass — 2048 x 3072px |
> | Content clarity | Pass — full outfit visible, well-lit |
> | Multiple images | Single image — 1 Quad |
>
> All checks pass. Proceed.

---

### Step 1b: Product Analysis

> **AI says:**
>
> Here's my analysis of your garment:
>
> | Data Point | Identified |
> |------------|-----------|
> | **Product Type** | Full look — matching jacket + A-line skirt set (coordinates) |
> | **Fabric** | Cotton twill, matte finish, medium weight, structured but soft enough to swing |
> | **Color Palette** | Camel / Warm tan — consistent warm beige across both pieces |
> | **Silhouette** | Jacket: blouson fit, stand collar, elasticized waist. Skirt: A-line, mid-calf, panel hem |
> | **Key Details** | Gold snap buttons down front, chest flap pocket with button, elasticized waist seam separating jacket and skirt, black leather crossbody bag with brass D-ring buckle, white ankle socks, black-and-white Mary Jane shoes |
> | **Styling Potential** | The A-line skirt is the hero for street shots — it will catch movement beautifully. The crossbody bag strap bisects the outfit and adds graphic interest. |
> | **Movement Behavior** | A-line skirt will swing laterally mid-stride. Blouson jacket has slight volume that bounces. Crossbody bag will swing against hip. Skirt panel hem will lift with each step. |

---

### Step 1c: Detect Input Type

> **AI (internal):** Type 3 — Model Wearing Garment. A woman is wearing the outfit in the image. Face, body, and full look are visible. Single image with both model and garment.

---

### Step 1d: Gather Required Inputs

> **AI says:**
>
> Beautiful set — the swing on that A-line skirt is going to photograph incredibly on the street. I need 4 inputs to set up your shoot:

> **AI presents (using AskQuestion or conversationally):**
>
> 1. **City**: New York, London, Milan, Paris, or Florence?
> 2. **Season**: Spring/Summer or Fall/Winter?
> 3. **Gender**: Womenswear or Menswear?
> 4. **Model**: Keep the same model from your image, or cast someone new?

> **User says:** "Paris, Fall/Winter, Womenswear, keep the same model."

---

### Step 1e: Auto-Cast

> Skipped — user chose to keep existing model.
>
> **AI locks model persona (from image):** "East Asian woman, mid-20s, slim build, black chin-length bob, quiet confident energy."

---

### Step 1f: Input Validation Gates

> | Gate | Check | Result |
> |------|-------|--------|
> | Florence + Gender | Paris + Womenswear | Pass — not Florence |
> | Season + City | Paris FW — standard PFW calendar (Feb/Mar) | Pass |
> | Model locked | "East Asian woman, mid-20s, black bob, quiet confidence" | Pass |
> | Input type noted | Type 3: Model Wearing Garment | Noted — single `--reference` with both model and garment |
>
> All gates pass.

> **AI says:**
>
> Locked in: **Paris, Fall/Winter, Womenswear, same model.** Let me scout some locations for you.

**STOP — user confirmed. Proceed to Step 2.**

---

### Step 2: The "Location Scout" (The Pitch)

> **AI says:**
>
> Here are 3 Street Sets for your Paris FW shoot:
>
> ---
>
> ### Street Set 1: "Le Marais Morning"
>
> | Element | Direction |
> |---------|-----------|
> | **Micro-Location** | Narrow side street off Rue de Turenne, Le Marais — gallery-lined, fashion boutiques, bistro at the corner |
> | **Time of Day** | Daytime |
> | **Lighting** | Late morning soft Parisian light, diffused through thin cloud cover. Cream Haussmann stone bounces warm light upward. Gentle shadows from narrow buildings. |
> | **Street Texture** | Café rattan chairs stacked outside a closed bistro, a Morris column with a torn poster, dark green Wallace fountain at the corner, weathered wooden shutters |
> | **Season Atmosphere** | Fall/Winter: grey sky with silver light breaks, bare plane trees, wet cobblestone from overnight rain, passersby in wool coats and scarves |
> | **Photographer Reference** | Melodie Jeng's clean confidence — bright, sharp, no-nonsense. The Impression PFW standard. |
>
> **Preview**: She's walking down a rain-wet Le Marais side street, phone in hand, the camel set popping against grey Parisian stone.
>
> ---
>
> ### Street Set 2: "Saint-Germain Blue Hour"
>
> | Element | Direction |
> |---------|-----------|
> | **Micro-Location** | Boulevard Saint-Germain near Café de Flore — wide sidewalk, literary Left Bank energy |
> | **Time of Day** | Blue Hour |
> | **Lighting** | Deep blue twilight sky, warm tungsten spilling from café windows onto wet pavement. Dual-tone: cool ambient vs warm interior light. |
> | **Street Texture** | Café de Flore's green awning reflected in puddles, vintage bookshop next door, zinc-topped sidewalk tables with water glasses, a parked Smart car |
> | **Season Atmosphere** | Fall/Winter: early darkness (5pm blue hour), warm breath visible, reflections everywhere on wet stone, passersby clutching coffee cups |
> | **Photographer Reference** | Adam Katz Sinding's dramatic light — cinematic, warm-cool contrast, The Impression PFW. |
>
> **Preview**: Blue hour on Saint-Germain — the camel set glows warm against the cold blue sky, café light catching the gold snap buttons.
>
> ---
>
> ### Street Set 3: "Montmartre Rain"
>
> | Element | Direction |
> |---------|-----------|
> | **Micro-Location** | Cobblestone slope on Rue Lepic, Montmartre — bohemian, hilly, vine-covered walls |
> | **Time of Day** | Daytime (overcast, raining) |
> | **Lighting** | Flat overcast light with rain — diffused, no shadows, everything glistens. The wet cobblestone is a mirror. |
> | **Street Texture** | Steep cobblestone with rain rivulets, iron railings, vine-covered stone wall, a boulangerie with fogged-up windows, a red umbrella in the background |
> | **Season Atmosphere** | Fall/Winter: Paris rain (photographic gold). Passersby with umbrellas. Wet leaves on stone. The romance of being caught in the rain. |
> | **Photographer Reference** | Acielle / Style du Monde — Parisian ease meets natural elements. |
>
> **Preview**: She's mid-stride on a rain-soaked Montmartre cobblestone, the A-line skirt swinging, passersby with umbrellas blurred behind her.
>
> ---
>
> Which set speaks to you?

> **User says:** "Set 2 — Saint-Germain Blue Hour."

**STOP — user selected. Proceed to Confirm Brief.**

---

### CHECKPOINT: Confirm Brief

> **AI says:**
>
> ### Generation Brief — Ready to Shoot
>
> | Parameter | Value |
> |-----------|-------|
> | **Input Image** | Camel cotton trench coat set (lookbook photo) |
> | **City** | Paris |
> | **Neighborhood** | Boulevard Saint-Germain, near Café de Flore |
> | **Season** | Fall/Winter |
> | **Gender** | Womenswear |
> | **Time of Day** | Blue Hour |
> | **Lighting** | Deep blue twilight, warm tungsten from café windows, dual-tone cool/warm |
> | **Street Texture** | Café de Flore green awning, wet pavement reflections, zinc-topped tables, vintage bookshop, parked Smart car |
> | **Input Type** | Type 3: Model Wearing Garment |
> | **Model Persona** | East Asian woman, mid-20s, slim build, black chin-length bob, quiet confident energy |
> | **Garment Description** | Camel cotton twill matching set — blouson jacket with stand collar, gold snap buttons, chest flap pocket, elasticized waist; A-line mid-calf skirt with panel hem. Black leather crossbody bag with brass D-ring buckle. White ankle socks, black-and-white Mary Jane shoes. |
> | **Movement Behavior** | A-line skirt swings laterally mid-stride. Blouson jacket bounces slightly. Crossbody bag swings against hip. Panel hem lifts with each step. |
> | **Photographer Reference** | Adam Katz Sinding, The Impression PFW — dramatic light, cinematic warm-cool contrast |
>
> ### The 4 Shots I'll Generate:
> 1. **Walking Approach** — 50mm f/1.8 — eyes DOWN at phone, skirt swinging, blurred passerby mandatory
> 2. **Candid Moment** — 50mm f/1.8 — eyes PAST camera, waist-up crop showing collar/buttons/bag strap
> 3. **Standing Full-Body** — 50mm f/1.8 — eyes MIDDLE DISTANCE, full outfit collar-to-shoes
> 4. **Profile Detail** — 35mm f/2.0 — eyes 90° PROFILE, extreme close-crop on stand collar and snap buttons, warm café bokeh
>
> Shall I proceed?

> **User says:** "Go for it."

**STOP — brief confirmed. Proceed to Step 3.**

---

### Step 3: The "Shutter" Execution

> **AI generates Shot 1 (Walking Approach).**
>
> **Per-Shot Check:**
> - Eye line DOWN (at phone)? Yes
> - Blurred passerby present? Yes — a woman in a navy wool coat carrying a paper bag, walking left-to-right, out of focus
> - Fabric shows motion? Yes — A-line skirt is swinging, panel hem lifted
> - Garment matches reference? Yes — same camel twill, gold snap buttons, crossbody bag
>
> Pass. Proceed to Shot 2.

> **AI generates Shot 2 (Candid Moment).**
>
> **Per-Shot Check:**
> - Eye line PAST camera? Yes — looking slightly right, soft smile
> - Upper-body crop? Yes — waist up
> - Garment construction visible? Yes — stand collar, gold buttons, elasticized waist, bag strap with D-ring
> - Same background continuity? Yes — same Haussmann stone, blurred café lights
>
> Pass. Proceed to Shot 3.

> **AI generates Shot 3 (Standing Full-Body).**
>
> **Per-Shot Check:**
> - Eye line MIDDLE DISTANCE? Yes — gazing past the lens, neutral expression
> - Full outfit visible collar-to-shoes? Yes — all visible including white socks and Mary Janes
> - Weight on one foot? Yes — left hip slightly dropped
> - Blurred passerby? Yes — a man with a briefcase, soft focus right side
>
> Pass. Proceed to Shot 4.

> **AI generates Shot 4 (Profile Detail).**
>
> **Per-Shot Check:**
> - Full PROFILE (90°)? Yes — complete profile, looking left
> - Extreme close-crop shoulder-up? Yes — collar and top 2 buttons fill the frame
> - Fabric texture legible? Yes — cotton twill weave visible
> - Warm bokeh? Yes — amber café lights in background
>
> Pass. All 4 shots complete.

---

### Post-Generation Review

> **AI says:**
>
> Here's your Street Quad — 4 candid moments on Boulevard Saint-Germain at blue hour:
>
> [Presents 4 images]
>
> **Checklist:**
> - [x] Eye Line Rule — down, past, middle distance, 90° profile (all different)
> - [x] Blurred Passerby — present in Approach, Full-Body, visible in Candid Moment bokeh
> - [x] Outfit Consistency — identical camel set, shoes, bag, accessories in all 4
> - [x] City Authenticity — unmistakably Parisian (Haussmann stone, zinc roofs, café glow)
> - [x] Street Artifacts — wet pavement reflections, warm bokeh spots, motion blur on skirt
> - [x] Consistent Cast — same architectural backdrop and lighting across the sequence
> - [x] Lens Consistency — 50mm/35mm perspective throughout
> - [x] Fabric in Motion — skirt swings in Approach, panel hem visible
>
> Are you happy with all 4 angles, or should I reshoot any specific shot?

> **User says:** "These are great. Love the blue hour café glow."

---

### Step 4: The Final Delivery

> **AI compiles `STREET_GALLERY.md`** using the gallery template and saves all assets:
>
> ```
> projects/paris-saint-germain-fw26/
> ├── outputs/
> │   ├── street_1_approach.png
> │   ├── street_2_candid_moment.png
> │   ├── street_3_full_body.png
> │   └── street_4_profile_detail.png
> └── STREET_GALLERY.md
> ```

---

### Step 5: The "Street Clip" (Optional)

> **AI says:**
>
> Would you like to animate one of these into a 5-second Street Clip? Pick your favorite shot — I'll turn it into a slow-motion vertical video of the model walking past the camera.

> **User says:** "Yes — animate the Walking Approach."

> **AI generates video from `street_1_approach.png`.**
>
> **Video Quality Check:**
> - [x] Model moves naturally — smooth walking motion
> - [x] Garment fabric moves — skirt swings with stride
> - [x] Background has subtle movement — passerby drifts, café light flickers
> - [x] No AI artifacts — clean
>
> **AI says:**
>
> Your Street Clip is ready — 5 seconds of slow-motion walking past Café de Flore at blue hour. The skirt swing looks incredible in motion.
>
> [Presents video]
>
> Your complete Street Gallery is saved to `projects/paris-saint-germain-fw26/`.

---
---

## Scenario B: Type 1 — Product Only (Menswear, Florence)

### User Uploads

The user uploads a flat-lay product shot of a navy linen double-breasted blazer.

---

### Step 1a: Input Image Validation

> All checks pass. Single image, high-res, garment clearly visible.

---

### Step 1b: Product Analysis

> **AI says:**
>
> | Data Point | Identified |
> |------------|-----------|
> | **Product Type** | Blazer — double-breasted, structured tailoring |
> | **Fabric** | Linen, medium weight, natural slub texture, soft matte finish |
> | **Color Palette** | Deep navy blue — rich, saturated, slightly muted by linen texture |
> | **Silhouette** | Slim-fit, peak lapels, suppressed waist, natural shoulder, slightly longer length |
> | **Key Details** | 6 gold buttons (4 functional, 2 decorative), working buttonholes on cuffs, chest welt pocket, two flap pockets, pick-stitched edges, half-lined interior |
> | **Styling Potential** | Classic Pitti Uomo energy — structured enough to photograph sharp, but the linen gives it relaxed Italian ease |
> | **Movement Behavior** | Linen has natural drape and slight crumple. Lapels will hold shape in motion. The longer length means the hem will sway with each step. Pocket flaps may lift slightly in wind. |

---

### Step 1c: Detect Input Type

> **AI (internal):** Type 1 — Product Only. Flat-lay shot, no model visible. Will need to auto-cast a model.

---

### Step 1d: Gather Required Inputs

> **AI says:**
>
> This is a product image, so I'll cast a model to wear this blazer on the street. Let me get your direction first:
>
> 1. **City?**
> 2. **Season?**
> 3. **Gender?**
> 4. **Model**: Would you like to describe who you envision wearing this, or should I cast someone who fits the blazer's energy and the city?

> **User says:** "Florence, Spring/Summer, Menswear, you cast."

---

### Step 1e: Auto-Cast Logic

> **AI builds auto-cast based on:**
> - Garment: structured DB blazer → confident, angular features
> - Gender: Menswear
> - City: Florence (Pitti Uomo) → classic Italian elegance, detail-obsessed, "peacock" energy
> - Season: SS → June Pitti, hot sun, lighter styling
>
> **AI presents:**
>
> Here's who I'd cast for this blazer at Pitti Uomo:
>
> ### Auto-Cast Sheet
>
> | Attribute | Value |
> |-----------|-------|
> | **Ethnicity** | Southern European (Italian) |
> | **Age Range** | Early 30s |
> | **Build** | Slim, broad-shouldered, tailoring-friendly proportions |
> | **Hair** | Dark brown, swept back with natural texture, medium length |
> | **Energy** | Controlled confidence — the Pitti "peacock" who dresses with intention but never looks like he's trying. Slight knowing half-smile. |
> | **Styling Notes** | Pair with: cream linen trousers (wide-leg, single pleat), brown suede tassel loafers without socks, white linen pocket square (casual puff fold), gold vintage watch on left wrist. No tie — open-collar white Oxford shirt beneath. |
>
> Does this work, or would you adjust?

> **User says:** "Perfect. Let's go."

**STOP — cast approved. Model locked.**

---

### Step 1f: Input Validation Gates

> | Gate | Check | Result |
> |------|-------|--------|
> | Florence + Gender | Florence + Menswear | Pass |
> | Season + City | Florence SS = Pitti Uomo June | Pass |
> | Model locked | "Southern European man, early 30s, swept-back dark hair, Pitti peacock confidence" | Pass |
> | Input type noted | Type 1: Product Only (auto-cast) | Noted — single `--reference` with garment only, model via `--model_persona` |
>
> All gates pass.

**STOP — all inputs locked. Proceed to Step 2.**

---

### Step 2: The "Location Scout" (The Pitch)

> **AI proposes 3 Florence Street Sets.** User selects:
>
> **Street Set 1: "Fortezza da Basso, Daytime"** — the classic Pitti shot. Stone walls, military architecture, strong Tuscan sun. Tommy Ton-style clean geometry.

**STOP — user selected.**

---

### CHECKPOINT: Confirm Brief

> **AI presents brief with all Florence/Pitti/menswear parameters locked.**
>
> User confirms.

**STOP — brief confirmed.**

---

### Step 3: The "Shutter" Execution

> AI generates 4 shots with menswear-specific adjustments:
>
> **Shot 1 (Walking Approach):** Full-body, model walking toward camera wearing the navy DB blazer over cream trousers. Phone in hand. A blurred pair of well-dressed men visible behind him — Pitti group dynamic. Strong Tuscan sun, stone wall background.
>
> **Per-Shot Check:** Eye line DOWN. Blurred passerby (pair of men in suits). Blazer hem sways. Gold buttons catch sunlight. Pass.
>
> **Shot 2 (Candid Moment):** Waist-up crop. Model caught mid-conversation with someone off-frame — the "controlled candidness" unique to Pitti where subjects know the camera is there but don't perform. Garment detail visible: peak lapel, gold buttons, pick-stitching, white pocket square.
>
> **Per-Shot Check:** Eye line PAST camera. Waist-up. Construction visible. Same Fortezza stone wall in bokeh. Pass.
>
> **Shot 3 (Standing Full-Body):** Full look documented collar-to-shoes. Weight on one foot, hand adjusting cuff (the Pitti "detail obsession" gesture). Every element visible: navy blazer, cream trousers, suede loafers, no socks, watch, pocket square.
>
> **Per-Shot Check:** Eye line MIDDLE DISTANCE. Full outfit visible. Asymmetric stance. Blurred Pitti attendee behind. Pass.
>
> **Shot 4 (Profile Detail):** Extreme close-crop. Full profile showing: peak lapel width, pick-stitching detail, gold button at close range, linen texture visible, pocket square puff. Warm amber bokeh from Fortezza stone in sun.
>
> **Per-Shot Check:** 90° PROFILE. Shoulder-up crop. Linen texture legible. Warm stone bokeh. Pass.

---

### Post-Generation Review

> All checks pass. AI presents 4-image Quad.
>
> **User says:** "The detail shot is perfect — you can see the pick-stitching. Ship it."

---

### Steps 4-5

> AI compiles STREET_GALLERY.md with Florence/Pitti metadata. User declines video clip.
>
> Complete.

---

## Scenario C: Type 2 — Product + Model (Womenswear, Milan)

### User Uploads

The user uploads **two images**:
1. A product shot of a red silk wrap dress on a hanger
2. A separate photo of a model (headshot / half-body) — a Black woman with shoulder-length braids

---

### Step 1a: Input Image Validation

> Both images pass. Two images uploaded — need to clarify relationship.

---

### Step 1b: Product Analysis

> **AI says:**
>
> | Data Point | Identified |
> |------------|-----------|
> | **Product Type** | Dress — wrap silhouette, midi length |
> | **Fabric** | Silk charmeuse, high sheen, lightweight, liquid drape |
> | **Color Palette** | Vivid cherry red — saturated, warm-toned |
> | **Silhouette** | Wrap closure, V-neckline, fitted waist with tie belt, A-line midi skirt |
> | **Key Details** | Self-fabric tie belt, surplice neckline, flutter sleeves, side seam pockets |
> | **Styling Potential** | The liquid silk will catch every light reflection and movement. Wrap closure creates dynamic diagonal lines across the body. |
> | **Movement Behavior** | Silk charmeuse will flow and ripple with every step. Flutter sleeves will lift in wind. The A-line skirt will swing dramatically mid-stride. Tie belt ends will trail behind. |

---

### Step 1c: Detect Input Type

> **AI (internal):** Type 2 — Product + Model. Two separate images uploaded. Image 1 is a garment on a hanger (no person). Image 2 is a person not wearing the garment. Need to confirm with user.

> **AI says:**
>
> I see you've uploaded two images. Just to confirm:
> - **Image 1** (red silk wrap dress on hanger) → this is the **garment**
> - **Image 2** (woman with braids) → this is the **model** you want to wear it
>
> Is that right?

> **User says:** "Yes, that's right."

---

### Step 1d: Gather Required Inputs

> **AI says:**
>
> That red silk is going to look incredible in motion. I'll put this dress on your model. 3 more questions:
>
> 1. **City**: New York, London, Milan, Paris, or Florence?
> 2. **Season**: Spring/Summer or Fall/Winter?
> 3. **Gender**: Womenswear or Menswear?

> (Note: no model preference question needed — Type 2 already has a model.)

> **User says:** "Milan, Spring/Summer, Womenswear."

---

### Step 1e: Auto-Cast

> Skipped — Type 2 already has a model reference image.
>
> **AI locks model persona (from model image):** "Black woman, late 20s, athletic build, shoulder-length braids, warm confident energy."
>
> **AI says:** "I see your model — late 20s, shoulder-length braids, warm confident energy. I'll keep her exactly as she appears. The red silk against her skin tone is going to photograph beautifully in Milan sunlight."

---

### Step 1f: Input Validation Gates

> | Gate | Check | Result |
> |------|-------|--------|
> | Florence + Gender | Milan + Womenswear | Pass — not Florence |
> | Season + City | Milan SS — MFW calendar (Sept) | Pass |
> | Model locked | "Black woman, late 20s, braids, warm confidence" — locked from model image | Pass |
> | Input type + references | Type 2: `--reference dress.png --model_reference model.png` | Noted — two images |
> | Two-image clarity | Confirmed: image 1 = garment, image 2 = model | Pass |
>
> All gates pass.

**STOP — all inputs locked. Proceed to Step 2.**

---

### Step 2: The "Location Scout" (The Pitch)

> **AI proposes 3 Milan Street Sets.** User selects:
>
> **Street Set 2: "Brera Golden Hour"** — warm Mediterranean light on ochre walls, cobblestone, gallery terraces, Vespa parked at the corner. That red silk will glow against the warm stone.

**STOP — user selected.**

---

### CHECKPOINT: Confirm Brief

> **AI says:**
>
> Here's the full brief — look good?
>
> | Parameter | Value |
> |-----------|-------|
> | **Input Type** | Type 2: Product + Model (two separate images) |
> | **Reference Images** | `dress.png` (garment) + `model.png` (model) |
> | **City** | Milan |
> | **Neighborhood** | Brera district — gallery-lined cobblestone streets |
> | **Season** | Spring/Summer |
> | **Gender** | Womenswear |
> | **Time of Day** | Golden Hour |
> | **Model Persona** | Black woman, late 20s, athletic build, shoulder-length braids, warm confident energy (from model image) |
> | **Garment** | Red silk charmeuse wrap dress — V-neck, flutter sleeves, tie belt, A-line midi |
> | **Movement Behavior** | Silk flows and ripples with every step. Flutter sleeves lift. A-line skirt swings dramatically. Tie belt ends trail. |
>
> I'll generate 4 shots using both your images — the dress from image 1 on the model from image 2.
>
> Shall I proceed?

> **User says:** "Go."

**STOP — brief confirmed.**

---

### Step 3: The "Shutter" Execution

> **AI generates all 4 shots using `--reference dress.png --model_reference model.png`.**
>
> **Shot 1 (Walking Approach):** Full-body, the model from image 2 walking toward camera wearing the red silk wrap dress from image 1. Silk rippling mid-stride, tie belt trailing. Phone in hand. A blurred man in a linen suit visible behind. Golden Brera light on ochre walls.
>
> **Per-Shot Check:** Eye line DOWN. Blurred passerby. Silk in motion. Garment matches product reference. Model face matches model reference. Pass.
>
> **Shot 2 (Candid Moment):** Waist-up. Model caught mid-laugh, looking past camera. Dress detail visible: wrap closure, silk sheen at V-neckline, flutter sleeve.
>
> **Per-Shot Check:** Eye line PAST camera. Same model face. Garment construction visible. Same Brera background. Pass.
>
> **Shot 3 (Standing Full-Body):** Full look. Weight on left foot, one hand on hip. Red silk catching golden light. Complete outfit from wrap neckline to shoes.
>
> **Per-Shot Check:** Eye line MIDDLE DISTANCE. Full outfit. Blurred passerby. Same model. Same garment. Pass.
>
> **Shot 4 (Profile Detail):** Extreme close-crop profile. Silk charmeuse texture legible at close range. Braids contrast against red silk shoulder. Warm amber bokeh from gallery windows.
>
> **Per-Shot Check:** 90° PROFILE. Shoulder-up. Fabric texture clear. Warm bokeh. Same model. Pass.

---

### Post-Generation Review

> All checks pass, with the additional Type 2 check:
> - [x] **Model fidelity**: The person in all 4 shots matches the model reference image (face, braids, skin tone, build)
> - [x] **Garment fidelity**: The dress in all 4 shots matches the product reference image (red silk, wrap closure, flutter sleeves)
>
> AI presents the Quad. User approves.

---

### Steps 4-5

> AI compiles STREET_GALLERY.md with Milan metadata and Type 2 references noted. User requests a Street Clip from the Walking Approach.
>
> Complete.

---
---

## Friction Points Identified During Mock

After running all three scenarios, these areas were noted for smoothness:

1. **Step 1d question count**: For Type 3 (Scenario A), the user answers 4 questions (city, season, gender, model preference). For Type 2 (Scenario C), only 3 questions — model preference is skipped since the model image is already provided. For Type 1 (Scenario B), 4 questions but the 4th is "describe or auto-cast." **Recommendation: Always batch questions in a single message. Adapt the count to the input type.**

2. **Step 1c two-image clarification (Type 2)**: When the user uploads 2 images, the AI must confirm which is the garment and which is the model. This adds a turn but prevents catastrophic misassignment. **Keep this gate — it's quick and essential.**

3. **Step 1e auto-cast approval**: Only applies to Type 1. Type 2 and Type 3 skip it. This means Type 2 has the fewest STOP gates before generation — fastest path from upload to output.

4. **Step 2 → CHECKPOINT flow**: Two consecutive STOP gates (select a set, then confirm brief). The Confirm Brief could feel redundant after the user just chose a set. **Recommendation: If the user's set selection was clear and all previous parameters are locked, the brief confirmation can be lighter — "Here's the full brief, look good? I'll start generating." Not a 3-paragraph table every time.**

5. **Per-Shot Checkpoint during Step 3**: Internal checks only — the user sees the complete Quad together, not 4 separate approvals.

6. **Type 2 model fidelity**: The biggest risk in Type 2 is that the AI changes the model's appearance (different face, different hair, different skin tone). The post-generation review must explicitly check model fidelity against the model reference image. **This is critical — add to the per-shot check: "Model face matches model reference?"**

7. **Type 1 auto-cast styling notes**: When the user uploads just one piece (e.g., a blazer), the auto-cast should include complete styling notes for complementary pieces (trousers, shoes, accessories). The AI is styling a full look, not just casting a face.

8. **Step 5 offer**: Clean transition across all types. No friction.
