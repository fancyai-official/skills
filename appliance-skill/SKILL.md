---
name: appliance-skill
description: Analyzes small appliance product features and generates high-end commercial photography. Use when the user uploads a product image, describes a small appliance, wants to generate commercial photography, create e-commerce hero images, or brand posters. Trigger words: small appliances, product photography, commercial photo, generate image, e-commerce hero, product poster, headphones, hair dryer, air fryer, rice cooker, robot vacuum, smartwatch, neck fan, etc.
---

# Small Appliance Commercial Photography Skill

## When to Use

When the user uploads a product image or describes a small appliance and wants to generate commercial photography, e-commerce hero images, or brand posters, **immediately** execute the following four steps without waiting for further instructions.

---

## Four-Step Execution Flow

### Step 1: Product Feature Analysis

Read the product image or description and extract the following:

| Dimension | Extract |
|---|---|
| **Product Category** | Headphones / Hair Dryer / Air Fryer / Robot Vacuum / Smartwatch / Neck Fan / etc. |
| **Primary Material** | Matte plastic / Mirror metal / Painted / Frosted / Leather / Transparent |
| **Main Color** | Black / White / Silver / Gold / Orange / Red / Colorful |
| **Product Form** | Rounded / Angular / Slender / Flat / O-shaped / U-shaped / Composite |
| **Key Selling Point** | Noise cancellation / Waterproof / Lightweight / Smart / High power / Portable / etc. |
| **Target User** | Tech-savvy male / Sophisticated female / Homemaker / Athlete / Business professional / etc. |

### Step 2: Style Selection

**Before selecting a style, you MUST first use the Read tool to read `/Users/liujunhong/Desktop/appliance-skill-2/appliance-skill/product-profiles.md`, find the entry for the current product category, and extract: forbidden styles, composition recommendations, and material rendering focus.**

Based on the product category and selling points, select 1–2 best-matching styles from the following 14:

| Style Code | Style Name | Best For | Core Visual |
|---|---|---|---|
| `DARK` | Extreme Dark Tone | Black tech products, headphones, speakers | Pure black BG + cold white spotlight, Dyson-style |
| `WAVE` | Sound Wave / Airflow Visualization | Headphones, speakers, air purifiers, fans | Physical effect light surrounding product |
| `SPLASH` | Frozen Water Splash Waterproof | Headphones, sports gear, kitchen appliances | Water crown + IPX waterproof theme |
| `WHITE` | Pure White Minimalist E-commerce | All product categories | White BG three-point light, Apple-style |
| `SCENE` | Lifestyle Outdoor Aesthetics | Kitchen appliances, home devices, beauty devices | Outdoor natural scene + product as hero |
| `COSMOS` | Cosmic / Epic Natural Scene | High-end flagship products, launch key visuals | Cosmos / snow mountain / canyon dwarfing the product |
| `TECH` | AI Tech Futuristic | Smart devices, robots, robot vacuums | Blue AI particles + data streams |
| `STONE` | Rock / Natural Setting | Phones, mid-to-high-end appliances, watches | Product on rock, warm orange background |
| `COLOR_ECHO` | Color Echo / Brand Color Universe | Any product with a distinct brand color | Product color = background color family, material contrast creates texture |
| `LIFESTYLE` | Partial Human Interaction | Headphones, watches, beauty devices, handheld | Hands/ears/wrists in frame, no face, conveys usage experience |
| `PORTAL` | Ring / Frame Stage Effect | Purifiers, headphones, speakers, vertical/round products | Product framed by glowing ring, alternate world visible inside |
| `EXPLOSION` | Dynamic Explosive Power | Sports headphones, shavers, flagship vacuums, watches | Product static at explosion/shatter center, extreme performance feel |
| `MATERIAL_SCENE` | Material-Echo Outdoor Setting | Flagship products emphasizing material/craft | Product among same-material props, reinforcing texture perception |
| `FLAT_CONTEXT` | Overhead Lifestyle Story | Headphones, portable devices, phone accessories | Top-down product + lifestyle props, telling target user's lifestyle |

**Style Selection Logic:**
- Black product → Prioritize `DARK` or `WAVE`
- White / colorful product → Prioritize `WHITE` or `SCENE`
- Distinct brand color (red / orange / green) → Prioritize `COLOR_ECHO`
- Waterproof selling point → Must use `SPLASH`
- Smart / AI selling point → Prioritize `TECH`
- High-end launch key visual → Prioritize `COSMOS` or `PORTAL`
- Kitchen appliances → Prioritize `SCENE` or `STONE`
- Wearable products (headphones / watch / neck fan) → Consider `LIFESTYLE`
- Flagship performance product → Consider `EXPLOSION`
- Portable accessories → Consider `FLAT_CONTEXT`
- O-shaped / round products (neck AC / bladeless fan / purifier) → Consider `PORTAL`

### Step 3: Prompt Generation

**Must execute the following two reads in order before assembling the prompt:**

1. **Use the Read tool to read `/Users/liujunhong/Desktop/appliance-skill-2/appliance-skill/reference-analysis.md`**, find the visual formula best matching the selected style, and extract its English quick-imitation prompt as the base framework.
2. **Use the Read tool to read `/Users/liujunhong/Desktop/appliance-skill-2/appliance-skill/prompt-templates.md`**, find the six-layer structure template for the selected style code, and fill in the product info from Step 1 (product name / main color / material) into the placeholders.

