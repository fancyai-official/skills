<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 参考图视觉公式库

> 来源：对 `参考/` 文件夹中实际商业大片的逐帧提炼，共分析 21 张高质量渲染图。
> 每条视觉公式包含：背景特征、光影方案、构图要点、适配产品、可直接复用的英文快速模仿提示词。

---

## 通用质量基底词（Quality Foundation Keywords）

> **每个视觉公式的快速模仿提示词末尾必须追加以下基底词，原样追加，不可删减。**
> 这些关键词来自参考图精致度的核心来源：Octane CGI 渲染质感 + 产品本体细节精准度 + 场景-产品物理融合。

```
Unreal Engine 5 Octane render style, hyperrealistic 3D CGI commercial product visualization, every physical detail of the product precisely rendered including buttons textures logos and surface grain, ambient occlusion, product casting realistic soft shadow on surface, subtle environmental light reflections and catchlights on product body, cinematic shallow depth of field with razor-sharp product and gently blurred background, volumetric atmospheric haze in the scene, seamlessly integrated product no floating pasted-on look, 8K resolution ultra-detail, award-winning commercial photography, no text no watermarks
```

> **构图独立原则**：只学习参考图的光影方向、材质表现、场景氛围，构图/角度/产品摆放必须完全重新设计，绝对不能复制参考图布局。

---

## 公式一：峡谷悬浮水镜（CANYON_FLOAT）

**视觉特征**
- 橙红色或深灰色砂岩峡谷两侧夹道，形成天然框架
- 产品悬浮于峡谷中央偏低位置，映出完整水面倒影
- 低角度仰拍，天空露出渐变暖橙/玫瑰金色日落光
- 绝对静止的水面铺满画面下半部

**适配产品**：智能手表、手环、TWS 耳机、小型智能设备

**对应 SKILL 风格代号**：`STONE` / `COSMOS`

**快速模仿提示词**
```
{product_name} floating levitating in mid-air inside a narrow sandstone canyon gorge, towering terracotta red rocky canyon walls flanking both sides, warm orange sunset sky visible at top, perfectly still dark water below creating mirror reflection of the product, low angle upward view, cinematic depth of field, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式二：星空黑沙丘水镜（STARRY_DUNE）

**视觉特征**
- 深藏青蓝星空占据画面上 60%，满天星点
- 产品立于黑色丝绒质感沙丘峰脊，沙丘曲线极度流畅
- 画面下方有平静水面，完整映出产品和星空
- 整体色调深蓝+冷黑，无暖色，科技感极强
- 竖构图为主，产品居中

**适配产品**：旗舰手机、黑色智能设备、智能音箱、TWS 耳机充电盒

**对应 SKILL 风格代号**：`DARK` / `COSMOS`

**快速模仿提示词**
```
{product_name} standing upright on the crest of dark silk-like black sand dunes, deep indigo starry night sky filled with thousands of stars above, calm reflective dark water in the foreground perfectly mirroring both the product and the stars, cool blue-black color palette, long exposure atmosphere, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式三：暖沙漠宏观陈设（DESERT_VAST）

**视觉特征**
- 大画幅广角镜头，产品尺寸相对场景较小，突出"渺小感"
- 沙漠红岩地貌：岩柱、仙人掌、枯草、碎石铺地
- 暖琥珀色天空（橙+米黄）漫射光，无硬影
- 产品放置在石台或平地上，如艺术装置
- 画面有丰富景深层次：前景岩石/草 → 产品 → 远景地貌

**适配产品**：投影仪、家庭音箱、电饭煲、空气净化器

**对应 SKILL 风格代号**：`STONE` / `SCENE`

**快速模仿提示词**
```
{product_name} placed on flat desert sandstone rocks, vast red rock desert canyon landscape with towering rock formations, dry golden desert grass, sparse cacti, soft diffused warm amber sunset sky, wide-angle cinematic composition, product sharp in middle ground surrounded by atmospheric desert depth, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式四：品牌色幻境水岛（COLOR_DREAMLAND）

**视觉特征**
- 场景整体统一于一种饱和品牌色（紫色、薰衣草、星空蓝等）
- 产品置于水中小岩岛上，四周为彩色静止水面+同色调植被
- 远景有圆润色调沙丘/山丘，与天空几乎同色渐变
- 产品颜色与场景色系呼应或形成中性色对比
- 拍摄角度：略仰视正面构图

**适配产品**：投影仪、便携音箱、空气净化器、有鲜明品牌色的小家电

**对应 SKILL 风格代号**：`COLOR_ECHO` / `COSMOS`

**快速模仿提示词**
```
{product_name} resting on a small rocky island surrounded by {brand_color} colored still water, {brand_color} lavender sand dunes and rolling hills in the background, {brand_color} gradient sky matching the landscape, golden amber wild grass accents, perfect water reflection of the product, soft cinematic lighting, wide-angle lens, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式五：雪地动态（SNOW_DYNAMIC）

