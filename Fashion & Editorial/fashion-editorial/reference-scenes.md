# Scenes: MLB types and layered light (combined reference)

This file merges the original **MLB requirements sheet scene summary** with the **scene layering / lighting vocabulary**: the first half covers **scene types and taboos** from the requirements sheet; the second half covers **how the frame is built**—foreground / midground / background, light direction, materials, depth of field. They complement each other; scene choice must follow the main Skill: **natural light / sunny feel, airy, slightly higher saturation**; by default avoid luxury hotel lobbies and symmetrical office elevator halls (unless the client requests otherwise).

---

## MLB requirements sheet — scene summary

Source: user’s local MLB requirements workbook (spreadsheet columns **required scene** + production notes in **delivery rhythm / cautions**). For **internal** reference when picking scenes for the 6 frames; if a specific SKU sheet conflicts, follow that job’s sheet. **Layering, light, DoF, and other “scene diagram” wording** is in the lower half of this file, **“Scene diagram: layering and light vocabulary”**, complementing the **types + taboos** above.

### Quick reference (align first)

**High-frequency scenes**: street / urban, Instagram café inside/out, dessert shop, luxury car / G-Wagen / yacht / airport / cabin, stadium / music festival, seaside / beach / pool, parking lot, elevator, pedestrian bridge / stairs, terrace coffee, etc.

**Common taboos**: no European architecture; background not too empty; no garbled / Korean / English signage; some jobs forbid zebra crossings; avoid unrelated street signs / manhole covers / etc. (per job line).

---

### High-frequency scene types (mixable; rewrite into prompt)

- **Street / urban**: Korean-style street, Instagram storefront, city road (many sheets say **no zebra crossing**), urban architecture, parking lot, curbside café, city walk, clean urban (no pedestrians), wide-aperture street-photo feel.
- **Coffee / dessert**: influencer café **doorway** or **inside/outside**, Instagram café, dessert shop front, café floor-to-ceiling glass, terrace café (distant buildings), **seaside / small-town** café door, elevator inside/outside (as background).
- **Car / travel / mobility**: luxury car / G-Wagen beside or on roof, getting-in motion, sports car (if color too loud, switch to white/yellow), airport departures level, inside aircraft cabin, yacht / harbor, poolside.
- **Sports / vacation**: stadium spectating, baseball/tennis vibe, music festival, summer beach/island, sand, yacht deck, stadium.
- **Other**: record store inside/outside, gas station, music festival, bridge/stairs, stadium, elevator, poolside orange/coconut and other summer props.

### Global taboos (recurring in sheet)

- **Architecture**: no **European classical** buildings; background **not too empty**.
- **Text**: no **garbled** text, no **Korean**, no **English signage**; no unrelated **street signs / manhole covers / plaques / text / QR codes** (per job line).
- **Props**: no props that clash with the scene (e.g. **oil painting**); **children must not hold coffee**; adults may have coffee/phone but **not the same handheld prop in every frame**.
- **Other**: zebra crossing often explicitly forbidden; some jobs forbid chairs / raw-wood chairs / green cast, etc. (follow that line’s **required scene**).

### Adults / children / DX (write into internal prompt with the scene)

- **Adults**: Korean-style female model; may drink coffee / use phone; **no big laugh** (neutral or slight smile); no arms wide open; no heart/V/peace/wave poses; sunglasses **not covering face in all 4 frames** (often ~3 frames with face visible); tone not too yellow.
- **Children**: ages 8–12, sweet, airy-bangs long hair; no big laugh showing teeth; no hands in pockets; no coffee; no heart/V/peace; background not too dark; not cut off from subject; no white edge framing.
- **DX**: outdoor/sporty tilt; sweet female / natural male; **no sunglasses**; logo toward camera, clear; on profile, face not full 180°—show part of the other side; often need **at least one frame of upper-body logo detail**.

### How to use MLB

When generating: align with **quick reference** above, then pick **one** sub-type below closest to the user’s triple-choice; concretize as “café doorway + road,” “street depth + railing,” etc.; fold taboos into **internal** negative or constraint sentences; **do not** dump the full text to the user.

