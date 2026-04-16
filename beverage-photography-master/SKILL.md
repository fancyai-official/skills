<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

---
name: beverage-photography-master
description: 酒水饮料商业大片生成专家。用户提供产品图后，自动分析产品→推荐美学风格→用户确认→构建Prompt→批量生成5张4K大片（动态飞溅/微距特写/场景叙事/静物氛围/创意概念）→图片存本地并实时展示。当用户提到"酒水大片"、"饮料大片"、"酒水产品摄影"或上传酒水产品图时使用。
---

# 酒水饮料商业大片拍摄大师

## 重要配置 🔧

`campaign_helper.py` 与 `http_nano_banana.py` 均放在**本 Skill 目录**内（`.cursor/skills/000beverage-photography-master/`），无需任何额外部署步骤，换机器直接可用。

```python
import os, sys

# 三级兜底：环境变量 → cwd 自动检测 → 明确报错
_env = os.environ.get('BEVERAGE_SKILL_DIR')
_cwd = os.path.join(os.getcwd(), '.cursor', 'skills', '000beverage-photography-master')

SKILL_DIR = _env if _env and os.path.isfile(os.path.join(_env, 'campaign_helper.py')) \
            else _cwd if os.path.isfile(os.path.join(_cwd, 'campaign_helper.py')) \
            else None

if not SKILL_DIR:
    raise RuntimeError("找不到 skill 依赖文件，请设置环境变量 BEVERAGE_SKILL_DIR 指向 skill 目录")

sys.path.insert(0, SKILL_DIR)

from campaign_helper import create_campaign_folder, save_image_to_campaign, save_campaign_info
from http_nano_banana import nano_banana_image_gen_sync
import requests
```

> 💡 **输出目录**：生成的图片默认存到 `{当前工作区根目录}/酒水大片输出/`。  
> 如需自定义，设置环境变量 `BEVERAGE_OUTPUT_DIR=/your/path` 即可，无需改代码。

---

## 核心工作流程

### ⚠️ 产品图要求

用户必须提供**纯净的产品图**（白底/纯色背景、产品清晰完整、无复杂场景元素）。

❌ 严禁使用：已包含创意拍摄的图片、复杂背景营销图。

---

### 第一步：产品分析与信息收集

读取用户提供的纯净产品图，进行分析并在线搜索产品信息：

**1. 产品图像分析**
- 产品类型识别（烈酒、葡萄酒、啤酒、鸡尾酒、软饮）
- 包装特征提取（瓶身设计、罐装、品牌标识）
- 颜色和材质识别

**2. 在线产品信息搜索** 🔍 **（关键步骤）**

搜索策略：`[品牌名] + [产品名] + "颜色" / "color"`

重点确认：
- **液体真实颜色**（琥珀色/深红/透明/粉色/黄色/绿色等，必须准确）
- **官方图片参考**：查看官方产品图中饮料在杯中的呈现

**3. 综合确定**：产品类型、液体颜色、包装风格、品牌定位、目标场景

---

### 第二步：美学风格 × 拍摄技法组合

**策略**：先选1种美学风格（统一调性），再应用5种拍摄技法（多样视角）。

#### 五大美学风格（选1种）

| 风格 | 调性 | 适用产品 |
|------|------|---------|
| **A 柔和自然** 🌸 | pastel色系、虚化背景、柔和光 | 高端优雅、节日限定、女性市场 |
| **B 高饱和建筑** 🎨 | 鲜艳纯色、清晰纹理、硬光投影 | 年轻时尚、夏日、能量饮料 |
| **C 戏剧氛围** 🎭 | 深色调、烟雾光束、强对比 | 高端烈酒、奢华品牌、夜间场景 |
| **D 场景叙事** 📖 | 真实环境、生活化道具、自然光 | 各类需要故事感的产品 |
| **E 极简商业** ⚪ | 纯色背景、产品为焦点、干净光 | 高端简约、电商主图 |

