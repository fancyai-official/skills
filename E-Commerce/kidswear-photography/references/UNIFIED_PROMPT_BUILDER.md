# Unified 4-Layer Prompt Construction System

> A complete, reusable prompt generation template; model gender/race is passed in based on user selection in Step 0a/0b, scene (`scene_type`) is passed in based on user selection in Step 2, expression is automatically configured based on garment.
>
> **For detailed outfit styling rules, see [FASHION_STYLIST.md](FASHION_STYLIST.md)** (including garment_type identification logic, fashion pairing prohibited list, Shot 4/5 close-up focus switching rules)

---

## Core Architecture

### Automated Decision System

```python
# Automatically select configuration based on garment analysis (scene/expression/lighting; race/gender passed by caller)
def auto_config_from_garment(garment_analysis, age_group="6-10", model_race="asian", model_gender="girl", scene_type=None):
    """
    Input:
      garment_analysis - Garment analysis result
      age_group    - User Step 0c selection: "3-6" / "6-10" / "10-14"
      model_race   - User Step 0b selection: "asian" / "european"
      model_gender - User Step 0a selection: "boy" / "girl"
      scene_type   - User Step 2 selection: e.g., "garden_setting" / "luxury_manor", etc. (Auto-inferred if None)
    Output: Complete configuration (model/model type/expression/scene, etc.)
    """
    
    # 1. Determine brand tier
    if has_luxury_features(garment_analysis):
        brand_tier = "luxury"
    elif has_fashion_features(garment_analysis):
        brand_tier = "fashion"
    else:
        brand_tier = "mass"
    
    # 2. Model gender and type: Passed in after user selection in Step 0a/0b, no auto-inference here.
    #    model_gender = "boy" / "girl"       ← User Step 0a selection, passed via parameter
    #    model_race   = "asian" / "european" ← User Step 0b selection, passed via parameter
    generation_model = "image_gen"  # Uniformly use image_gen
    
    # 3. Age group configuration (age_group passed from user selection: "3-6" / "6-10" / "10-14")
    # Note: auto_config_from_garment receives age_group parameter and passes it to subsequent steps
    age_group_config = {
        "3-6":  {"age_desc": "4-5 year old",
                 "body_desc": "petite toddler proportions, chubby cheeks and naturally round face",                 "expression": "innocent sweet smile with childlike wonder"},
        "6-10": {"age_desc": "7-8 year old",
                 "body_desc": "slender child proportions with natural youthful energy",                 "expression": "bright engaging smile with youthful vitality"},
        "10-14":{"age_desc": "11-12 year old",
                 "body_desc": "pre-teen lean proportions with more defined elegant features",                 "expression": "composed cool confidence with subtle editorial edge"},
    }
    age_cfg = age_group_config.get(age_group, age_group_config["6-10"])
    
    # 4. Determine expression style
    expression = select_expression(
        category=garment_analysis.get("category", "") if isinstance(garment_analysis, dict) else getattr(garment_analysis, "category", ""),
        style=garment_analysis.get("style", "fashion") if isinstance(garment_analysis, dict) else getattr(garment_analysis, "style", "fashion"),
        brand_tier=brand_tier
    )
    
    return {
        "model_race":      model_race,    # From parameter (User Step 0b)
        "model_gender":    model_gender,  # From parameter (User Step 0a)
        "model_age":       age_cfg["age_desc"],
        "model_body":      age_cfg["body_desc"],
        "generation_model": generation_model,
        "brand_tier":      brand_tier,    # luxury / fashion / mass
        "expression":      expression,
        "action_style":    "standard",    # Default action style, build_character uses this field
        "narrative":       select_narrative(garment_analysis),
        "scene_type":      scene_type or select_scene(garment_analysis),  # Prioritize user Step 2 selection, otherwise auto-infer
        "style_ref":       select_style_reference(garment_analysis)
    }
```

---

## Unified 4-Layer Template

**Structure Explanation**: Layer 1/2/3/4

### Layer 1: Narrative Theme (Simple Description)