**两种子变体：**

### 5A：禅意涟漪（SNOW_ZEN）
- 产品居中立于纯白雪面上，周围有清晰的同心圆涟漪刻纹
- 远景：雪山+冻湖或雪丘，晴天淡蓝天空
- 构图方正平稳，静谧冷峻感

**快速模仿提示词**
```
{product_name} placed at the center of concentric circular ripple patterns engraved in pristine white snow, snowy alpine mountain landscape in background with frozen lake, clear pale blue sky, perfectly symmetrical composition, soft diffused daylight, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

### 5B：飞雪冲击（SNOW_IMPACT）
- 产品被大量飞雪/碎冰包裹，动态定格瞬间
- 雪粒四溅，产品本体清晰锋利
- 配色：纯白+冷蓝天空+暗沙漠植物点缀（暖红/棕）形成对比

**快速模仿提示词**
```
{product_name} frozen in mid-explosion of white snow burst and flying ice crystals, surrounded by exploding snow spray caught in ultra-high-speed freeze-frame, dry red desert plants in foreground, bright clear blue sky, vivid contrast between warm earth tones and icy white explosion, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

**适配产品**：运动相机、户外耳机、吹风机、防水设备

**对应 SKILL 风格代号**：`SPLASH` / `EXPLOSION`

---

## 公式六：沙尘爆发旋涡（DUST_VORTEX）

**视觉特征**
- 产品静止悬浮或嵌入画面中心
- 从产品底部向外扩散的旋涡形沙尘涟漪（类似陨石撞击坑）
- 沙粒/碎石以放射状飞散，产品周围轻微沙尘雾化
- 背景简洁：暖土色调（棕/赭/卡其），天空较少
- 俯视或45°斜视构图均适用

**适配产品**：吹风机、剃须刀、便携音箱、旗舰扫地机

**对应 SKILL 风格代号**：`EXPLOSION`

**快速模仿提示词**
```
{product_name} at the epicenter of a powerful sand vortex, concentric sand ripple impact craters radiating outward from the product, fine sand particles and small rocks blasting outward in radial spray, warm brown earthy color palette, dramatic overhead or 45-degree angle, product perfectly sharp and static amid chaos, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式七：月夜玄岩宏场景（MOONLIT_ROCK）

**视觉特征**
- 深灰玄武岩/熔岩地貌，岩石质感粗粝
- 产品立于岩石群中，远景有水面
- 夜空深蓝到黑色渐变，有明显月亮（圆月或弦月）
- 枯黄野草点缀岩缝，暖冷色系张力
- 平视构图，天空占50%以上

**适配产品**：投影仪、智能音箱、空气净化器、黑灰色系产品

**对应 SKILL 风格代号**：`COSMOS` / `DARK`

**快速模仿提示词**
```
{product_name} standing on dark volcanic basalt rocks under a deep navy night sky, prominent crescent or full moon glowing above the horizon, dry golden grass growing from rocky crevices, calm water reflecting moonlight in the distance, horizon-level perspective, atmospheric moonlit haze, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式八：宇宙水镜大球景（COSMIC_MIRROR）

**视觉特征**
- 背景有巨大发光星球/月球，占据画面 30-40% 宽度
- 山脉剪影呈平行线排布在星球前
- 产品放置于水面边的岩石上，水面完整倒映星球和山
- 整体蓝紫色冷调，科幻感强
- 产品材质与冷光形成细腻高光

**适配产品**：运动相机、科技感小家电、黑色智能设备

**对应 SKILL 风格代号**：`COSMOS`

