<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 14种风格完整提示词模板库

> 每种风格提供：**六层结构模板**（含占位符）+ **填充说明** + **增强关键词**
>
> 占位符说明：
> - `{product_name}` — 产品精确英文名（如：wireless earbuds, hair dryer, robot vacuum）
> - `{main_color}` — 产品主色（如：matte black, pearl white, champagne gold）
> - `{material}` — 主体材质（如：matte plastic, brushed aluminum, glossy ABS）
> - `{brand_color}` — 品牌色（如：deep purple, forest green, coral red）
> - `{accent_color}` — 点缀色/发光颜色（如：cyan blue, warm amber, electric green）

---

## DARK — 极致暗调质感

**适用**：黑色科技产品、耳机、音箱、剃须刀

**六层结构**
```
[主体] {main_color} {product_name}, {material} surface with microscopic texture detail
[背景] pure matte black background, deep shadow gradient
[光影] single cold white spotlight from upper-left at 45°, crisp hard shadow, subtle rim light on edges
[材质] {material} body catching specular highlights, fine surface grain visible
[构图] centered floating composition, slight 3/4 angle rotation, product shadow below
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
Matte black {product_name} with {material} surface and microscopic texture detail, pure matte black background with deep shadow gradient, single cold white spotlight from upper-left at 45° creating crisp hard shadow and subtle rim light on edges, specular highlights catching on {material} body showing fine surface grain, centered floating composition at slight 3/4 angle rotation with product shadow below, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## WAVE — 声波/气流可视化

**适用**：耳机、音箱、空气净化器、吹风机、风扇

**六层结构**
```
[主体] {product_name} in {main_color}
[背景] dark gradient background transitioning from near-black to deep {brand_color} or charcoal
[光影] multiple concentric glowing wave rings or airflow particle trails emanating from the product, bioluminescent blue-cyan glow, soft ambient fill
[材质] {material} product body sharp and crisp at center, motion blur on surrounding wave elements
[构图] product centered, waves radiating outward in all directions, extreme depth of field
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} surrounded by glowing concentric sound wave rings and particle trails emanating outward, dark gradient background from near-black to deep charcoal, bioluminescent cyan-blue waves glowing with soft ambient fill, {material} product body sharp and crisp at center with motion-implied wave elements in motion blur, product centered with waves radiating symmetrically in all directions, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## SPLASH — 水花定格防水

**适用**：耳机、运动相机、吹风机、防水小家电

**六层结构**
```
[主体] {product_name} in {main_color}
[背景] clean white or light cyan background, or dramatic dark studio gradient
[光影] frozen water crown splash surrounding the product, ultra-high-speed freeze-frame, water droplets catching studio light
[材质] {material} product surface wet with water droplets, IPX waterproof visual metaphor
[构图] product centered slightly below water splash crown, low angle or eye-level, symmetrical water explosion
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} at the center of an exploding water crown splash frozen in ultra-high-speed freeze-frame, clean white studio background, water droplets catching bright studio light creating crystalline highlights, {material} product surface wet with fine water droplets conveying IPX waterproof capability, product centered slightly below the symmetrical water explosion crown at low angle, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## WHITE — 纯白极简电商

**适用**：全品类通用，尤其厨电、美容仪、白色产品

**六层结构**
```
[主体] {product_name} in {main_color}, clean and pristine
[背景] pure white seamless background, soft infinite white backdrop
[光影] classic three-point lighting setup: key light from upper-left, fill light from right, rim light from behind, soft diffused shadows
[材质] {material} surface showing subtle material texture, clean product edges
[构图] product centered or slightly right-of-center, slight 3/4 rotation, floating minimal shadow below
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} clean and pristine, pure white seamless infinite white backdrop, classic three-point lighting with soft key light from upper-left fill light from right and subtle rim light from behind casting soft diffused shadow, {material} surface showing subtle texture with clean sharp product edges, product centered at slight 3/4 rotation with minimal floating shadow below, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## SCENE — 户外自然生活美学

