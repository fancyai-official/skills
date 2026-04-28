# Model presets and prompt density (editorial six-pack)

Load this file when building **Step 4** internal prompts and when running **Image QC** items related to face, body, hair, and accessories. **Pick phrases; do not stack synonyms.**

## 1. Model preference tiers

Align with user or client sheet (matches business UI); internal prompt uses the right column **in English, pick don’t stack**.

| Option | Internal direction (example phrases—pick, don’t stack) |
|--------|--------------------------------------------------------|
| Asian female (Korean editorial face) | Korean beauty editorial face, refined bone structure, understated glam |
| Asian female (sweet, clear) | **Sweetness must match expression + makeup**; **influencer-petite face** + **Asian makeup** (JP/KR clear skin, not heavy Western contour). **Positive anchors (sweet energetic; V-line compatible)**: **oval melon-seed face, large eyes, high nose bridge**—English: `oval melon-seed face`, `delicate oval face`, `large expressive eyes` / `large doe eyes`, `high straight nose bridge` (may merge with `V-line slim jaw`, `large gentle eyes`; **don’t** stack synonyms). Also: `sweet clear skin`, `dewy fresh complexion`, `Asian beauty makeup`, `East Asian soft glam`, `influencer-style petite face`, `V-line slim jaw`, `large gentle eyes`, `aegyo-sal subtle`, `peachy pink blush`, `glossy gradient lips`, `gentle approachable expression`, `soft subtle smile` or `warm friendly eyes`, `looking at camera` with **soft** eye contact. **Hair**: **don’t** hard-code “must be pure black”; **prefer dark brown-black / near-black brown**. **Hard rule**: **no** unfounded light gold, light brown, bleached look (honey brown, honey tea, light chestnut, obvious highlights) **unless client writes light hair**. Use `dark brown-black hair`, `near-black brown hair`, `deep espresso brown`; Avoid: `honey brown hair`, `golden brown hair`, `light chestnut`, `bleached hair look`, `obvious blonde highlights`. **Avoid**: **wide round face / moon face / mature cold editorial face**; English Avoid: `round puffy face`, `moon face`, `wide round cheeks`, `chubby cheeks`, `flat wide face`, `square jaw`, `broad face`, `soft undefined features` (sweet tier pairs with **oval / V-line, large eyes, high bridge** + small face; **if user requests plus-size or round-face aesthetic, follow user**); **middle part + heavy curls / noodle waves** → replace with `youthful hairstyle`, `airy bangs or side-swept`, `straight or soft S-curl`, `high pony or half-up`; Avoid cold editorial: `stern aloof stare`, `moody high-fashion cold face`, `intimidating glare`, `mature fashion editorial bone structure` (pick, don’t stack) |
| Western female (cool editorial) | cool editorial, sharp cheekbones, distant chic |
| Western female (soft elegant) | soft elegant, warm sophisticated, graceful presence |
| I’ll specify | **First** get short written description (mood/hair/ethnic leaning), then abstract to English phrases |

## 2. Priority and exceptions

- **Priority (hard order)**: user/client **model preference** **>** step 1 brand hair/makeup norms **>** step 3 emotion; on conflict, **user’s written choice wins**.
- **If user didn’t say**: infer from brand + triple-choice and **confirm in one sentence**—don’t silently apply wrong ethnicity/mood.
- **Exception**: **male model**, **plus-size**, or other **not in table**—don’t use the five labels; follow user text + brand; still obey face/mood and eye rules in this file.

## 3. “Asian female (sweet, clear)” addendum

Failure modes: **sweet makeup / cold face**, **large mature face**, **moon face**, **middle-part big curl**, distant editorial face.

When this tier is selected, internal prompt **plus** table must enforce:

1. **Face**—**influencer-petite head scale** (matches body-proportion “small face” below); **avoid** wide square mature face, high-cheek “editorial” bone, cold supermodel structure; **moon face / too round-flat** conflicts with V-line/petite—write Avoid (`round puffy face`, etc.). **Negative references**: wide jaw, flat wide low structure, dull features, light brown side volume + heavy bangs widening face—**counter** with **oval + large eyes + high bridge** anchors, not only “pretty.”
2. **Hair**—**no** default **middle part + heavy curls**; **young, light** styles (airy/full bangs, side-part soft wave, straight, half-up, high pony), consistent set. **Hair color**: prefer dark brown-black; **hard rule** no unfounded light gold/brown/bleach unless client **writes** light hair.
3. **Makeup**—**East Asian–style**: clear base, soft brows, subtle aegyo-sal / under-eye bright, peach or coral blush, glossy lips—**not** heavy Western contour.
4. **Expression**—warm, approachable; avoid cold face from table Avoid.
5. **vs brand**: if brand is icy but client picked this tier, **client model preference wins**.
6. **Retry**: if too cold, add expression lines; if face too large/moon or hair wrong, add **small face + oval/V-line/sharp slim jaw + large eyes + high bridge + hair + Avoid**—don’t fight garment constraints.

