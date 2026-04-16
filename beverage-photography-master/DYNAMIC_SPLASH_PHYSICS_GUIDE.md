<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 动态飞溅型物理合理性指南

## 问题说明

**用户反馈**：
> "动态飞溅型如果是倒酒水的时候没有人手拿着，产品是悬空的，是不是不合理？要不只展示局部倒酒水（不出现手），但如果展示了完整的瓶身在倒酒水，应该有个手在拿"

**问题本质**：
- **物理违和感**：完整瓶身悬空倾倒违反重力和物理常识
- **商业可信度下降**：不真实的画面降低广告可信度
- **需要灵活方案**：既要动态效果，又要物理合理

## 错误案例分析

### ❌ 错误案例1：完整瓶身悬空倾倒

```
Prompt: "Full [Product] bottle tilted in air, pouring liquid into glass, 
         dynamic splash, floating bottle"
```

**问题**：
- 完整瓶身清晰可见
- 瓶身呈倾斜角度（45°-60°）
- 液体正在倒出
- **但没有任何支撑（无手、无支架）**
- 瓶子"漂浮"在空中

**为什么不合理**：
- 违反基本物理（重力）
- 观众潜意识感到"假"、"不真实"
- 类似悬浮魔术，但这不是魔术广告
- 降低产品的可信度和高端感

### ❌ 错误案例2：瓶身倾倒但手部缺失

```
Prompt: "[Product] bottle pouring into glass, liquid flowing, 
         bottle at 45 degree angle, dynamic pour"
```

**问题**：
- 瓶身完整，倾斜倒酒
- 没有明确"hand holding"
- AI可能生成悬空瓶身

**结果**：50%概率出现物理违和画面

## 正确做法

### ✅ 方案A：完整瓶身倾倒 + 手部握持（推荐用于lifestyle场景）

**适用场景**：
- 强调人与产品的互动
- 生活化、真实感的场景叙事
- 展现使用场景和体验感

**Prompt模板**：
```
Dynamic commercial photography: [Product] being poured into glass with elegant hand.

POURING ACTION:
- Hand gracefully holding [Product] bottle/can at [neck/body]
- Bottle tilted at natural angle (30-45 degrees)
- Liquid flowing from bottle into glass, creating gentle splash
- Hand visible: [choose style below]

HAND STYLE OPTIONS:
Option 1 - 女性优雅手：
  "Elegant female hand with manicured nails, delicate grip on bottle neck,
   refined gesture, soft skin tone"

Option 2 - 男性力量手：
  "Masculine hand with natural skin tone, firm grip on bottle body,
   confident pouring motion"

Option 3 - 部分可见手：
  "Hand partially visible at bottle base, fingers wrapped around bottle,
   focus on pouring action rather than hand detail"

FROZEN MOMENT:
- High-speed freeze (1/8000s shutter), liquid droplets suspended mid-air
- Splash in glass captured at peak moment
- Ice cubes and liquid in dynamic motion

PHYSICAL REALISM:
- Hand position anatomically correct
- Natural grip (not awkward or stiff)
- Bottle weight supported (believable hold)

AESTHETIC: [选定的美学风格]

AVOID: floating bottle, no support, physically impossible poses
```

**优势**：
- ✅ 物理合理（手提供支撑）
- ✅ 真实可信（真实使用场景）
- ✅ 情感连接（人的参与感）
- ✅ 高端感（优雅的手部动作）

**注意事项**：
- 手部要自然优雅，不能僵硬
- 握持位置合理（瓶颈最常见）
- 手部不要喧宾夺主（可以部分虚化或部分可见）
- 指甲、肤色要符合品牌调性

---

### ✅ 方案B：局部倾倒（仅瓶口）无需手部（推荐用于产品聚焦）

**适用场景**：
- 强调产品本身和液体质感
- 避免手部干扰产品焦点
- 更纯粹的产品摄影风格

**Prompt模板**：
```
Dynamic commercial photography: Close-up of [Product] pouring moment.

COMPOSITION:
- Close framing on bottle neck/opening
- Liquid flowing out from opening, creating stream
- Bottle body extends beyond frame top (implied: held outside frame)
- Glass positioned below, receiving liquid

POURING DETAILS:
- Liquid stream clearly visible, flowing smoothly
- Splash in glass, frozen moment (1/8000s)
- Droplets suspended in air, ice cubes in motion
- Focus on liquid texture, color, and transparency

FRAMING TECHNIQUE:
- Tight crop: only show bottle neck/top 1/3 of bottle
- Bottom of frame: glass with splash
- Implication: hand holds bottle above frame (not visible, but implied)
- This creates "someone is pouring" feeling without showing hand

PHYSICAL REALISM:
- Pouring angle natural (30-45 degrees implied by liquid trajectory)
- Liquid flow physics correct (gravity, arc, velocity)
- No floating bottle visible (cropping solves this)

AESTHETIC: [选定的美学风格]

RESULT: Dynamic pour without hand distraction, physically plausible through framing
```

