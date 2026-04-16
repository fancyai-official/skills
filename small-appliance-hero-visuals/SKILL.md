<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

---
name: small-appliance-hero-visuals
description: Analyze small-appliance product traits and produce premium commercial hero imagery. Use when the user uploads a product photo, describes a small appliance, wants commercial photography, e-commerce hero shots, or brand posters. Triggers include small appliances, hero shots, commercial photography, image generation, e-commerce main images, product posters, headphones, hair dryers, air fryers, rice cookers, robot vacuums, watches, neck fans, etc.
---

# Small-appliance commercial hero image generation

## 使用时机

用户上传产品图或描述小家电产品，想生成商业大片、电商主图、品牌海报时，**立即**按以下四步执行，无需等待用户进一步说明。

---

## 四步执行流程

### Step 1：产品特征分析

读取产品图或描述，提炼以下信息：

| 维度 | 提炼内容 |
|---|---|
| **产品类别** | 耳机 / 吹风机 / 空气炸锅 / 扫地机 / 手表 / 挂脖风扇 等 |
| **主体材质** | 哑光塑料 / 镜面金属 / 烤漆 / 磨砂 / 皮革 / 透明件 |
| **主色调** | 黑 / 白 / 银 / 金 / 橙 / 红 / 彩色 |
| **产品形态** | 圆润 / 棱角 / 细长 / 扁平 / O型 / U型 / 复合体 |
| **核心卖点** | 降噪 / 防水 / 轻量 / 智能 / 大功率 / 便携 等 |
| **目标用户** | 科技男 / 精致女 / 家庭主妇 / 运动人群 / 商务人士 等 |

### Step 2：风格选择

**在选择风格前，必须先使用 Read 工具读取 `/Users/liujunhong/Desktop/家电skill/.cursor/skills/家电skill/product-profiles.md`，找到当前产品类别对应的条目，提取：禁用风格、构图建议、材质渲染重点。**

根据产品类别和卖点，从以下14种风格中选1-2个最匹配的：

| 风格代号 | 风格名 | 适合产品 | 核心视觉 |
|---|---|---|---|
| `DARK` | 极致暗调质感 | 黑色科技产品、耳机、音箱 | 纯黑背景+冷白聚光，戴森风 |
| `WAVE` | 声波/气流可视化 | 耳机、音箱、空气净化器、风扇 | 物理效果光效围绕产品 |
| `SPLASH` | 水花定格防水 | 耳机、运动设备、厨电 | 水冠皇冠+IPX防水主题 |
| `WHITE` | 纯白极简电商 | 全品类通用 | 白底三点光，Apple风 |
| `SCENE` | 场景化生活美学 | 厨电、家居小电、美容仪 | 真实生活场景+产品主角 |
| `COSMOS` | 宇宙/自然宏大场景 | 高端产品、发布会主视觉 | 宇宙/雪山/峡谷衬托产品渺小 |
| `TECH` | AI科技未来感 | 智能设备、机器人、扫地机 | 蓝色AI粒子+数据流 |
| `STONE` | 岩石/自然陈设 | 手机、中高端小家电、手表 | 产品立于岩石上，暖橙背景 |
| `COLOR_ECHO` | 颜色呼应/品牌色宇宙 | 任何有鲜明品牌色的产品 | 产品色=背景色系，材质差异产生质感对比 |
| `LIFESTYLE` | 人物局部互动 | 耳机、手表、美容仪、手持设备 | 手/耳/腕局部入画，不露脸，传递使用体验 |
| `PORTAL` | 圆环/窗框舞台感 | 净化器、耳机、音箱、竖形/圆形产品 | 产品被圆环包裹，框内透出另一世界 |
| `EXPLOSION` | 动态爆发力量感 | 运动耳机、剃须刀、扫地机旗舰、手表 | 产品静止于爆炸/破碎中心，性能感极强 |
| `MATERIAL_SCENE` | 材质呼应陈设 | 强调材质/工艺的旗舰产品 | 产品与同材质道具共存，强化质感认知 |
| `FLAT_CONTEXT` | 俯拍生活故事 | 耳机、便携设备、手机配件 | 俯拍产品+生活道具，讲述目标用户生活方式 |

**风格选择逻辑：**
- 黑色产品 → 优先 `DARK` 或 `WAVE`
- 白色/彩色产品 → 优先 `WHITE` 或 `SCENE`
- 有鲜明品牌色（红/橙/绿）→ 优先 `COLOR_ECHO`
- 防水卖点 → 必选 `SPLASH`
- 智能/AI卖点 → 优先 `TECH`
- 高端发布主视觉 → 优先 `COSMOS` 或 `PORTAL`
- 厨房类产品 → 优先 `SCENE` 或 `STONE`
- 佩戴类产品（耳机/手表/挂脖）→ 可选 `LIFESTYLE`
- 旗舰性能产品 → 可选 `EXPLOSION`
- 便携配件类 → 可选 `FLAT_CONTEXT`
- O型/圆形产品（挂脖空调/无叶风扇/净化器）→ 可选 `PORTAL`

### Step 3：生成提示词

**必须按顺序执行以下两步读取，再组装提示词：**

1. **使用 Read 工具读取 `/Users/liujunhong/Desktop/家电skill/.cursor/skills/家电skill/reference-analysis.md`**，找到与所选风格最匹配的视觉公式，提取其英文快速模仿提示词作为基础框架。
2. **使用 Read 工具读取 `/Users/liujunhong/Desktop/家电skill/.cursor/skills/家电skill/prompt-templates.md`**，找到所选风格代号对应的六层结构模板，将 Step 1 提炼的产品信息（产品名/主色调/材质）填入占位符。

按 **六层结构** 组装最终提示词：