After model tier is chosen (or user-confirmed inference), execute consistently with **Face and mood** and **Facial detail density** below; if table vs brand text conflicts, **priority** in Section 2 wins.

## 4. Eyes default (internal prompts)

**Eyes default to camera** (hard default)—write `looking at camera, eye contact` or equivalent.

## 5. Body proportions (hard rule)

**Every** internal prompt **must** include: `small face, normal natural neck length, high waist long legs, fashion model proportions`, plus picks from **`balanced head-to-body ratio`**, **`realistic adult fashion model body proportions`**, **`elongated leg line`**, **`long legs in natural proportion`** (full body / three-quarter especially—avoid legs cropped away).

**Also** Avoid semantics: `big head`, `oversized head`, `disproportionate head`, `chibi proportions`, `Q-version body`, `long neck`, `giraffe neck`, `short legs`, `stubby legs`, `tiny legs`. Target: **small face**, **natural neck**, **high waist long legs**, **normal head-to-body (not bobblehead, not stubby)**. **Common failure**: big head + short legs—**rerun that frame only** and reinforce required phrases. **Chest-up** may enlarge face—add `head size proportional to shoulders`, `slender neck`, still consistent with `small face`.

## 6. Face and mood

Model **looks good**, alive; **makeup/mood follow brand** (step 1); **makeup allowed**; **garment hero**; avoid grease, stare, duck lips. **When tier is “Asian female (sweet, clear)”**: match **Section 3**—**to camera** still **warm, soft**—don’t read “editorial” as **cold, zero sweetness**.

## 7. Facial detail density (hard rule)

**Default no moon face** (sweet tier: **oval / V-line, large eyes, high bridge** + **Avoid**; **if user writes plus-size/round aesthetic, follow user**). Like **outfit density**—**each** internal prompt **fills**: **no** only `beautiful Asian woman`, `pretty face`, `generic model face`. **No** only `delicate refined facial features`, `natural beauty`, `soft features` without **concrete face/eyes/nose/lips**—else random samples yield **moon face, light hair, bare lifestyle face** (fail sweet tier → **Image QC** rerun).

**Must state**:

1. **Face shape** + **Avoid** (anti-moon); sweet tier anchor **oval** (`oval melon-seed face`, etc.) + **V-line** (may say “same Avoid as table”).
2. **≥3 feature lines** from eyes/nose/lips/brows/aegyo-sal—**eyes/nose** should hit **large eyes**, **high bridge**.
3. **Skin**—one line (dewy, matte, etc.).
4. **Hair color + style + Avoid**—same as Section 1 table / Section 3 (may say “same hair hard rule as table”).
5. **Makeup ≥2 specifics**—brow, blush, lip, base.

For **magazine-cover sweet energy**, may add `model-tier beauty`, `magazine cover quality` **with** the five—**not** instead of them. **All five required**; verify in **Image QC item 4**.

## 8. Body, eyes, pose; outfit visibility

- Natural walk, weight shift; hands with **extras** (sunglasses, coffee, hem/collar); **default no bags**.
- **Pose variety** frames 2–6 vs frame 1: **stand / sit / lean / walk**—see [reference-pose-vocabulary.md](reference-pose-vocabulary.md) (**Usage**, Section 6).
- **Outfit visibility** seated/full/lean—see [reference-outfit.md](reference-outfit.md) Section 7.
- **Eyes** mostly to lens; side body OK, eyes toward camera; **frame 4** front variation, to camera.

## 9. Limbs and anatomy

Complete limbs; five fingers; crop sensibly; **shoes on feet**; no extra/floating shoes, hand–shoe fusion; don’t prompt `holding shoe...` unless client asks.

## 10. Outfit and extras (good-looking)

- **Outfit (good-looking)**: required vocabulary + density; **hero unchanged**; cohesive extras; default no bag/jewelry words unless written.
- **Extra accessories**: default **no bags**; no earrings/necklace unless **written**; cohesive hat/glasses/headphones; don’t block product; not every frame max props; kids/Excel follow sheet.

## 11. Composition and scale (apparel-first)

- **Large subject in frame**; **upper-body priority** for tops but vary scale; frame 3 full when pants/shoes matter.
- **Frame 5 “half-body”** = **three-quarter / mid-thigh**, not tight chest-only—`three-quarter shot, mid-thigh crop, outfit full visibility, waist and pockets visible`.
