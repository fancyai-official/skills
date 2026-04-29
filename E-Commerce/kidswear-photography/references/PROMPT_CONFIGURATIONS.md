# Prompt Configuration Example Library

> Demonstrates how different garment types configure the 4-layer variables

---

## Configuration 1: Luxury Jacket (Bonpoint Style)

### Garment Analysis
```python
garment_analysis = {
    "category": "luxury_jacket",
    "style": "european_classic",
    "brand_tier": "luxury",
    "fabric": "organic cotton knit",
    "texture": "visible weave pattern",
    "colors": ["navy blue", "cream", "bordeaux"],
    "brand_elements": ["embroidered Bonpoint badge", "metal snap buttons", "contrast trim"],
    "features": ["classic bomber cut", "ribbed cuffs", "premium lining"],
    "aesthetic": "refined European luxury, understated elegance"
}
```

### Auto-Generated Configuration
```python
auto_config = {
    "model_race": "european",
    "model_age": "7-8 year old",
    "model_gender": "boy",  # Selected by user in Step 0a: "boy" / "girl"
    "generation_model": "image_gen",
    "expression": "luxury_serious",  # serious calm, composed confidence
    "lifestyle": "villa vacation",
    "setting": "European manor weekend",
    "persona": "young gentleman",
    "scene_type": "luxury_manor",
    "lighting_style": "soft_elegant",
    "action_style": "standing_editorial"
}
```

### 4-Layer Variable Specific Values

**Universal Quality Keywords (At the beginning of all prompts)**
```
Fashion editorial lookbook style, brand catalog photography / light magazine editorial style,
realistic and textured skin, realistic fabric texture, real commercial editorial photography texture, high definition, realistic, 8k,
documentary film texture, real subtle film grain, high-end film editorial.
```

**Layer 1: Narrative Theme**
```
Luxury kidswear editorial / European manor lifestyle
```

**Layer 2: Subject Persona**
```
# ⚠️ Scene framing must be fetched from SKILL.md "12 Scenes Overview → luxury_manor" based on Shot number, different for each image
# Below is the Shot 1 example (manor driveway front view):
Scene framing: Manor driveway front view — vintage automobile hood and grille in near-background,
manicured lawn extending behind, estate stone facade softly visible in distance. Full-body framing.

A 6-8 year old European mixed-race child model with realistic skin texture,
with a calm, mature, restrained temperament,
possessing "little gentleman" composure and effortless elite aura.

Pose and action: Classic fashion editorial stance with designed elegance,
standing naturally with composed posture (NOT casual everyday standing),
body upright with choreographed asymmetry,
weight slightly shifted to right leg creating designed balance,
left hand gently resting at garment hem with refined control,
right hand at side showing aristocratic ease,
every detail choreographed for luxury presentation (commercial campaign, NOT family photo).

Expression: Serious calm with designed sophistication,
nonchalant confidence with minimal micro-expression (NOT candid everyday face),
mouth straight or 1mm curve showing composed maturity,
eyes with scrutinizing gaze displaying designed aristocratic presence.
```

**Layer 3: Outfit Styling**
```
Complete Outfit Styling (garment_type: upper_body — luxury jacket):
- Upper body: Wearing the exact same luxury jacket from reference image (preserve embroidered badge, metal buttons, fabric texture exactly)
- Lower body: Tailored wide-leg trousers in cream or warm camel — clean silhouette with refined drape
- Footwear: Classic leather oxford shoes or clean leather loafers
- NO bags, hats, or accessories (focus on garment only)
- Overall styling: European aristocratic editorial — understated luxury with refined proportions
```

**Layer 4: Style Reference**
```
Luxury fashion editorial / High-end brand catalog photography / European manor lifestyle magazine.
Timeless aristocratic aesthetic / Premium kidswear campaign presentation.
```

---

## Configuration 2: Sportswear (Balabala Basketball Series)

### Garment Analysis
```python
garment_analysis = {
    "category": "sports_wear",
    "style": "athletic_basketball",
    "brand_tier": "fashion",  # Mass fashion brand
    "fabric": "moisture-wicking mesh",
    "texture": "breathable athletic fabric",
    "colors": ["electric blue", "orange", "white"],
    "brand_elements": ["Balabala logo", "number print", "brand tape"],
    "features": ["sleeveless design", "loose fit", "athletic cut"],
    "aesthetic": "energetic youth sports"
}
```

