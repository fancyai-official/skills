---
name: kidswear-photography-master
description: Professional kidswear photography generation system. Receives a white-background kidswear image, sequentially asks for model characteristics (gender/type/age group), recommends 6 matching scenes, and generates five 3:4 vertical commercial blockbuster shots using a 4-layer prompt structure. Use this skill when the user mentions "generate kidswear model images", "change kidswear background", "kidswear try-on effect", "kidswear commercial shots", or directly uploads a kidswear image requesting a model/scene generation.
---

# Kidswear Photography Master System

## Instructions

### Step 1: Intelligent Clothing Analysis & Scene Recommendation (Ask User)
When the user provides a white-background kidswear image, execute the following workflow:
1. **Intelligent Clothing Analysis (Background)**:
   - Automatically identify: category, style, brand tier, color, material, season.
   - Determine brand tone: luxury / fashion / mass-market / sports.
   - Identify `garment_type`: `upper_body`, `lower_body`, `full_outfit`, `dress`.
2. **Consolidated Parameter Confirmation (Ask Once)**:
   - After analyzing the white-background image, consult the "Scene Recommendation Mapping Table" below to select the 6 most suitable scenes.
   - Confirm all required parameters from the user in a single message:
     > Your clothing style is identified as [Insert Identified Style]. I recommend the following 6 most matching photography scenes for you:
     > - **A. [Scene Name in English]** — [1-sentence description, under 10 words]
     > - **B. [Scene Name in English]** — [1-sentence description]
     > ... (list all 6)
     >
     > To generate the perfect model images, please also let me know:
     > 1. Model Gender (Boy / Girl)
     > 2. Model Type (Asian / European)
     > 3. Age Group (3-6 years / 6-10 years / 10-14 years)
     > 
     > You can reply directly, for example: "Choose scene B, girl, Asian, 6-10 years."
   - Wait for the user's combined reply, record `scene_type`, gender, model type, and age group, then proceed directly to the image generation workflow.
   - > **Tip**: If the user already provided some or all of this information when uploading the image, use the provided info and only ask for the missing parts.

**Scene Recommendation Mapping Table:**
| Clothing Characteristics | Recommended 6 Scenes (Ordered by Priority) |
|---------|--------------------------|
| Luxury brands / High-end formal wear / Refined jackets | luxury_manor, garden_setting, cozy_home, vintage_train, resort_pool, wild_forest |
| Sportswear / Functional outdoor / Ball sports | sports_venue, farm_field, metro_adventure, cozy_home, wild_forest, beach_natural |
| Princess dresses / Gowns / Lace wear / Dresses | garden_setting, cozy_home, luxury_manor, farm_field, resort_pool, beach_natural |
| School uniforms / Preppy style / Plaid shirts | indoor_school, garden_setting, metro_adventure, cozy_home, farm_field, wild_forest |
| Casual wear / Hoodies / Daily outfits | cozy_home, metro_adventure, garden_setting, farm_field, wild_forest, beach_natural |
| Resort wear / Fresh summer / Beach style | beach_natural, resort_pool, garden_setting, farm_field, cozy_home, wild_forest |
| Streetwear / Cool outfits / Printed wear | sports_venue, metro_adventure, cozy_home, farm_field, garden_setting, wild_forest |
| Winter wear / Thick coats / Ski suits | snow_mountain, cozy_home, metro_adventure, farm_field, wild_forest, luxury_manor |

**12 Scenes Overview (For User Display):**
> When the Agent generates images, the `narrative_theme` and all `Scene framing` MUST match the user's selected `scene_type`, fetching values directly from this table to inject into the code.

