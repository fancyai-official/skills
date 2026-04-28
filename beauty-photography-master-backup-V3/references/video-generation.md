# Phase 5: Video Ad Generation

After the user is satisfied with the campaign image set, offer to create a short cinematic video ad.

Ask:

```markdown
Generate a short video ad from the selected campaign images?

- Yes, generate video
- No, skip
```

If yes, let the user pick which campaign image should be used as the video's first frame:

```markdown
Which campaign image should become the video's first frame?

- Shot 1: Hero
- Shot 2: Detail
- Shot 3: Environment
- Other selected campaign image
```

## Video Motion Prompt

Construct a motion-focused prompt that describes camera movement, lighting animation, environmental motion, and product fidelity.

```markdown
{camera movement} shot of the selected product campaign image.
Preserve the product's exact silhouette, closure geometry, material, label placement, and luxury set design from the first frame.
{lighting animation}. {environmental motion}.
Cinematic beauty commercial, luxury fragrance advertisement, smooth motion, professional color grading, premium campaign finish.
```

## Camera Movement Options

- **Slow dolly zoom in**: slow push-in that emphasizes product detail
- **Gentle orbit around**: subtle camera arc that reveals dimensionality
- **Slow pull-back reveal**: starts close, then reveals the full set
- **Static with subtle parallax**: premium stillness with micro-depth movement
- **Crane down**: downward reveal that feels dramatic and editorial

## Lighting Animation

- Golden light slowly shifting across the glass or packaging surface
- Soft caustics dancing on nearby marble, water, or reflective surfaces
- Light gradually transitioning from cool to warm
- Rim light subtly tracing the bottle or container edge
- Highlight line gliding across the cap, label, or curved body

Match the lighting physics to the product material. Do not describe caustics or transmission for frosted, matte, ceramic, or opaque packaging.

## Environmental Motion

- Particles floating gently in the air
- Petals drifting slowly through the frame
- Water ripples expanding outward
- Silk fabric undulating in a gentle breeze
- Mist swirling around the base
- Subtle shadow movement from leaves, curtains, or sculptural props

## Generation Guidance

Generate a short video from the selected campaign image as the first frame. Keep motion elegant and restrained; the product should remain stable, recognizable, and premium.

Recommended defaults:

| Setting | Recommendation |
|---------|----------------|
| Duration | 3-5 seconds |
| Aspect ratio | Match the selected campaign image |
| Variants | 1-2 options unless the user asks for more |
| Motion intensity | Low to medium; avoid chaotic movement |

## QA Before Presenting

Review the video before showing it:

| Check | What to verify |
|-------|----------------|
| Product identity | Product remains recognizable throughout |
| Shape stability | Bottle/container does not melt, stretch, or morph |
| Closure fidelity | Cap, pump, stopper, or lid remains consistent |
| Label stability | Label does not drift unnaturally; minor AI text changes may be acceptable |
| Motion quality | Camera movement is smooth and premium |
| Material truth | Light behavior matches the product material |

If the product shape changes significantly, regenerate with stronger fidelity language and calmer motion.

## Presentation

Show the final video result as playable media or a link, plus a one-sentence creative description. Do not expose generation internals, tool parameters, temporary URLs, request IDs, raw logs, or provider details.