**适用**：厨电、家居小电、美容仪、咖啡机（KV大片必须使用户外场景）

**六层结构**
```
[主体] {product_name} in {main_color} as the hero of an outdoor nature scene
[背景] outdoor natural setting — morning misty mountain stone platform / coastal rocky shore at golden sunrise / beside a clear mountain stream in birch forest / alpine meadow at dusk — with natural complementary elements
[光影] warm golden hour sunlight or crisp cool daylight from one side, long soft shadow, natural atmospheric glow
[材质] {material} product surfaces catching warm outdoor golden light or cool natural daylight
[构图] product on natural stone/rock surface in foreground, scenic outdoor environment softly blurred in background, rule-of-thirds placement
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} as the hero placed on flat natural stone surface in a morning misty mountain setting, warm golden sunrise light streaming from the right side casting a long soft shadow leftward with warm amber glow on {material} product surface, mossy rock and mountain stream in soft bokeh background, product sharp in foreground following rule of thirds with natural outdoor atmosphere, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## COSMOS — 宇宙/自然宏大场景

**适用**：高端旗舰产品、发布会主视觉、手表、耳机

**六层结构**
```
[主体] {product_name} in {main_color}, appearing small yet significant
[背景] epic natural or cosmic landscape — massive glowing planet, Milky Way galaxy, towering mountain canyon, or deep space — creating grand scale contrast
[光影] ambient cosmic light with single dramatic directional source, product rim lit by distant celestial glow
[材质] {material} catching faint cosmic ambient light, surface detail preserved
[构图] product occupying 15-25% of frame to emphasize epic scale, centered or lower-third, vast environment dominates
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} floating or resting small yet significant against an epic backdrop of a massive glowing planet and Milky Way galaxy above a mountain range silhouette, ambient cosmic blue-purple light with single directional celestial glow rim-lighting the {material} product surface, product occupying 20% of frame centered against the vast cosmic environment conveying grand scale, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## TECH — AI科技未来感

**适用**：智能设备、扫地机器人、AI音箱、智能家电

**六层结构**
```
[主体] {product_name} in {main_color} with glowing status indicators
[背景] dark background with floating holographic blue data particles, wireframe grid floor, circuit board patterns
[光影] cool blue-cyan ambient glow from floating particles, electric blue rim light on product edges, subtle lens flares
[材质] {material} product reflecting blue holographic particle light on its surface
[构图] product centered slightly low, particles and data streams flowing diagonally around it
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} with glowing status indicators centered on a dark background with floating holographic blue-cyan AI data particles and subtle wireframe grid floor, cool blue-cyan particle ambient glow with electric blue rim lighting on product edges and subtle lens flares, {material} surface reflecting holographic particle light, product centered slightly low with data streams and particles flowing diagonally around it, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## STONE — 岩石/自然陈设

**适用**：手机、中高端小家电、手表、投影仪

**六层结构**
```
[主体] {product_name} in {main_color}
[背景] natural rock formation or stone platform setting — desert sandstone / volcanic basalt / limestone plateau — with warm amber or cool grey tones
[光影] warm afternoon sun at low angle, casting long product shadow, golden rim light on product edges
[材质] {material} product contrasting against rough natural stone texture, {main_color} popping against earthy stone
[构图] product placed on prominent stone surface, rock foreground frame, atmospheric background landscape
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} resting on prominent flat desert sandstone rock, natural rock formation landscape with warm amber earthy tones and distant desert terrain, warm low-angle afternoon sun casting long product shadow with golden rim light catching {material} product edges, {main_color} product contrasting against rough natural stone texture, rock foreground framing with atmospheric hazy background landscape, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## COLOR_ECHO — 颜色呼应/品牌色宇宙

**适用**：有鲜明品牌色的任何产品

