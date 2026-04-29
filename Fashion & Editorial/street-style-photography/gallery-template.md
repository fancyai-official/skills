# Street Gallery Template

Use this template to compile the final `STREET_GALLERY.md` deliverable. The shot names and count are flexible — fill in whatever 4 (or 5) shots were actually selected from the 12-type vocabulary.

---

```markdown
# Street Gallery: [Project Name]

**City**: [New York / London / Milan / Paris / Florence]
**Neighborhood**: [Specific micro-location]
**Season**: [Spring/Summer or Fall/Winter] [Year]
**Gender**: [Womenswear / Menswear]
**Time of Day**: [Daytime / Blue Hour / Golden Hour / Night / Mixed]
**Location**: [Selected spot from Step 2]
**Input Type**: [Type 1: Product Only / Type 2: Product + Model / Type 3: Model Wearing Garment]
**Reference Images**: [Type 1: `product.png` / Type 2: `product.png` + `model.png` / Type 3: `lookbook.png`]
**Model Persona**: [Type 1: auto-cast description / Type 2: locked from model image / Type 3: kept from input or new cast]
**Shot Selection**: [List the 4 chosen types and one-line reasoning, e.g. "Detail → Full Look → Through-Crowd → Laughing Candid — craft first, then context, then crowd energy, then human warmth"]

---

## The Set

### 1. [Shot Type Label]
![Shot 1](outputs/street_1_[shot_type].png)

**City Metadata**: Shot on [lens], [Neighborhood], [City] | [Time of Day] | Fujifilm X-T5
**Eye Line**: [direction] | **Composition**: [key compositional element of this shot]

---

### 2. [Shot Type Label]
![Shot 2](outputs/street_2_[shot_type].png)

**City Metadata**: Shot on [lens], [Neighborhood], [City] | [Time of Day] | Fujifilm X-T5
**Eye Line**: [direction] | **Composition**: [key compositional element of this shot]

---

### 3. [Shot Type Label]
![Shot 3](outputs/street_3_[shot_type].png)

**City Metadata**: Shot on [lens], [Neighborhood], [City] | [Time of Day] | Fujifilm X-T5
**Eye Line**: [direction] | **Composition**: [key compositional element of this shot]

---

### 4. [Shot Type Label]
![Shot 4](outputs/street_4_[shot_type].png)

**City Metadata**: Shot on [lens], [Neighborhood], [City] | [Time of Day] | Fujifilm X-T5
**Eye Line**: [direction] | **Composition**: [key compositional element of this shot]

---

### 5. [Optional Variant Shot — only if a 5th was needed]
![Shot 5](outputs/street_5_[shot_type].png)

**City Metadata**: Shot on [lens], [Neighborhood], [City] | [Time of Day] | Fujifilm X-T5
**Eye Line**: [direction] | **Composition**: [key compositional element of this shot]

*(Delete this section if only 4 shots were taken.)*

---

## Product Reference

| Attribute | Detail |
|-----------|--------|
| **Product Type** | [e.g., Oversized wool coat] |
| **Fabric** | [e.g., Heavyweight brushed wool, matte finish] |
| **Color** | [e.g., Camel / Bone White] |
| **Silhouette** | [e.g., Oversized, drop shoulder, mid-calf length] |
| **Key Details** | [e.g., Horn buttons, patch pockets, notch lapel] |

---

## Location & Technical

| Element | Direction |
|---------|-----------|
| **Micro-Location** | [Full location description] |
| **Lighting** | [Lighting description] |
| **Street Texture** | [Background elements] |
| **Photographer Style** | [Referenced photographer and approach] |
| **Camera** | Fujifilm X-T5 / Canon EOS R5 (digital, natural color science, no film grain) |
| **Lens Range** | [List actual lenses used based on shots selected] |

---

## Street Clip (Optional)

[If generated:]

![Street Clip](outputs/street_clip.mp4)

**Clip Metadata**: 5-second slow-motion vertical (9:16) | [Neighborhood], [City] | Model walking past camera | Shallow DOF

[If not generated:]

*No street clip requested for this gallery.*

---

## Generation Log

| # | Shot Type | `--type` | File | Status |
|---|-----------|----------|------|--------|
| 1 | [Shot Type Label] | `[shot_type]` | `street_1_[shot_type].png` | [Generated / Regenerated] |
| 2 | [Shot Type Label] | `[shot_type]` | `street_2_[shot_type].png` | [Generated / Regenerated] |
| 3 | [Shot Type Label] | `[shot_type]` | `street_3_[shot_type].png` | [Generated / Regenerated] |
| 4 | [Shot Type Label] | `[shot_type]` | `street_4_[shot_type].png` | [Generated / Regenerated] |
| 5 | [Shot Type Label or —] | `[shot_type]` | `street_5_[shot_type].png` | [Generated / Skipped] |
| — | Street Clip | — | `street_clip.mp4` | [Generated / Skipped] |
```
