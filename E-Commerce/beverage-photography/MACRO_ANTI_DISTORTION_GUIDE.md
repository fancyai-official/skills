# Macro Close-up Anti-Distortion Technical Guide

## Problem Statement

**User feedback**: In the Rio product's Scene 3 (Macro Close-up), the product appeared severely distorted.

**Root cause**: Using a macro lens to do an extreme close-up of the entire product causes perspective distortion, making the bottle or can appear stretched, warped, or disproportionate.

## Error Case Analysis

### ❌ Error 1: Using the Entire Product as Macro Subject
```
Prompt: "Macro extreme close-up of [Product] bottle"
```
**Result**: Bottle body stretched or widened, label distorted, brand logo deformed — unacceptable.

### ❌ Error 2: Near-Distance Shot of Entire Product
```
Prompt: "Extreme close-up shot of entire [Product] can"
```
**Result**: Exaggerated can perspective, top-to-bottom proportion distorted, product unrecognizable.

### ❌ Error 3: Macro Focus on Label or Bottle Cap
```
Prompt: "Macro focus on [Product] label and cap"
```
**Result**: Label text distorted, bottle cap warped, product detail inaccurate.

## Correct Approach

### ✅ Core Principle: Macro Shoots the Detail — Product Stays in Background

**Key thinking**:
- **Macro subject**: Local detail (condensation, bubbles, texture)
- **Product position**: Mid-ground or background, presented fully and sharply
- **Depth of field control**: Shallow DOF highlights detail, but product remains clearly recognizable

### ✅ Correct Approach 1: Macro on Surface Water Droplets

```
Prompt: 
Macro commercial photography: [Product] with extreme focus on surface condensation.

COMPOSITION:
- Foreground (macro focus): Condensation droplets on bottle surface (0.5-2mm water beads), 
  extreme close-up of micro droplets with crystal-clear details
- Mid-ground: [Product] bottle clearly visible, perfect shape, label readable, 
  no distortion, sharp and recognizable
- Background: Soft bokeh with [aesthetic style colors]

TECHNICAL:
- Macro lens focus distance: 10-15cm from droplet surface
- Product distance: 30-50cm from camera (normal perspective)
- Shallow depth of field (f/2.8-f/4)
- Product remains in acceptable focus zone

AVOID: extreme close-up of entire bottle, product warping, label distortion
```

**Effect**: Foreground droplets ultra-sharp (macro), product in mid-ground perfectly rendered (no distortion).

### ✅ Correct Approach 2: Macro on In-Glass Bubbles

```
Prompt:
Macro commercial photography: Cocktail glass with [liquid] and extreme bubble detail.

COMPOSITION:
- Foreground (macro focus): Bubbles rising in liquid (1-3mm bubbles), 
  extreme close-up showing bubble texture, internal reflections, carbonation details
- Mid-ground: [Product] bottle/can clearly visible beside glass, 
  perfect proportions, label sharp, brand recognizable
- Background: [Aesthetic style backdrop - blurred/architectural/dramatic as chosen]

TECHNICAL:
- Macro focus on liquid bubbles in glass (15-20cm from camera)
- Product placement: 40-60cm from camera (safe distance, no distortion)
- Depth of field: f/4-f/5.6 (bubbles sharp, product acceptably sharp)

AVOID: macro of product itself, ensure product maintains correct shape and scale
```

**Effect**: In-glass bubbles captured in fine detail (macro), product bottle fully and beautifully presented (no distortion).

### ✅ Correct Approach 3: Macro on Ice Cube Texture

```
Prompt:
Macro commercial photography: Ice cube with internal crystal structure.

COMPOSITION:
- Foreground (macro focus): Ice cube with visible internal cracks and frost texture,
  extreme close-up showing crystal patterns (macro at 8-12cm)
- Mid-ground: [Product] clearly visible in perfect condition, 
  bottle/can shape accurate, label text readable
- Background: [Aesthetic style environment]

TECHNICAL:
- Macro subject: ice cube (close-up reveals crystal structure)
- Product: placed at safe distance (35-50cm), normal lens perspective
- Lighting: backlight through ice for translucent effect

AVOID: product in macro range, keep product at normal shooting distance
```

**Effect**: Ice cube internal structure sharp (macro), product shape standard (no distortion).

## Universal Macro Anti-Distortion Prompt Template