```
[主体] + [背景/环境] + [光影] + [材质] + [构图] + [技术规格]
```

生成时必须包含：
- 产品精确英文名称
- 所选风格的核心视觉元素
- 材质描述（对应 Step 1 提炼的材质）
- 构图张力（悬浮、斜角、景深层次）

**【构图独立原则】**: 只学习参考图的光影方向、材质表现、场景氛围，构图/角度/产品摆放必须完全重新设计，绝对不能复制参考图布局。

**【强制户外原则】**: 所有生成图必须使用户外自然环境背景。
- 合法场景：雪地/粉雪岩石/沙漠/峡谷/玄武岩台/山岳/熔岩大地/海岸岩礁/星空水岛/沙地禅境/荒野冰川/水涟漪冰原
- 严禁使用以下任何室内场景词：kitchen、bedroom、bathroom、studio、tabletop、living room、countertop、interior、marble counter、wooden table、desk、countertop、dining room
- 即使是厨电产品（电饭煲/空气炸锅/咖啡机），KV 大片也必须使用户外宏大自然场景

**【强制第 7 层 — 质量基底词 (Quality Foundation Layer)】**
在六层结构拼接完成后，原样追加以下关键词，不可删减：

```
Unreal Engine 5 Octane render style, hyperrealistic 3D CGI commercial product visualization, every physical detail of the product precisely rendered including buttons textures logos and surface grain, ambient occlusion, product casting realistic soft shadow on surface, subtle environmental light reflections and catchlights on product body, cinematic shallow depth of field with razor-sharp product and gently blurred background, volumetric atmospheric haze in the scene, seamlessly integrated product no floating pasted-on look, 8K resolution ultra-detail, award-winning commercial photography, no text no watermarks
```

### Step 4：执行生图

**使用 Shell 工具执行以下 Python 脚本调用 nano banana 生图（禁止使用 GenerateImage 工具）：**

```python
python3 -c "
import sys
sys.path.insert(0, '/Users/liujunhong/Desktop/家电skill')
from http_nano_banana import nano_banana_image_gen_sync

prompt = '''此处填入 Step 3 生成的完整英文提示词'''
img_urls = ['此处填入用户上传的产品图本地路径']  # 无产品图时改为 None

urls = nano_banana_image_gen_sync(
    prompt=prompt,
    img_urls=img_urls if img_urls and img_urls[0] else None,
    ratio='1:1',
    image_size='2K',
    pic_num=1,
)
for u in urls:
    print(u)
"
```

**参数说明：**
- `prompt` — Step 3 产出的完整英文提示词
- `img_urls` — 用户上传了产品图时填入本地绝对路径，脚本会自动上传并作为参考图；无产品图时填 `None`
- `ratio` — 默认 `1:1`；竖图改为 `9:16`；横图改为 `16:9`
- `image_size` — 默认 `2K`
- `pic_num` — 每次生成张数，默认 `1`

脚本输出图片 URL，将 URL 展示给用户。

生图后，基于结果主动提供：
- 本次使用的风格和理由（1-2句）
- 2-3个可以继续尝试的方向

---

## 快速参考：各产品类别最佳风格

完整档案（含禁用风格/构图/材质重点）需在 Step 2 通过 Read 工具读取 `product-profiles.md` 获取；参考图视觉公式需在 Step 3 通过 Read 工具读取 `reference-analysis.md` 获取。以下为快速索引：

| 产品 | 首选风格 | 新增推荐 |
|---|---|---|
| 真无线耳机 (TWS) | `DARK` `WAVE` `SPLASH` | `PORTAL` `LIFESTYLE` `FLAT_CONTEXT` |
| 头戴耳机 | `DARK` `COSMOS` `STONE` | `COLOR_ECHO` `LIFESTYLE` `MATERIAL_SCENE` |
| 吹风机 | `DARK` `WAVE` `WHITE` | `COLOR_ECHO` `LIFESTYLE` |
| 空气炸锅 | `SCENE` `STONE` `WHITE` | `MATERIAL_SCENE` `FLAT_CONTEXT` |
| 扫地机器人 | `TECH` `DARK` `SCENE` | `PORTAL` `EXPLOSION` |
| 电风扇/无叶 | `WAVE` `COSMOS` `DARK` | `PORTAL` `COLOR_ECHO` |
| 空气净化器 | `WAVE` `TECH` `WHITE` | `PORTAL` `COSMOS` |
| 电饭煲 | `SCENE` `STONE` `WHITE` | `MATERIAL_SCENE` `FLAT_CONTEXT` |
| 美容仪/剃须刀 | `SCENE` `WHITE` `TECH` | `COLOR_ECHO` `LIFESTYLE` `EXPLOSION` |
| 智能音箱 | `DARK` `TECH` `WAVE` | `PORTAL` `COSMOS` |
| 挂脖风扇/空调 | `SCENE` `STONE` `DARK` | `PORTAL` `LIFESTYLE` `COLOR_ECHO` |
| 智能手表/手环 | `DARK` `STONE` `COSMOS` | `EXPLOSION` `COLOR_ECHO` `LIFESTYLE` |

---

## 输出规范

每次生图任务完成后，输出：

1. **产品分析摘要**（3-5行）
2. **选用风格及理由**（1-2句）
3. **生成的图片**（nano banana Shell 调用结果 URL）
4. **可继续探索的方向**（2-3个备选）

---

## Additional Resources

- 产品类型与风格详细映射：[product-profiles.md](product-profiles.md)
- 完整提示词模板库（14种风格六层结构）：[prompt-templates.md](prompt-templates.md)
- 57张参考图分类索引与模仿提示词：[reference-analysis.md](reference-analysis.md)
