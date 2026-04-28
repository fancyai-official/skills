# Product Animation Prompt Templates by Category

Each category provides: Recommended Animation Direction + Seedance English Template + Taboos

---

## 1. Clothing/Accessories

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Fabric Flowing | Dresses, silk, chiffon, thin tops |

### Seedance Prompt

**Fabric Flowing:**
```
A [dress/blouse/skirt] in [color] hanging in a minimal studio setting.
Warm diffused light filters through a half-open window from camera left,
casting soft directional shadows. Structured silhouette transitions to fluid drape
as the fabric moves with realistic weight and momentum. Slow dolly-in
emphasizing fabric weave and surface texture. Physically-based cloth simulation,
no fabric morphing. Fashion editorial aesthetic, Gucci-inspired cinematic quality,
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

### Kling Prompt (Model Wearing Showcase)

**Wearing & Walking:**
```
Minimal studio backdrop. Model in [color] [garment type], standing at rest.
Shot 1 (0-5s): Wide shot, slow dolly forward. Model walks naturally toward camera,
garment draping and swaying with each step. Soft diffused overhead light,
fashion editorial aesthetic.
Shot 2 (5-10s): Medium shot from side, model turns slowly in place. Fabric movement
catches the side-light from camera left, revealing texture and silhouette.
Cool neutral color grade.
No morphing clothes, no distorted proportions, no extra people, no flickering textures.
shot_type: customize, aspect_ratio: "9:16", resolution: "1080P"
```

### Taboos

- Avoid `multiple people` (easily generates extra characters)
- Avoid `fast motion` (fabric easily deforms)
- Avoid describing complex pattern details (easily ignored or changed)

---

## 2. Beauty/Skincare

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Liquid Flowing | Serums, lotions, foundation opening and pouring |
| Product Rotation | Bottle/packaging showcase, 360° turntable |

### Seedance Prompt

**Liquid Flowing:**
```
A [serum/essence/foundation] bottle on a smooth obsidian reflective surface.
The cap slowly opens and a single drop of [golden/pearl-white/clear] liquid
descends the side with realistic surface tension and gravity.
Shallow depth of field, soft backlight with subtle
chromatic aberration rim. Slow motion, luxury feel.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Product Rotation:**
```
A premium [skincare product name] bottle on a white velvet pedestal.
Soft key light from 45° above and camera left caresses the curved packaging,
creating refined specular highlights without overexposure. Smooth 180° clockwise orbit,
shallow depth of field. Close-up texture reveal showing
surface luminosity and material quality. Elegant and minimal,
La Mer editorial style. 4K, no text, no watermark,
no ghosting, temporal coherence, stabilized.
```

### Taboos

- Avoid `pouring large amount` (easily spills out of control)
- Avoid `hands` (hand movements easily deform)
- Avoid `open packaging` (packaging fonts are easily changed)

---

## 3. Food/Beverages

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Steam Rising | Hot drinks, soups, freshly baked food |
| Water Droplets/Condensation | Cold drinks, beer, bottled beverages |

### Seedance Prompt