```
Macro commercial photography: [Product] with extreme detail on [micro subject].

⚠️ CRITICAL COMPOSITION RULE:
- MACRO FOCUS: [Specific detail] (condensation/bubbles/ice/texture) - extreme close-up
- PRODUCT PLACEMENT: [Product] clearly visible in mid-ground/background, 
  perfect shape, no distortion, label readable, brand recognizable

FOREGROUND (pin-sharp macro):
[Detailed description of micro subject - e.g., "0.5-2mm water droplets on surface, 
crystalline clarity, light refraction visible"]

MID-GROUND (sharp, undistorted):
[Product] bottle/can in perfect condition, correct proportions, label text clear

BACKGROUND:
[Aesthetic style backdrop - soft bokeh/architectural/dramatic/minimal as chosen]

TECHNICAL NOTES:
- Macro lens on [micro subject] at 8-15cm
- Product at 30-60cm (normal perspective distance)
- Depth of field: f/2.8-f/5.6 (macro sharp, product acceptably sharp)

AESTHETIC STYLE: [selected aesthetic style - Soft Natural / High-Saturation Architectural / etc.]

AVOID: 
❌ extreme close-up of entire bottle/can
❌ macro of product label or cap
❌ product as macro subject (causes distortion)

✅ ENSURE: Product remains recognizable, undistorted, professional presentation
```

## Technical Explanation

### Why Does Distortion Occur?

1. **Perspective exaggeration**: Macro lens is very close to subject (5–15cm), greatly amplifying perspective effect
2. **Distortion**: Wide-angle-like spatial compression — near end enlarged, far end shrunk
3. **Extremely shallow DOF**: At f/2.8–f/4, only a few centimeters in front-back are sharp; if product is within macro range, it will be partially blurred AND distorted

### How to Avoid It?

1. **Separate shooting subjects**:
   - Macro subject: small detail (droplets, bubbles, texture) — distance 5–15cm
   - Product subject: complete product — distance 30–60cm (normal shooting distance)

2. **Depth of field control**:
   - Use f/4–f/5.6 rather than f/1.8 (stop down slightly)
   - Ensure product is within acceptable depth of field (slightly less sharp than macro subject, but shape is clear)

3. **Layered composition**:
   - Foreground: macro detail (pin-sharp)
   - Mid-ground: product (sharp and undistorted)
   - Background: environment (blurred or sharp, depending on aesthetic style)

## Key Phrases

### ✅ Recommended:

- "Macro focus on condensation droplets on surface, product clearly visible in background"
- "Extreme close-up of bubbles in glass, [Product] bottle sharp and recognizable behind"
- "Macro detail of ice crystals, product at safe distance with correct proportions"
- "Micro water beads on bottle surface (foreground), product label readable (mid-ground)"
- "Product clearly visible in perfect condition, no distortion, while macro focuses on [detail]"

### ❌ Avoid:

- "Extreme close-up of entire bottle"
- "Macro shot of [Product] can"
- "Close-up of product from very near"
- "Extreme close-up of bottle label"
- "Macro of bottle cap and top"

## Quality Checklist

After generating a Macro Close-up image, check:

- [ ] **Correct macro subject**: detail (droplets/bubbles/texture), NOT the entire product
- [ ] **Product shape is standard**: bottle/can proportions correct, no stretching or compression
- [ ] **Label clearly readable**: brand logo recognizable, text not distorted
- [ ] **Natural perspective**: product presentation follows normal viewing angle, no exaggerated perspective
- [ ] **Clear depth layers**: Foreground (macro) → Mid-ground (product) → Background (environment)

## Case Comparison

### Successful Case Characteristics

- ✅ Ultra-sharp macro detail in foreground (visual attraction)
- ✅ Product perfectly presented in mid-ground (brand recognition)
- ✅ Overall image has depth-of-field layering (professional photography quality)
- ✅ Product has zero distortion (commercially usable)

### Failed Case Characteristics

- ❌ Product fills entire frame and macro-zoomed (perspective distortion)
- ❌ Bottle/can body disproportionate (unrecognizable)
- ❌ Label distorted (brand damage)
- ❌ No foreground macro detail (not a real macro shot)

## Summary

**Correct understanding of Macro Close-up**:
- NOT "shoot the product very close up"
- But "shoot the microscopic detail associated with the product, while the product itself is presented at standard size"

**Execution Points**:
1. Define the macro subject clearly (droplets, bubbles, ice crystals, texture)
2. Keep product at safe distance (30–60cm, normal perspective)
3. Describe each layer explicitly in the Prompt
4. Emphasize "no distortion, perfect shape, label readable"
5. Check product shape and proportions after generation

**Avoid These Mistakes**:
- Never let AI treat the entire product as the "macro subject"
- Never use "extreme close-up of entire bottle/can"
- Always include "product at safe distance, no distortion" in the Prompt