**快速模仿提示词**
```
{product_name} placed on dark rocks at the edge of perfectly still reflective water, enormous glowing white-blue planet or moon dominating the background sky, layered mountain silhouettes in front of the planet, calm water mirroring the planet and product, deep blue-purple cosmic color palette, cinematic wide-angle, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式九：冰雪碎石近景（ICE_FRAGMENT）

**视觉特征**
- 产品横斜倚靠或嵌于碎冰/粗雪晶体中
- 极近距离特写，冰晶颗粒感清晰可见
- 散落鹅卵石和石块，冷灰蓝色调
- 产品 LED 灯/发光元件作为唯一暖色/彩色点缀
- 竖构图，产品斜对角线摆放

**适配产品**：吹风机、除螨仪、便携小家电、有发光设计的产品

**对应 SKILL 风格代号**：`SPLASH` / `MATERIAL_SCENE`

**快速模仿提示词**
```
{product_name} resting diagonally on a bed of crushed ice and snow crystals, scattered gray pebbles and small rocks mixed in the ice, close-up macro detail, glowing {accent_color} LED light on the product as the only warm accent, cold blue-grey icy color palette, natural diffused overcast light, extreme material texture detail, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式十：粉雪岩石山岳（SNOW_MOUNTAIN_ROCK）

**视觉特征**
- 产品自然斜倚/横置于雪覆深色花岗岩岩块缝隙中，非正立
- 背景：连绵雪山峰脊，清透蓝天或粉紫日落天，中焦软化处理
- 光影：冷漫射日光从一侧打亮产品主体面，另一侧有轻微补光
- 前景雪粒颗粒感细腻可见，岩石纹理粗粝与产品材质形成对比
- 产品表面有轻薄霜/雪粉自然附着感

**适配产品**：手机、平板、充电器、耳机、细长/扁平小家电

**对应 SKILL 风格代号**：`STONE` / `SPLASH`

**快速模仿提示词**
```
{product_name} resting naturally at a diagonal angle wedged against snow-dusted dark granite boulder surface, panoramic chain of snow-capped mountain peaks in soft bokeh background, crisp cool diffused daylight from the right side illuminating the product face, fine snow powder granules visible on both rock and product edges, cold blue-white color palette with dramatic rock texture contrast, low-angle perspective showing snow foreground detail, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式十一：熔岩大地黑曜（VOLCANIC_LAND）

**视觉特征**
- 产品垂直站立于火山灰/玄武岩广阔大地，地面有橙红熔岩裂缝自然发光
- 背景远处有多座活火山锥冒烟升腾，暗红/深褐天空
- 光影：熔岩裂缝从正下方投出暖橙底光；远景大气散射提供极暗顶光
- 整体极暗调，产品是画面中最亮主体
- 宽幅KV构图（16:9）张力最强，地面广阔感突出

**适配产品**：黑色科技产品、游戏设备、黑色耳机、深色扫地机、深色手机

**对应 SKILL 风格代号**：`DARK` / `EXPLOSION`

**快速模仿提示词**
```
{product_name} standing upright on vast dark volcanic basalt plains, ground surface cracked with glowing orange-red lava veins radiating heat light from below, multiple distant volcano cones erupting smoke against a deep crimson-charcoal sky, warm orange lava underlighting illuminating the product base with dramatic rim lighting, extremely dark overall atmosphere with product as the brightest element, wide cinematic 16:9 landscape, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式十二：沙地禅境倾插（SAND_ZEN_TILT）

**视觉特征**
- 产品底部嵌入/斜插于细沙中，有重力下沉感，非漂浮于沙面
- 沙面有清晰风蚀纹路或禅意同心圆涟漪刻纹，近景沙粒颗粒感极强
- 低角度仰视，背景为渐变暖橙/米黄沙丘，天际线柔和
- 产品主体面朝向镜头清晰可辨
- 暖金黄色调主导，产品颜色与沙地色形成材质差异对比

**适配产品**：TWS耳机充电盒、手机、便携小设备、扁平类产品

**对应 SKILL 风格代号**：`STONE` / `COLOR_ECHO`