**Steam Rising:**
```
A steaming [coffee/ramen/soup] in a bowl/cup on a dark stone surface.
Condensation droplets slowly form on the chilled exterior.
Gentle steam rising with realistic fluid simulation. Static macro shot
with slow-motion pour revealing liquid clarity and depth.
Warm amber volumetric side light, cozy premium atmosphere.
Nespresso-inspired editorial style.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Water Droplets/Cold Drink:**
```
A chilled [bottle/can] of [beverage name] on a dark wet reflective surface.
Condensation droplets slowly form and run down the bottle with realistic
surface tension and gravity. Cool dramatic rim lighting, slow dolly-in,
refreshing advertisement style. 4K, no text, no watermark,
no ghosting, temporal coherence, stabilized.
```

### Taboos

- Avoid `eating` (people in frame easily deform)
- Avoid `multiple ingredients falling` (too many elements cause chaos)
- Avoid overly describing brand logos (LOGO fonts will be modified)

---

## 4. Digital/3C

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Booth Rotation | Showcase of phones, earphones, watches, cameras, etc. |
| Light Effect Scan | Metallic products, showing material craftsmanship |

### Seedance Prompt

**Booth Rotation:**
```
A [product: smartphone/earbuds/smartwatch] on a matte black surface.
The product slowly emerges from darkness. Precise specular highlight traces
the chamfered edge as the camera performs a slow low-angle tilt up,
revealing the full form. Studio three-point lighting with hard shadow definition
on one side and soft fill on the other. No lens flare.
Apple-inspired minimalist precision aesthetic.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Light Effect Scan:**
```
A [metal/glass] [product name] on a dark surface. A soft light beam slowly
sweeps across the surface, revealing fine material texture and craftsmanship.
Physically accurate metal sheen, chromatic aberration rim on edges.
Dramatic studio lighting, slow dolly-in.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

### Taboos

- Avoid `screen showing content` (screen content easily shows gibberish)
- Avoid `unboxing` (multi-object interaction easily deforms)
- Avoid writing specific model numbers (AI might incorrectly render numbers)

---

## 5. Jewelry/Accessories

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Light Sparkling | Diamonds, crystals, gemstone accessories |
| Slow Motion Close-up | Showcase of rings, necklaces, bracelet details |

### Seedance Prompt

**Light Sparkling:**
```
A [diamond ring/crystal necklace/gemstone bracelet] resting on a cool gray gradient surface.
Single soft key light from 45° above and camera left.
All light originates from material surface reflection and ambient environment only.
The gemstone reveals its inner depth and quiet luminosity through the interplay
of ambient light and metal reflection — not from added sparkle or artificial effects.
Slow 180° clockwise orbit, shallow depth of field.
No artificial sparkle, no sudden light bursts, no added light rays,
no lens flare, no over-saturated reflections.
Tiffany-inspired high-end editorial style, restrained and material-honest.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Slow Motion Close-up:**
```
An extreme close-up of a [gold/silver/rose gold] [jewelry type] slowly rotating
on a black obsidian pedestal. Soft sweeping key light reveals fine engraving and
metal texture. Smooth 180° orbit, rack focus from overall form to detail.
Soft focused background, sharp foreground, jewelry catalog style.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

### Kling Prompt (Wearing Showcase)

**Hand Wearing Close-up:**
```
Dark velvet surface, single spotlight from above. A slender wrist enters frame from below.
Shot 1 (0-5s): Slow dolly forward, wrist moves toward camera wearing [ring/bracelet/necklace].
Side-light from camera left reveals metal texture and gem facets. Shallow depth of field.
Shot 2 (5-10s): Camera holds static. Wrist rotates slightly, jewelry catches the light
creating sparkle and refractive caustics. Macro close-up, luxury jewelry aesthetic.
No morphing jewelry, no extra hands, no color shifts, no flickering.
shot_type: customize, aspect_ratio: "9:16", resolution: "1080P"
```

### Taboos

- Avoid `multiple pieces` (multiple pieces of jewelry easily overlap and deform)
- Avoid `face` (faces have a high probability of appearing but are hard to control)
- Avoid `bright white background` (gemstone sparkles lack contrast on a white background)

---

## 6. Home/Furniture

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Product Rotation Showcase | Independent home items like chairs, lamps, ornaments |
| Material Light Effect | Texture showcase of wood grain, fabric, metal, glass, etc. |

### Seedance Prompt

**Product Rotation Showcase:**
```
A [furniture/home decor item] rests in a minimal interior setting.
Warm afternoon light enters from a window at camera left, casting long gentle
shadows across the surface. Camera performs a slow dolly toward the material
surface, revealing wood grain texture, fabric weave, or metal sheen in precise detail.
Smooth 270° clockwise orbit to complete the reveal.
Muji-inspired calm and honest aesthetic.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Material Light Effect:**
```
Close-up of a [wooden/fabric/metal] surface of a [product name].
A soft sweeping key light slowly moves across, revealing fine grain and texture detail.
Warm studio lighting with physically accurate material sheen.
Slow dolly-in, lifestyle photography style.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

### Kling Prompt (Lifestyle Scene Narrative)

**Home Scene Multi-shot:**
```
Warm minimalist living room, afternoon sunlight through sheer curtains.
Shot 1 (0-5s): Wide establishing shot. Camera performs very slow dolly right revealing
the [furniture/decor item] in foreground. Neutral earth-tone palette.
Warm side-light from camera left creating long gentle shadows.
Shot 2 (5-10s): Medium close-up, slow dolly forward toward the product. Material texture
becomes visible — wood grain, fabric weave, or metal sheen. Soft lifestyle photography aesthetic.
No people, no cluttered background, no distortion, no flickering light.
shot_type: customize, aspect_ratio: "16:9", resolution: "1080P"
```

### Taboos

- Avoid `person using` (human interaction actions have a high deformation rate)
- Avoid `multiple furniture pieces` (multiple pieces of furniture in the same frame easily cause chaos)
- Avoid describing complex interior furnishings (too many background elements steal the show)

---

## 7. Pet Supplies

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Product Close-up Rotation | Packaging showcase of pet snacks, toys, supplies |
| Texture Close-up | Soft materials like pet beds, plush toys |

### Seedance Prompt

**Product Close-up Rotation:**
```
A [pet product: toy/treat bag/accessory] centered on a clean white or light gray background.
Soft even three-point lighting with no harsh shadows, building a sense of trust and clarity.
Steady composed framing with a slow 360° orbit showing all sides clearly.
Clean, approachable, and reliable aesthetic. Royal Canin-inspired product-first style.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Texture Close-up:**
```
Extreme close-up of a soft [plush/fabric] [pet bed/toy].
Slow dolly-in, revealing fluffy texture and fine stitching detail.
Soft sweeping key light from the side, warm diffused fill light.
Cozy and gentle atmosphere. 4K, no text, no watermark,
no ghosting, temporal coherence, stabilized.
```

