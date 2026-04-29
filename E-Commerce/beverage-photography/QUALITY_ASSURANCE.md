# Quality Assurance & Verification System

## Core Quality Standards

Based on analysis of 90+ top photographer works, every generated image must meet the following standards:

### Must-Have Standards

**0. Originality** ⭐⭐⭐⭐⭐ 🆕
- Scene must be 100% original — do not imitate reference cases
- Planned from the user's clean product image
- Apply learned techniques but keep scenes unique
- Reference cases are for learning only, not for generation input

**1. Product Clarity** ⭐⭐⭐⭐⭐
- Product is clearly recognizable, not blurry
- Label / packaging details are visible
- Material texture feels real (glass, metal, liquid)

**2. Lighting Quality** ⭐⭐⭐⭐⭐
- Backlight / sidelight / soft light applied correctly
- Highlights not blown out; shadows retain detail
- Bokeh / atmospheric light effects look natural

**3. Composition Balance** ⭐⭐⭐⭐⭐
- Subject position follows rule of thirds or golden ratio
- Visual center of gravity is stable
- Appropriate negative space and breathing room

**4. Color Harmony** ⭐⭐⭐⭐⭐
- Color palette matches brand tone
- Complementary / gradient colors used properly
- Overall color scheme is unified

**5. Commercial Usability** ⭐⭐⭐⭐⭐
- Meets commercial photography standards
- Ready to use in marketing campaigns
- Strong visual impact

### Excellence Standards (Nice to Have)

**6. Creative Uniqueness** ⭐⭐⭐⭐
- Unique perspective or creative angle
- Goes beyond conventional photography thinking

**7. Emotional Resonance** ⭐⭐⭐⭐
- Evokes emotional association
- Tells the brand story

**8. Detail Refinement** ⭐⭐⭐⭐
- Ice cubes, bubbles, water droplets are perfect
- Decorative elements are precisely placed

---

## Quality Verification Process

### Phase 1: Pre-Generation Check

**Prompt Quality Checklist**
```
Check before generating:
□ Using user's clean product image, not a reference case
□ Product type clearly described
□ Lighting scheme is specific (source / angle / color temperature)
□ Scene elements are complete (background / props / material)
□ Mood description is clear (emotion / color tone)
□ Technical parameters defined (depth of field / angle / ratio)
□ Professional terms from keyword library used correctly
□ Referenced the Prompt template for the selected style
□ Scene design is original — not copied from reference cases
```

### Phase 2: Generation Monitoring

```python
# Log parameters during generation
generation_log = {
    "scene_type": "Dynamic Splash",
    "prompt": "full prompt content",
    "tool": "GenerateImage",
    "ratio": "16:9",
    "resolution": "4K",
    "reference_image": "product_url",
    "generation_time": "25s"
}
```

### Phase 3: Post-Generation Evaluation

**Manual Evaluation Checklist**
```
Visual Assessment (1–5 score):
□ First impression (visual impact)          _/5
□ Product presentation (clarity & appeal)   _/5
□ Lighting quality (professional & artistic)_/5
□ Composition layout (balance & creativity) _/5
□ Color usage (harmony & brand match)       _/5
□ Detail handling (refinement & realism)    _/5
□ Overall feel (premium & commercial)       _/5

Total: _/35   Rating: ________
30–35: Outstanding ⭐⭐⭐⭐⭐
25–29: Excellent   ⭐⭐⭐⭐
20–24: Good        ⭐⭐⭐
15–19: Acceptable  ⭐⭐
<15:   Needs Redo  ⭐
```

---

## Benchmark Case References

### Benchmark Library

Selected from 90 reference cases — the "gold standard" for each style:

**Dynamic Splash Benchmark**
- Stella Rosa red wine liquid splash
- Key metrics: S-curve liquid, crystalline droplets, pure black background, high contrast

**Still Life Atmosphere Benchmark**
- Glenfiddich whiskey bar scene
- Key metrics: bokeh effect, warm tones, wood texture, luxurious ambiance