### Auto-Generated Configuration
```python
auto_config = {
    "model_race": "asian",  # Example value, selected by user in Step 0b: "asian" / "european"
    "model_age": "7-8 year old",
    "model_gender": "girl",
    "generation_model": "image_gen",
    "expression": "sports_focused",  # focused determination
    "lifestyle": "hard court",
    "setting": "outdoor sports venue",
    "persona": "young athlete",
    "scene_type": "sports_venue",
    "lighting_style": "bright_active",
    "action_style": "dynamic_athletic"
}
```

### 4-Layer Variable Specific Values

**Layer 1: Narrative Theme**
```
Youth sports fashion / vibrant outdoor hard court lifestyle
```

**Layer 2: Subject Persona**
```
# ⚠️ Scene framing must be fetched from SKILL.md "5-Shot Scene Breakdown Table → sports_venue" based on Shot number, different for each image
# Below is the Shot 1 example (court front view):
Scene framing: Court front view — sports net or court barrier running horizontally in mid-background,
vibrant blue hard court surface underfoot with court line markings,
green windbreak boards or bleacher structure softly blurred beyond. Full-body framing.

(Fill in based on model_race / model_gender / age_group, example is Asian girl 6-10 years old)
7-8 year old Asian girl fashion model — premium Chinese child beauty:
Porcelain-fair luminous skin with natural soft rosy flush on cheeks,
large dark brown eyes with subtle natural double eyelids and long natural dark lashes,
small delicate nose with softly rounded upturned tip, naturally pink small lips,
softly oval face with gentle youthful plumpness,
Pose and action: Athletic ready stance with designed naturalness,
captured at peak court moment frozen in perfect balance (NOT real playing action),
body in composed athletic stance with knees slightly bent,
arms in natural athletic position at sides or slightly raised,
upper body showing controlled athletic power emphasizing garment beautifully,
frozen at most photogenic instant (commercial sports editorial, NOT everyday sports photo).

Expression: Focused determination with designed authenticity,
eyes locked on target with choreographed intensity (NOT candid everyday expression),
eyebrows slightly furrowed showing controlled focus,
mouth slightly pressed with composed athletic concentration.
```

**Layer 3: Outfit Styling**
```
Complete Outfit Styling (garment_type: upper_body — sportswear):
- Upper body: Wearing the exact same sports top from reference image (preserve all brand logos, colors, graphics exactly)
- Lower body: Wide-leg balloon-fit track pants in matching navy/black, or relaxed cargo shorts in neutral tone
- Footwear: Chunky high-top sneakers or bold athletic shoes with clean colorway
- NO bags, hats, or accessories (focus on garment only)
- Overall styling: Contemporary youth sports editorial — relaxed silhouettes, coordinated tonal palette
```

**Layer 4: Style Reference**
```
Fashion editorial lookbook style / Brand catalog photography / Youth sports magazine editorial.
Athletic lifestyle campaign aesthetic / Commercial sports fashion presentation.
```

---

## Configuration 3: Princess Dress (French Fairy Dress)

### Garment Analysis
```python
garment_analysis = {
    "category": "princess_dress",
    "style": "french_romantic",
    "brand_tier": "fashion",
    "fabric": "tulle and lace",
    "texture": "layered soft tulle with delicate lace",
    "colors": ["blush pink", "ivory", "dusty rose"],
    "brand_elements": ["floral appliqués", "satin ribbon", "pearl details"],
    "features": ["puffy skirt", "fitted bodice", "flowing layers"],
    "aesthetic": "romantic fairy-tale elegance"
}
```

### Auto-Generated Configuration
```python
auto_config = {
    "model_race": "asian",  # Can be Asian model
    "model_age": "7-8 year old",
    "model_gender": "girl",
    "generation_model": "image_gen",
    "expression": "princess_dreamy",  # gentle sweetness, dreamy elegance
    "lifestyle": "garden party",
    "setting": "private flower garden",
    "persona": "young princess",
    "scene_type": "garden_setting",
    "lighting_style": "golden_hour",
    "color_style": "soft_dreamy",
    "action_style": "elegant_feminine"
}
```

### 4-Layer Variable Specific Values

**Layer 1: Narrative Theme**
```
Fairy-tale fashion / dreamy childhood / 
elegant young lady aesthetic / private garden setting / 
graceful young princess charm
```

