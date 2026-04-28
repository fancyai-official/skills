---
name: beverage-photography-master-github
description: Beverage commercial photography expert. Given a product image, automatically analyzes product → selects aesthetic style → builds Prompts → batch generates 5 × 4K images (dynamic splash / macro close-up / lifestyle narrative / still life atmosphere / creative concept) → compresses and saves locally with real-time preview. Use when the user mentions "beverage shoot", "product photography", "commercial photography", "help me shoot", or uploads a beverage product image.
---

# Beverage Commercial Photography Master

## Setup 🔧

**Helper script**: `campaign_helper.py` (same directory as this skill)

Import before starting:
```python
import sys, os
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SKILL_DIR)
from campaign_helper import (
    create_campaign_folder,
    compress_image_to_target_size,
    save_image_to_campaign,
    save_campaign_info
)
```

**Image generation tool**: Use the `GenerateImage` tool.

---

## Core Workflow

### ⚠️ Product Image Requirements

User must provide a **clean product image** (white/solid background, product fully visible, no complex scene elements).

❌ Do NOT use: images that already contain creative staging, complex marketing backgrounds.

---

### Step 1: Product Analysis & Information Collection

Read the user's clean product image, analyze it, and search online for product info:

**1. Product Image Analysis**
- Product type identification (spirits, wine, beer, cocktail, soft drink)
- Packaging feature extraction (bottle design, can, brand identity)
- Color and material recognition

**2. Online Product Search** 🔍 **(Critical Step)**

Search strategy: `[brand name] + [product name] + "color" / "liquid color"`

Key confirmations:
- **True liquid color** (amber / deep red / clear / pink / yellow / green etc. — must be accurate)
- **Official imagery**: check how the drink appears in a glass in official product photos

**3. Determine**: product type, liquid color, packaging style, brand positioning, target scene

---

### Step 2: Aesthetic Style × Shooting Technique Combination

**Strategy**: Select 1 aesthetic style (unified tone), then apply 5 shooting techniques (diverse perspectives).

#### Five Aesthetic Styles (choose 1)

| Style | Tone | Best For |
|-------|------|---------|
| **A Soft Natural** 🌸 | pastel palette, blurred background, gentle light | premium elegant, limited edition, female market |
| **B High-Saturation Architectural** 🎨 | vivid solid colors, sharp textures, hard shadow | youth, summer, energy drinks |
| **C Dramatic Atmospheric** 🎭 | dark tones, smoke/beams, high contrast | premium spirits, luxury brands, nighttime |
| **D Lifestyle Narrative** 📖 | real environments, casual props, natural light | any product needing a story |
| **E Minimalist Commercial** ⚪ | solid background, product as focus, clean light | high-end minimal, e-commerce hero |

#### Five Shooting Techniques (one per image)

| Technique | Core Feature | Key Note |
|-----------|-------------|---------|
| **1 Dynamic Splash** 💦 | liquid splash, frozen moment | full bottle pouring must have a hand holding it |
| **2 Macro Close-up** 🔍 | bubbles, droplets, extreme detail | focus on detail — not the whole bottle (causes distortion) |
| **3 Lifestyle Narrative** 📖 | real-life scene, storytelling | props must feel natural, avoid staged look |
| **4 Still Life Atmosphere** 🕯️ | careful composition, mood lighting | refined prop arrangement, emotional resonance |
| **5 Creative Concept** 🎨 | artistic, rule-breaking | clear concept, visually striking |

#### 🎯 Aesthetic Style Decision Tree

- **Premium elegant product** → Style A (Soft Natural) or C (Dramatic Atmospheric)
- **Young trendy product** → Style B (High-Saturation Architectural) or D (Lifestyle Narrative)
- **Classic traditional product** → Style C (Dramatic Atmospheric) or E (Minimalist Commercial)
- **Holiday limited edition** → Style A (Soft Natural) or D (Lifestyle Narrative)
- **E-commerce hero image** → Style E (Minimalist Commercial) or D (Lifestyle Narrative)

#### 🛑 User Confirmation — Required Before Proceeding

After applying the decision tree, **pause and present the recommendation to the user** in this format:

> 📸 **Recommended Aesthetic Style**
>
> Based on the product analysis, I recommend **Style [X] — [Name]** because [1-sentence rationale].
>
> All 5 styles available:
> - A 🌸 Soft Natural — pastel, gentle light, premium/elegant
> - B 🎨 High-Saturation Architectural — vivid colors, bold shadows, youth/energy
> - C 🎭 Dramatic Atmospheric — dark tones, smoke, high contrast, luxury
> - D 📖 Lifestyle Narrative — real-life scene, natural props, storytelling
> - E ⚪ Minimalist Commercial — clean background, product focus, e-commerce
>
> Which style would you like to go with? (Reply A / B / C / D / E, or just confirm my recommendation)

**Do NOT proceed to Step 3 until the user replies with their chosen style.**

> 🔴 **After the user confirms a style, immediately read [photography-styles.md](photography-styles.md)** for the full tonal description and benchmark references for that style.

---

### Step 3: Precise Prompt Construction

**Core principle**: Different styles require different Prompt strategies — there is no universal template.

#### Universal Prompt Framework (7 Dimensions)

**1. Scene Concept** — story theme + target emotion + aesthetic style positioning

**2. Product Description** — product type, packaging details, **true liquid color**, packaging material, product state (condensation / iced)