### Taboos

- Avoid `real animal` (AI-generated pet actions are uncontrollable and easily deform)
- Avoid `pet playing with toy` (interaction actions between animals and objects have a high distortion rate)
- Avoid describing complex toy structural details (details are easily ignored or rendered incorrectly)

---

## 8. Maternity/Baby

### Recommended Animation Direction

| Direction | Applicable Scene |
|------|---------|
| Product Rotation Showcase | Packaging showcase of single items like bottles, strollers, toys |
| Material Sense of Security | Soft texture of cotton, silicone, soft materials |

### Seedance Prompt

**Product Rotation Showcase:**
```
A [baby product: bottle/toy/clothing] placed on a soft cream-white background.
Ultra-soft wrap-around fill light from all sides eliminates harsh shadows,
creating a gentle cotton-soft and pure atmosphere. Smooth 270° clockwise orbit,
very slow pace. Warm white color temperature, safe and tender feel.
Johnson & Johnson-inspired pure and caring aesthetic.
4K, no text, no watermark, no ghosting, temporal coherence, stabilized.
```

**Material Sense of Security:**
```
Close-up of a soft [cotton/silicone] [baby item].
Slow dolly-in, soft sweeping key light gently highlights the smooth
and safe texture. Warm pastel tones, minimalist background,
tender and caring atmosphere. 4K, no text, no watermark,
no ghosting, temporal coherence, stabilized.
```

### Taboos

- Avoid `baby` / `infant` / `child` (high risk of deformation when infants/toddlers are in frame)
- Avoid describing specific use actions (such as feeding, holding, and other human interactions)
- Avoid `bright saturated colors` (high saturation colors do not match the tone of maternity/baby products)