| scene_type | Name | Short Description | narrative_theme (Injected into Code) |
|-----------|--------|----------|--------------------------------------|
| luxury_manor | Luxury Manor | European manor, classic sports car, manicured lawn | Luxury kidswear editorial, European manor weekend lifestyle |
| sports_venue | Sports Venue | Blue hard court, net fencing, athletic vibe | Youth sports fashion, vibrant outdoor hard court lifestyle |
| garden_setting | Garden Setting | Deep green cypress wall / Floral bench / Rose arch (Randomized) | Direction A → `European manor garden editorial, deep green botanical backdrop lifestyle` / Direction B → `French dramatic garden editorial, abundant blooming flowers lifestyle` / Direction C → `Dreamy kidswear editorial, romantic flower garden lifestyle` |
| resort_pool | Resort Pool | Blue pool, palm trees, luxury resort hotel | Summer resort kidswear editorial, luxury poolside lifestyle |
| beach_natural | Natural Beach | Ocean waves, sandy beach, coastal rocks | Natural beach kidswear editorial, coastal lifestyle |
| indoor_school | Indoor School | Studio preppy style, props set, editorial vibe | School life kidswear editorial, minimal indoor studio academic lifestyle |
| cozy_home | Cozy Home | Modern home / Bright window / European vintage study (Randomized) | Style A → `Cozy home kidswear editorial, warm interior lifestyle` / Style B → `Cozy home kidswear editorial, bright window-side natural light lifestyle` / Style C → `Cozy home kidswear editorial, European vintage home interior lifestyle, refined Old Money aesthetic` |
| wild_forest | Wild Forest | Forest path, tree canopy, green bushes | Wild forest kidswear editorial, outdoor nature lifestyle |
| farm_field | Farm Field | Barn wheat field / Bamboo fence (Randomized) | Style A → `Farm field kidswear editorial, countryside lifestyle` / Style B → `Asian pastoral farm editorial, bamboo fence countryside lifestyle` |
| snow_mountain | Snow Mountain | Snow slope, mountain ridge, ski lift | Snow mountain kidswear editorial, alpine lifestyle |
| vintage_train | Vintage Train | Classic train, platform, brass-accented carriage | Vintage train kidswear editorial, nostalgic travel lifestyle |
| metro_adventure | Metro Adventure | Showa cream carriage, warm lighting, round handles (Randomized) | Style A/B → `Retro metro adventure, urban subway car lifestyle, city childhood explorer journey` / Style C → `Showa-era retro metro adventure, warm vintage subway interior lifestyle` |

### Step 2: Confirm Fashion Stylist Matching
Read `references/FASHION_STYLIST.md` to execute outfit styling:
- `upper_body` → Keep the top, match with stylish bottoms + footwear for the model.
- `lower_body` → Keep the bottom, match with a stylish top + footwear for the model.
- `full_outfit` / `dress` → Keep the full outfit, match with footwear only.
- **STRICTLY PROHIBITED**: Skinny jeans, basic white tees, and other un-designed basic items.

### Step 3: Automatically Configure Generation Parameters
- **Model Gender**: Based on user selection (boy / girl). Do not auto-infer.
- **Model Type**: Based on user selection (asian / european). Do not auto-infer.
- **Model Age**: Dynamically configured based on the user's selected age group.
- **Photography Scene**: Based on user confirmation (`scene_type`).
- **Generation Model**: Uniformly use `image_gen_sync`.
- **Expression Style**: Auto-matched based on clothing type:
  - Luxury / Formal: serious calm, composed confidence
  - Sportswear: focused determination, energetic vitality
  - Princess Dress: gentle sweetness, dreamy elegance
  - Casual Wear: bright cheerful smile, relaxed ease
  - Streetwear: cool edgy vibe, confident swagger

### Step 4: Construct 4-Layer Precise Prompts
> 🛑 **System-Level Failsafe Directives**:
> - During the parameter collection and user questioning phase, **STRICTLY PROHIBITED** from reading any other Markdown files.
> - Upon receiving the complete user selection and preparing to construct prompts, you **MUST ONLY** read `references/SCENE_FRAMING_RULES.md` to obtain the 5 camera angles for the current scene.
> - When preparing to generate code (constructing prompts and API calls), the Agent **MUST** use the `Read` tool to read `references/UNIFIED_PROMPT_BUILDER.md` to obtain the full model feature description templates and the image generation boilerplate code.

All scenes use the identical 4-layer structure:
1. Layer 1: Narrative theme (includes simple scene description)
2. Layer 2: Subject persona (Scene framing, gender, model type, age group, pose description, expression description)
3. Layer 3: Outfit styling (includes clothing reference image, fashion matching suggestions, excludes bags/accessories)
4. Layer 4: Style reference (Photography style / Brand tone / Visual references)

### Step 5: Validate Core Requirements (Commercial Editorial Standard)
This system generates **commercial fashion editorials**, not daily snapshots:
- ✅ Every pose is **choreographed**
- ✅ Every expression is **designed**
- ✅ Capture the **peak moment**, NOT blurry action
- ✅ **Commercial editorial style**, NOT family snapshot
- ✅ Shot 2 Dynamic Moment: Both feet on the ground in a power pose, **NOT jumping off the ground**
> For detailed standards, refer to: `references/COMMERCIAL_PHOTOGRAPHY_STANDARDS.md`
> **Code Execution Tip**: Before running the image generation code, it is recommended to call `scripts/quality_check_system.py` to verify if the prompts meet all optimization requirements.

