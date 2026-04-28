# Complete Runnable Code Examples

> This file is only read during actual image generation and contains two sets of complete runnable code templates.
> The two examples use sportswear and a luxury jacket as scenes. You can freely choose an Asian or European model by switching the `model_race` variable without needing to change the template.

---

## Example 1: Sportswear

**Complete runnable code, containing all 4 layers of detailed content:**

```python
import sys, os
from datetime import datetime
import requests

# Dynamically add the skill directory to the Python path (ensures it can run in any working directory)
_skill_dir = os.path.join(os.getcwd(), '.cursor', 'skills', '0kidswear-photography-master-C')
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)
from generate_image import image_gen_sync

# Create a save folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_dir = os.path.join(os.getcwd(), 'generated_photos', timestamp)
os.makedirs(save_dir, exist_ok=True)

def download_image(url, save_path):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")

# ========== Configuration ==========
garment_url = "https://example.com/sports_wear_white_bg.jpg"

garment_analysis = {
    "category": "sports_wear",
    "style": "athletic_basketball",
    "brand_tier": "fashion",
}

# ========== User Four-Step Selection (Assigned Sequentially) ==========
model_gender = "girl"        # Step 0a: User selects "boy" / "girl"
model_race   = "asian"       # Step 0b: User selects "asian" / "european"
age_group    = "6-10"        # Step 0c: User selects "3-6" / "6-10" / "10-14"
scene_type   = "sports_venue"  # Step 2: Fill in based on user selection, check SKILL.md for available values
                               # Options: luxury_manor / sports_venue / garden_setting / resort_pool /
                               #          beach_natural / indoor_school / cozy_home / wild_forest /
                               #          farm_field / snow_mountain / vintage_train / metro_adventure
                               # ⚠️ cozy_home has 3 style variants, metro_adventure has 3 carriage styles
                               #    After selection, narrative_theme and Scene framing must be synchronously adjusted

age_group_config = {
    "3-6":  {"age_desc": "4-5 year old",
             "body_desc": "petite toddler proportions, chubby cheeks and naturally round face",             "expression": "innocent sweet smile with childlike wonder",
             "footwear": "toddler-friendly velcro athletic sneakers with clean colorway",
             "face_asian_girl": "round baby-soft face with plump youthful cheeks, very large luminous dark eyes relative to face, delicate baby features with natural sweet charm",
             "face_asian_boy":  "adorable round face with natural baby plumpness, bright large dark eyes, clean fresh features with boyish sweetness"},
    "6-10": {"age_desc": "7-8 year old",
             "body_desc": "slender child proportions with natural youthful energy",             "expression": "bright engaging smile with youthful vitality",
             "footwear": "classic kids athletic sneakers with clean colorway",
             "face_asian_girl": "softly oval face with gentle youthful plumpness, refined elegant features with age-appropriate grace",
             "face_asian_boy":  "clean oval face with natural proportions, expressive dark eyes with energetic boyish appeal"},
    "10-14":{"age_desc": "11-12 year old",
             "body_desc": "pre-teen lean proportions with more defined elegant features",             "expression": "composed cool confidence with subtle editorial edge",
             "footwear": "trendy chunky high-top sneakers with bold design",
             "face_asian_girl": "gently defined oval face with refined delicate features and emerging adolescent elegance",
             "face_asian_boy":  "clean defined face with refined proportions, confident composed expression and editorial-quality presence"},
}
age_cfg = age_group_config[age_group]

# Uniformly use image generation model
generation_fn = image_gen_sync

print(f"✅ Model Gender: {model_gender} | Model Type: {model_race} | Generation Model: {generation_fn.__name__}")
print(f"✅ Child Model Age Group: {age_group} years ({age_cfg['age_desc']})")

# ========== Build 4-Layer Prompts ==========

# Universal quality keywords (Included in all prompts)
universal_quality = """
Fashion editorial lookbook style, brand catalog photography / light magazine editorial style,
realistic and textured skin, realistic fabric texture, real commercial editorial photography texture,
high definition, realistic, 8k, documentary film texture, real subtle film grain, high-end film editorial.
"""

# Layer 1: Narrative Theme (Simple description)
narrative_theme = "Youth sports fashion, vibrant outdoor hard court lifestyle"  # ← matches sports_venue

# Layer 2: Subject Persona (Includes action, pose, expression)
_gender_word = "girl" if model_gender == "girl" else "boy"

# Face Description: gender+race dual branch, applying precise beauty DNA (Refer to ASIAN_MODEL_DNA.md)
if model_race == "asian" and model_gender == "girl":
    _face_desc = (
        "Porcelain-fair luminous skin with natural soft rosy flush on cheeks, "
        "large dark brown eyes with subtle natural double eyelids and long natural dark lashes, "
        "small delicate nose with softly rounded upturned tip, "
        f"naturally pink small lips with soft childlike fullness, {age_cfg['face_asian_girl']}."
    )
elif model_race == "asian":  # boy
    _face_desc = (
        "Fair smooth porcelain-like skin, bright clear large dark brown eyes with natural expressive energy, "
        "naturally defined soft dark brows, clean small nose, fresh natural lips, "
        f"clean well-proportioned face with natural boyish charm, {age_cfg['face_asian_boy']}."
    )
else:  # european
    _face_desc = f"Refined classic European features, realistic skin texture with subtle freckles, {age_cfg['body_desc']}."

# Facial features brief summary (used in Shot 2-5 prompts to enforce consistency)
if model_race == "asian" and model_gender == "girl":
    _face_summary = (
        "porcelain-fair luminous skin, large dark brown eyes with long natural dark lashes, "
        f"small delicate upturned nose, naturally pink lips, {age_cfg['face_asian_girl']}"
    )
elif model_race == "asian":  # boy
    _face_summary = (
        "fair smooth skin, bright clear large dark brown eyes with natural expressive energy, "
        f"clean well-proportioned features with natural boyish charm, {age_cfg['face_asian_boy']}"
    )
else:  # european
    _face_summary = "refined European mixed-heritage features, natural realistic skin texture"

model_character = f"""
{age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model,

Face: {_face_desc}

Body: Fresh athletic presence with natural grace and youthful energy,
camera-friendly poise showing childlike beauty and elegant posture.

Pose and action: 
Athletic ready-to-shoot stance with designed naturalness and commercial precision:
- Feet: Positioned shoulder-width apart with slight natural splay, weight balanced evenly or slightly forward on balls of feet
- Knees: Slightly bent showing athletic readiness (NOT locked straight)
- Hips: Square to camera with confident stable base
- Torso: Upright with slight forward lean from hips (approx 5-10 degrees), shoulders naturally squared
- Arms: One arm relaxed at side, other arm slightly raised with hand at waist or chest level in natural athletic ready position, showing confident posture without tension
- Hands: Relaxed natural fingers, easy athletic presence without gripping any prop
- Head: Lifted with chin parallel to ground or slightly elevated, face directly toward camera
- Eyes: Locked on target point (basket direction) with sharp focused gaze, eyebrows naturally positioned
- Expression: Focused athletic determination - eyebrows slightly lowered showing concentration, mouth closed or slightly open in controlled breathing, overall face showing "moment before action" intensity
- Overall body line: Creating strong vertical presence with balanced athletic geometry, every joint angle contributing to "peak readiness frozen in time" aesthetic

Commercial editorial stance (NOT casual everyday snapshot): designed composition emphasizing both athletic power and garment presentation.

Expression: 
Focused athletic determination with designed authenticity and commercial control:
- Eyes: Locked intensely on target (basket direction) with clear sharp focus, pupils dilated showing concentration, visible eye light creating sparkle and life
- Eyebrows: Slightly lowered and drawn together showing intense focus (NOT relaxed, NOT raised), creating subtle furrow between brows
- Mouth: Closed with lips naturally together or slightly parted in controlled athletic breathing, NO smile, NO teeth showing, slight tension in jaw showing determination
- Overall facial tension: Controlled intensity - face engaged but not strained, showing "moment of truth" concentration
- Emotional tone: Serious athletic focus, competitive determination, commercial intensity (NOT candid everyday smile, NOT playful expression)

This is peak concentration moment in commercial sports editorial (NOT casual game play, NOT everyday snapshot).
"""

# Layer 3: Outfit Styling
garment_type = "upper_body"

if garment_type == "upper_body":
    garment_styling = f"""
Complete Outfit Styling (garment_type: upper_body):
- Upper body: Wearing the exact same sports top from reference image (preserve all brand logos, colors, graphics exactly)
- Lower body: Wide-leg balloon-fit track pants in matching navy/black, or relaxed cargo shorts in neutral tone
  (Stylist note: wide silhouette balances the athletic top; NO skinny jeans, NO tight leggings)
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: Contemporary youth sports editorial — relaxed silhouettes, coordinated tonal palette
"""
elif garment_type == "lower_body":
    garment_styling = f"""
Complete Outfit Styling (garment_type: lower_body):
- Lower body: Wearing the exact same bottom from reference image (preserve all details exactly)
- Upper body: Cropped athletic hoodie or sports tank top in complementary neutral tone
  (Stylist note: cropped top creates proportion with athletic bottoms; NO oversized heavy jacket)
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: Balanced athletic editorial — coordinated volume and tonal harmony
"""
elif garment_type in ["full_outfit", "dress"]:
    garment_styling = f"""
Complete Outfit Styling (garment_type: full_outfit):
- Wearing the complete outfit from reference image exactly as shown (preserve all details)
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: Complete look as designed — let the full outfit speak
"""

# Layer 4: Style Reference
style_reference = """
Fashion editorial lookbook style / Brand catalog photography / Youth sports magazine editorial.
Athletic lifestyle campaign aesthetic / Commercial sports fashion presentation.
"""

# ========== Generate Shot 1 ==========
print("\n🎬 Generating Shot 1: Full-body standard athletic stance...")

shot1_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Scene framing: Court front view — sports net or court barrier running horizontally in mid-background, vibrant blue hard court surface underfoot with court line markings, green windbreak boards or bleacher structure softly blurred beyond. Full-body framing.

{model_character}

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}
"""

shot1_urls = generation_fn(
    prompt=shot1_prompt,
    img_urls=[garment_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot1_path = os.path.join(save_dir, "01_full_body_athletic.jpg")
download_image(shot1_urls[0], shot1_path)
model_reference_url = shot1_urls[0]

# ========== Generate Shot 2-5 ==========
print("\n🎬 Generating Shot 2: Dynamic athletic moment...")

shot2_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Sideline fence — metal chain-link fence filling background diagonally, colored court surface extending to mid-ground, strong direct sunlight creating sharp graphic shadow patterns on court surface. Full-body action framing.

Pose and action: 
Dynamic athletic moment frozen at peak with designed naturalness - capturing mid-dribble power instant:
- Feet: BOTH feet firmly planted flat on court surface (NOT jumping, NOT airborne), positioned in athletic split stance (one foot slightly forward), toes gripping ground showing power transfer readiness
- Knees: Deeply bent (approximately 90-100 degrees) in dynamic crouch showing explosive power ready to release, front knee tracking over toes, back knee loaded with spring tension
- Hips: Dropped low in athletic squat position, rotated slightly toward dribble direction, showing coiled energy
- Torso: Leaning forward aggressively (approx 20-30 degrees from vertical), shoulders squared and engaged, core visibly tensed showing power control
- Arms: One arm (dribbling arm) extended downward at approximately 45-degree angle with hand making contact with ball at its apex or just after bounce, other arm extended outward for balance with fingers spread
- Hands: Dribbling hand with fingers spread wide showing ball control at moment of push, wrist flexed showing active engagement with ball, non-dribbling hand in protective/balance position
- Head: Turned toward movement direction, chin slightly tucked, neck engaged showing dynamic action awareness
- Eyes: Intensely focused on ball/court/opponent zone (NOT looking at camera), pupils tracking movement, showing athletic concentration in action
- Expression: Concentrated athletic focus with natural intensity - eyebrows slightly furrowed, mouth closed or slightly open in controlled breathing, face showing "in the zone" engagement
- Overall body geometry: Creating powerful diagonal line from back foot through torso to extended arm, showing controlled athletic explosion captured at perfect moment

This is PEAK ATHLETIC MOMENT FREEZE with both feet grounded (commercial sports editorial, NOT actual jumping, NOT blurry motion, NOT casual play).

Expression: Concentrated athletic focus with natural intensity - capturing "in the zone" moment:
- Eyes: Intensely tracking ball/court/action zone (NOT looking at camera), pupils dilated and focused downward/forward, showing active athletic engagement
- Eyebrows: Naturally lowered in concentration, slight furrow between brows showing mental focus during physical action
- Mouth: Slightly open in controlled athletic breathing OR closed with lips pressed together showing exertion control, NO smile, NO teeth showing prominently
- Face overall: Showing controlled intensity and athletic immersion - NOT casual play expression, NOT posed smile for camera
- Emotional tone: Deep athletic concentration, competitive engagement, "nothing else exists in this moment" focus

This is authentic athletic concentration captured at peak moment (commercial sports editorial intensity, NOT everyday casual play, NOT looking at camera).

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}

"""

shot2_urls = generation_fn(
    prompt=shot2_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot2_path = os.path.join(save_dir, "02_dynamic_action.jpg")
download_image(shot2_urls[0], shot2_path)

print("\n🎬 Generating Shot 3: Side profile display...")

shot3_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Low dynamic court angle — wide colored hard court surface extending behind model, court boundary lines receding diagonally creating depth, green perimeter boards or open blue sky at upper frame. Full-body dynamic side framing.

Pose and action:
Side profile athletic stance with designed editorial precision - emphasizing garment silhouette and body line:
- Feet: Positioned in natural walking stance (one foot slightly forward), weight distributed 60/40 favoring front leg, creating elegant leg line
- Knees: Front knee slightly bent (subtle 5-10 degree flex), back leg straighter creating graceful S-curve through lower body
- Hips: Angled at 45 degrees to camera, creating clean side profile showing garment drape and fit
- Torso: Upright with natural posture, rib cage lifted, showing confident vertical presence, shoulders squared in profile
- Arms: One arm hanging naturally at hip level with relaxed fingers, other arm naturally positioned at opposite side, both showing relaxed but controlled athletic placement
- Hands: Basketball-holding hand with fingers gently curved around ball (NOT gripping tightly), showing casual athletic connection to prop
- Head: Profile view turned 90 degrees from camera OR slight 75-degree turn allowing partial face visibility, chin level or slightly lifted
- Eyes: Gaze directed straight ahead in profile OR natural side-glance toward camera (NOT full face turn), showing calm awareness
- Expression: Calm composed confidence - eyebrows relaxed in natural position, mouth closed or slight natural expression, face showing athletic poise and self-assurance
- Overall body line: Creating elegant vertical line from head through torso to grounded legs, with subtle contraposto (weight shift) adding natural grace

This is classic fashion profile stance emphasizing garment silhouette (commercial editorial posing, NOT casual standing).

Expression:
Calm focused determination with profile elegance:
- Eyes: Gazing straight ahead in profile view OR gentle side-glance toward camera, showing quiet confidence and self-possession
- Eyebrows: Naturally relaxed in neutral position, creating serene composed look
- Mouth: Closed with lips naturally together OR slight hint of composed smile (subtle upturn at corners), showing inner confidence
- Face overall: Serene athletic poise - NOT intense, NOT overly serious, showing quiet strength and natural grace
- Emotional tone: Composed confidence, quiet determination, elegant self-assurance

This is calm editorial poise emphasizing profile beauty and garment presentation (commercial fashion stance, NOT action intensity).

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}

"""

shot3_urls = generation_fn(
    prompt=shot3_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot3_path = os.path.join(save_dir, "03_side_profile.jpg")
download_image(shot3_urls[0], shot3_path)

print(f"\n🎬 Generating Shot 4: {'Bottom' if garment_type == 'lower_body' else 'Top'} detail close-up...")

shot4_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Courtside bench seat — model seated on courtside chair or bench, vibrant blue or orange-blue court surface extending behind and to the side at shallow depth of field creating saturated color wash, yellow or colored chair framing the near-background. Upper/half-body framing.

Pose and action:
{"Lower body 3/4 composition — emphasizing bottom garment details and fabric quality:" if garment_type == "lower_body" else "Upper body 3/4 composition with designed casualness — emphasizing garment details and brand presence:"}
{"- Camera framing: 3/4 body from waist down, showing full lower body silhouette and construction" if garment_type == "lower_body" else "- Body angle: Torso rotated approximately 30-45 degrees from camera, creating 3/4 view that shows both front and side dimension of garment"}
{"- Legs: Slight natural stance showing garment drape, one leg slightly forward revealing silhouette" if garment_type == "lower_body" else "- Shoulders: Relaxed but aligned, one shoulder (near-camera) slightly forward creating depth"}
{"- Hands: Casually placed on hips or gently resting at garment hem to frame the lower garment naturally" if garment_type == "lower_body" else "- Arms: One arm naturally resting at side with soft relaxed fingers, other arm lightly at waist or gently touching garment hem"}
- Head: Turned toward camera, chin at natural level or slightly lifted
- Eyes: Direct confident gaze toward camera OR looking slightly off-camera creating thoughtful mood
- Expression: Relaxed athletic confidence - slight natural smile OR composed serious look
- Weight distribution: Casual stance with weight on one leg (hip slightly dropped), creating natural relaxed contrapposto
- Overall composition: {"Framing lower body prominently, showing garment construction, waistband, and leg silhouette" if garment_type == "lower_body" else "Framing face and upper torso prominently, with garment logo/branding visible and emphasized"}

This is casual confident editorial {"lower-body" if garment_type == "lower_body" else "upper-body"} framing (commercial fashion closer composition, NOT snapshot selfie style).

Expression:
Relaxed athletic confidence with warm approachability - personality-forward mood:
- Eyes: Direct confident eye contact with camera showing comfortable camera presence OR looking slightly off-camera (15-30 degrees) creating contemplative thoughtful mood
- Eyebrows: Naturally relaxed in neutral comfortable position, NOT furrowed, NOT raised, showing ease
- Mouth: Gentle natural smile with slight upward curve at corners showing warmth and approachability OR composed neutral expression with relaxed lips showing cool confidence, NO wide grin, teeth may show slightly in natural smile
- Face overall: Showing personality and character - warm friendly energy OR cool composed confidence, face conveying "this is who I am" authenticity
- Emotional tone: Approachable warmth, confident ease, natural charm, relaxed athletic cool

This is personality-forward editorial mood emphasizing both garment and character (commercial lifestyle warmth, NOT intense sports focus, NOT stiff formal pose).

【Layer 3: Outfit Styling】
{garment_styling}
{
"Special emphasis on lower body details: fabric texture, waistband, leg silhouette and construction."
if garment_type == "lower_body" else
"Special emphasis on full-outfit / dress silhouette: overall garment drape, waist definition, skirt flow or full-length construction, fabric quality from head to toe."
if garment_type in ["dress", "full_outfit"] else
"Special emphasis on upper body: brand logo, fabric texture, collar/sleeve design details."
}

【Layer 4: Style Reference】
{style_reference}

"""

_shot4_suffix = 'lower' if garment_type == 'lower_body' else ('full_outfit' if garment_type in ['dress', 'full_outfit'] else 'upper')
shot4_urls = generation_fn(
    prompt=shot4_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot4_path = os.path.join(save_dir, f"04_{_shot4_suffix}_detail.jpg")
download_image(shot4_urls[0], shot4_path)

print(f"\n🎬 Generating Shot 5: {'Bottom' if garment_type == 'lower_body' else 'Top'} half-body portrait...")

shot5_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Court center lifestyle — sports net or perimeter boards softly blurred in background, colored court surface with line markings underfoot. Half-body portrait framing.

Pose and action:
Half-body portrait composition with relaxed natural presence:
- Body positioning: Standing in naturally relaxed stance OR casually leaning against court structure (fence post, hoop pole, bench back), creating easy comfortable presence
- Weight distribution: Weight casually shifted to one leg with opposite hip slightly dropped, OR if leaning - body angle creating diagonal line showing relaxed ease
- Shoulders: Naturally dropped and relaxed (NOT squared/tensed), showing authentic casual posture
- Arms: Both hands relaxed, one hanging naturally at side, other lightly resting at waist or lightly touching garment hem — no props
- Hands: Fingers in natural relaxed curves, NO rigid placement, showing ease and comfort in moment
- Head: Angled naturally - slight tilt showing relaxed ease OR straight-on for direct connection
- Eyes: Warm direct gaze toward camera showing confident ease OR looking slightly away creating narrative moment
- Expression: Relaxed genuine warmth - natural smile showing real happiness OR calm contentment
- Overall body language: Showing "post-game relaxation" OR "taking a moment" OR "casual confidence"

This is authentic relaxed lifestyle moment (commercial editorial naturalness, NOT forced casual, NOT stiff portrait).

Expression:
Relaxed genuine warmth with authentic personality:
- Eyes: Warm inviting gaze toward camera OR looking naturally away suggesting caught-in-moment authenticity
- Eyebrows: Completely relaxed in natural resting position
- Mouth: Natural genuine smile OR gentle content closed-mouth smile, NO forced grin
- Emotional tone: Genuine warmth, authentic happiness, comfortable ease

【Layer 3: Outfit Styling】
{garment_styling}
{
"Full lower body presentation showing complete bottom garment, waistband detail, and leg silhouette."
if garment_type == "lower_body" else
"Full-length or 3/4-length presentation showcasing complete dress/outfit silhouette, fabric movement, and overall garment harmony."
if garment_type in ["dress", "full_outfit"] else
"Full upper body presentation from waist up, showing complete styling."
}

【Layer 4: Style Reference】
{style_reference}

"""

shot5_urls = generation_fn(
    prompt=shot5_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot5_path = os.path.join(save_dir, "05_half_body_portrait.jpg")
download_image(shot5_urls[0], shot5_path)

# ========== Summary Output ==========
all_urls = shot1_urls + shot2_urls + shot3_urls + shot4_urls + shot5_urls

print(f"\n{'='*60}")
print(f"✅ Commercial editorial generation complete!")
print(f"{'='*60}")
print(f"📁 Saved location: {save_dir}")
print(f"📊 Total: {len(all_urls)} images (five 3:4 verticals)")
print(f"🎯 Model used: {generation_fn.__name__}")
print(f"👤 Model gender: {model_gender} | Model type: {model_race}")
print(f"\nFile list:")
for i in range(1, 6):
    print(f"  0{i}_*.jpg")
print(f"\nOnline links:")
for i, url in enumerate(all_urls, 1):
    print(f"  {i}. {url}")
```