**六层结构**
```
[主体] {product_name} in neutral {main_color} or {brand_color}
[背景] monochromatic {brand_color} tonal world — sand dunes, hills, water, sky all in harmonious {brand_color} color family
[光影] soft diffused ambient light matching {brand_color} tone, minimal hard shadows, dreamlike quality
[材质] {material} product in {main_color} contrasting against {brand_color} environment through material difference rather than color
[构图] product on small rock island or pedestal in center of {brand_color} landscape, water reflection present
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} resting on a rocky island surrounded by {brand_color} tonal world — {brand_color} still water, {brand_color} rolling sand dunes, {brand_color} gradient sky all in harmonious color family, soft diffused {brand_color} ambient light with minimal hard shadows creating dreamlike quality, {material} product contrasting against {brand_color} environment through material texture difference, product centered on rock island with perfect {brand_color} water reflection, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## LIFESTYLE — 人物局部互动

**适用**：耳机、手表、美容仪、手持设备、挂脖风扇

**六层结构**
```
[主体] {product_name} in {main_color} being worn or held by human partial body
[背景] lifestyle environment — city street / gym / cafe / bedroom — soft bokeh
[光影] natural ambient light or warm window light, soft skin tone rendering
[材质] {material} product detail visible at close range, skin texture contrast against product surface
[构图] partial human body (hands/wrists/ears/neck only — no face), product as focal point, 50-85mm portrait depth of field
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} being worn on wrist / held in hand / worn on ears — partial human body shot with no face visible — in soft bokeh lifestyle environment of modern city street or cozy interior, warm natural ambient light with gentle skin tone rendering, {material} product detail sharp at close range contrasting against human skin texture, partial body composition with product as focal point at 50-85mm portrait depth of field, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## PORTAL — 圆环/窗框舞台感

**适用**：净化器、耳机、音箱、圆形/竖形产品

**六层结构**
```
[主体] {product_name} in {main_color} standing inside or framed by a circular ring structure
[背景] glowing circular ring/portal framing the product, through the ring reveals a different world — cosmic scene, nature landscape, or abstract light field
[光影] ring emitting ambient glow that illuminates the product from multiple directions, volumetric light rays
[材质] {material} product picking up ring glow color, surface highly polished or matte depending on product
[构图] product perfectly centered within ring frame, ring occupying 60-70% of frame width, dramatic forced perspective
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} standing perfectly centered within a glowing luminous circular ring portal, through the ring reveals a breathtaking cosmic nebula or alpine landscape beyond, ring emitting warm or cool ambient glow illuminating the {material} product surface with volumetric light rays, product and ring centered occupying dramatic forced perspective with ring at 65% frame width, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## EXPLOSION — 动态爆发力量感

**适用**：运动耳机、剃须刀、旗舰扫地机、手表

**六层结构**
```
[主体] {product_name} in {main_color}, perfectly static and pristine at explosion center
[背景] material-appropriate explosion — sand/dust vortex, ice shards, metallic fragments, electrical sparks — radiating from product center
[光影] dramatic studio lighting from above, explosion elements catching and scattering light, product remains perfectly lit
[材质] {material} product surface immaculate and sharp despite surrounding chaos, tiny debris/particles landing on edges
[构图] product dead center, explosion radiating symmetrically outward, slight overhead or straight-on angle
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} perfectly static and pristine at the dead center of a powerful {material}-themed explosion — sand vortex and flying rock debris or ice shards radiating symmetrically outward — dramatic studio overhead lighting scattering through explosion elements, {material} product surface immaculate and sharp amid surrounding chaos with tiny particles landing on edges, product centered with explosion radiating outward in slight overhead angle, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## MATERIAL_SCENE — 材质呼应户外陈设

**适用**：强调工艺/材质的旗舰产品、高端厨电、手表