**Link to `editorial-fashion-six`**: the sheet may still list “elevator,” but that Skill **by default avoids** pure **business elevator lobby / hotel lobby** symmetrical compositions (see that Skill step 1 and 5). When client Excel explicitly asks for elevator, follow **that job**; otherwise prefer outdoor, street, coffee lifestyle, etc., over cold office corridors.

---

## Scene diagram: layering and light vocabulary

For **internal** English prompts in `editorial-fashion-six`, to fix **empty, flat, single-wall** backgrounds. Complements **MLB** above: **MLB** = sheet **types and taboos**; **this section** = **how the frame grows**—foreground / midground / background, light, materials, DoF. Scene choice still obeys MLB taboos and the main Skill.

### 1. How to use

1. From triple-choice and MLB quick reference, **lock a scene family** (café terrace, waterfront, stadium edge, etc.).
2. **Split into three layers**: at least **one** recognizable element each; avoid only `blur background`.
3. Add **one light line**: direction + hardness + time-of-day feel (see §3).
4. Taboos still in constraints: **no garbled signage, no European classical façade, no unrelated large text**, etc. (full MLB above).

### 2. Spatial layers (English phrases, pick and combine)

| Layer | Role | Example phrases |
|------|------|-----------------|
| **Foreground** | Frame, depth | `foreground railing or planter`, `blurred leaves in front`, `glass reflection edge`, `bokeh street lamp` |
| **Midground** | Subject zone, context | `midground cafe terrace seating`, `parked cars soft blur`, `boardwalk wooden planks`, `stadium seating blur` |
| **Background** | Skyline / sea / blocks, not competing | `distant city skyline haze`, `horizon line over water`, `soft hills in far background`, `layered buildings atmospheric perspective` |

Whole-sentence option: `layered composition, foreground midground background separation, environmental depth, rich scene details`.

### 3. Light and time

| Intent | Phrases |
|------|---------|
| Bright and airy (default) | `bright natural daylight`, `soft sunlight`, `clear airy light` |
| Golden hour | `soft golden hour light`, `warm low sun rim light` |
| Side light, sculpting | `directional side sunlight`, `soft shadows defining form` |
| Overcast soft (still bright, not muddy) | `soft overcast but bright`, `even illumination, not muddy gray` |
| Window light indoors | `large window light`, `soft daylight from window, interior lifestyle` |

Avoid conflicting with main Skill unless brand/user asks low-key: `dark moody`, `flat gray studio`, `underexposed`.

### 4. Ground and “footing”

Add realism: state **what is underfoot** so the subject does not float.

- `urban sidewalk concrete texture`, `wooden deck planks`, `sand with subtle footprints`, `parking lot asphalt with painted lines`, `court rubber surface`  
- When sheet forbids zebra crossing as hero, do not write `zebra crossing as main focus`.

### 5. Layer “recipes” by scene type (templates)

Structural templates; swap nouns per brand and MLB type.

| Scene family | Foreground | Midground | Background |
|--------------|------------|-----------|------------|
| Instagram café terrace | Soft greenery edge, outdoor chair back corner | Glass door reflection, wood deck dining | Street depth, soft pedestrian blur |
| Waterfront boardwalk | Wood railing, rope | Planks, subject stance | Sea, horizon |
| Urban street | Curb / shop window corner | Building façade verticals | Layered blocks |
| Stadium / sports edge | Fence grid blur | Track or grass edge | Stands or sky |
| Rooftop skyline | Glass rail reflection | Terrace paving | City silhouette |
| Parking (clean) | Column perspective | Soft ground markings | Distant massing |

### 6. Materials and mood (short)

`warm wood`, `brushed metal railing`, `painted stucco wall`, `glass curtain reflection`, `woven outdoor furniture`, `terracotta planter`, `salt air haze` — pick 1–2, do not stack.

### 7. DoF and photo feel

`shallow depth of field`, `soft bokeh circles`, `subject sharp background creamy blur`, `editorial environmental portrait`, `high-end commercial location photography` — with **large subject in frame**, background **rich but blurred**, not competing with garment.

### 8. Vs. delivering “scene plates” only

This Skill outputs **on-location fashion portraits**; if the client wants **empty location plates** (no model), that is outside the default workflow—call it out separately. Internally you may still use the table to **abstract layers** for empty-scene prompts, aligned with the job.