**Example 1 Key Configuration:**
- Shot 1: Basketball court front view (court + hoop)
- Shot 2: Sideline view (metal fence + bleachers), dynamic pose with both feet grounded
- Shot 3: Corner view (corner lines + hoop post), side profile
- Shot 4: Close-up view (court texture + distant blur), upper body details
- Shot 5: Center view (center circle + full court), relaxed half-body

---

## Example 2: Luxury Jacket

**Complete runnable code, showing luxury-tier configuration:**

```python
import sys, os
from datetime import datetime
import requests

# Dynamically add the skill directory to the Python path (ensures it can run in any working directory)
_skill_dir = os.path.join(os.getcwd(), '.cursor', 'skills', '0kidswear-photography-master-C')
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)
from generate_image import image_gen_sync

# Create a save folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_dir = os.path.join(os.getcwd(), 'generated_photos', f"{timestamp}_luxury")
os.makedirs(save_dir, exist_ok=True)

def download_image(url, save_path):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")

# ========== Configuration ==========
garment_url = "https://example.com/luxury_jacket_white_bg.jpg"

garment_analysis = {
    "category": "luxury_jacket",
    "style": "european_classic",
    "brand_tier": "luxury",
}

# ========== User Four-Step Selection (Assigned Sequentially) ==========
model_gender = "boy"          # Step 0a: User selects "boy" / "girl"
model_race   = "european"     # Step 0b: User selects "asian" / "european"
age_group    = "6-10"         # Step 0c: User selects "3-6" / "6-10" / "10-14"
scene_type   = "luxury_manor" # Step 2: Fill in based on user selection, check SKILL.md for available values

# Uniformly use image generation model
generation_fn = image_gen_sync

print(f"✅ Model Gender: {model_gender} | Model Type: {model_race} | Generation Model: {generation_fn.__name__}")

# ========== Build 4-Layer Prompts ==========

# Universal quality keywords (Included in all prompts)
universal_quality = """
Fashion editorial lookbook style, brand catalog photography / light magazine editorial style,
realistic and textured skin, realistic fabric texture, real commercial editorial photography texture,
high definition, realistic, 8k, documentary film texture, real subtle film grain, high-end film editorial.
"""

# Layer 1: Narrative Theme (Simple description)
narrative_theme = "Luxury kidswear editorial, European manor weekend lifestyle"  # ← matches luxury_manor

# Layer 2: Subject Persona (Includes action, pose, expression)
age_group_config = {
    "3-6":  {"age_desc": "4-5 year old",
             "body_desc": "petite toddler proportions, chubby cheeks and naturally round face",             "expression": "innocent sweet smile with childlike wonder",
             "footwear": "soft strap leather shoes or toddler mary janes",
             "face_asian_girl": "round baby-soft face with plump youthful cheeks, very large luminous dark eyes relative to face, delicate baby features with natural sweet charm",
             "face_asian_boy":  "adorable round face with natural baby plumpness, bright large dark eyes, clean fresh features with boyish sweetness"},
    "6-10": {"age_desc": "7-8 year old",
             "body_desc": "slender child proportions with natural youthful energy",             "expression": "bright engaging smile with youthful vitality",
             "footwear": "classic leather oxford shoes or clean leather loafers",
             "face_asian_girl": "softly oval face with gentle youthful plumpness, refined elegant features with age-appropriate grace",
             "face_asian_boy":  "clean oval face with natural proportions, expressive dark eyes with energetic boyish appeal"},
    "10-14":{"age_desc": "11-12 year old",
             "body_desc": "pre-teen lean proportions with more defined elegant features",             "expression": "composed cool confidence with subtle editorial edge",
             "footwear": "classic leather loafers or lace-up oxfords",
             "face_asian_girl": "gently defined oval face with refined delicate features and emerging adolescent elegance",
             "face_asian_boy":  "clean defined face with refined proportions, confident composed expression and editorial-quality presence"},
}
age_cfg = age_group_config[age_group]
print(f"✅ Child Model Age Group: {age_group} years ({age_cfg['age_desc']})")

_gender_word = "girl" if model_gender == "girl" else "boy"

# Face Description: gender+race dual branch, applying precise beauty DNA
if model_race == "asian" and model_gender == "girl":
    _face_desc = (
        "Porcelain-fair luminous skin with natural soft rosy flush on cheeks, "
        "large dark brown eyes with subtle natural double eyelids and long natural dark lashes, "
        "small delicate nose with softly rounded upturned tip, "
        f"naturally pink small lips with soft childlike fullness, {age_cfg['face_asian_girl']}."
    )
elif model_race == "asian":  # boy
    _face_desc = (
        "Fair smooth porcelain-like skin, bright clear large dark brown eyes with natural expressive energy, "
        "naturally defined soft dark brows, clean small nose, fresh natural lips, "
        f"clean well-proportioned face with natural boyish charm, {age_cfg['face_asian_boy']}."
    )
else:  # european
    _face_desc = f"Refined classic European features, realistic skin texture with subtle freckles, {age_cfg['body_desc']}."

# Facial features brief summary
if model_race == "asian" and model_gender == "girl":
    _face_summary = (
        "porcelain-fair luminous skin, large dark brown eyes with long natural dark lashes, "
        f"small delicate upturned nose, naturally pink lips, {age_cfg['face_asian_girl']}"
    )
elif model_race == "asian":  # boy
    _face_summary = (
        "fair smooth skin, bright clear large dark brown eyes with natural expressive energy, "
        f"clean well-proportioned features with natural boyish charm, {age_cfg['face_asian_boy']}"
    )
else:  # european
    _face_summary = "refined European mixed-heritage features, natural realistic skin texture"

model_character = f"""
{age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} fashion model,

Face: {_face_desc}

Pose and action: Standing naturally with refined posture beside vintage car showing designed elegance,
one hand gently resting on car door in composed editorial gesture (NOT casual everyday stance),
weight slightly shifted in perfectly balanced aristocratic pose.
Every detail choreographed for luxury editorial presentation (commercial campaign, NOT family snapshot).

Expression: Serious calm with designed sophistication,
composed confidence showing subtle aristocratic reserve (NOT candid everyday smile),
eyes gazing forward with quiet determination, refined editorial mood.
"""

# Layer 3: Outfit Styling
garment_type = "upper_body"

if garment_type == "upper_body":
    garment_styling = f"""
Complete Outfit Styling (garment_type: upper_body — luxury jacket):
- Upper body: Wearing the exact same luxury jacket from reference image (preserve embroidered badge, metal buttons, fabric texture exactly)
- Lower body: Tailored wide-leg trousers in cream or warm camel — clean silhouette with refined drape
  (Stylist note: wide-leg trousers elevate the look; NO generic jeans, NO athletic shorts)
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: European aristocratic editorial — understated luxury with refined proportions
"""
elif garment_type == "lower_body":
    garment_styling = f"""
Complete Outfit Styling (garment_type: lower_body):
- Lower body: Wearing the exact same bottom from reference image (preserve all details exactly)
- Upper body: Fitted ribbed knit top or crisp linen shirt in complementary neutral
  (Stylist note: clean fitted top balances tailored bottom; NO oversized or athletic top)
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: Luxury editorial coordination — refined simplicity with quality materials
"""
elif garment_type in ["full_outfit", "dress"]:
    garment_styling = f"""
Complete Outfit Styling (garment_type: full_outfit/dress):
- Wearing the complete outfit from reference image exactly as shown
- Footwear: {age_cfg['footwear']}
- NO bags, hats, or accessories
Overall styling: Complete luxury look — let the full garment design speak
"""

# Layer 4: Style Reference
style_reference = """
Luxury fashion editorial / High-end brand catalog photography / European manor lifestyle magazine.
Timeless aristocratic aesthetic / Premium kidswear campaign presentation.
"""

# ========== Generate Shot 1 ==========
print("\n🎬 Generating Shot 1: Full-body standard elegant stance...")

shot1_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Scene framing: Manor driveway front view — vintage automobile hood and front grille in near-background, manicured lawn extending behind, estate stone facade softly visible in distance. Full-body head-to-toe framing.

{model_character}

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}
"""

shot1_urls = generation_fn(
    prompt=shot1_prompt,
    img_urls=[garment_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot1_path = os.path.join(save_dir, "01_full_body_elegant.jpg")
download_image(shot1_urls[0], shot1_path)
model_reference_url = shot1_urls[0]

# ========== Generate Shot 2-5 ==========
print("\n🎬 Generating Shot 2: Elegant walking moment...")

shot2_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} child model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Garden path angle — brick pathway receding diagonally behind model, tall topiary hedges framing both sides, manor windows and climbing roses blurred in deep background. Full-body walking framing.

Pose and action: Elegant walking moment captured at peak graceful instant with designed naturalness,
body in perfectly balanced mid-stride showing refined movement (NOT casual everyday walking),
one arm naturally resting at side with soft relaxed fingers in choreographed editorial gesture,
frozen at most photogenic moment emphasizing luxury garment flow.
Designed sophisticated movement (commercial editorial, NOT family candid photo).

Expression: Composed confidence and aristocratic ease with designed sophistication.

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}

"""

shot2_urls = generation_fn(
    prompt=shot2_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot2_path = os.path.join(save_dir, "02_elegant_walking.jpg")
download_image(shot2_urls[0], shot2_path)

print("\n🎬 Generating Shot 3: Side profile aristocratic silhouette...")

shot3_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} child model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Car side profile — vintage automobile side body curves in near-background, ancient oak tree canopy above, soft garden bokeh beyond car. Full-body side profile framing.

Pose and action: Side profile aristocratic stance,
body turned showing refined garment silhouette, one hand resting on vintage car elegantly.

Expression: Quiet confidence and sophistication.

【Layer 3: Outfit Styling】
{garment_styling}

【Layer 4: Style Reference】
{style_reference}

"""

shot3_urls = generation_fn(
    prompt=shot3_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot3_path = os.path.join(save_dir, "03_side_profile_luxury.jpg")
download_image(shot3_urls[0], shot3_path)

print(f"\n🎬 Generating Shot 4: {'Bottom' if garment_type == 'lower_body' else 'Top'} luxury detail close-up...")

shot4_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} child model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Close approach — vintage car door window glass creating curved reflection in near-background, leather interior detail softly visible through glass, estate garden blurred beyond. Upper-body tight framing, extreme shallow depth of field.

Pose and action: {"Lower body 3/4 refined composition, standing elegantly to display bottom garment silhouette and fabric quality, legs in natural refined stance." if garment_type == "lower_body" else "Upper body 3/4 refined composition, arms positioned showing luxury garment details, one hand adjusting jacket collar with elegant gesture."}

Expression: Composed aristocratic confidence.

【Layer 3: Outfit Styling】
{garment_styling}
{
"Special emphasis on bottom garment: fabric drape, waistband construction, leg silhouette quality."
if garment_type == "lower_body" else
"Special emphasis on full-outfit / dress: overall silhouette harmony, garment drape quality, waist definition, fabric texture from neckline to hem."
if garment_type in ["dress", "full_outfit"] else
"Special emphasis on Bonpoint badge, metal buttons, luxury fabric texture."
}

【Layer 4: Style Reference】
{style_reference}

"""

_shot4_suffix2 = 'lower' if garment_type == 'lower_body' else ('full_outfit' if garment_type in ['dress', 'full_outfit'] else 'upper')
shot4_urls = generation_fn(
    prompt=shot4_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot4_path = os.path.join(save_dir, f"04_{_shot4_suffix2}_luxury_detail.jpg")
download_image(shot4_urls[0], shot4_path)

print(f"\n🎬 Generating Shot 5: {'Bottom' if garment_type == 'lower_body' else 'Half-body'} aristocratic portrait...")

shot5_prompt = f"""
{universal_quality}

【Layer 1: Narrative Theme】
{narrative_theme}

【Layer 2: Subject Persona】
Same {age_cfg['age_desc']} {'Asian' if model_race == 'asian' else 'European mixed-heritage'} {_gender_word} child model as Shot 1 reference image,
face features: {_face_summary},
maintaining fully consistent appearance and age.

Scene framing: Estate front — manor stone portico columns in background, sculptural garden urn on one side, climbing rose arch framing upper corner of composition, soft afternoon light. Half-body portrait framing.

Pose and action: Half-body aristocratic portrait composition,
natural elegant standing pose with dog companion, arms relaxed showing refined posture.

Expression: Serene confidence and sophistication.

【Layer 3: Outfit Styling】
{garment_styling}
{
"Full lower body garment presentation, emphasizing fabric quality and refined silhouette from waist down."
if garment_type == "lower_body" else
"Full-length dress/outfit presentation — showcasing complete silhouette, fabric movement, and overall garment luxury from head to toe."
if garment_type in ["dress", "full_outfit"] else
"Full luxury garment presentation, complete styling effect."
}

【Layer 4: Style Reference】
{style_reference}

"""

_shot5_suffix = 'lower_body' if garment_type == 'lower_body' else ('full_outfit' if garment_type in ['dress', 'full_outfit'] else 'half_body')
shot5_urls = generation_fn(
    prompt=shot5_prompt,
    img_urls=[garment_url, model_reference_url],
    ratio="3:4",
    image_size="4K",
    pic_num=1
)
shot5_path = os.path.join(save_dir, f"05_{_shot5_suffix}_luxury_portrait.jpg")
download_image(shot5_urls[0], shot5_path)

# ========== Summary Output ==========
all_urls = shot1_urls + shot2_urls + shot3_urls + shot4_urls + shot5_urls

print(f"\n{'='*60}")
print(f"✅ Luxury commercial editorial generation complete!")
print(f"{'='*60}")
print(f"📁 Saved location: {save_dir}")
print(f"📊 Total: {len(all_urls)} images (five 3:4 verticals)")
print(f"🎯 Model used: {generation_fn.__name__}")
print(f"👤 Model gender: {model_gender} | Model type: {model_race}")
print(f"\nFile list:")
for i in range(1, 6):
    print(f"  0{i}_*.jpg")
print(f"\nOnline links:")
for i, url in enumerate(all_urls, 1):
    print(f"  {i}. {url}")
```

**Example 2 Key Configuration:**
- Shot 1: Standing by car view (car + lawn + dog)
- Shot 2: Garden path view (path + manor building + hedges)
- Shot 3: Car side profile view (car body curves + dog + big tree), side profile
- Shot 4: Close-up view (car doors/windows + leather interior), upper body details
- Shot 5: Manor front view (manor facade + sculpture garden + dog)