```python
def build_narrative(config, garment_analysis):
    """Build narrative theme (simple description)
    
    ⚠️ IMPORTANT: When calling, directly pass the narrative_theme string obtained from SKILL.md "12 Scenes Overview" table based on scene_type, instead of relying on this function to auto-infer based on garment style.
    
    Correct usage:
        narrative_theme = "Youth sports fashion, vibrant outdoor hard court lifestyle"  # From SKILL.md table
        # Directly use narrative_theme, do not call build_narrative()
    
    The following templates serve only as fallbacks (when scene_type is unknown):
    """
    
    narrative_templates = {
        "luxury": "Luxury kidswear editorial / European manor lifestyle",
        "fashion": "Contemporary kids fashion / modern editorial style",
        "sports": "Youth sports fashion / athletic lifestyle",
        "princess": "Fairy-tale fashion / dreamy childhood / elegant young lady aesthetic / graceful young princess",
        "casual": "Modern kids lifestyle / everyday fashion / natural childhood moments / carefree young spirit"
    }
    
    style = garment_analysis.get("style", "fashion") if isinstance(garment_analysis, dict) else getattr(garment_analysis, "style", "fashion")
    return narrative_templates.get(style, narrative_templates["fashion"])
```

---

### Layer 2: Subject Persona

> **⚠️ Commercial Editorial Standard:** All actions and expressions must reflect "designed naturalness" and "peak moment freeze", avoid "casual everyday" style

