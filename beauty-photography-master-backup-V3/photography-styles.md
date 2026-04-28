# Photography Principles for Perfume Advertising

A principles-based reference for understanding WHY certain photography techniques work on glass perfume bottles, enabling creative reasoning and novel prompt construction -- not template copying.

## Quick Navigation

| If you are in... | Read these sections |
|---|---|
| Phase 2 (Creative Direction) | VI (Four Commercial Approaches), VII (Fragrance-Mood), III (Echo vs. Contrast), V (Style Vocabulary) |
| Phase 3.2 (Prompt Construction) | Use the Prompt Construction Principles and Master Template inline in SKILL.md Phase 3.2. For evidence/background: IV (Empirical Findings, Phase D Advanced), I (Light Physics -- subsection matching the bottle's glass type) |
| Any phase (reference only) | II (Composition Psychology) |

---

## I. Light Physics on Glass and Liquid

Understanding how light physically interacts with glass is the single most important skill for perfume photography. Glass does NOT behave like other objects.

### The Fundamental Difference

Opaque objects reflect light off their surface -- you see the light hitting the object. Glass **refracts light through its volume** -- you see what's behind and around the object, bent and distorted by the glass. This means:

- **Front lighting fails on glass.** Blasting light at a glass bottle from the front creates blown-out white hotspots and reveals nothing about the bottle's form. The glass just becomes a mirror reflecting the light source.
- **Backlighting reveals form.** When light comes from behind, it passes *through* the glass and liquid, revealing color, density, internal structure, and surface contour. Every curve in the glass acts as a tiny lens, bending the background light.
- **Edge lighting defines shape.** Light grazing the edges of a bottle creates glowing contours that separate the transparent object from its background -- without this, a clear glass bottle disappears.

### Two Master Techniques: Dark Field and Bright Field

| Technique | Setup | What You See | WHY It Works | When to Use |
|-----------|-------|-------------|--------------|-------------|
| Dark Field | Light behind subject, blocked by a dark panel so only edge-spill reaches the glass | Glowing edges on a dark background; the bottle appears to emit light | Light "grazes" curved glass surfaces, creating luminous contours by refraction at steep angles. The dark background provides maximum contrast for these glowing edges. | Dramatic, sensual, mysterious moods; dark/luxury aesthetics; bottles with interesting edge geometry |
| Bright Field | Background fully lit; dark cards ("negative fill") placed beside the glass to create dark edge lines | Dark-edged bottle on a bright background; crisp silhouette | The bright background transmits through the glass uniformly, while dark cards create contrast lines along edges by their absence of light. Engraving and surface detail become visible through differential refraction. | Clean, modern, editorial moods; bottles with engraving/embossing; when you need to show surface detail |

**Principle**: Detail in glass is revealed through **contrast** -- every curve and surface change acts as a lens. If there is little contrast in the light environment, there will be little visible detail in the glass.

### How Liquid Affects Light

The liquid inside a perfume bottle is a second optical layer:

- **Clear liquid (light gold, transparent)**: Light passes through with minimal color shift; you see refraction patterns and the back wall through the bottle. Creates a "window" effect.
- **Saturated liquid (deep amber, rich color)**: Absorbs certain wavelengths, creating a strong color glow when backlit. The bottle becomes a glowing lantern of color. The denser the color, the more it glows.
- **Opacity level matters**: At ~30% opacity, light transmits freely and you see through the bottle. At ~70%, the liquid itself becomes the light source when backlit, producing warm caustics on surrounding surfaces. At ~100% opacity (opaque bottles), the bottle behaves more like a regular object.

### Frosted and Opaque Glass: Different Physics, Not Less Physics

Frosted, matte, or pearlescent glass behaves fundamentally differently from clear glass. Where clear glass transmits and refracts light, frosted glass **scatters** light within its surface:

- **Surface scattering**: Light hitting frosted glass doesn't pass through -- it scatters in many directions within the surface layer, creating a soft, diffuse glow. The bottle appears to emit light from within rather than transmitting it through.
- **Micro-highlights**: The granular or textured surface catches light at thousands of tiny points, creating a field of micro-highlights (like morning dew on a surface). This is the frosted glass equivalent of caustics.
- **No refraction, no caustics**: Frosted glass does NOT create the caustic light patterns that clear glass does. Describing caustics on a frosted bottle will mislead the AI model into rendering incorrect transparency.
- **Pearlescent effects**: Some frosted glass has a pearlescent or iridescent quality, where the color shifts subtly depending on viewing angle. Describe this as "pearlescent surface shifting subtly in the light" rather than "transparent glass."

**For AI prompts**: Use scattering and surface-glow language, NOT transmission/refraction language. "Light scattering within the frosted surface creating a soft internal luminosity" >> "light refracting through the glass." See Phase D Experiment 3 findings in Section IV for empirical validation.

### Caustics: The Luxury Signature

Caustics are concentrated light patterns cast onto surfaces by refractive objects -- the dancing light patterns you see on a tablecloth beneath a wine glass. They are a **signature of authentic glass photography**:

- **What creates them**: Strong directional light + curved glass surfaces + a surface nearby to catch the patterns
- **Why they matter**: Caustics are proof of real glass refraction. They make a scene feel physically authentic and luxurious. No other material creates them.
- **How to describe them**: "warm caustics dancing on the marble surface," "light refracting through the glass creating golden light patterns on the table," "concentrated light pools beneath the bottle"

### Reflections on Glass: Friend and Enemy

Glass reflects its entire environment like a mirror. This is both the challenge and the opportunity:

- **Unwanted reflections** (studio equipment, photographer, surroundings) destroy the illusion. Professional photographers surround the bottle with diffusion panels, black cards, and reflectors to control exactly what appears on each glass surface.
- **Intentional reflections** (gradient cards, colored surfaces, structured light) define the bottle's three-dimensional form. A strip of light reflected on the glass side communicates curvature. A gradient from light to dark across the surface communicates depth.
- **For AI prompts**: Describe the desired reflection behavior, not just the lighting: "soft gradient reflections on the glass surface," "a single clean highlight line running along the bottle's curve."

### Surface Material and Light Physics

Glass always "shows" what's around it. The surface material beneath the bottle directly affects how the bottle looks:

| Surface | Light Behavior | Effect on Glass Bottle |
|---------|---------------|----------------------|
| Polished marble | Soft diffuse reflection upward; veins create organic shadow patterns | Marble acts as a passive fill light from below, lifting shadows. The organic vein texture contrasts with the bottle's precision geometry. |
| Black glass/mirror | Perfect specular reflection | Creates a complete mirror double of the bottle. Doubles visual impact. Communicates ultimate luxury through symmetry. |
| Water surface | Mirror reflection + ripple distortion | Creates a living, breathing reflection. Water drops add movement. The imperfect reflection feels more real than a mirror. |
| Matte stone/concrete | Absorbs light, no reflection | Maximum contrast between the luminous glass and the dead-matte surface. The bottle appears to glow. |
| Velvet/fabric | Absorbs light deeply, creates texture contrast | The bottle's brilliance is amplified against the light-absorbing fabric. Fabric folds create organic lines that contrast with the bottle's hard edges. |
| Wet surface | Thin-film reflection + texture | Fresh, dynamic feel. The reflective sheen adds depth without the perfection of a mirror. |

---

## II. Composition Psychology

Every compositional choice communicates meaning to the viewer, whether intentionally or not. Understanding WHY these principles work enables you to make intentional choices.

### Why Placement Matters

| Placement | Psychological Effect | WHY It Works |
|-----------|---------------------|--------------|
| **Dead center** | Monument, icon, authority | The viewer has nowhere else to look -- the object demands complete attention. Used by brands that want to say "THIS is the product, nothing else matters." (Chanel No.5) |
| **Rule of thirds** | Story, journey, elegance | The off-center placement creates visual tension -- the eye moves between the subject and the negative space, suggesting a narrative. The viewer's eye "travels" across the image. |
| **Edge tension** | Intrigue, editorial, avant-garde | Placing the bottle at the frame edge breaks expectations. It says "this isn't a product shot, it's art." Creates discomfort that draws attention. |
| **Golden ratio** | Natural beauty, harmony | Mirrors proportions found in nature (shells, flowers). Feels intrinsically "right" without the viewer knowing why. Creates sophisticated balance. |

### Why Negative Space = Luxury

This is the most powerful principle in luxury advertising: **scarcity communicates value**. Just as a luxury boutique has few items in a large space, generous negative space around a perfume bottle says:

- "This product is important enough to deserve all this space"
- "We don't need to fill the frame with distractions"
- "The bottle IS the entire story"

The inverse is also true: a crowded frame with many props communicates abundance, storytelling, or lifestyle -- appropriate for botanical/editorial concepts but counterproductive for pure luxury.

### Why Camera Angle Shapes Perception

| Angle | Perception | WHY |
|-------|-----------|-----|
| **Hero low (below eye level)** | Power, grandeur, aspiration | Looking up at an object triggers the same psychological response as looking up at a monument or authority figure. The bottle becomes something to aspire to. |
| **Eye level** | Honesty, directness, equality | Mimics how we meet another person's gaze. Creates a sense of encounter with the product. Feels trustworthy and intimate. |
| **Elevated 3/4** | Elegance, overview, revealing | Shows both the front face and the top of the bottle simultaneously. Reveals cap design and liquid level. The slight elevation creates a sense of informed sophistication. |
| **Overhead flat lay** | Editorial, curated, storytelling | The overhead view removes perspective distortion -- everything exists on a 2D plane. This is the "arranged collection" view, perfect for telling a story with props and context. |
| **Dutch angle (tilt)** | Dynamism, disruption, modernity | Tilting the camera breaks the expected horizontal/vertical grid. Creates energy and tension. Says "this brand is different, edgy, unconventional." |

### Depth Cues and Dimension

A photograph is a 2D surface. Creating the illusion of 3D space requires deliberate cues:

- **Shallow depth of field** (blurred background): Separates the bottle from its environment, creates intimacy, directs focus. The blur itself communicates that a real lens captured this. Use for hero shots and emotional close-ups.
- **Deep focus** (everything sharp): Creates an "entire world" effect. Everything in the scene matters equally. Use for flat lays and environmental storytelling.
- **Foreground elements** (slightly blurred props in front of the bottle): Create layers of depth. The viewer's eye passes through these layers to reach the bottle, creating a journey.
- **Atmospheric perspective** (fog, mist, haze): Softens distant elements, mimicking how air scatters light over distance. Creates depth and mood simultaneously.

---

## III. Color, Material, and Emotional Perception

Color is the fastest emotional communicator in advertising. Viewers respond to color within milliseconds, before they consciously process the image.

### Color Psychology in Fragrance Context

| Color Family | Emotional Response | WHY (Psychological Mechanism) | Fragrance Association |
|-------------|-------------------|-------------------------------|----------------------|
| **Gold / Warm Amber** | Opulence, celebration, warmth | Gold is universally associated with precious metals, sunlight, and wealth across cultures. Triggers reward pathways. | Oriental, luxury limited editions, evening fragrances |
| **Deep Burgundy / Wine** | Sensuality, depth, sophistication | Dark reds combine the energy of red with the depth of black. Associated with aged wine, blood, and passion. | Intense florals, woody orientals, seductive fragrances |
| **Black** | Power, mystery, exclusivity | Black absorbs all light -- it represents the unknown, the hidden, the exclusive. "What you can't see is more desirable." | Niche luxury, evening, oud-based |
| **White / Cream** | Purity, freshness, modernity | White reflects all light -- it represents openness, nothing-to-hide, clean slate. | Clean fragrances, summer scents, skincare-adjacent |
| **Cool Blue / Silver** | Calm, clarity, freshness | Blue mimics sky and water -- the two largest "clean" natural elements. Triggers parasympathetic relaxation. | Aquatic, fresh, sport, daytime |
| **Blush Pink / Rose** | Romance, tenderness, femininity | Soft pink combines the energy of red with the purity of white. Associated with flowers, skin, and dawn. | Floral, romantic, youthful |
| **Deep Green** | Nature, vitality, groundedness | Green is the color of living plants. Triggers associations with health, growth, and natural authenticity. | Herbal, green, vetiver, natural ingredients |

### Color Grading: How Post-Processing Shifts Perception

The same bottle in the same setting can tell completely different stories through color grading:

- **Warm golden grading**: Adds richness, luxury, evening atmosphere. Makes glass appear to glow from within.
- **Cool desaturated grading**: Creates editorial sophistication, modernity, morning freshness. Makes glass appear crystalline.
- **High contrast (crushed blacks)**: Drama, mystery, editorial edge. Hides details in shadow, revealing only what you choose to show.
- **Low contrast (lifted shadows)**: Softness, dreaminess, accessibility. Nothing is hidden; the mood is gentle and inviting.
- **Split-tone (warm highlights, cool shadows)**: Creates dimensional color contrast. The warm-cool interplay adds visual richness and perceived depth.

### Material Contrast Principle

The fundamental principle of luxury product photography is **contrast between the product and its environment**:

- Glass is brilliant, transparent, refractive → pair it with matte, opaque, light-absorbing surfaces to maximize contrast
- Glass is hard, geometric, precise → pair it with soft, organic, flowing elements (fabric, flowers, water) to create tension
- Glass is cold and inorganic → pair it with warm, living elements to create emotional warmth

This contrast is WHY velvet-on-glass, marble-under-crystal, and flowers-around-bottles are enduring archetypes -- they work at a fundamental visual level, not just as aesthetic conventions.

### Echo vs. Contrast: Two Creative Strategies for Campaign Diversity

Beyond material contrast within a single image, there is a higher-level creative choice that determines how an entire **set** of campaign images feels: whether the environment **echoes** or **contrasts** the bottle's inherent emotional register.

**Echo strategy**: The environment mirrors the bottle's mood. A dark purple bottle on dark velvet under moody side light. A fresh citrus bottle on white marble in bright sunlight. This amplifies the bottle's existing identity -- safe, cohesive, on-brand. Most campaigns default to echo because it feels "natural."

**Contrast strategy**: The environment deliberately opposes the bottle's mood. A dark purple bottle on white marble in bright morning light with fresh green fig leaves. A delicate pink bottle on raw concrete under harsh side light. This creates visual tension -- the bottle stands out MORE because it's the unexpected element. Often more memorable, more editorial, and more shareable.

**Neither is inherently better.** A strong campaign set uses both: echo for the on-brand hero shot, contrast for the editorial surprise. The problem occurs when ALL concepts echo the same mood -- the campaign looks like one photoshoot, not three different stories.

| Bottle Identity | Echo Environment | Contrast Environment |
|---|---|---|
| Dark purple, sensual (Tom Ford) | Black velvet, moody chiaroscuro, deep shadows | Bright white marble, morning sunlight, fresh fig leaves and green botanicals |
| Soft pink, feminine (Guerlain) | Blush silk, soft diffused light, peonies | Raw concrete, stark side light, architectural minimalism |
| Clear/aquatic, fresh (Armani) | Water surface, cool blue light, glass | Warm wood, golden hour window light, Mediterranean lifestyle |
| Gold/amber, opulent (Chanel) | Dark museum backdrop, dramatic spot light | Bright field of white flowers, natural daylight, airy |

**Why contrast works on dark bottles specifically**: Dark-colored bottles (deep purple, dark amber, black glass) have a natural gravitational pull toward dark environments. But dark-on-dark reduces visual contrast -- the bottle can disappear into its environment. Placing a dark bottle in a bright environment maximizes the bottle's visual weight. The bottle becomes the singular dramatic element rather than part of a uniformly dark scene.

---

## IV. Prompt Translation Patterns

This section maps photography principles to specific AI prompt phrasings. These patterns translate physical photography knowledge into language that image generation models understand.

### Glass and Transparency

| Photography Principle | Effective Prompt Phrasing | WHY This Wording Works |
|----------------------|--------------------------|----------------------|
| Backlit glass revealing color | `light refracting through the clear glass bottle, revealing the rich amber liquid within` | Describes the physical process (refracting through) rather than just the result |
| Edge-lit definition | `glowing rim light defining the bottle's silhouette edges against the dark background` | Specifies WHERE the light appears (rim, edges) and WHAT it does (defining silhouette) |
| Glass transparency | `crystal-clear glass with visible refraction, the background subtly distorted through the curved bottle walls` | Describes the optical effect (refraction, distortion) that proves real glass |
| Caustics | `warm caustic light patterns cast onto the marble surface beneath the bottle, concentrated pools of refracted light` | Names the phenomenon AND describes its visual appearance |
| Liquid glow | `amber liquid at 70% opacity glowing warmly when backlit, light passing through creating warm golden tones` | Specifies opacity level and the light interaction behavior |
| Internal reflections | `internal reflections visible within the glass body, light bouncing between the front and back walls of the bottle` | Describes the multi-bounce behavior inside thick glass |

### Lighting Setups

| Photography Setup | Effective Prompt Phrasing | Visual Result |
|-------------------|--------------------------|---------------|
| Three-point studio | `Three-point softbox lighting: key light at 45 degrees from left creating defined shadows, fill light from right at half intensity, backlight creating rim highlights on the glass edges` | Balanced, professional, dimensional |
| Dark field / moody | `Single dramatic side light from the left, deep shadows enveloping the right side, the glass bottle's edges glowing against the dark background, chiaroscuro contrast` | Dramatic, sensual, mysterious |
| High-key clean | `Bright, even illumination from large overhead softbox, minimal shadows, clean white environment, the bottle appearing crisp and modern against pure white` | Fresh, modern, clinical luxury |
| Natural window | `Warm directional sunlight streaming from a window on the left side, soft diffused natural shadows, golden hour warmth, the bottle catching a single bright highlight` | Intimate, authentic, lifestyle |
| Rim backlight | `Strong backlight creating a luminous halo around the bottle's silhouette, the glass edges glowing, liquid color intensified by transmitted light` | Ethereal, dramatic reveal |

### Surface and Environment

| Photography Element | Effective Prompt Phrasing | WHY This Specific Wording |
|--------------------|--------------------------|--------------------------|
| Marble surface | `Placed on polished Calacatta marble with grey veining, the marble's subtle sheen acting as a soft reflector beneath the bottle` | Names a specific marble type; describes its light-reflecting function |
| Water reflection | `Standing on a shallow pool of still water, its perfect mirror reflection visible below, a single water droplet creating gentle concentric ripples` | Specifies the water state (still/shallow) and the dynamic element (ripple) |
| Velvet drape | `Rich midnight-blue velvet draped beside the bottle, its deep folds absorbing light and creating maximum contrast with the luminous glass surface` | Describes the velvet's FUNCTION (absorbing light, creating contrast) not just its appearance |
| Black glass surface | `Placed on a polished black glass surface, a perfect mirror reflection of the bottle visible below, creating visual symmetry and doubling the product's presence` | Describes the mirror effect and its purpose (doubling presence) |
| Atmospheric fog | `Wisps of fine atmospheric mist curling around the bottle's base, adding depth and mystery, the mist catching and scattering the rim light into a soft glow` | Describes HOW the mist interacts with the lighting |

### Camera and Technical

> **Empirical finding (Phase C, Experiment 4 -- confirmed across both Chanel No.5 and Byredo Bal d'Afrique):** Camera gear names (e.g. "Hasselblad H6D," "Phase One IQ4," "120mm macro lens," "f/5.6") have **no measurable effect** on generated output. Images generated with and without gear specifications are virtually identical across different camera systems and bottle types. **Do not waste prompt tokens on equipment names.** Instead, describe the desired VISUAL OUTCOME (shallow depth of field, sharp focus, overhead perspective) without naming the gear that would achieve it.

| Photography Concept | Effective Prompt Phrasing |
|--------------------|--------------------------|
| Shallow DOF / intimacy | `shallow depth of field, razor-sharp focus on the bottle label, background dissolving into creamy blur` |
| Macro detail | `extreme close-up, tight framing on the bottle's cap detail, every facet and engraving visible in sharp focus` |
| Hero angle | `shot from slightly below eye level, the bottle towering heroically, front-to-back sharpness` |
| Wide environmental | `wide shot, the entire styled scene in deep focus, the bottle positioned at the left third of the frame` |
| Overhead editorial | `shot from directly overhead, the bottle and props arranged in a deliberate flat-lay composition, deep focus` |
| Film aesthetic | `warm analog film aesthetic reminiscent of Kodak Portra 400, subtle grain texture, slightly lifted blacks, warm amber color shift in highlights` |

### Quality and Style Anchors

These baseline phrases ground the generation in commercial photography reality:

```
Luxury beauty advertising campaign photograph, high-end commercial fragrance photography,
professional studio lighting with expert glass handling, razor-sharp product focus,
medium format quality, 8K resolution, professional color grading and retouching,
magazine-quality editorial finish
```

For specific commercial tones:

| Tone | Anchor Phrase |
|------|--------------|
| Prestige luxury | `in the style of a Vogue Beauty editorial, refined luxury, museum-quality precision` |
| Modern minimal | `contemporary minimalist advertising, clean geometric composition, Scandinavian design sensibility` |
| Sensual editorial | `dark sensual beauty photography, moody chiaroscuro, editorial for luxury fashion magazine` |
| Fresh lifestyle | `bright natural beauty photography, effortless luxury lifestyle, morning light editorial` |
| Art-forward | `conceptual beauty photography merging fine art and commerce, gallery-quality visual, avant-garde composition` |

### Prompt Construction Principles & Master Template

> **Operational versions of these are inline in SKILL.md Phase 3.2.** The empirical evidence behind each principle is documented below in the Empirical Findings and Phase D sections.

### Empirical Prompt Findings (Phase C Experiments -- Cross-Bottle Validated)

These findings are from controlled A/B testing on image generation outputs, validated across two fundamentally different bottles:
- **Chanel No.5**: Rectangular body, flat panels, rich amber liquid (~70% opacity), faceted crystal stopper, Art Deco heritage
- **Byredo Bal d'Afrique**: Cylindrical body, curved glass, near-clear liquid (~15% opacity), solid matte black dome cap, Scandinavian minimalist

The hierarchy held across both bottles, confirming these are **general prompt principles**, not bottle-specific quirks.

#### What Matters Most → Least for Prompt Quality

1. **Scene/approach selection** (HIGH IMPACT -- confirmed across both bottles): The commercial approach (botanical, light/shadow, lifestyle, abstract) is the single most impactful prompt element. Each approach produces dramatically different images. Choosing the right approach is more important than perfecting any other prompt element. Both bottles produced 4 visually distinct, high-quality results across all 4 approaches.

2. **Functional descriptions** (MEDIUM-HIGH IMPACT, scales with surface interactivity): Describing what elements DO with light produces better results than just naming them.
   - Surface: `marble acting as a soft reflector beneath the bottle, warm caustic light pooling on the stone surface` >> `on polished marble` >> `on marble`
   - The functional language transforms passive surfaces into active participants -- the model renders reflections, caustic patterns, and light interactions that don't appear with name-only descriptions.
   - **Scaling principle**: Functional descriptions have MORE impact on reflective/interactive surfaces (polished marble, glass, water) than on absorptive surfaces (linen, matte wood, concrete). You can only prompt for light interactions the material physically supports. With Chanel on marble, the improvement was dramatic (visible caustics, reflections). With Byredo on linen, the improvement was moderate (better fabric dimension, contrast).
   - **Anti-freelancing bonus**: Vague surface descriptions (e.g. "on stone") cause the model to freely choose wildly different surfaces between generations. Naming the specific material locks in consistency.

3. **Lighting precision** (MEDIUM IMPACT, scales with bottle optical complexity): Physics-based lighting language produces more controlled and realistic glass behavior than generic terms, but the difference is incremental.
   - `single hard key light from the left refracting through the glass creating warm caustic patterns on the marble surface, glowing bottle edges from rim backlight` >> `chiaroscuro side lighting from 45 degrees left, strong shadows` >> `dramatic lighting`
   - Generic prompts like "dramatic lighting" let the model freelance -- it may add unrequested elements (flowers, platforms, particles) to fill the creative gap. Specific language prevents this.
   - **Scaling principle**: Physics-based lighting descriptions have MORE impact on optically complex bottles (rich amber liquid that colors light, faceted glass that creates visible caustics) than on optically simple bottles (near-clear liquid, smooth cylinder). With Chanel's amber liquid, the physics description created dramatic caustics and glow effects. With Byredo's near-clear liquid, the improvement was real but subtler (edge definition, surface caustic lines). **When the liquid doesn't visibly interact with light, describe how the glass shape and cap materials interact with light instead.**

4. **Camera gear names** (NO IMPACT -- confirmed across both bottles and camera systems): Equipment specifications produce no visible difference in output. Tested with Hasselblad H6D + 120mm macro (Chanel) and Phase One IQ4 + Schneider 120mm macro (Byredo) -- both identical to no-camera versions. Describe the visual effect you want instead.
   - `shallow depth of field with sharp focus on the label` = same result as `Shot on Phase One IQ4 with Schneider 120mm at f/4.5, shallow depth of field`

#### The Scaling Principle

The impact of prompt specificity on Tiers 2 and 3 scales with how much the described material physically interacts with light. Invest prompt tokens where the physics is richest: for a clear glass bottle on marble, spend heavily on light-through-glass and marble reflection descriptions; for a matte ceramic bottle on linen, spend more on scene composition and overall mood instead. See the complete Scaling Principle table (including frosted glass) in the Phase D section below.

#### Anti-Freelancing Principle (Cross-Bottle Confirmed)

When prompts are vague, image generation can fill creative gaps by inventing elements not requested (flowers appearing in a pure product shot, glass platforms materializing, atmospheric particles, random surface choices). To prevent this: **be explicit about what IS in the scene and what ISN'T**. A specific, complete scene description leaves no room for the model to improvise unwanted additions. Confirmed: "on stone" produced marble in one variant and terrazzo in another; "on raw linen fabric with visible weave texture" produced consistent results.

### Phase D Advanced Findings (Guerlain Aqua Allegoria -- Frosted Glass & Complex Geometry)

These findings extend the Phase C hierarchy with new dimensions tested on a fundamentally different bottle:
- **Guerlain Aqua Allegoria Perle Rosa Rossa**: Frosted pearlescent pink opaque glass, intricate gold honeycomb lattice dome cap (~40 hexagonal cells), gold sphere finial, multi-material (gold + frosted glass + clear glass base band)

This bottle tests dimensions the clear-glass bottles (Chanel, Byredo) could not: structural fidelity of complex geometry, frosted glass physics, prompt structure, scene complexity limits, and multi-material light description.

#### Reference Image Dominance (Experiments 1, 2, 4, 5)

Multiple experiments converged on a fundamental principle: **the reference image, not the text description, is the primary driver of structural fidelity.**

- **Structural description granularity doesn't matter** (Exp 2): "gold cap" vs. an exhaustive construction description ("gold honeycomb lattice dome cap with ~40 hexagonal cells arranged in honeycomb pattern, each cell revealing pink glass beneath...") produced nearly identical honeycomb rendering. The model copies the reference image's geometry regardless of text detail level.
- **Scene complexity doesn't degrade bottle detail** (Exp 4): Even maximally complex scenes (abundant roses, pearl necklace, gold leaf, silk ribbon, atmospheric mist) preserved the honeycomb cap's full structural integrity. There is NO "complexity budget."
- **Prompt ordering doesn't affect fidelity** (Exp 5): Bottle-first, scene-first, and "sandwich reinforcement" (repeating key structural details at the end) all produced equivalent results. The model processes prompt + reference image holistically, not sequentially.
- **Complex geometry survives across all approaches** (Exp 1): The honeycomb lattice was preserved across botanical, light/shadow, lifestyle, and abstract scenes with no degradation.

**Practical takeaway**: When a reference image is provided, spend prompt tokens on scene/lighting/mood rather than on exhaustive bottle structure descriptions. A brief named description ("gold honeycomb dome cap topped with a gold sphere") is sufficient -- the visual reference handles structural fidelity. Save your prompt budget for what the reference image CAN'T convey: the new scene, lighting behavior, and atmosphere.

#### Material Mismatch Principle (Experiment 3)

**Using physics descriptions for the WRONG material actively harms output.**

- Clear-glass physics language ("light refracting through the glass revealing the liquid color within, caustic patterns on the surface") applied to frosted/opaque glass made the model attempt to render transparency that doesn't exist -- the frosted glass became semi-translucent with physically incorrect caustic patterns.
- Adapted frosted-glass physics language ("light scattering within the pearlescent surface creating a soft internal luminosity, the granular texture catching micro-highlights") produced superior results with accurate opacity, correct luminous glow, and authentic texture.
- Generic physics ("beautiful lighting") produced acceptable but unremarkable results -- better than WRONG physics, worse than ADAPTED physics.

**New rule -- Match physics language to material**:

| Glass Type | Physics Description Approach | Key Terms |
|---|---|---|
| Clear glass, visible liquid | Refraction, transmission, caustics, liquid color glow | "light refracting through," "caustic patterns," "liquid glowing warmly" |
| Frosted/opaque glass | Surface scattering, internal luminosity, micro-highlights, texture | "light scattering within the surface," "soft internal glow," "micro-highlights on granular texture" |
| Crystal/faceted glass | Prismatic dispersion, sharp caustics, facet reflections | "each facet catching light," "prismatic dispersion," "sharp caustic lines" |

**This extends the Scaling Principle**: Frosted/opaque glass is not "low impact" -- it's "different impact." Physics descriptions DO matter for frosted glass, but they must describe scattering and surface effects, not transmission and refraction. Using clear-glass physics on frosted glass is **worse** than using no physics language at all.

#### Multi-Material Light Descriptions (Experiment 6)

For bottles with 3+ distinct materials (e.g., gold metal + frosted glass + clear glass), two approaches were tested:

- **Per-material sequential**: Describe each material's light behavior independently ("light reflecting off the gold lattice. Light scattering in the frosted glass. Light refracting through the clear base.")
- **Interaction-focused (light journey)**: Describe how light moves ACROSS materials ("warm light strikes the gold honeycomb first, catching specular highlights, then passes through the hexagonal cells to scatter into the frosted pink glass, creating internal luminosity, and at the base transitions to clear refraction...")

Both produced excellent results. The light journey approach showed marginally more cohesive lighting at material transitions and more pronounced caustic effects at the clear glass base, but with slightly higher risk of model freelancing. The per-material sequential approach was more predictable and controlled.

**Practical recommendation**: Either approach works. For product shots where precision matters most, use per-material sequential (simpler, more predictable). For editorial/artistic shots where cohesion and atmosphere matter, try the light journey approach. The difference is incremental, not transformative.

#### Updated Scaling Principle (with Frosted Glass)

| Material Property | Prompt Specificity Impact | Why |
|---|---|---|
| Rich amber liquid, faceted glass | HIGH -- physics descriptions create visible caustics, colored glow, refraction patterns | More optical interactions to describe = more the model can render |
| Near-clear liquid, smooth cylinder | MODERATE -- physics descriptions improve edge definition, surface caustics | Fewer visible interactions, but glass shape still interacts with light |
| Frosted/opaque glass | MODERATE-HIGH -- but requires ADAPTED physics (scattering, not refraction) | Wrong physics actively harms; adapted physics creates accurate luminosity and texture |
| Matte black cap, opaque materials | LOW -- limited light interaction to describe | Opaque materials absorb light; no refraction to prompt for |
| Reflective surfaces (marble, glass) | HIGH -- functional descriptions create visible reflections, light pooling | Surface actively participates in light story |
| Absorptive surfaces (linen, wood) | MODERATE -- functional descriptions improve contrast, dimension | Surface absorbs rather than interacts; describe contrast, shadow, texture |

**Confirmed non-factors** (no measurable effect): structural description detail when a reference image is provided, prompt ordering (bottle-first = scene-first = sandwich), scene complexity on bottle fidelity, camera gear names.

---

## V. Style Vocabulary

These are compositional archetypes to use as vocabulary when building concepts. Each archetype is a starting point, not a fixed recipe -- the best results come from combining elements across archetypes based on the specific bottle's identity.

### Composition Archetypes

| Archetype | Core Principle | Light | Surface | Color | Prompt Keywords |
|-----------|---------------|-------|---------|-------|-----------------|
| Sculptural Precision | Product as monument; measured, deliberate, architectural | Controlled studio light revealing every contour; shadows as compositional elements | Matte stone, plaster, smooth concrete | Restrained neutrals; product is the only color | `sculptural still life, geometric negative space, controlled studio light, monochromatic surface, clarity of form` |
| Poetic Color Play | Color as the emotional vehicle; product within a color field | Soft even illumination letting color dominate; warm-cool interplay | Colored acrylic, painted backdrops, tinted glass | Bold but refined -- jewel tones, pastels, or monochromatic saturation | `poetic color field, tonal gradient backdrop, refined saturation, soft even light, color-as-emotion` |
| Organic Tension | Manufactured object vs. raw nature; structured vs. flowing | Mixed -- studio precision on product, softer natural feel on organic elements | Raw wood, earth, rough stone, botanical beds | Rich saturated naturals -- deep greens, warm ambers, berry | `organic still life, botanical elements, natural tension, asymmetric composition` |
| Minimalist Materiality | Radical simplicity; all attention on material truth | Precision lighting revealing glass transparency, metallic sheen, liquid density | Reflective or ultra-matte -- polished black, mirror, seamless white | Monochrome or very limited; the bottle IS the color story | `minimalist precision, material truth, glass transparency, single-source lighting, ultra-refined` |
| Intimate Naturalism | Caught in a real moment; natural, unforced | Window-light simulation, warm and directional with soft shadows | Linen, natural wood, ceramic, warm-toned surfaces | Muted warm -- cream, sand, terracotta, soft gold | `natural window light, intimate atmosphere, warm muted tones, casual elegance, golden hour` |
| Film Analog Warmth | Tactile quality of analogue photography; warm grain | Warm, slightly diffused, embracing lens flare or light leaks | Textured, tactile -- crumpled fabric, rough paper | Warm saturated -- amber, ochre, deep rose; Kodak Portra tones | `analogue film warmth, Kodak Portra, tactile textures, slight grain, warm diffused light` |
| Contemporary Editorial | Modern art sensibility; muted, refined | Soft, almost flat -- emphasis on color relationships over drama | Muted tones -- dusty pink, sage green, warm gray | Intentionally desaturated or dusty; never bright | `contemporary editorial, muted dusty palette, refined understatement, sophisticated restraint` |
| Art-Commerce Hybrid | Iconoclastic; luxury feels youthful and irreverent | High-gloss studio but applied unconventionally -- colored light, unusual angles | Unexpected juxtapositions -- high-shine with raw | Bold, sometimes clashing -- always intentional | `fresh irreverent luxury, bold color clash, unconventional angle, high-gloss, art-meets-commerce` |

### Lighting Vocabulary

| Technique | Description | Effect on Glass Bottle | Prompt Terms |
|-----------|-------------|----------------------|--------------|
| Soft Diffused Top | Large source directly above | Even illumination, gentle gradients, minimal harsh reflections | `soft overhead diffused light, gentle gradient on glass` |
| Dramatic Side | Hard or semi-hard from 45-90° | Strong shadows, reveals texture/embossing, creates depth | `dramatic side lighting at 45 degrees, defined shadows` |
| Rim Backlight | Light behind/beside the edge | Glowing edges, silhouette definition, reveals liquid color by transmission | `rim backlight, glowing bottle edges, silhouette definition` |
| Window Natural | Simulated daylight from one side | Warm, organic feel; soft directional shadows | `natural window light from the left, warm directional shadows` |
| Low-Key Dramatic | Minimal light, deep shadows dominate | Mystery, sensuality; only key features illuminated | `low-key dramatic lighting, deep shadows, selective illumination` |
| High-Key Clean | Bright, even, shadow-free | Fresh, clinical, modern; emphasizes design purity | `high-key even illumination, minimal shadows, clean white` |

### Set Design Elements

| Element Type | Options | When to Use |
|-------------|---------|-------------|
| **Surfaces** | Polished marble, matte stone, water pool, silk/satin, sand, black glass, raw concrete, wet surface | Choose based on desired reflection behavior and contrast with glass |
| **Backgrounds** | Seamless gradient, textured wall, color block, atmospheric fog, environmental scene, pure black, soft paper curve | Choose based on how much story vs. product focus you need |
| **Props** | Botanicals (roses, jasmine, citrus), aquatic (water, ice, mist), mineral (crystals, pebbles), textile (silk, velvet), architectural (concrete, metal), metallic (gold leaf, brass), glass (prisms, spheres), edible (vanilla, cinnamon, citrus) | Choose props that reinforce the creative thesis -- they should tell the SAME story as the bottle |

---

## VI. Four Commercial Campaign Approaches

These are the four dominant approaches used by luxury perfume brands in real campaigns. Each solves a fundamental challenge: perfume bottles are cold, manufactured objects made of glass and metal. These approaches each add a different dimension of life, emotion, or meaning to the bottle.

### Approach 1: Ingredient & Botanical Immersion

**The Core Idea**: Surround the bottle with the natural ingredients it contains -- flowers, fruit, bark, herbs, citrus. This creates an immediate sensory bridge: the viewer sees peaches and imagines the scent of peach; they see roses and feel the fragrance before smelling it.

**WHY It Works (The Temperature Principle)**:
- Glass and metal are cold, geometric, manufactured. Natural elements are warm, organic, alive.
- This contrast creates **emotional warmth** -- the viewer's eye bounces between the precision of the bottle and the imperfection of a petal, a sliced fruit, a rough bark surface.
- The ingredients also serve as **visual proof** of what's inside. They answer the fundamental challenge of perfume advertising: how do you photograph a smell? By showing its components.

**Sub-Variations Observed in Campaigns**:

| Variation | Technique | Mood | Brands That Use It |
|-----------|-----------|------|--------------------|
| **Ingredient Explosion** | Bottle at center, surrounded/engulfed by full-bleed ingredients (sliced fruit, flowers, leaves). Overhead or frontal, white or neutral background, deep focus. | Abundant, vibrant, sensory overload | Tom Ford (Bitter Peach, Neroli Portofino, Rose Prick, Costa Azzurra), Burberry |
| **Gentle Petal Framing** | Bottle among delicately arranged flowers/branches, soft diffused light, airy composition, white background | Feminine, romantic, airy | Jo Malone, Van Cleef & Arpels, Guerlain |
| **Dark Botanical** | Same immersion technique but on black background with moody, saturated botanicals | Mysterious, gothic, sensual | Tom Ford Noir de Noir, niche brands |
| **Ingredient + Surface** | Bottle on marble or glass shelf with flowers arranged as architectural element, not just scattered | Structured, editorial, refined | Acqua di Parma, Giorgio Armani (Si Fiori) |

**Key Photography Principles at Play**:
- **Light**: Usually bright, even illumination to show ingredient textures and colors accurately. High-key for light versions, low-key for dark botanical variants.
- **Composition**: Centered bottle with radial or organic arrangement of elements. The bottle is always the sharpest focus point; some ingredient elements may blur at edges.
- **Color**: The ingredients themselves ARE the color palette. The bottle's liquid color should harmonize with the surrounding ingredients.
- **Scale**: Ingredients often appear larger than reality relative to the bottle, creating an enveloping effect.

**Prompt Translation Patterns**:
- `perfume bottle nestled among [lush peonies / sliced blood oranges / fresh rosemary sprigs], the organic textures of the natural elements contrasting with the precision of the glass`
- `surrounded by abundant [ingredient], filling the entire frame, the bottle as the calm geometric center within a sea of organic forms`
- `[flowers/fruit] arranged around the bottle, water droplets on the glass and petals suggesting freshness, the ingredients spilling beyond the frame edges`
- For dark variant: `deep [black/purple] [roses/berries] enveloping the bottle on a pure black background, the gold label catching a single accent light, moody and sensual`

### Approach 2: Light & Shadow Drama

**The Core Idea**: Let the light itself be the subject. Use dramatic, sculpted light to reveal how glass refracts, reflects, and transforms illumination. The bottle becomes a light-catching instrument -- a prism, a jewel, a sculptural light event.

**WHY It Works (The Visual Tension Principle)**:
- Glass is one of the few materials that simultaneously reflects AND transmits light. When lit dramatically, every facet, curve, and edge becomes visible.
- Strong contrast between light and shadow creates **visual tension** -- the eye is drawn to the boundary between illuminated and dark areas. This tension holds attention and communicates power, luxury, and mystery.
- The technique reduces everything to pure form and light, stripping away context. The bottle stands alone as an object of desire.

**Sub-Variations Observed in Campaigns**:

| Variation | Technique | Mood | Brand Examples |
|-----------|-----------|------|---------------|
| **Spotlight Chiaroscuro** | Single concentrated light beam on bottle against deep black or dark textured surface. Bottle tilted or angled dynamically. | Dramatic, powerful, masculine | D&G (The One on gold mosaic), Armani Code |
| **Graphic Split** | Bottle placed on a stark light/dark boundary (split background, half-and-half). Strong geometric shadow play. | Bold, modern, high-contrast | YSL Y (black/white vertical split), Armani Code Absolu (gold leaf/black split) |
| **Refraction Theater** | Extreme close-ups of light passing through glass, creating caustics, internal reflections, and color projections. Lens blur used to abstract the light patterns. | Intimate, jewel-like, hypnotic | Chanel No.5 (inverted bottle with caustics), Chanel Comete (faceted glass catching light) |
| **Textured Light Play** | Bottle on richly textured metallic or woven surface that catches and scatters light in complex patterns | Opulent, artisanal, rich | YSL Exquisite Embroidery (gold mosaic weave) |
| **Magnified Glass Physics** | Glass curvature used as lens, creating distortion, light bending, and visual drama. Bottle seen through or surrounded by glass elements | Experimental, editorial | Chanel No.5 (bottle within curved glass) |

**Key Photography Principles at Play**:
- **Light**: Low-key dominates. Single or minimal light sources. The shadows are as important as the highlights. Light quality ranges from hard (sharp shadows, defined edges) to sculpted (soft gradients on glass surfaces).
- **Composition**: Dynamic angles -- Dutch tilt, diagonal placement, extreme close-up. The bottle is often not straight; it leans, tilts, or is cropped. This breaks the expected "product on table" convention and creates energy.
- **Color**: Extremely limited -- gold/black, amber/shadow, silver/black. The bottle's own material and liquid color become the only chromatic statement against a monochrome environment.
- **Surface**: Textured surfaces (gold leaf, woven metal, rough stone) that interact with light in complex ways, creating a dialogue between the bottle's smooth glass and the environment's texture.

**Prompt Translation Patterns**:
- `dramatic chiaroscuro lighting, single spotlight from above-left illuminating the glass bottle, deep shadows enveloping the scene, the glass edges catching and bending the light into bright contour lines`
- `bottle placed on the boundary between deep black and bright gold surfaces, the glass refracting both environments simultaneously, strong graphic split composition`
- `extreme close-up of light passing through the faceted glass, golden caustic patterns dancing on the dark surface below, the glass acting as a prism`
- `bottle tilted at a dynamic diagonal angle on [textured gold / woven metallic] surface, single concentrated beam of warm light creating dramatic shadows and highlights`

### Approach 3: Lifestyle Still Life

**The Core Idea**: Place the perfume bottle within a scene of daily life -- on a vanity, beside a morning coffee, among objects of personal ritual. The bottle becomes part of a lived moment rather than an isolated product.

**WHY It Works (The Connection Principle)**:
- By placing the bottle among recognizable objects (glassware, food, fabric, books), the viewer mentally places it into their OWN life. The image answers not "what does it look like?" but "what does it feel like to own and use this?"
- Lifestyle shots create **aspiration through identification** -- unlike pure product shots that say "look at this object," lifestyle says "imagine this is your morning, your evening, your world."
- The everyday objects provide scale, context, and human presence without showing a person. A glass of wine, a silk scarf, an olive -- these are traces of a person's taste and choices.

**Sub-Variations Observed in Campaigns**:

| Variation | Technique | Mood | Brand Examples |
|-----------|-----------|------|---------------|
| **Classical Still Life** | Perfume arranged with food, glassware, ceramics in the tradition of Dutch/Italian still life painting. Warm side light, film-like grain | Timeless, cultured, sensory | Afriedlander for Armani Prive (cheese, olive, water bottle), Diptyque |
| **Sunny Lifestyle** | Bottle in bright natural sunlight with colored fabrics, on a pedestal or surface, strong natural shadows | Joyful, warm, Mediterranean | Adam Savitch for LV (Sun Song with silk scarf, bright sunlight) |
| **Indoor Sanctuary** | Bottle in a domestic interior -- on a shelf, beside candles, among books. Natural window light. | Intimate, personal, calming | Diptyque (Tam Dao indoors, Orpheon) |
| **Ingredient Landscape** | Raw ingredients arranged as if from a kitchen garden or apothecary, bottle among them. Not immersion but curation. | Authentic, artisanal, ingredient-forward | Diptyque (Orpheon ingredients, Eau Papier ingredients) |

**Key Photography Principles at Play**:
- **Light**: Natural or natural-simulating light. Window light, golden hour, warm directional. Film grain and analog color often added to reinforce the "real moment" feeling. This is the opposite of the studio precision in Approach 2.
- **Composition**: Rule of thirds or golden ratio. The bottle is important but not dominating -- it exists in relationship with other objects. Multiple focal points create a scene to explore.
- **Color**: Warm, muted, analog-feeling. Earth tones, warm ambers, natural material colors. Often desaturated slightly for a film-like quality.
- **Props**: Must feel authentic and considered -- not random objects but things that communicate a specific lifestyle and taste. Each object tells part of the story.

**Prompt Translation Patterns**:
- `still life composition in the style of classical painting, perfume bottle arranged with [a glass of amber wine, aged cheese, a green olive, a water carafe], warm side lighting, analog film grain, painterly atmosphere`
- `bottle on a [marble / linen-covered / wooden] surface in warm natural sunlight streaming from a window, casting long soft shadows, a [silk scarf / open book / ceramic cup] beside it, intimate lifestyle moment`
- `artisanal ingredient arrangement, the bottle among [raw vanilla pods, cinnamon bark, dried flowers, citrus peels] as if displayed in a perfumer's workshop, natural light, earth-toned palette`
- `indoor vanity scene, the bottle on a [brass tray / marble shelf] beside [a candle, a small vase of flowers], soft morning window light, warm muted tones, personal and intimate`

### Approach 4: Abstract & Surreal

**The Core Idea**: Place the bottle within a non-representational, conceptual environment. Sculptural forms, liquid textures, impossible physics. The bottle becomes an art object in a gallery of imagination.

**WHY It Works (The Elevation Principle)**:
- Abstraction removes the product from any recognizable context, forcing the viewer to engage with it purely as form, color, and material. This is the most "art-forward" approach.
- Surreal environments communicate **brand ambition** -- "this fragrance is not ordinary, it exists in a world of its own."
- The impossibility of the scene (glossy sculptural blobs, floating elements, unnatural physics) creates **visual fascination**. The viewer studies the image because it can't be quickly categorized.

**Sub-Variations Observed in Campaigns**:

| Variation | Technique | Mood | Brand Examples |
|-----------|-----------|------|---------------|
| **Sculptural Surrealism** | Bottle surrounded by large glossy organic forms (like liquid sculptures, blown glass, or molten material). Strong backlight creating transparency and shadow interplay | Bold, artistic, avant-garde | MFK Baccarat Rouge 540 (glossy red sculptural blobs) |
| **Material Abstraction** | Impossible textures or materials surrounding the bottle -- liquid metal, crystalline structures, geometric forms | Futuristic, niche, conceptual | High-concept fashion/niche campaigns |
| **Color Field** | Bottle placed within a monochromatic or gradient color environment with minimal other elements, the color itself creating the mood | Minimal, poetic, contemplative | Art-fashion crossover campaigns |

**Key Photography Principles at Play**:
- **Light**: Often strong backlighting to create transparency effects in the abstract elements. Light passes through materials, creating depth, shadow, and color interplay. The abstract forms themselves become light-modifiers.
- **Composition**: The bottle is central but embedded within the abstract environment. The boundary between product and art blurs. Often uses tight framing to maximize the surreal impact.
- **Color**: Typically monochromatic or very limited, derived from the bottle's own color story. The abstract elements echo and amplify the product's color (red bottle = red sculptural forms).
- **Surface**: High-gloss, reflective materials that interact with light dramatically. The shininess creates visual richness and luxury associations.

**Prompt Translation Patterns**:
- `bottle surrounded by large glossy [red/amber/gold] sculptural organic forms, like frozen liquid or molten glass, strong backlight creating dramatic shadows and transparency effects, surreal luxury still life`
- `perfume bottle emerging from an abstract landscape of [crystalline structures / liquid metal / geometric prisms], the glass bottle both belonging to and standing apart from the impossible environment`
- `monochromatic [red/gold/blue] abstract composition, the bottle as the only recognizable object within flowing sculptural forms, art-meets-commerce, gallery-quality photography`

---

## VII. Fragrance-Mood Starting Points

> **These are starting-point associations, NOT fixed recipes.** Each row describes the *default* mood for a fragrance family -- the direction most campaigns gravitate toward. Use ONE concept from this default (the "echo"), but deliberately pull at least one other concept from a DIFFERENT row's lighting or color direction (the "contrast"). For example, a woody/oriental bottle (default: dramatic, dark) shot with the Fresh/Citrus row's lighting (high-key, backlit, bright) and surface (white marble) creates an unexpected, powerful result. See Section III "Echo vs. Contrast" for the principle.
>
> **Mandatory for concept diversity**: When proposing 3 concepts, at least one must use a lighting or color direction from a DIFFERENT fragrance family row than the bottle's natural family. This single rule prevents all concepts from collapsing into the same mood.

| Fragrance Family | Default Mood | Lighting Direction | Color Direction | Surface Direction | Prompt Boost |
|-----------------|-------------|-------------------|----------------|-------------------|-------------|
| Fresh / Citrus | Bright, airy, energetic | High-key, backlit for liquid glow | White, citrus yellow, leaf green | Water, glass, white marble | `bright morning light, airy freshness, crystalline clarity` |
| Floral | Soft, romantic, warm | Warm diffused, golden hour | Blush pink, cream, gold, lavender | Silk, soft stone, petal-strewn | `romantic soft glow, warm golden light, feminine elegance` |
| Woody / Oriental | Dramatic, mysterious, deep | Low-key, dramatic side, warm gels | Deep burgundy, amber, dark gold | Dark wood, velvet, leather | `dramatic chiaroscuro, deep shadows, warm amber glow` |
| Aquatic / Marine | Cool, crystalline, serene | Cool-toned, backlit, rim lighting | Ocean blue, silver, seafoam | Water, glass, polished silver | `cool crystalline clarity, oceanic serenity, silver-blue` |
| Gourmand | Warm, indulgent, comforting | Warm golden, close and enveloping | Caramel, chocolate, vanilla, warm gold | Rich wood, warm ceramics | `warm golden indulgence, honeyed light, tactile richness` |
| Powdery / Musky | Soft, ethereal, delicate | Ultra-soft, diffused, low contrast | Nude, soft pink, pearl, champagne | Soft fabric, matte finishes | `ethereal softness, powder-soft haze, delicate luminosity` |