#### 五大拍摄技法（5张图各用一种）

| 技法 | 核心特点 | 关键注意 |
|------|---------|---------|
| **1 动态飞溅** 💦 | 液体飞溅、冻结瞬间 | 完整瓶身倾倒必须有手握持 |
| **2 微距特写** 🔍 | 气泡水珠、极致细节 | 聚焦局部细节，不拍整瓶（会变形） |
| **3 场景叙事** 📖 | 生活场景、故事感 | 道具真实自然，避免摆拍感 |
| **4 静物氛围** 🕯️ | 精心构图、氛围光影 | 道具组合精致，情感共鸣 |
| **5 创意概念** 🎨 | 艺术化、打破常规 | 概念清晰，视觉惊艳 |

#### 🎯 美学风格选择决策树

- **高端优雅产品** → 风格A（柔和自然）或 C（戏剧氛围）
- **年轻时尚产品** → 风格B（高饱和建筑）或 D（场景叙事）
- **传统经典产品** → 风格C（戏剧氛围）或 E（极简商业）
- **节日限定产品** → 风格A（柔和自然）或 D（场景叙事）
- **电商主图需求** → 风格E（极简商业）或 D（场景叙事）

#### ⏸️ 暂停：向用户展示推荐并等待确认

根据以上决策树，向用户输出如下格式的推荐卡片（**禁止跳过，必须等用户回复后才能进入第三步**）：

---

📸 **为您推荐以下美学风格，请选择一种：**

**推荐1：风格X（xx名称）** ← 主推，匹配度最高
- 调性：...
- 原因：（结合产品特点说明，1–2句）

**推荐2：风格Y（xx名称）** ← 备选
- 调性：...
- 原因：（结合产品特点说明，1–2句）

> 也可以告诉我您想要的其他风格（A/B/C/D/E 任选），或直接回复「用推荐1」/「用推荐2」。

---

✅ **收到用户回复后**，将所选风格记为 `aesthetic_style_label`，然后：

> 🔴 **立即阅读 [KEYWORD_LIBRARY.md](KEYWORD_LIBRARY.md) 中对应字母章节**，获取该美学风格的调性关键词与禁用组合，再进入第三步。  
> 🔴 **[photography-styles.md](photography-styles.md)** 实际为 **五大技法**的标杆案例与模板（文档内「风格1～5」= 技法1～5），**在第三步按每条 Prompt 所对应的技法**，查阅其中**相应技法**章节即可；勿当作 A–E 美学说明。

---

### 第三步：Prompt 精准构建

**核心理念**：不同风格使用不同Prompt策略，没有通用模板。

#### 通用Prompt框架（7个维度）

**1. 场景概念** — 故事主题 + 目标情绪 + 美学风格定位

**2. 主体描述** — 产品类型、瓶身细节、**液体真实颜色**、包装材质、产品状态（condensation/冰冻）

**3. 背景设计**（根据风格）：
- 风格A → `soft blurred background with pastel tones, natural depth of field`
- 风格B → `corrugated wall with highly saturated [color], texture clearly visible`
- 风格C → `dark gradient background with colored smoke, volumetric lighting`
- 风格D → `outdoor [场景] setting, natural environment`
- 风格E → `clean white background, minimalist setup`

**4. 道具配置**（根据风格）：
- 风格A → 丰富精致（水果+花朵+装饰球+器皿）
- 风格B → 现代几何（金属框架+装饰球）
- 风格C → 少量精致（强调氛围）
- 风格D → 生活化组合（真实使用道具）
- 风格E → 无或极少道具

**5. 光影方案**（根据风格）：
- 风格A → `soft natural daylight, gentle shadows, warm lighting feel`（⚠️ 避免 hard light）
- 风格B → `directional light from 45° creating clear cast shadows`（⚠️ 避免 soft diffused）
- 风格C → `single spotlight from above, dramatic high contrast, rim lighting`
- 风格D → `natural environmental lighting, realistic shadows`
- 风格E → `clean product lighting, even illumination`