```python
def build_character(config, shot_number=1):
    """Build subject persona description (incorporating commercial editorial standards and model consistency)"""
    
    # Retrieve age group related configurations from config
    model_age    = config["model_age"]    # e.g., "4-5 year old" / "7-8 year old" / "11-12 year old"
    model_body   = config["model_body"]   # Body/face shape description
    model_gender = config.get("model_gender", "girl")
    model_race   = config.get("model_race", "asian")
    _gender_word = "girl" if model_gender == "girl" else "boy"
    
    # Model base features (Refer to ASIAN_MODEL_DNA.md to understand the beauty DNA analysis basis)
    character_templates = {
        "european": """
            A {age} European mixed-race child {gender} model with realistic skin texture, {body_desc},
            refined classic European features, high-end fashion model appearance.
        """,
        "asian_girl": """
            {age} Asian girl fashion model — premium Chinese child beauty:

            Face: Porcelain-fair luminous skin with natural soft rosy flush on cheeks,
            large dark brown eyes with subtle natural double eyelids and long natural dark lashes,
            small delicate nose with softly rounded upturned tip,
            naturally pink small lips with soft childlike fullness,
            {face_desc}, clean refined Chinese child beauty aesthetic.

            Body: {body_desc}, elegant natural grace with childlike camera-ready poise.

            Overall: Premium children's fashion model with refined photogenic Chinese girl beauty.
        """,
        "asian_boy": """
            {age} Asian boy fashion model — premium Chinese child model:

            Face: Fair smooth porcelain-like skin,
            bright clear large dark brown eyes with natural expressive energy,
            naturally defined soft dark brows, clean small nose, fresh natural lips,
            {face_desc}, natural boyish charm with photogenic Chinese child model appeal.

            Body: {body_desc}, fresh confident presence with natural youthful vitality.

            Overall: Premium children's fashion model with clean photogenic Chinese boy energy.
        """
    }
    
    # Expression options (All expressions are "designed")
    expression_library = {
        "luxury_serious": """
            Expression: Serious calm with designed sophistication,
            composed confidence showing subtle aristocratic reserve (NOT candid everyday expression),
            minimal micro-expression with refined control,
            eyes gazing with quiet determination.
        """,
        "luxury_warm": """
            Expression: Serene confidence with designed gentle sophistication,
            soft subtle smile showing warmth yet refinement (NOT big everyday smile),
            composed elegance with approachable quality,
            designed warmth maintaining luxury aesthetic.
        """,
        "sports_focused": """
            Expression: Focused determination with designed authenticity,
            concentrated engagement with choreographed intensity (NOT candid excitement),
            eyebrows slightly furrowed showing controlled focus,
            eyes locked on target with sharp determined gaze.
        """,
        "sports_energetic": """
            Expression: Energetic confidence with designed vitality,
            bright confident smile showing controlled enthusiasm (NOT uncontrolled laugh),
            eyes sparkling with choreographed energy,
            commercial sports editorial mood.
        """,
        "princess_dreamy": """
            Expression: Gentle sweetness with designed elegance,
            soft gentle smile with choreographed tender quality (NOT casual grin),
            eyes with composed dreamy contemplation,
            refined fairy-tale aesthetic.
        """,
        "casual_cheerful": """
            Expression: Bright cheerful smile with designed naturalness,
            natural smile showing composed happiness (NOT big everyday laugh),
            eyes bright with controlled carefree joy,
            commercial casual editorial mood.
        """,
        "street_cool": """
            Expression: Cool edgy vibe with designed confidence,
            neutral or slight smirk with choreographed attitude (NOT random pose),
            eyes showing composed directness,
            commercial streetwear editorial aesthetic.
        """
    }
    
    # Action detail templates (incorporating precise 9-body-part descriptions and Shot 2 constraints)
    action_templates = {
        "standing_editorial": """
            Pose and action: Classic fashion editorial stance with designed naturalness,
            body naturally upright in composed pose (NOT casual everyday standing),
            - Feet: Positioned shoulder-width apart, weight slightly shifted creating choreographed asymmetry
            - Knees: Slightly bent (NOT locked straight)
            - Hips: Square to camera with confident stable base
            - Torso: Upright with natural posture, rib cage lifted
            - Arms: One arm naturally resting at side with soft relaxed fingers, other arm lightly at waist or gently touching garment hem
            - Hands: Casually placed with refined control, fingers in natural relaxed curves
            - Head: Lifted with chin parallel to ground or slightly elevated
            - Eyes: Direct confident gaze toward camera
            every detail designed for commercial presentation.
        """,
        "dynamic_athletic": """
            Pose and action: Peak athletic moment frozen with designed grace,
            captured at perfect instant (NOT blurry real action),
            - Feet: {shot_feet_logic}
            - Knees: Deeply bent in dynamic crouch showing explosive power
            - Hips: Dropped low in athletic squat position
            - Torso: Leaning forward aggressively, shoulders squared
            - Arms: Positioned to emphasize garment beautifully, one arm extended
            - Hands: Fingers spread showing control
            - Head: Turned toward movement direction, neck engaged
            - Eyes: Intensely focused on action zone (NOT looking at camera)
            commercial sports editorial composition (NOT everyday sports photo).
        """,
        "elegant_feminine": """
            Pose and action: Elegant graceful pose with designed femininity,
            body in natural S-curve showing choreographed elegance (NOT casual stance),
            - Feet: Positioned elegantly, weight distributed favoring front leg
            - Knees: Front knee slightly bent creating natural grace
            - Hips: Angled to accentuate garment drape
            - Torso: Upright with natural posture, showing confident vertical presence
            - Arms: One arm hanging naturally, other gently positioned at side
            - Hands: Delicately positioned (resting naturally or holding a small prop) with refined control
            - Head: Angled naturally, chin slightly lifted
            - Eyes: Soft dreamy gaze or direct confident look
            frozen at most photogenic moment,
            commercial princess editorial aesthetic (NOT everyday dress-up).
        """
    }
    
    # Select template key and face summary based on race and gender
    if model_race == "asian":
        template_key = f"asian_{_gender_word}"
        face_desc = config.get(f"face_asian_{_gender_word}", "")
        if _gender_word == "girl":
            face_summary = f"porcelain-fair luminous skin, large dark brown eyes, small delicate nose, {face_desc}"
        else:
            face_summary = f"fair smooth skin, bright clear large dark brown eyes, clean well-proportioned features, {face_desc}"
    else:
        template_key = "european"
        face_desc = ""
        face_summary = "refined European mixed-heritage features, natural realistic skin texture"

    # Enforce model consistency for Shots 2-5
    if shot_number > 1:
        character = f"Same {model_age} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model as Shot 1 reference image,\nface features: {face_summary},\nmaintaining fully consistent appearance and age."
    else:
        # Full character description for Shot 1
        character = character_templates[template_key].format(
            age=model_age,
            body_desc=model_body,
            gender=_gender_word,
            face_desc=face_desc,
            **{k: v for k, v in config.items() if k not in ("model_age", "model_body", "model_gender")}
        )
        
    expression = expression_library[config["expression"]]
    
    # Dynamic athletic logic specifically injecting Shot 2 constraints
    shot_feet_logic = "BOTH feet firmly planted flat on court surface (NOT jumping, NOT airborne)" if shot_number == 2 else "Positioned in athletic split stance"
    
    action = action_templates[config.get("action_style", "standing_editorial")].format(
        shot_feet_logic=shot_feet_logic, 
        **config
    )
    
    return f"{character}\n\n{expression}\n\n{action}"
```

---

### Layer 3: Outfit Styling (NO accessories)

