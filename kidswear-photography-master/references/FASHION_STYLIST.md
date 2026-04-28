# Fashion Stylist System

> This file is read during "outfit styling" decisions. The stylist role is responsible for identifying the reference garment type and intelligently pairing it with a complete, fashionable, and trendy outfit.

---

## Stylist Philosophy

**Core Principle: The styling in kidswear editorials is not everyday wear; it is commercial fashion editorial styling.**

Every reference garment should be treated as a "hero piece". The rest of the outfit serves the hero piece, and the overall styling must:
- Have a sense of design, storytelling, and brand tone
- Align with current kidswear fashion trends (Minnow / Bonpoint / Jacadi / Zara Kids / H&M Kids editorial level)
- Be proportionally balanced: oversize tops with loose bottoms, fitted tops with wide-leg bottoms

---

## Step 1: Identify Garment Type (`garment_type`)

After receiving the white-background image, you must first determine:

```
garment_type:
  "upper_body"  → Top (T-shirt/hoodie/jacket/shirt/vest/polo/knit top, etc.)
  "lower_body"  → Bottom (Pants/shorts/skirt/midi skirt, etc.)
  "full_outfit" → Complete outfit (Matching top and bottom set)
  "dress"       → Dress/romper/jumper
```

---

## Step 2: Determine Styling Direction Based on Type

### Scenario A: Reference image is a top (`upper_body`)
→ Keep the reference top, **match with stylish bottoms + footwear**

### Scenario B: Reference image is a bottom (`lower_body`)
→ Keep the reference bottom, **match with a stylish top + footwear**

### Scenario C: Reference image is a full outfit or dress (`full_outfit` / `dress`)
→ Keep the complete reference outfit, **only match with footwear** (no additional top/bottom needed)

---

## Styling Rule Library

### A. Top → Match with Bottom

#### Sports / Street Style Top
- **Recommended Bottoms**:
  - Wide-leg cargo shorts in neutral tones (khaki, olive, black)
  - Balloon-fit track pants with elastic cuffs
  - Relaxed athletic shorts with side stripe detail
  - Wide-leg sweatpants in matching or tonal color
- **Footwear**: Chunky sneakers / high-top canvas sneakers / sporty slides
- **STRICTLY PROHIBITED**: Skinny jeans, tight denim, fitted leggings (too tight, too everyday)

#### Casual / Hoodie / Oversize Style Top
- **Recommended Bottoms**:
  - Wide-leg relaxed trousers in linen or cotton (neutrals: oat, ivory, khaki)
  - Paper-bag waist shorts with tie detail
  - Loose plaid wide-leg pants
  - Boxy bermuda shorts with clean silhouette
- **Footwear**: Chunky loafers / low-top vintage sneakers / mary jane flats
- **STRICTLY PROHIBITED**: Skinny jeans, tight leggings (ruins proportions)

#### Luxury / Refined / Formal Style Top
- **Recommended Bottoms**:
  - Tailored wide-leg trousers in cream, camel, or navy
  - A-line midi skirt in solid or subtle plaid
  - Pleated shorts with clean tailoring
  - Flowing midi skirt in soft fabric
- **Footwear**: Leather loafers / mary jane shoes / oxford shoes / white sneakers (clean minimal)
- **STRICTLY PROHIBITED**: Athletic shorts, ripped jeans, cargo pants (conflicting tone)

#### Princess / Sweet / Lace / Floral Style Top
- **Recommended Bottoms**:
  - Tulle puff skirt in matching or contrast pastel
  - Flowing pleated chiffon skirt
  - Tiered ruffle midi skirt
  - Layered organza skirt
- **Footwear**: Ballet flats / mary jane shoes with bow / delicate sandals
- **STRICTLY PROHIBITED**: Track pants, cargo shorts, athletic bottoms (style conflict)

#### Neutral / Oversize Jacket / Outerwear
- **Recommended Bottoms**:
  - Wide-leg relaxed shorts in matching tone
  - Straight-leg wide trousers
  - Mini pleated skirt for contrast
  - Loose bermuda shorts
- **Footwear**: Chunky sneakers / combat boots (mini) / platform loafers
- **STRICTLY PROHIBITED**: Skinny pants, fitted jeans

---

### B. Bottom → Match with Top

#### Wide-leg Pants / Cargo Pants / Palazzos
- **Recommended Tops**:
  - Cropped relaxed cotton tee (fitted at shoulder, short hem)
  - Oversized linen or cotton button-up shirt (tucked loosely or knotted)
  - Cropped knit sweater or pullover
  - Simple sleeveless tank or ribbed crop top
- **Footwear**: Chunky sneakers / loafers / platform sandals
- **Styling Logic**: Loose bottom → top needs a cinched waist or cropped length, avoid "loose all over"