**6. 色彩策略**（根据风格）：
- 风格A → `soft pastel [color], muted elegant palette`（⚠️ 避免 highly saturated）
- 风格B → `highly saturated [color], vibrant bold colors`（⚠️ 避免 soft tones）
- 风格C → `deep dark tones, dramatic color accents`

**7. 真实感结尾** — `shot on Canon EOS R5, not 3D render, not CGI, authentic photographic quality`

> 🔴 **构建每条Prompt前，必须读取以下文件：**
> - **[PROMPT_GUIDE.md](PROMPT_GUIDE.md)** — 获取对应风格的完整Prompt模板和组合示例
> - **[KEYWORD_LIBRARY.md](KEYWORD_LIBRARY.md)** — 获取对应风格的关键词组，确保风格一致性
> - **[scene-library.md](scene-library.md)** — 按**技法**获取场景灵感和具体道具/环境描述
> - **[lighting-techniques.md](lighting-techniques.md)** — 获取光影方案细节
> - 若包含**动态飞溅**技法 → 必须读取 **[DYNAMIC_SPLASH_PHYSICS_GUIDE.md](DYNAMIC_SPLASH_PHYSICS_GUIDE.md)**
> - 若包含**微距特写**技法 → 必须读取 **[MACRO_ANTI_DISTORTION_GUIDE.md](MACRO_ANTI_DISTORTION_GUIDE.md)**

---

### 第四步：批量生成与自动存储

**生成配置**
- 脚本：`http_nano_banana.py`（与 SKILL 同目录，自动加载）
- 模型：`nano-banana-pro`
- 分辨率：`4K`
- **默认比例**（用户未指定时）：场景1用 `16:9`，场景2~5用 `3:4`

**核心生成代码**（`techniques_ordered` 为「产品分析决策树」排出的 5 个技法名称列表，顺序因品类而异；`prompts` 与之对齐）

```python
import os, sys

# 三级兜底：环境变量 → cwd 自动检测 → 明确报错
_env = os.environ.get('BEVERAGE_SKILL_DIR')
_cwd = os.path.join(os.getcwd(), '.cursor', 'skills', '000beverage-photography-master')

SKILL_DIR = _env if _env and os.path.isfile(os.path.join(_env, 'campaign_helper.py')) \
            else _cwd if os.path.isfile(os.path.join(_cwd, 'campaign_helper.py')) \
            else None

if not SKILL_DIR:
    raise RuntimeError("找不到 skill 依赖文件，请设置环境变量 BEVERAGE_SKILL_DIR 指向 skill 目录")

sys.path.insert(0, SKILL_DIR)

from campaign_helper import create_campaign_folder, save_image_to_campaign, save_campaign_info
from http_nano_banana import nano_banana_image_gen_sync
import requests

project_folder = create_campaign_folder(product_name)

for i, (prompt, technique_name) in enumerate(zip(prompts, techniques_ordered), 1):
    ratio = "16:9" if i == 1 else "3:4"
    print(f"\n正在生成 场景{i}/5：{aesthetic_style_label} × {technique_name}")

    result = nano_banana_image_gen_sync(
        prompt=prompt,
        img_urls=[product_image_url],
        app_model_type="nano-banana-pro",
        ratio=ratio,
        image_size="4K",
        pic_num=1,
        timeout=260
    )

    img_url = result['result'][0]
    img_data = requests.get(img_url).content
    filepath = save_image_to_campaign(img_data, project_folder, i, technique_name)

    print(f"✅ 已保存: {filepath}")
    # 立即用 Read 工具读取 filepath 以显示图片给用户

save_campaign_info(
    project_folder,
    product_name,
    aesthetic_style_label,
    techniques_ordered,
    prompts,
    liquid_color,
)
```

---

### 第五步：输出呈现与项目总结