```python
# ===== Garment Type Identification =====
# garment_type determined after analyzing the white-background image:
#   "upper_body"  → Top (T-shirt/hoodie/jacket/shirt, etc.)
#   "lower_body"  → Bottom (Pants/skirt/shorts, etc.)
#   "full_outfit" → Complete outfit (Matching top and bottom)
#   "dress"       → Dress/romper

def select_bottom_styling(garment_analysis):
    """Select fashionable bottom based on top style (called when reference image is a top)"""
    style = garment_analysis.get("style", "casual")
    brand_tier = garment_analysis.get("brand_tier", "fashion")
    
    if style in ["athletic", "sports", "streetwear", "basketball"]:
        return "Wide-leg balloon-fit track pants in matching tonal color, OR relaxed cargo shorts in neutral (olive/black/khaki) — NO skinny jeans, NO tight leggings"
    elif style in ["casual", "hoodie", "sweatshirt", "oversize"]:
        return "Wide-leg relaxed linen or cotton trousers in oat/ivory/khaki, OR paper-bag waist shorts with tie detail, OR loose plaid wide-leg pants — NO skinny jeans"
    elif brand_tier == "luxury" or style in ["formal", "classic", "european"]:
        return "Tailored wide-leg trousers in cream, camel, or navy with refined drape, OR A-line midi skirt in solid or subtle plaid, OR pleated shorts with clean tailoring"
    elif style in ["princess", "sweet", "floral", "lace", "romantic"]:
        return "Tulle puff skirt in matching or contrast pastel, OR flowing pleated chiffon skirt, OR tiered ruffle midi skirt"
    elif style in ["neutral", "minimal", "contemporary"]:
        return "Wide-leg relaxed shorts in matching tone, OR straight-leg wide trousers, OR mini pleated skirt"
    else:
        return "Wide-leg relaxed trousers in neutral tone — coordinated and stylish, NOT skinny jeans"

def select_top_styling(garment_analysis):
    """Select fashionable top based on bottom style (called when reference image is a bottom)"""
    style = garment_analysis.get("style", "casual")
    category = garment_analysis.get("category", "pants")
    
    if category in ["wide_leg_pants", "cargo_pants", "trousers"]:
        return "Cropped relaxed cotton tee (short hem), OR oversized linen button-up shirt loosely tucked, OR cropped knit sweater"
    elif category in ["skirt", "midi_skirt", "pleated_skirt"]:
        return "Oversized knit sweater or cardigan, OR tucked-in linen button-up shirt, OR fitted ribbed turtleneck"
    elif category in ["shorts", "athletic_shorts", "sport_shorts"]:
        return "Cropped hoodie or zip-up sweatshirt, OR sports tank top, OR lightweight bomber jacket"
    elif category in ["maxi_skirt", "long_skirt", "flowing_skirt"]:
        return "Fitted ribbed knit top or camisole, OR simple cropped tee with clean neckline, OR lightweight linen shirt"
    elif category in ["mini_skirt", "micro_skirt"]:
        return "Oversized graphic tee (tucked front), OR knit sweater vest over tee, OR puff-sleeve blouse"
    else:
        return "Cropped relaxed top in complementary neutral tone — creates balanced proportion"

def select_footwear_styling(garment_analysis, age_group="6-10"):
    """Select footwear based on overall style (incorporating age group adaptation logic)"""
    style = garment_analysis.get("style", "casual")
    brand_tier = garment_analysis.get("brand_tier", "fashion")
    
    if style in ["athletic", "sports", "basketball", "streetwear"]:
        if age_group == "3-6":
            return "toddler-friendly velcro athletic sneakers with clean colorway"
        elif age_group == "10-14":
            return "trendy chunky high-top sneakers with bold design"
        else:
            return "classic kids sneakers with clean colorway"
    elif brand_tier == "luxury" or style in ["formal", "classic", "european"]:
        if age_group == "3-6":
            return "soft strap leather shoes or toddler mary janes"
        elif age_group == "10-14":
            return "classic leather loafers or lace-up oxfords"
        else:
            return "classic leather oxford shoes or clean leather loafers"
    elif style in ["princess", "sweet", "floral", "romantic"]:
        if age_group == "3-6":
            return "soft strap ballet flats or toddler mary jane shoes with bow detail"
        elif age_group == "10-14":
            return "elegant ballet flats or refined mary jane shoes"
        else:
            return "ballet flats or mary jane shoes with bow detail"
    elif style in ["casual", "oversize", "hoodie"]:
        if age_group == "3-6":
            return "toddler slip-on flats or soft velcro sneakers"
        elif age_group == "10-14":
            return "chunky loafers or trendy low-top vintage sneakers"
        else:
            return "chunky loafers, low-top vintage sneakers, or mary jane flats"
    elif style in ["neutral", "minimal"]:
        if age_group == "3-6":
            return "clean soft white velcro sneakers or simple strap loafers"
        elif age_group == "10-14":
            return "minimalist leather sneakers or clean modern loafers"
        else:
            return "clean white sneakers or simple leather loafers"
    else:
        return "stylish shoes appropriate to garment aesthetic"

def build_garment(garment_analysis, garment_url, garment_type="upper_body", age_group="6-10"):
    """Build garment description (explicitly without accessories)"""
    
    # Universal garment preservation statement
    garment_preservation = """Wearing the exact same clothing from reference image, 
    keep all original garment details unchanged."""
    
    if garment_type == "upper_body":
        coordination = f"""
    Fashion styling coordination (upper_body reference):
    - Upper body: Wearing the exact same garment from reference image (preserve ALL details)
    - Lower body: {select_bottom_styling(garment_analysis)}
    - Footwear: {select_footwear_styling(garment_analysis, age_group)}
    - NO bags, hats, or accessories
        """
    elif garment_type == "lower_body":
        coordination = f"""
    Fashion styling coordination (lower_body reference):
    - Lower body: Wearing the exact same garment from reference image (preserve ALL details)
    - Upper body: {select_top_styling(garment_analysis)}
    - Footwear: {select_footwear_styling(garment_analysis, age_group)}
    - NO bags, hats, or accessories
        """
    else:  # full_outfit or dress
        coordination = f"""
    Wearing the complete outfit from reference image exactly as shown (preserve ALL details).
    - Footwear: {select_footwear_styling(garment_analysis, age_group)}
    - NO bags, hats, or accessories
        """
    
    return f"""
    {garment_preservation}
    
    Garment details from analysis:
    - Category: {garment_analysis.get('category', '')}
    - Fabric texture: {garment_analysis.get('fabric', '')}
    - Brand elements: {garment_analysis.get('brand_elements', '')}
    - Color palette: {garment_analysis.get('colors', '')}
    - Design features: {garment_analysis.get('features', '')}
    
    {coordination}
    Overall styling: {garment_analysis.get('aesthetic', 'Fashion editorial aesthetic, coordinated and stylish')}
    """
```

