# Usage Examples

This document demonstrates how to use the beverage commercial photography skill.

## ⚠️ Important: Product Image Requirements

### Correct Product Images

Users must provide a **clean product image**:
- ✅ White or simple solid color background
- ✅ Product clearly and fully visible
- ✅ No complex scene elements
- ✅ E-commerce product photos or official product shots are fine

### Incorrect Input

❌ **Do NOT use**:
- Complete scene images from the reference library
- Images that already contain creative staging
- Marketing images with complex backgrounds

### Why Use a Clean Product Image?

**Reason**: AI needs to plan scenes creatively from a clean product image — not imitate existing scenes.

**Correct use of reference cases**:
- Learn lighting techniques
- Learn composition principles
- Learn color matching
- NOT as generation input

---

## Quick Start

### Example 1: Whiskey Product Shoot

**User Input**
```
Help me shoot a commercial photo set for this whiskey bottle
[attached product image: clean product shot on white or simple background]
```

**AI Workflow**

**1. Product Analysis**
```
Product type: Whiskey (spirits)
Liquid color: Amber
Packaging style: Luxurious, premium
Bottle design: Glass bottle, refined label
Brand positioning: High-end luxury
Target scene: Bar, premium club
```

**2. Scene Planning**
5 styles selected:
1. Still Life Atmosphere (lead) — warm bar scene
2. Dynamic Splash — ice cube splash
3. Macro Close-up — liquid detail
4. Lifestyle Narrative — fireside enjoyment
5. Creative Concept — metallic geometric space

**3. Generate Images**

Call the `GenerateImage` tool for each scene:

```markdown
# Scene 1: Still Life Atmosphere
Description:
Atmospheric lifestyle beverage photography, premium whiskey bottle and glass 
on wooden bar counter, warm ambient lighting, soft bokeh background with 
blurred lights, shallow depth of field, golden hour glow, cozy bar atmosphere, 
professional product photography, amber liquid in glass, luxury setting, 
cinematic mood, high-end commercial shot, 16:9 ratio, 4K resolution.

Reference Image: [user's whiskey product image URL]
```

**4. Output**
```
✅ Scene 1/5: Still Life Atmosphere
Description: Warm bar environment, whiskey bottle and glass on wooden counter, bokeh effect
Image: [displayed via Read tool]

✅ Scene 2/5: Dynamic Splash
Description: Whiskey bottle and glass, ice cubes splashing, amber liquid, dark background
Image: [displayed via Read tool]

✅ Scene 3/5: Macro Close-up
Description: Extreme close-up of ice and whiskey liquid, crystalline texture
Image: [displayed via Read tool]

✅ Scene 4/5: Lifestyle Narrative
Description: Whiskey by fireplace, warm firelight, winter atmosphere
Image: [displayed via Read tool]

✅ Scene 5/5: Creative Concept
Description: Whiskey bottle in gold geometric framework, modern luxury expression
Image: [displayed via Read tool]
```

---

## Example 2: Cocktail Shoot

**User Input**
```
This is our new pink cocktail, need social media promotional images
[local image: /Users/mac/products/pink_cocktail.png]
```

**AI Workflow**

**1. Product Analysis**
```
Product type: Cocktail
Liquid color: Pink
Container: Cocktail glass
Brand positioning: Young, fashionable
Target scene: Social media, youth gatherings
```

**2. Scene Planning**
5 styles selected:
1. Macro Close-up (lead) — social media friendly
2. Dynamic Splash — pour moment
3. Creative Concept — gradient background
4. Lifestyle Narrative — party tabletop
5. Still Life Atmosphere — refined still life

**3. Generation Parameters**

```markdown
# Scene 1: Macro Close-up (portrait ratio for mobile)
Description:
Macro beverage photography, extreme close-up of pink cocktail, 
crystal clear ice cubes with pristine details, fresh berry garnish, 
tiny bubbles and condensation droplets, pink to purple gradient background, 
soft diffused lighting, shallow depth of field, ultra sharp focus on details, 
fresh and vibrant colors, commercial product photography, 3:4 vertical ratio, 4K resolution.

Reference Image: /Users/mac/products/pink_cocktail.png
```

