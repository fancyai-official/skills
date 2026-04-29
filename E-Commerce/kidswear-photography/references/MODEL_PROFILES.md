# 👤 Age Group Configuration and Model Description

### Age Group Mapping Table

```python
# Age group (assigned after user selection: "3-6" / "6-10" / "10-14")
age_group_config = {
    "3-6": {
        "age_desc":   "4-5 year old",
        "body_desc":  "petite toddler proportions, chubby cheeks and naturally round face, cute and cherubic childlike charm",
        "expression": "innocent sweet smile with childlike wonder",
        "face_asian_girl": "round baby-soft face with plump youthful cheeks, very large luminous dark eyes relative to face, delicate baby features with natural sweet charm",
        "face_asian_boy":  "adorable round face with natural baby plumpness, bright large dark eyes, clean fresh features with boyish sweetness",
    },
    "6-10": {
        "age_desc":   "7-8 year old",
        "body_desc":  "slender child proportions with natural youthful energy, clean and fresh presence",
        "expression": "bright engaging smile with youthful vitality",
        "face_asian_girl": "softly oval face with gentle youthful plumpness, refined elegant features with age-appropriate grace",
        "face_asian_boy":  "clean oval face with natural proportions, expressive dark eyes with energetic boyish appeal",
    },
    "10-14": {
        "age_desc":   "11-12 year old",
        "body_desc":  "pre-teen lean proportions with more defined features, emerging adolescent elegance",
        "expression": "composed cool confidence with subtle editorial edge",
        "face_asian_girl": "gently defined oval face with refined delicate features and emerging adolescent elegance",
        "face_asian_boy":  "clean defined face with refined proportions, confident composed expression and editorial-quality presence",
    },
}
age_cfg = age_group_config[age_group]  # age_group is determined by user selection
```

### Asian Model Core Description Template

> Refer to ASIAN_MODEL_DNA.md to understand the complete beauty DNA analysis basis

```python
# model_gender selected by user: "boy" / "girl"

if model_gender == "girl":
    model_character = f"""
{age_cfg['age_desc']} Asian girl fashion model — premium Chinese child beauty:

Face: Porcelain-fair luminous skin with natural soft rosy flush on cheeks,
large dark brown eyes with subtle natural double eyelids and long natural dark lashes,
small delicate nose with softly rounded upturned tip,
naturally pink small lips with soft childlike fullness,
{age_cfg['face_asian_girl']}.

Body: {age_cfg['body_desc']}, elegant natural grace with childlike camera-ready poise.
Expression: {age_cfg['expression']} with designed authenticity (NOT candid everyday expression).
Note: Adjust expression and pose based on garment type, always maintaining commercial editorial standards
"""
else:  # boy
    model_character = f"""
{age_cfg['age_desc']} Asian boy fashion model — premium Chinese child model:

Face: Fair smooth porcelain-like skin, bright clear large dark brown eyes with natural expressive energy,
naturally defined soft dark brows, clean small nose, fresh natural lips,
{age_cfg['face_asian_boy']}.

Body: {age_cfg['body_desc']}, fresh confident presence with natural youthful vitality.
Expression: {age_cfg['expression']} with designed authenticity (NOT candid everyday expression).
Note: Adjust expression and pose based on garment type, always maintaining commercial editorial standards
"""
```

### European Model Core Description Template

```python
# model_gender selected by user: "boy" / "girl"
_gender_word = "girl" if model_gender == "girl" else "boy"

model_character = f"""
{age_cfg['age_desc']} European mixed-race child {_gender_word} model,
realistic skin texture,
{age_cfg['body_desc']}, refined classic European features, high-end fashion model appearance.

Expression: {age_cfg['expression']} with designed sophistication,
composed confidence (NOT candid everyday expression).
Note: Adjust expression and pose based on garment type, always maintaining commercial editorial standards
"""
```

---

## 💻 Image Generation Code Framework

```python
import sys, os
from datetime import datetime
import requests

# Dynamically add skill directory to Python path (ensures runnable in any working directory)
_skill_dir = os.path.join(os.getcwd(), '.cursor', 'skills', '0kidswear-photography-master-C')
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)
from generate_image import image_gen_sync

# Create save folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_dir = os.path.join(os.getcwd(), 'generated_photos', timestamp)
os.makedirs(save_dir, exist_ok=True)

def download_image(url, save_path):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")

# Shot 1 generation (pass garment image)
shot1_urls = image_gen_sync(
    prompt=shot1_prompt, img_urls=[garment_url],
    ratio="3:4", image_size="4K", pic_num=1
)
model_reference_url = shot1_urls[0]  # Save as model reference for subsequent Shots

# Shot 2-5 generation (pass garment image + model reference image to ensure model consistency)
shot2_urls = image_gen_sync(
    prompt=shot2_prompt, img_urls=[garment_url, model_reference_url],
    ratio="3:4", image_size="4K", pic_num=1
)
```

> ⚠️ **During actual image generation, you must read [EXAMPLES.md](EXAMPLES.md)**, copy the corresponding template, and run it after modifying the following six key variables:
> 1. `model_gender` ← Fill with `"boy"` or `"girl"` based on user selection
> 2. `model_race` ← Fill with `"asian"` or `"european"` based on user selection
> 3. `age_group` ← Fill with `"3-6"` / `"6-10"` / `"10-14"` based on user selection
> 4. `scene_type` ← Fill based on user selection, e.g., `"garden_setting"` (Check "12 Scenes Overview" table)
> 5. `garment_url` ← Replace with the actual white-background garment image URL
> 6. `garment_type` ← **Fill based on the white-background image analysis result** (Must be judged accurately):
>    - `"upper_body"` → Top (T-shirt/hoodie/jacket/shirt, etc.)
>    - `"lower_body"` → Bottom (pants/skirt/shorts, etc.)
>    - `"full_outfit"` → Complete outfit (matching top and bottom)
>    - `"dress"` → Dress/romper
>
> `garment_type` determines: styling matching direction, focus of Shot 4/5 close-ups, and matched garment prompt content. **Must be filled correctly, otherwise the entire stylist system fails**.
>
> If the garment type is not "sportswear" or "luxury jacket", you also need to read **[UNIFIED_PROMPT_BUILDER.md](UNIFIED_PROMPT_BUILDER.md)** to get the matching scene template.
>
> 💡 Optional Quality Check: Run `enforce_quality_check()` in `quality_check_system.py` to quality check the prompts and ensure all optimization requirements are implemented.