---

### Layer 4: Style Reference

```python
def build_style_reference(config, garment_analysis):
    """Build style reference (based on brand tier)"""
    
    style_templates = {
        "luxury": """
            Luxury fashion editorial / High-end brand catalog photography / European manor lifestyle magazine.
            Timeless aristocratic aesthetic / Premium kidswear campaign presentation.
        """,
        "fashion": """
            Fashion editorial lookbook style / Brand catalog photography / Youth sports magazine editorial.
            Contemporary lifestyle campaign / Commercial fashion presentation.
        """,
        "casual": """
            Lifestyle magazine editorial / Casual brand catalog / Contemporary kids fashion.
            Natural lifestyle aesthetic / Everyday fashion campaign.
        """
    }
    
    return style_templates[config["brand_tier"]]
```

## Universal Quality Keywords

**Must be added at the beginning of all prompts:**

```python
universal_quality = """
Fashion editorial lookbook style, brand catalog photography / light magazine editorial style,
realistic and textured skin, realistic fabric texture, real commercial editorial photography texture, high definition, realistic, 8k,
documentary film texture, real subtle film grain, high-end film editorial.
"""
```

---

## Scene Randomization Logic

```python
import random

def resolve_scene_variant(scene_type):
    """
    Resolves the randomization logic for multi-variant scenes (garden_setting, cozy_home, farm_field, metro_adventure)
    to ensure consistency across the 5 shots.
    
    Returns the specific style key/direction that should be used to look up the scene framing.
    """
    if scene_type == "garden_setting":
        return random.choices(["Direction A", "Direction B", "Direction C"], weights=[0.4, 0.4, 0.2])[0]
    elif scene_type == "cozy_home":
        return random.choices(["Style A", "Style B", "Style C"], weights=[0.25, 0.25, 0.5])[0]
    elif scene_type == "farm_field":
        return random.choice(["Style A", "Style B"])
    elif scene_type == "metro_adventure":
        return random.choice(["Style A", "Style B", "Style C"])
    return None  # No variant for other scenes
```

---

## Complete Prompt Template