- 每张图生成后**立即用 Read 工具显示图片**（不展示URL）
- 完成后输出项目文件夹路径、美学风格选择理由、5张图说明、文件大小统计

> 🔴 **全部生成完毕后，必须读取 [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md)**，对照所选美学风格的质检清单逐项核查，并在总结中说明是否达标。

**文件夹与文件命名**（`save_image_to_campaign` 输出为 JPEG，扩展名 `.jpg`）：

- 根目录：`/Users/mac/酒水大片skill/{clean_product_name}_campaign_{timestamp}/`
- 每场景：`scene_{序号}_{技法英文slug}.jpg`，其中**序号 1～5 对应本轮生成顺序**，**slug 对应当前场景实际技法**（由「产品分析决策树」决定，**不得**写死为 `scene_1_dynamic_splash`）。

**示例（葡萄酒：动态 → 静物 → 叙事 → 微距 → 创意）**：

```
/Users/mac/酒水大片skill/{product}_campaign_{timestamp}/
├── scene_1_dynamic_splash.jpg
├── scene_2_still_life_atmosphere.jpg
├── scene_3_lifestyle_narrative.jpg
├── scene_4_macro_closeup.jpg
└── scene_5_creative_concept.jpg
```

**示例（烈酒：静物 → 动态 → 微距 → 叙事 → 创意）**：

```
/Users/mac/酒水大片skill/{product}_campaign_{timestamp}/
├── scene_1_still_life_atmosphere.jpg
├── scene_2_dynamic_splash.jpg
├── scene_3_macro_closeup.jpg
├── scene_4_lifestyle_narrative.jpg
└── scene_5_creative_concept.jpg
```

---

## 产品分析决策树（技法主推）

| 产品类型 | 主推技法 | 组合顺序 |
|---------|---------|---------|
| 烈酒（威士忌/白兰地/伏特加）| 静物氛围 | 静物 → 动态 → 微距 → 叙事 → 创意 |
| 葡萄酒 | 动态飞溅 | 动态 → 静物 → 叙事 → 微距 → 创意 |
| 啤酒 | 场景叙事 | 叙事 → 微距 → 动态 → 创意 → 静物 |
| 鸡尾酒 | 微距特写 | 微距 → 动态 → 创意 → 叙事 → 静物 |
| 软饮/能量饮料 | 创意概念 | 创意 → 叙事 → 微距 → 动态 → 静物 |

---

## 子文件读取时机（必须遵守）

| 文档 | 用途 | 读取时机 |
|------|------|---------|
| [KEYWORD_LIBRARY.md](KEYWORD_LIBRARY.md) | 美学风格 A–E 关键词与调性 | 🔴 第二步选定 A–E 后**立即读取** |
| [photography-styles.md](photography-styles.md) | 五大**技法**标杆案例与模板（非 A–E） | 🔴 第三步按**当前技法**查阅对应章节 |
| [PROMPT_GUIDE.md](PROMPT_GUIDE.md) | 完整Prompt模板和组合示例 | 🔴 第三步构建Prompt前**必须读取** |
| [scene-library.md](scene-library.md) | 30+场景模板库（按技法） | 🔴 第三步构建Prompt前**必须读取** |
| [lighting-techniques.md](lighting-techniques.md) | 光影方案细节 | 🔴 第三步构建Prompt前**必须读取** |
| [DYNAMIC_SPLASH_PHYSICS_GUIDE.md](DYNAMIC_SPLASH_PHYSICS_GUIDE.md) | 飞溅物理合理性 | 🔴 含动态飞溅技法时**必须读取** |
| [MACRO_ANTI_DISTORTION_GUIDE.md](MACRO_ANTI_DISTORTION_GUIDE.md) | 微距防变形规则 | 🔴 含微距特写技法时**必须读取** |
| [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) | 按风格质检清单 | 🔴 第五步全部生成后**必须读取** |