**优势**：
- ✅ 物理合理（手在画面外，暗示存在）
- ✅ 产品聚焦（无手部干扰）
- ✅ 动态效果（倾倒和飞溅）
- ✅ 构图简洁（产品为视觉中心）

**关键技巧**：
- 通过**裁切**解决物理问题
- 画面外的手（隐含但不可见）
- 液体轨迹暗示倾倒角度
- 观众自动"脑补"画面外的手

---

### ✅ 方案C：飞溅特写 + 产品静置（推荐用于视觉冲击）

**适用场景**：
- 强调液体飞溅的视觉冲击
- 产品作为"静态英雄"呈现
- 避免倾倒动作，聚焦飞溅瞬间

**Prompt模板**：
```
High-speed commercial photography: Dynamic splash with [Product] hero shot.

SPLASH FOCUS:
- Liquid splash frozen mid-air (ice water/beverage/alcohol)
- Multiple droplets suspended, creating dramatic spray
- Ice cubes flying, water droplets caught at peak moment
- Splash height: 10-30cm above glass

PRODUCT PLACEMENT:
- [Product] bottle/can placed statically on surface
- Position: beside glass, slightly behind, or in background
- Product perfectly still (no motion, no pouring)
- Label clearly visible, product in spotlight

FROZEN MOMENT:
- Ultra high-speed capture (1/8000s to 1/12000s feel)
- Every droplet sharp and defined
- Ice cube mid-rotation, water beads spherical
- Splash at peak dynamic moment

PHYSICAL SETUP:
- Splash appears to be from: liquid poured into glass (completed action), 
  OR ice cube dropped into liquid (impact splash)
- [Product] is NOT the source of splash (just positioned in scene)
- Splash origin: glass itself (liquid already in glass, ice drop impact)

AESTHETIC: [选定的美学风格]

RESULT: Maximum visual impact, product as static hero, no floating bottle issue
```

**优势**：
- ✅ 完全避免倾倒物理问题
- ✅ 最大化飞溅视觉冲击
- ✅ 产品完美静态呈现
- ✅ 适合所有美学风格

**飞溅来源设定**：
- 冰块落入杯中（冰块撞击液体产生飞溅）
- 液体倒入杯中瞬间（倾倒已完成，拍摄飞溅）
- 玻璃杯碰撞瞬间（鸡尾酒场景）

---

## 三种方案对比

| 方案 | 物理合理性 | 动态感 | 产品聚焦 | 适用风格 | 难度 |
|------|-----------|--------|---------|---------|------|
| **A. 完整瓶身+手** | ✅ 完美 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 柔和自然/场景叙事 | ⭐⭐⭐ |
| **B. 局部倾倒** | ✅ 完美 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 所有风格 | ⭐⭐ |
| **C. 飞溅特写** | ✅ 完美 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高饱和/戏剧/柔和自然 | ⭐ |

## 选择建议

### 根据美学风格选择

**柔和自然风格** 🌸
- 推荐：方案A（手部优雅倾倒）
- 原因：强调温馨人性化，手部增加生活感
- 手部风格：女性优雅手，细腻柔和

**高饱和建筑风格** 🎨
- 推荐：方案C（飞溅特写）
- 原因：强调视觉冲击，产品与建筑背景对比强烈
- 飞溅效果：爆发力强，色彩对比鲜明

**戏剧氛围风格** 🎭
- 推荐：方案C（飞溅特写）或方案B（局部倾倒）
- 原因：神秘感，飞溅在光束中的悬浮效果
- 光影重点：液体在光影中的戏剧性

**场景叙事（D）或柔和自然（A）**（明亮、清透、生活化场景）
- 推荐：方案B（局部倾倒）
- 原因：清爽动感，液体流动的清透感
- 重点：液体的清澈和通透质感

**极简商业（E）**
- 推荐：方案C（飞溅特写，最简构图）
- 原因：避免手部复杂元素，保持极简
- 构图：产品+飞溅，纯色背景

### 根据产品类型选择