**Macro Close-up Benchmark**
- Blood orange cocktail macro
- Key metrics: extreme detail, vibrant colors, gradient background, fresh feel

**Lifestyle Narrative Benchmark**
- Tecate beer outdoor scene
- Key metrics: real setting, natural light, lifestyle feel, storytelling

**Creative Concept Benchmark**
- BRAE geometric metal scene
- Key metrics: geometric elements, metal texture, artistic quality, modern feel

---

## Iteration & Improvement

### When Results Fall Short

**Issue 1: Product not sharp enough**
```python
improved_prompt = original_prompt + """
, product in ultra sharp focus, crystal clear details, 
high definition product photography, pristine clarity
"""
# Parameter adjustment
resolution = "4K"
```

**Issue 2: Lighting not professional enough**
```python
improved_prompt = original_prompt + """
, professional studio lighting, three-point lighting setup,
dramatic rim lighting, controlled highlights, soft shadows
"""
lighting_keywords = [
    "backlit", "rim lighting", "soft diffused light",
    "dramatic lighting", "ambient glow"
]
```

**Issue 3: Composition imbalanced**
```python
improved_prompt = original_prompt + """
, rule of thirds composition, balanced layout,
professional commercial photography composition,
centered product with negative space
"""
```

**Issue 4: Colors not harmonious**
```python
improved_prompt = original_prompt + """
, harmonious color palette, [complementary color] color scheme,
professional color grading, cinematic color treatment
"""
```

**Issue 5: Lacks commercial feel**
```python
improved_prompt = original_prompt + """
, high-end commercial photography, advertising quality,
luxury product shot, premium brand aesthetic,
professional marketing photography
"""
```

---

## Benchmark Validation Cases

### Validation Test 1: Red Wine Liquid Splash

**Target benchmark**: Stella Rosa red wine case

**Test prompt**:
```
Commercial beverage photography, premium red wine bottle with 
dramatic crimson liquid splash in elegant S-curve motion around 
the bottle, pure black background, strong backlighting creating 
glowing translucent liquid edges, frozen droplets suspended in 
mid-air with crystal clarity, high contrast dramatic lighting, 
liquid appears luminous and jewel-like, professional advertising 
photography, ultra sharp product details, 8k resolution, 
cinematic quality
```

**Evaluation criteria**:
- S-curve liquid splash ✓ / ✗
- Crystalline droplets ✓ / ✗
- Pure black background ✓ / ✗
- Clear backlight effect ✓ / ✗
- High contrast drama ✓ / ✗
- Product clearly visible ✓ / ✗

**Target pass rate**: ≥80% (5/6 items)

---

### Validation Test 2: Geometric Creative Scene

**Target benchmark**: BRAE geometric metal scene

**Test prompt**:
```
Creative concept beverage photography, rose gold beverage can 
and crystal cocktail glass arranged in geometric rose gold metal 
framework, modern minimalist aesthetic with clean lines, purple 
gradient background with soft bokeh effect, hard directional 
lighting creating metallic reflections, luxurious and futuristic 
atmosphere, high-end commercial photography, sharp focus on 
products, artistic composition, sophisticated and elegant
```

**Evaluation criteria**:
- Geometric framework structure ✓ / ✗
- Realistic metal texture ✓ / ✗
- Purple gradient background ✓ / ✗
- Modern luxury feel ✓ / ✗
- Product clearly prominent ✓ / ✗

**Target pass rate**: ≥80% (4/5 items)

---

## Quality Assurance Commitment

**Baseline Guarantees**:
- Product visibility rate: ≥95%
- Lighting professionalism: ≥80/100
- Commercial usability rate: ≥85%
- Overall satisfaction: ≥4.0/5.0

**Excellence Targets**:
- Reaches benchmark case level: ≥80% of scenes
- Exceeds benchmark case: ≥20% of scenes
- Zero reshoot rate: <5%

**Remediation if below standard**:
- Regenerate for free
- Prompt optimization suggestions
- Parameter adjustment guidance
- Until satisfied

---

When using this skill, follow the quality verification process to ensure every generated image meets commercial photography standards.