**3. Background Design** (by style):
- Style A → `soft blurred background with pastel tones, natural depth of field`
- Style B → `corrugated wall with highly saturated [color], texture clearly visible`
- Style C → `dark gradient background with colored smoke, volumetric lighting`
- Style D → `outdoor [scene] setting, natural environment`
- Style E → `clean white background, minimalist setup`

**4. Props** (by style):
- Style A → rich and refined (fruits + flowers + ornaments + glassware)
- Style B → modern geometric (metal frames + decorative spheres)
- Style C → minimal and refined (emphasize atmosphere)
- Style D → lifestyle combination (real-use props)
- Style E → none or minimal props

**5. Lighting** (by style):
- Style A → `soft natural daylight, gentle shadows, warm lighting feel` (⚠️ avoid hard light)
- Style B → `directional light from 45° creating clear cast shadows` (⚠️ avoid soft diffused)
- Style C → `single spotlight from above, dramatic high contrast, rim lighting`
- Style D → `natural environmental lighting, realistic shadows`
- Style E → `clean product lighting, even illumination`

**6. Color Strategy** (by style):
- Style A → `soft pastel [color], muted elegant palette` (⚠️ avoid highly saturated)
- Style B → `highly saturated [color], vibrant bold colors` (⚠️ avoid soft tones)
- Style C → `deep dark tones, dramatic color accents`

**7. Realism Closing Line** — `shot on Canon EOS R5, not 3D render, not CGI, authentic photographic quality`

> 🔴 **Before building each Prompt, you MUST read the following files:**
> - **[PROMPT_GUIDE.md](PROMPT_GUIDE.md)** — full Prompt templates and combination examples for the selected style
> - **[KEYWORD_LIBRARY.md](KEYWORD_LIBRARY.md)** — keyword groups for the selected style to ensure consistency
> - **[scene-library.md](scene-library.md)** — scene inspiration and specific prop/environment descriptions
> - **[lighting-techniques.md](lighting-techniques.md)** — detailed lighting scheme references
> - If **Dynamic Splash** technique is included → must read **[DYNAMIC_SPLASH_PHYSICS_GUIDE.md](DYNAMIC_SPLASH_PHYSICS_GUIDE.md)**
> - If **Macro Close-up** technique is included → must read **[MACRO_ANTI_DISTORTION_GUIDE.md](MACRO_ANTI_DISTORTION_GUIDE.md)**

---

### Step 4: Batch Generation & Auto Storage

**Generation Config**
- Tool: `GenerateImage`
- Resolution: `4K`
- **Default ratio** (when user does not specify): Scene 1 → `16:9`, Scenes 2–5 → `3:4`

**Core Generation Process**
Use the `GenerateImage` tool to generate each scene one by one.
For each scene, provide the constructed prompt as the `description` and the user's product image as the `reference_image_paths`.
After each image is generated, it will be automatically saved and displayed.

---

### Step 5: Output & Project Summary

- After each image is generated, **immediately use the Read tool to display it** (do not show URLs)
- After completion, output: project folder path, aesthetic style choice rationale, notes on all 5 images, file size summary

> 🔴 **After all images are generated, you MUST read [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md)**, check each item on the quality checklist for the selected aesthetic style, and report pass/fail in the summary.

**Folder Structure**:
```
<skill_dir>/output/{product}_campaign_{timestamp}/
├── scene_1_dynamic_splash.png
├── scene_2_macro_closeup.png
├── scene_3_lifestyle_narrative.png
├── scene_4_still_life_atmosphere.png
└── scene_5_creative_concept.png
```

---

## Product Analysis Decision Tree (Lead Technique)

| Product Type | Lead Technique | Sequence |
|-------------|---------------|---------|
| Spirits (whiskey / brandy / vodka) | Still Life Atmosphere | Still → Splash → Macro → Narrative → Concept |
| Wine | Dynamic Splash | Splash → Still → Narrative → Macro → Concept |
| Beer | Lifestyle Narrative | Narrative → Macro → Splash → Concept → Still |
| Cocktail | Macro Close-up | Macro → Splash → Concept → Narrative → Still |
| Soft drink / Energy drink | Creative Concept | Concept → Narrative → Macro → Splash → Still |

---

## Sub-file Reading Schedule (Must Follow)

| File | Purpose | When to Read |
|------|---------|-------------|
| [photography-styles.md](photography-styles.md) | Full tonal description of all 5 styles | 🔴 Immediately after deciding style in Step 2 |
| [PROMPT_GUIDE.md](PROMPT_GUIDE.md) | Full Prompt templates and combination examples | 🔴 Before building Prompts in Step 3 |
| [KEYWORD_LIBRARY.md](KEYWORD_LIBRARY.md) | Style-specific keyword library | 🔴 Before building Prompts in Step 3 |
| [scene-library.md](scene-library.md) | 30+ scene template library | 🔴 Before building Prompts in Step 3 |
| [lighting-techniques.md](lighting-techniques.md) | Detailed lighting scheme reference | 🔴 Before building Prompts in Step 3 |
| [DYNAMIC_SPLASH_PHYSICS_GUIDE.md](DYNAMIC_SPLASH_PHYSICS_GUIDE.md) | Splash physics plausibility | 🔴 When Dynamic Splash technique is used |
| [MACRO_ANTI_DISTORTION_GUIDE.md](MACRO_ANTI_DISTORTION_GUIDE.md) | Macro anti-distortion rules | 🔴 When Macro Close-up technique is used |
| [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) | Style-specific quality checklist | 🔴 After all images generated in Step 5 |