---

## Example 3: Beer Summer Theme

**User Input**
```
Shoot our new craft beer, summer outdoor theme
[product image URL]
```

**Scene Planning**
1. Lifestyle Narrative (lead) — beach ice bucket
2. Macro Close-up — frost condensation
3. Dynamic Splash — foam explosion
4. Lifestyle Narrative — pool party
5. Creative Concept — cool blue vibes

**Ratio Selection**
- Scene 1: 16:9 landscape (outdoor scene showcase)
- Scenes 2–5: 3:4 portrait (standard set)

---

## Example 4: Premium Wine

**User Input**
```
This is an aged red wine, needs to convey history and quality
[product image]
```

**Scene Planning**
1. Still Life Atmosphere (lead) — wine cellar scene
2. Dynamic Splash — red wine liquid splash
3. Lifestyle Narrative — dinner table wine moment
4. Macro Close-up — wine texture
5. Creative Concept — mirror reflection

---

## Common Scene Combination Recommendations

### Social Media Promotion
- Macro Close-up + Creative Concept + Lifestyle Narrative
- Ratio: 3:4 portrait or 1:1 square
- Color: High saturation, gradient backgrounds

### E-commerce Product Page
- Still Life Atmosphere + Macro Close-up + Dynamic Splash
- Ratio: 1:1 square
- Focus: Product detail clarity

### Brand Image Campaign
- Still Life Atmosphere + Lifestyle Narrative + Creative Concept
- Ratio: 16:9 landscape
- Atmosphere: Premium, storytelling

### Seasonal Marketing
- Summer: Lifestyle Narrative (outdoor) + Macro Close-up (refreshing)
- Winter: Still Life Atmosphere (warm) + Lifestyle Narrative (home)
- Holiday: Creative Concept (festive elements) + Lifestyle Narrative (gathering)

---

## Advanced Tips

### 1. Reference Image Best Practices

**Single product image**
```python
img_urls=["product_image.jpg"]
```

**Multi-angle product images**
```python
# If multiple angles exist, choose the clearest one
img_urls=["product_front_view.jpg"]
```

### 2. Resolution Selection Guide

- **4K**: Ultra HD, print, large-format display (~10–15MB) **Recommended**
- **2K**: Web use, e-commerce detail pages (~2–5MB)
- **1K**: Quick preview, small social media images (~1–2MB)

### 3. Ratio Selection Strategy

- **1:1 square**: Instagram, product display, versatile
- **16:9 landscape**: Website banner, desktop display
- **3:4 portrait**: Mobile, vertical video cover, Stories (default)
- **9:16 portrait**: Full-screen mobile, reels

### 4. Model Selection

**GenerateImage Tool** (default — all jobs)
- Highest quality output
- Best for all commercial use
- Recommended for this skill

---

## Troubleshooting

### Issue 1: Generated image product not sharp enough

**Solutions**
- Add to prompt: `ultra sharp focus on product`, `product in sharp detail`
- Provide a higher-resolution reference image

### Issue 2: Scene style doesn't match expectation

**Solutions**
- Check if prompt includes the correct style keywords
- Reference the Prompt template in `PROMPT_GUIDE.md`
- Add more specific scene descriptions

### Issue 3: Generation timeout

**Solutions**
- Check network connection
- Increase `timeout` parameter: `timeout=260`
- Lower resolution: use `2K` instead of `4K`

### Issue 4: Local image upload failed

**Solutions**
- Confirm file path is correct
- Confirm file format is supported (jpg, png, etc.)
- Check file size (recommend <10MB)
- Switch to an image URL instead

---

## Best Practices Summary

1. **Provide a high-quality product image** — clear, well-lit, clean background
2. **Specify the use case** — inform AI of purpose (social media / e-commerce / print)
3. **Batch generate** — generate 5 different styles at once for selection
4. **Save your prompts** — record successful prompts for reuse
5. **Adjust ratio to fit final use** — choose ratio based on where the image will appear
6. **Default ratio** — Scene 1: 16:9, Scenes 2–5: 3:4

---

Ready to create stunning beverage commercial photography! 🍷