Assemble the final prompt using the **six-layer structure**:

```
[Subject] + [Background/Environment] + [Lighting] + [Material] + [Composition] + [Technical Specs]
```

The generated prompt must include:
- Precise English product name
- Core visual elements of the selected style
- Material description (matching the material extracted in Step 1)
- Compositional tension (floating, diagonal angle, depth-of-field layers)

**[Composition Independence Principle]**: Only learn the lighting direction, material expression, and scene atmosphere from reference images. The composition / angle / product placement must be completely redesigned — never copy the reference image layout.

**[Mandatory Outdoor Principle]**: All generated images must use outdoor natural environment backgrounds.
- Valid scenes: snow / snowy rocks / desert / canyon / basalt platform / mountain / lava plains / coastal reef / starry sky water island / sand zen / wilderness glacier / water ripple ice field
- Strictly forbidden indoor scene words: kitchen, bedroom, bathroom, studio, tabletop, living room, countertop, interior, marble counter, wooden table, desk, dining room
- Even for kitchen appliances (rice cooker / air fryer / coffee maker), KV hero images must use grand outdoor natural scenes

**[Mandatory Layer 7 — Quality Foundation Layer]**
After assembling the six-layer structure, append the following keywords verbatim — do not omit:

```
Unreal Engine 5 Octane render style, hyperrealistic 3D CGI commercial product visualization, every physical detail of the product precisely rendered including buttons textures logos and surface grain, ambient occlusion, product casting realistic soft shadow on surface, subtle environmental light reflections and catchlights on product body, cinematic shallow depth of field with razor-sharp product and gently blurred background, volumetric atmospheric haze in the scene, seamlessly integrated product no floating pasted-on look, 8K resolution ultra-detail, award-winning commercial photography, no text no watermarks
```

### Step 4: Execute Image Generation

**Use the GenerateImage tool** with the full English prompt from Step 3 as the `description`. If the user provided a product reference image, pass its local path in `reference_image_paths` (array) so generation can follow product form and details. Match aspect intent to the deliverable: `1:1` for square hero stills, `9:16` for portrait, `16:9` for landscape, when the tool or workflow supports ratio selection; otherwise state the intended ratio in the description.

**Parameter notes:**
- `description` — Complete English prompt from Step 3
- `reference_image_paths` — When the user uploaded a product image, include its absolute file path; omit or leave empty if there is no reference
- If image generation via tool is not available, output the final prompt and tell the user to run it in their own image API or app

After generation, proactively provide:
- The style used and the reason (1–2 sentences)
- 2–3 directions to explore further

---

## Quick Reference: Best Styles by Product Category

Full profiles (including forbidden styles / composition / material focus) must be retrieved in Step 2 via the Read tool from `product-profiles.md`; reference visual formulas must be retrieved in Step 3 via the Read tool from `reference-analysis.md`. The following is a quick index:

| Product | Primary Styles | Extended Recommendations |
|---|---|---|
| TWS Wireless Earbuds | `DARK` `WAVE` `SPLASH` | `PORTAL` `LIFESTYLE` `FLAT_CONTEXT` |
| Over-ear Headphones | `DARK` `COSMOS` `STONE` | `COLOR_ECHO` `LIFESTYLE` `MATERIAL_SCENE` |
| Hair Dryer | `DARK` `WAVE` `WHITE` | `COLOR_ECHO` `LIFESTYLE` |
| Air Fryer | `SCENE` `STONE` `WHITE` | `MATERIAL_SCENE` `FLAT_CONTEXT` |
| Robot Vacuum | `TECH` `DARK` `SCENE` | `PORTAL` `EXPLOSION` |
| Electric Fan / Bladeless Fan | `WAVE` `COSMOS` `DARK` | `PORTAL` `COLOR_ECHO` |
| Air Purifier | `WAVE` `TECH` `WHITE` | `PORTAL` `COSMOS` |
| Rice Cooker | `SCENE` `STONE` `WHITE` | `MATERIAL_SCENE` `FLAT_CONTEXT` |
| Beauty Device / Shaver | `SCENE` `WHITE` `TECH` | `COLOR_ECHO` `LIFESTYLE` `EXPLOSION` |
| Smart Speaker | `DARK` `TECH` `WAVE` | `PORTAL` `COSMOS` |
| Neck Fan / Neck AC | `SCENE` `STONE` `DARK` | `PORTAL` `LIFESTYLE` `COLOR_ECHO` |
| Smartwatch / Smart Band | `DARK` `STONE` `COSMOS` | `EXPLOSION` `COLOR_ECHO` `LIFESTYLE` |

---

## Output Format

After each image generation task, output:

1. **Product Analysis Summary** (3–5 lines)
2. **Style Used and Reason** (1–2 sentences)
3. **Generated Image** (result from the image generation step — URL, file path, or embedded asset)
4. **Directions to Explore Further** (2–3 alternatives)

---

## Additional Resources

- Detailed product-to-style mapping: [product-profiles.md](product-profiles.md)
- Full prompt template library (14 styles, six-layer structure): [prompt-templates.md](prompt-templates.md)
- 57 reference image classified index and imitation prompts: [reference-analysis.md](reference-analysis.md)