### Step 6: Generate Five 3:4 Vertical Images
Execute image generation, each must use a different scene perspective:
- Shot 1: Full-body standard standing pose + **Main Scene Perspective** (Frontal wide shot, iconic background element centered)
- Shot 2: Dynamic moment freeze (Both feet grounded, NOT jumping) + **Side-Line/Corner Perspective** (Diagonal framing, different background elements)
- Shot 3: Side profile clothing display + **Diagonal Turning Corner Perspective** (45-degree angle, another set of background elements)
- Shot 4: 3/4 body detail close-up + **Close-Up Extremely Shallow Depth of Field** (Background blurred into color bokeh, focus on clothing)
  - `upper_body` → Top fabric / brand elements / design details
  - `lower_body` → Bottom silhouette / waistband / fabric details
  - `dress`/`full_outfit` → Overall silhouette and most distinctive parts
- Shot 5: Half-body clothing close-up + **Core Scene Element** (Different position from Shot 1, central/distant landmark)
  - `upper_body` → Top neckline / cuffs / pattern texture
  - `lower_body` → Bottom pant legs / hem / pocket details
  - `dress`/`full_outfit` → Overall texture and design focus

> ⚠️ Mandatory Background Differentiation Rule: The 5 images MUST use 5 different camera and background combinations. No two images are allowed to have the same background. The `Scene framing:` paragraph MUST be added at the beginning of the [Layer 2: Subject persona] in each prompt.

## Examples

**Example 1: Generating a Princess Dress Model Image**
User says: "I want to generate a model image for this girl's princess dress" (and uploads a white-background image)
Actions:
1. Intelligently analyze the clothing as a princess dress, provide the 6 most matching scene options, and ask for gender, model type, and age group.
2. User replies: "Choose garden setting, girl, European, 6-10 years"
3. Read `references/SCENE_FRAMING_RULES.md` and `references/UNIFIED_PROMPT_BUILDER.md`.
4. Construct 4-layer prompts, and call the image generation model to generate five 3:4 vertical images in the `garden_setting` scene with different camera angle combinations.
Result: Outputs 5 kidswear model images meeting commercial editorial standards.

## Troubleshooting

- **Error: Generates casual daily snapshots instead of commercial editorials**
  - **Cause**: Used casual poses or laughing expressions, lacking a choreographed commercial feel.
  - **Solution**: Ensure every pose is carefully choreographed (designed naturalness), every expression has a designed feel (designed smile), captures the best moment (peak moment freeze), and read `references/COMMERCIAL_PHOTOGRAPHY_STANDARDS.md` for correction.
- **Error: Model is jumping, both feet off the ground**
  - **Cause**: Shot 2's pose prompt includes jumping.
  - **Solution**: Force Shot 2 pose to have both feet grounded in a power pose (NOT jumping off the ground).
- **Error: Background is repetitive or identical across images**
  - **Cause**: Did not add `Scene framing:` to Layer 2 Subject Persona or all images used the identical background description.
  - **Solution**: Select 5 different perspective descriptions for the corresponding scene_type from `references/SCENE_FRAMING_RULES.md`.

## Deep Learning & Support Documentation

All detailed reference materials have been moved to the `references/` directory. The system will load these files using the `Read` tool when needed (This utilizes the Progressive Disclosure principle, reducing unnecessary context overhead):
- Prompt Construction Logic → `references/UNIFIED_PROMPT_BUILDER.md`
- Specific Configuration Examples → `references/PROMPT_CONFIGURATIONS.md`
- Expression Selection → `references/EXPRESSION_GUIDE.md`
- Commercial Editorial Standards → `references/COMMERCIAL_PHOTOGRAPHY_STANDARDS.md`
- Complete Runnable Code Templates → `references/EXAMPLES.md`
- Reference Cases → `references/REFERENCES.md`
- Fashion Styling Rules & Banned List → `references/FASHION_STYLIST.md`
- Asian Child Model Facial DNA Reference → `references/ASIAN_MODEL_DNA.md`
- Automatic Quality Check System → `scripts/quality_check_system.py`