#### Skirts (A-line / Pleated / Midi)
- **Recommended Tops**:
  - Oversized knit sweater or cardigan (casual volume on top)
  - Tucked-in linen button-up shirt
  - Fitted ribbed turtleneck or long-sleeve top
  - Short puff-sleeve blouse
- **Footwear**: Mary jane shoes / loafers / ankle strap sandals / chelsea boots
- **Styling Logic**: Skirts inherently have feminine lines; tops can have a bit of volume

#### Athletic Shorts / Track Bottoms
- **Recommended Tops**:
  - Cropped hoodie or zip-up sweatshirt
  - Sports tank top or athletic crop top
  - Lightweight bomber jacket
  - Oversized graphic tee (knotted at waist)
- **Footwear**: Athletic sneakers / high-top canvas shoes / sports slides
- **Styling Logic**: Keep sports style consistent, choose athletic tops

#### Long Skirts / Flowy Skirts
- **Recommended Tops**:
  - Fitted ribbed knit top or camisole
  - Simple cropped tee with clean neckline
  - Lightweight linen shirt (open or tucked)
  - Knit polo shirt
- **Footwear**: Strappy sandals / espadrilles / simple mules
- **Styling Logic**: Long skirts flow; tops need to be simple to avoid stealing the show

#### Mini Skirts / Short Skirts
- **Recommended Tops**:
  - Oversized graphic tee (tucked front, hem out)
  - Knit sweater vest over tee
  - Puff-sleeve blouse
  - Cropped denim jacket or light jacket
- **Footwear**: Mary janes / platform sneakers / knee-high socks + loafers
- **Styling Logic**: Mini skirts are playful; tops can be fun but avoid being too formal

---

## Shot 4 / Shot 5 Close-up Focus Rules

```
if garment_type == "upper_body":
    Shot 4 → 3/4 body framing, focusing on top fabric, brand elements, design details
    Shot 5 → Half-body close-up, overall top texture and neckline/cuff/pattern details

elif garment_type == "lower_body":
    Shot 4 → 3/4 body framing, focusing on bottom fabric, waistband, silhouette details
    Shot 5 → Half-body close-up, overall bottom texture and pant leg/hem/pocket details

elif garment_type == "dress":
    Shot 4 → 3/4 body framing, showing the most distinctive part of the dress (neckline/waist/hem)
    Shot 5 → Half-body close-up, overall dress texture

elif garment_type == "full_outfit":
    Shot 4 → 3/4 body framing, showing the most recognizable design elements of the set
    Shot 5 → Half-body close-up, overall set styling texture
```

---

## Fashion Styling Quick Lookup Table

| Reference Type | Example | Styling Direction | Prohibited |
|-----------|------|---------|------|
| Sports Hoodie (Top) | Basketball tee, hoodie | Wide-leg track pants / cargo shorts | Skinny jeans |
| Luxury Jacket (Top) | Bonpoint jacket | Tailored wide-leg trousers / A-line skirt | Athletic shorts |
| Wide-leg Pants (Bottom) | Cargo wide-leg pants | Cropped knit / loose linen shirt | Puffer jacket (too heavy) |
| Tutu Dress (Dress) | Tulle dress | Match with shoes only | Any extra tops (ruins the whole) |
| Sports Shorts (Bottom) | Basketball shorts | Crop hoodie / sports tank | Formal shirt |
| Pleated Midi Skirt (Bottom) | Plaid pleated skirt | Oversized knit / fitted ribbed top | Track pants on top |

---

## Stylist Precautions

1. **Age Appropriateness**: Kidswear styling cannot be overly mature. Avoid over-exposure or adultified proportions.
   - **Footwear Selection Must Fit Age**:
     - **3-6 years (Toddler)**: Emphasize easy wear and comfort/cuteness, e.g., velcro sneakers, soft strap leather shoes / mary janes.
     - **6-10 years (Little Kid)**: Standard child fashion styles, e.g., classic kids sneakers, slip-on flats.
     - **10-14 years (Big Kid)**: Close to adult fashion but retaining youthfulness, e.g., trendy chunky sneakers, classic loafers, lace-up oxfords.
   - **Poses and Gestures**: Never allow overly cool/adult poses like "hands in pockets" (for young children) unless it fits a specific casual editorial. Usually use naturally relaxed poses (hands naturally hanging, gently touching hem, etc.).
2. **Color Coordination**: Matched clothing colors should be harmonious with the reference garment (tonal/neutral/complementary), avoid overly strong color clashes.
3. **Seasonal Consistency**: Select matches based on the seasonal feel (fabric/color) of the reference garment.
4. **Brand Tone**: The perceived tier of matched clothing must match the reference garment (don't pair a luxury top with bottoms that look like mass-market items).