**快速模仿提示词**
```
{product_name} partially embedded base-first into fine golden desert sand with natural gravity-sunk depth, sand surface showing wind erosion ripple grooves and zen circular ripple patterns in foreground close-up, low-angle upward perspective looking along the sand surface, warm golden sand dune landscape stretching to distant soft amber sky behind, sand grain macro texture visible around the product base, product face clearly visible toward camera, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式十三：水岸玄岩倒影（WATER_ROCK_REFLECT）

**视觉特征**
- 产品竖立于宽阔深色玄武岩/板岩台面平台，台面与浅层静水无缝衔接
- 水面极度平静，形成产品完整倒影（镜像精准）
- 背景：傍晚渐变天空（玫瑰橙/暗紫/深蓝）或模糊玄武岩地貌
- 远处可有琥珀色荧光水晶/岩石点缀丰富景深
- 宽幅水平构图，产品占左三分之一或居中

**适配产品**：大体积产品（扫地机、音箱、净化器、投影仪）、竖形产品

**对应 SKILL 风格代号**：`COSMOS` / `STONE`

**快速模仿提示词**
```
{product_name} standing upright on a broad flat dark basalt stone platform surrounded by shallow perfectly still water creating a razor-sharp mirror reflection below, amber glowing crystal formations and dark volcanic rock outcrops visible in the misty background, dramatic dusk gradient sky transitioning from deep rose-gold to dark purple above, cool-dark color palette with warm amber accent reflections in water, wide cinematic landscape composition, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 公式十四：水涟漪漂浮（WATER_RIPPLE_FLOAT）

**视觉特征**
- 产品悬浮于画面中心，正下方有向外扩散的同心圆水涟漪（类似声波可视化）
- 涟漪圆心与产品垂直对齐，产品仿佛是涟漪的音源
- 背景：冰原/荒野/苍山水墨风，宽幅冷灰调，轻度雾气
- 产品占画面35-40%，构图干净留白
- 冷蓝灰色调主导，极简高级感

**适配产品**：TWS耳机、开放式耳机、入耳式耳机、小型音频设备

**对应 SKILL 风格代号**：`WAVE` / `SPLASH`

**快速模仿提示词**
```
{product_name} levitating floating directly above the exact epicenter of expanding concentric water ripple circles on a misty tundra lake surface, product casting faint shadow downward onto the water ripples below, cool gray-blue mountain silhouettes fading into background atmospheric haze, minimal clean composition with product occupying 35-40% of frame centered, cold arctic blue-gray color palette, still ethereal atmosphere, Unreal Engine 5 Octane render style hyperrealistic 3D CGI commercial product visualization every physical detail precisely rendered ambient occlusion realistic shadow environmental catchlights volumetric atmospheric haze seamlessly integrated product 8K award-winning no text no watermarks
```

---

## 综合使用指南

| 视觉公式 | 关键词 | 最佳适用产品 | 禁忌 |
|---|---|---|---|
| 峡谷悬浮水镜 | 峡谷/悬浮/水面倒影 | 手表、TWS耳机 | 体型过大的产品比例失调 |
| 星空黑沙丘水镜 | 星空/黑沙/水面 | 手机、黑色智能产品 | 白色/彩色产品对比度不足 |
| 暖沙漠宏观陈设 | 沙漠/岩石/广角 | 投影仪、音箱、厨电 | 佩戴类产品无法展示使用感 |
| 品牌色幻境水岛 | 品牌色/水岛/涟漪 | 有品牌色的任何产品 | 无明显品牌色的黑白产品 |
| 雪地禅意涟漪 | 雪/涟漪/静谧 | 运动相机、户外设备 | 暖色系厨电 |
| 飞雪冲击 | 雪/爆炸/飞溅 | 防水设备、运动产品 | 精致美妆类产品 |
| 沙尘爆发旋涡 | 沙尘/旋涡/爆发 | 吹风机、剃须刀、音箱 | 厨电（食品安全联想负面） |
| 月夜玄岩 | 月光/玄岩/夜景 | 投影仪、音箱、净化器 | 鲜艳颜色产品（颜色丢失） |
| 宇宙水镜大球景 | 星球/山脉/水镜 | 运动相机、科技产品 | 生活类家电 |
| 冰雪碎石近景 | 冰晶/碎石/近景 | 吹风机、手持小家电 | 大型家电 |
| 粉雪岩石山岳 | 雪岩/斜倚/雪山背景 | 手机、耳机、充电器 | 圆形/大体积产品 |
| 熔岩大地黑曜 | 熔岩/黑曜/暗红天空 | 黑色科技/游戏产品 | 白色/厨电/食品类 |
| 沙地禅境倾插 | 沙地/斜插/涟漪纹 | TWS耳机盒、手机 | 圆柱形/重型产品 |
| 水岸玄岩倒影 | 玄岩台/静水/倒影 | 音箱、扫地机、投影仪 | 小体积产品（比例失调）|
| 水涟漪漂浮 | 涟漪/悬浮/冰原 | TWS耳机、开放式耳机 | 大型家电 |