**六层结构**
```
[主体] {product_name} in {main_color} with prominent {material} material story
[背景] outdoor natural stone platform or mountain summit flat rock, featuring natural material elements — weathered granite, river-smoothed slate, rough basalt slab — telling a material narrative against an outdoor landscape
[光影] warm late-afternoon directional sunlight from one side emphasizing material texture and reflectivity, long outdoor shadow
[材质] hero material ({material}) contrasting against rough outdoor stone surface — unified natural material world
[构图] product as dominant centerpiece on flat outdoor rock surface, natural landscape in soft bokeh background, slight 3/4 angle
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} with prominent {material} material story as dominant centerpiece on a broad flat weathered granite rock platform outdoors, surrounded by complementary natural material objects — smooth river stones, rough basalt fragments, dried alpine grass — unified in a natural material narrative, warm late-afternoon directional sunlight from the right emphasizing {material} texture and reflectivity with long outdoor shadow, misty mountain or desert landscape in soft bokeh background, product as hero at slight 3/4 angle, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## FLAT_CONTEXT — 俯拍生活故事

**适用**：耳机、便携设备、手机配件、小型家电

**六层结构**
```
[主体] {product_name} in {main_color} as hero of a curated flat lay
[背景] clean neutral surface (white marble, light wood grain, concrete) with lifestyle context props arranged around product
[光影] even overhead diffused daylight from above, minimal hard shadows, fresh and clean look
[材质] {material} product surface crisp and detailed against flat surface texture contrast
[构图] perfect overhead/top-down shot, product at golden ratio position or slightly off-center, props arranged to tell target user's lifestyle story
[规格] Unreal Engine 5 / Octane render, hyperrealistic 3D CGI product visualization, every physical product detail precisely rendered (buttons / logo / LED / surface grain), ambient occlusion + realistic ground shadow + environmental catchlights on product, cinematic shallow DOF sharp product blurred BG, volumetric haze, 8K commercial photography award-winning no text no watermarks
```

**完整示例**
```
{product_name} in {main_color} as hero of a carefully curated flat lay on clean white marble or light oak wood surface, surrounded by lifestyle context props — coffee mug, notebook, plants, keys — arranged to tell a {target_user} lifestyle story, even overhead diffused daylight from above with minimal hard shadows creating fresh and clean look, {material} product surface crisp and detailed contrasting against flat surface texture, perfect overhead top-down shot with product at slightly off-center golden ratio position, Unreal Engine 5 Octane render hyperrealistic 3D CGI product visualization every physical product detail precisely rendered ambient occlusion realistic shadow environmental catchlights cinematic shallow DOF volumetric haze 8K award-winning no text no watermarks
```

---

## 快速检索表

| 风格 | 关键视觉动词 | 核心环境名词 | 主要光源 |
|---|---|---|---|
| DARK | floating, crisp | black void, studio | cold spotlight |
| WAVE | radiating, pulsing | dark gradient, particles | bioluminescent glow |
| SPLASH | exploding, frozen | water crown, droplets | studio strobe |
| WHITE | clean, pristine | white seamless, infinite | three-point studio |
| SCENE | resting, living | kitchen, bedroom, bathroom | warm window light |
| COSMOS | dwarfed, epic | planet, galaxy, canyon | celestial ambient |
| TECH | glowing, data-flowing | grid, hologram, particles | cyan blue ambient |
| STONE | placed, grounded | sandstone, volcanic rock | warm afternoon sun |
| COLOR_ECHO | harmonizing | color dunes, tonal water | soft diffused |
| LIFESTYLE | worn, held | street, gym, café | natural ambient |
| PORTAL | framed, revealed | ring portal, alternate world | ring glow |
| EXPLOSION | static-at-center | sand vortex, ice shards | overhead dramatic |
| MATERIAL_SCENE | curated, tactile | material props, tabletop | directional studio |
| FLAT_CONTEXT | arranged, storytelling | flat lay, neutral surface | overhead daylight |