**Layer 2: Subject Persona**
```
(Fill in based on model_race / model_gender / age_group, example is Asian girl 6-10 years old)
7-8 year old Asian girl fashion model — premium Chinese child beauty:
Porcelain-fair luminous skin with natural soft rosy flush on cheeks,
large dark brown eyes with subtle natural double eyelids and long natural dark lashes,
small delicate nose with softly rounded upturned tip, naturally pink small lips,
softly oval face with gentle youthful plumpness,
Emotional expression: gentle sweetness, dreamy elegance,
soft gentle smile with tender quality,
eyes looking slightly upward with dreamy contemplative gaze,
expression showing innocent grace and fairy-tale quality.

Action details: Elegant graceful pose emphasizing dress beauty,
body in natural S-curve stance,
hands delicately holding dress sides to show layers,
or posture displaying refined feminine grace.
```

**Layer 3: Outfit Styling**
```
Complete Outfit Styling (garment_type: dress):
- Full garment: Blush pink French romantic princess dress — layered tulle skirt with ivory lace overlay, fitted bodice with floral appliqués and pearl details
- Upper body: Fitted bodice with delicate lace and satin ribbon waist tie, pearl button accents at center front
- Lower body / skirt: Voluminous puffy layered tulle skirt in blush pink and dusty rose gradient, flowing layers revealing soft movement
- Footwear: Ivory lace-trim ankle socks paired with blush pink T-strap leather shoes with small bow

Special emphasis on full-dress silhouette: layered tulle drape, waist ribbon definition, lace texture quality, and delicate fabric movement.
```

**Layer 4: Style Reference**
```
Commercial fashion editorial style — fairy-tale elegance meets luxury kidswear brand catalog.
Vogue Enfants / Jacadi Paris editorial aesthetic.
Dreamy soft-focus background with garden bokeh, garment as hero.
Aspect ratio 3:4 vertical, 4K resolution.
```

---

## Configuration 8: Casual Wear (Modern Daily Style)

### Garment Analysis
```python
garment_analysis = {
    "category": "casual_wear",
    "style": "modern_casual",
    "brand_tier": "mass",  # Mass brand
    "fabric": "cotton jersey",
    "texture": "soft comfortable knit",
    "colors": ["denim blue", "white", "gray"],
    "brand_elements": ["simple logo print", "contrast stitching"],
    "features": ["relaxed fit", "everyday style", "comfortable"],
    "aesthetic": "modern kids lifestyle"
}
```

### Auto-Generated Configuration
```python
auto_config = {
    "model_race": "asian",
    "model_age": "7-8 year old",
    "model_gender": "boy",
    "generation_model": "image_gen",
    "expression": "casual_cheerful",  # bright cheerful smile
    "lifestyle": "everyday moments",
    "setting": "urban casual environment",
    "persona": "carefree spirit",
    "scene_type": "cozy_home",  # Changed from urban_casual; city daily can choose cozy_home or garden_setting
    "lighting_style": "golden_hour",
    "color_style": "warm_vibrant",
    "action_style": "standing_editorial"  # But more relaxed version
}
```

---

## Quick Configuration Comparison Table

> Model type (Asian/European) is selected by the user in Step 0b, not automatically determined by garment type, and is not listed in this table.

| Garment Type | Generation Model | Expression Style | Scene Type | Lighting Style |
|---------|---------|---------|---------|---------|
| Luxury Formal | image_gen | luxury_serious | luxury_manor | soft_elegant |
| Sportswear | image_gen | sports_focused | sports_venue | bright_active |
| Princess Dress | image_gen | princess_dreamy | garden_setting | golden_hour |
| Resort Swimwear | image_gen | casual_cheerful | resort_pool | bright_active |
| Beachwear | image_gen | sports_energetic | beach_natural | natural_bright |
| School Uniform | image_gen | luxury_warm | indoor_school | soft_elegant |
| Autumn Homewear | image_gen | casual_cheerful | cozy_home | soft_elegant |
| Outdoor Adventure | image_gen | sports_energetic | wild_forest | natural_bright |
| Farm Field | image_gen | casual_cheerful | farm_field | golden_hour |
| Skiwear | image_gen | sports_focused | snow_mountain | natural_bright |
| Travel Wear | image_gen | casual_cheerful | vintage_train | soft_elegant |

---

**The system now supports 11 scene types, covering all 23 sets of reference cases!**

**Note: All types uniformly use the image_gen model.**

All configurations use the unified 4-layer structure, just with different variable values.