**高端烈酒**（威士忌、白兰地）
- 推荐：方案A（优雅手部倾倒）
- 手部风格：成熟男性手或精致女性手
- 倾倒动作：优雅、从容、仪式感

**啤酒/气泡水**
- 推荐：方案C（飞溅特写）
- 飞溅效果：爆发、冰爽、气泡丰富
- 产品位置：罐身完美静置

**鸡尾酒调酒**
- 推荐：方案A（调酒师手部）
- 手部风格：专业调酒师手法
- 场景：吧台、调酒环境

**果汁/软饮**
- 推荐：方案B（局部倾倒）
- 重点：果汁色彩、清新流动感
- 飞溅：温柔、清爽

## Prompt关键短语库

### ✅ 方案A：推荐短语

**手部描述**：
- "elegant female hand gracefully holding bottle neck"
- "masculine hand with confident grip on bottle body"
- "hand partially visible, fingers wrapped around bottle"
- "natural hand gesture, pouring motion"
- "manicured nails, delicate hold"

**倾倒动作**：
- "tilting bottle at 35-degree angle, liquid flowing smoothly"
- "gentle pour into glass, controlled stream"
- "bottle held at natural angle, liquid cascading"

**物理合理性强调**：
- "hand supporting bottle weight"
- "anatomically correct grip"
- "natural pouring posture"

### ✅ 方案B：推荐短语

**裁切构图**：
- "close-up of bottle neck/opening, liquid pouring out"
- "tight crop on bottle top, stream flowing into glass below"
- "bottle extends beyond frame top, hand implied outside frame"

**液体轨迹**：
- "liquid stream in smooth arc, natural gravity flow"
- "pour trajectory indicating 30-45 degree tilt angle"

### ✅ 方案C：推荐短语

**飞溅效果**：
- "liquid splash frozen mid-air, ice cubes flying"
- "dynamic splash at peak moment, droplets suspended"
- "ultra high-speed capture, every droplet sharp"

**产品静置**：
- "[Product] bottle placed statically on surface beside glass"
- "product positioned as static hero, no motion"
- "bottle perfectly still, splash happening in glass"

**飞溅来源**：
- "splash from ice cube impact in glass"
- "splash from completed pour action (bottle now static)"

### ❌ 避免短语

- ❌ "bottle floating in air"
- ❌ "bottle tilted with no support"
- ❌ "full bottle pouring without hand"
- ❌ "suspended bottle pouring liquid"
- ❌ "levitating bottle in pour action"

## 质量检查清单

生成动态飞溅型图片后，必须检查：

- [ ] **物理合理性**：倾倒动作是否符合物理常识？
- [ ] **方案识别**：属于A/B/C哪种方案？
- [ ] **如果是方案A**：
  - [ ] 手部是否可见？
  - [ ] 手部姿态是否自然？
  - [ ] 握持位置是否合理？
  - [ ] 手部与产品比例是否协调？
- [ ] **如果是方案B**：
  - [ ] 是否只显示瓶口/瓶颈部分？
  - [ ] 液体轨迹是否暗示倾倒角度？
  - [ ] 裁切是否自然（不显突兀）？
- [ ] **如果是方案C**：
  - [ ] 产品是否静置（无倾倒动作）？
  - [ ] 飞溅效果是否足够动感？
  - [ ] 飞溅来源是否合理（冰块落入/液体碰撞）？
- [ ] **避免问题**：
  - [ ] 无完整瓶身悬空倾倒
  - [ ] 无物理违和画面
  - [ ] 无"漂浮"瓶子

## 总结

**核心原则**：
1. **完整瓶身倾倒 → 必须有手**
2. **局部倾倒(仅瓶口) → 可以无手**
3. **飞溅特写 → 产品静置**

**选择策略**：
- 根据美学风格选择合适方案
- 根据产品定位选择手部风格
- 根据场景需求平衡动态与聚焦

**预防机制**：
- Prompt中明确方案选择
- 强调物理合理性关键词
- 使用质量检查清单验证

**应用到SKILL**：
- ✅ 已在技法1定义中增加"物理合理性保护"说明（3种方案）
- ✅ 已在组合示例2中增加详细的3种OPTION选择
- ✅ 已在通用技术关键词中增加"动态飞溅物理合理性指南"
- ✅ 已在质量控制检查清单中增加"特别检查项：动态飞溅型场景"

用户今后使用SKILL生成动态飞溅型场景时，AI将自动应用这些物理合理性保护机制，确保画面真实可信。