```python
prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}
# ⚠️ Use narrative_theme retrieved from SKILL.md "12 Scenes Overview" table by scene_type, do not use build_narrative()

【Layer 2: Subject Persona】
Scene framing: {scene_framing}
# ⚠️ scene_framing must be retrieved from SKILL.md "5-Shot Scene Breakdown Table" by scene_type + shot number, different for each image
{build_character(config, shot_number)}

【Layer 3: Outfit Styling】
{build_garment(garment_analysis, garment_url, garment_type=garment_type, age_group=age_group)}

【Layer 4: Style Reference】
{build_style_reference(config, garment_analysis)}
"""
```

---

## Complete Usage Example

```python
# 1. Garment Analysis (Auto or Manual)
garment_analysis = {
    "category": "luxury_jacket",
    "style": "european_classic",
    "brand_tier": "luxury",
    "fabric": "organic cotton",
    "colors": ["navy", "cream"],
    "brand_elements": ["embroidered badge", "metal buttons"],
    "features": ["classic cut", "premium construction"]
}

# 2. Auto-Generate Configuration
# ⚠️ Note: model_race, model_gender, scene_type are all passed in from user selection, not auto-inferred here:
scene_type = "luxury_manor"  # ← Fill in based on User Step 2 selection
config = auto_config_from_garment(
    garment_analysis,
    age_group=age_group,
    model_race=model_race,
    model_gender=model_gender,
    scene_type=scene_type   # User Step 2 selection
)

# Resolve specific variant for multi-style scenes
scene_variant = resolve_scene_variant(scene_type)
if scene_variant:
    print(f"Randomly selected scene variant: {scene_variant}")

# 3. Generate shot configurations for 5 images
shot_configs = [
    {"type": "full_body_standard", "focus": "complete_outfit"},
    {"type": "dynamic_action", "focus": "garment_movement"},  # If sportswear
    {"type": "side_profile", "focus": "silhouette"},
    {"type": "upper_detail", "focus": "brand_elements"},
    {"type": "half_body_texture", "focus": "fabric_quality"}
]

# 4. Build complete prompt for each image
scene_framing_table = {
    "luxury_manor": {
        1: "Manor driveway front view — vintage automobile hood and grille in near-background, manicured lawn extending behind, estate facade softly visible in distance. Full-body framing.",
        2: "Garden path angle — brick pathway receding diagonally, tall topiary hedges framing both sides, manor windows blurred in deep background. Full-body framing.",
        3: "Car side profile — vintage automobile side body curves in near-background, ancient oak tree canopy above, soft garden bokeh beyond. Full-body side profile framing.",
        4: "Close approach — vintage car door window glass creating curved reflection in background, leather interior detail softly visible. Upper-body tight framing, extreme shallow depth of field.",
        5: "Estate front — manor stone portico columns in background, sculptural garden urn on one side, rose arch framing upper corner. Half-body portrait framing.",
    },
    # For scenes with variants, structure like:
    # "garden_setting": {
    #     "Direction A": { 1: "...", 2: "..." },
    #     "Direction B": { 1: "...", 2: "..." },
    # }
    # Other 11 scene_types similarly
}

for shot_number, shot in enumerate(shot_configs, start=1):
    # Lookup framing logic considering variants
    if scene_variant:
        scene_framing = scene_framing_table.get(config.get("scene_type"), {}).get(scene_variant, {}).get(shot_number, "")
    else:
        scene_framing = scene_framing_table.get(config.get("scene_type", "luxury_manor"), {}).get(shot_number, "")
        
    prompt = f"""
    【Layer 1: Narrative Theme】
    {build_narrative(config, garment_analysis)}
    
    【Layer 2: Subject Persona】
    Scene framing: {scene_framing}

    {build_character(config, shot_number=shot_number)}
    
    【Layer 3: Outfit Styling】
    {build_garment(garment_analysis, garment_url, garment_type=garment_type, age_group=age_group)}
    
    【Layer 4: Style Reference】
    {build_style_reference(config, garment_analysis)}
    """
    
    # 5. Call corresponding model to generate
    result = image_gen_sync(prompt, ...)
```

---

## Configuration Library Index

For complete configuration examples of different garment types, see:
- [PROMPT_CONFIGURATIONS.md](PROMPT_CONFIGURATIONS.md) - Detailed configuration example library

For expression selection guide, see:
- [EXPRESSION_GUIDE.md](EXPRESSION_GUIDE.md) - Complete expression library

---

**This is the unified 4-layer prompt construction system!**

**Core Advantages:**
- ✅ Model gender/race are explicitly passed from user Step 0a/0b, not auto-inferred
- ✅ Unified 4-layer precise structure
- ✅ Scene (`scene_type`) is selected by user Step 2, expression is auto-configured based on garment
- ✅ Easy to expand and maintain
