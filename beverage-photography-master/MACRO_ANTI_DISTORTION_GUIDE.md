<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 微距拍摄防变形技术指南

## 问题说明

**用户反馈**：在Rio产品的场景3（微距特写型）中，产品出现严重变形。

**问题根源**：微距镜头对整个产品进行extreme close-up会导致透视变形（perspective distortion），使瓶身/罐身出现拉伸、扭曲、比例失调等问题。

## 错误案例分析

### ❌ 错误做法1：将整个产品作为微距主体
```
Prompt: "Macro extreme close-up of [Product] bottle"
```
**结果**：瓶身被拉长或变宽，标签扭曲，品牌logo变形，不可接受。

### ❌ 错误做法2：近距离拍摄产品全身
```
Prompt: "Extreme close-up shot of entire [Product] can"
```
**结果**：罐身透视夸张，上下比例失调，产品不可识别。

### ❌ 错误做法3：微距聚焦于标签或瓶盖
```
Prompt: "Macro focus on [Product] label and cap"
```
**结果**：标签文字扭曲，瓶盖变形，产品细节失真。

## 正确做法

### ✅ 核心原则：微距拍细节，产品在背景

**关键思路**：
- **微距主体**：局部细节（condensation、bubbles、texture）
- **产品位置**：中景或背景，完整清晰呈现
- **景深控制**：浅景深突出细节，但产品依然清晰可辨

### ✅ 正确做法1：微距拍摄表面水珠

```
Prompt: 
Macro commercial photography: [Product] with extreme focus on surface condensation.

COMPOSITION:
- Foreground (macro focus): Condensation droplets on bottle surface (0.5-2mm water beads), 
  extreme close-up of micro droplets with crystal-clear details
- Mid-ground: [Product] bottle clearly visible, perfect shape, label readable, 
  no distortion, sharp and recognizable
- Background: Soft bokeh with [aesthetic style colors]

TECHNICAL:
- Macro lens focus distance: 10-15cm from droplet surface
- Product distance: 30-50cm from camera (normal perspective)
- Shallow depth of field (f/2.8-f/4)
- Product remains in acceptable focus zone

AVOID: extreme close-up of entire bottle, product warping, label distortion
```

**效果**：前景水珠超级清晰（微距），产品在中景完美呈现（无变形）。

### ✅ 正确做法2：微距拍摄杯中气泡

```
Prompt:
Macro commercial photography: Cocktail glass with [liquid] and extreme bubble detail.

COMPOSITION:
- Foreground (macro focus): Bubbles rising in liquid (1-3mm bubbles), 
  extreme close-up showing bubble texture, internal reflections, carbonation details
- Mid-ground: [Product] bottle/can clearly visible beside glass, 
  perfect proportions, label sharp, brand recognizable
- Background: [Aesthetic style backdrop - blurred/architectural/dramatic as chosen]

TECHNICAL:
- Macro focus on liquid bubbles in glass (15-20cm from camera)
- Product placement: 40-60cm from camera (safe distance, no distortion)
- Depth of field: f/4-f/5.6 (bubbles sharp, product acceptably sharp)

AVOID: macro of product itself, ensure product maintains correct shape and scale
```

**效果**：杯中气泡精细入微（微距），产品瓶完整美观（无变形）。

### ✅ 正确做法3：微距拍摄冰块纹理

```
Prompt:
Macro commercial photography: Ice cube with internal crystal structure.

COMPOSITION:
- Foreground (macro focus): Ice cube with visible internal cracks and frost texture,
  extreme close-up showing crystal patterns (macro at 8-12cm)
- Mid-ground: [Product] clearly visible in perfect condition, 
  bottle/can shape accurate, label text readable
- Background: [Aesthetic style environment]

TECHNICAL:
- Macro subject: ice cube (close-up reveals crystal structure)
- Product: placed at safe distance (35-50cm), normal lens perspective
- Lighting: backlight through ice for translucent effect

AVOID: product in macro range, keep product at normal shooting distance
```

**效果**：冰块内部结构清晰（微距），产品形状标准（无变形）。

## Prompt构建模板

### 通用微距防变形模板

```
Macro commercial photography: [Product] with extreme detail on [micro subject].

⚠️ CRITICAL COMPOSITION RULE:
- MACRO FOCUS: [Specific detail] (condensation/bubbles/ice/texture) - extreme close-up
- PRODUCT PLACEMENT: [Product] clearly visible in mid-ground/background, 
  perfect shape, no distortion, label readable, brand recognizable

FOREGROUND (pin-sharp macro):
[Detailed description of micro subject - e.g., "0.5-2mm water droplets on surface, 
crystalline clarity, light refraction visible"]

MID-GROUND (sharp, undistorted):
[Product] bottle/can in perfect condition, correct proportions, label text clear

BACKGROUND:
[Aesthetic style backdrop - soft bokeh/architectural/dramatic/minimal as chosen]

TECHNICAL NOTES:
- Macro lens on [micro subject] at 8-15cm
- Product at 30-60cm (normal perspective distance)
- Depth of field: f/2.8-f/5.6 (macro sharp, product acceptably sharp)

AESTHETIC STYLE: [选定的美学风格 - 柔和自然/高饱和建筑/etc.]

AVOID: 
❌ extreme close-up of entire bottle/can
❌ macro of product label or cap
❌ product as macro subject (causes distortion)

✅ ENSURE: Product remains recognizable, undistorted, professional presentation
```

## 技术原理

### 为什么会变形？

1. **透视夸张**：微距镜头距离主体非常近（5-15cm），放大了透视效果
2. **畸变**：超广角式的空间压缩，远端缩小，近端放大
3. **景深极浅**：f/2.8-f/4光圈下，前后几厘米内才清晰，产品若在微距范围会部分虚化且变形

### 如何避免？

1. **分离拍摄主体**：
   - 微距主体：小型细节（水珠、气泡、纹理）- 距离5-15cm
   - 产品主体：完整产品 - 距离30-60cm（正常拍摄距离）

2. **景深控制**：
   - 使用f/4-f/5.6而非f/1.8（略收光圈）
   - 确保产品在可接受景深范围内（虽然比微距主体略虚，但形状清晰）

3. **构图分层**：
   - 前景：微距细节（pin-sharp）
   - 中景：产品（sharp且无变形）
   - 背景：环境（虚化或清晰，取决于美学风格）

## Prompt关键短语

### ✅ 推荐使用：

- "Macro focus on condensation droplets on surface, product clearly visible in background"
- "Extreme close-up of bubbles in glass, [Product] bottle sharp and recognizable behind"
- "Macro detail of ice crystals, product at safe distance with correct proportions"
- "Micro water beads on bottle surface (foreground), product label readable (mid-ground)"
- "Product clearly visible in perfect condition, no distortion, while macro focuses on [detail]"

### ❌ 避免使用：

- "Extreme close-up of entire bottle"
- "Macro shot of [Product] can"
- "Close-up of product from very near"
- "Extreme close-up of bottle label"
- "Macro of bottle cap and top"

## 检查清单

生成微距特写型图片后，必须检查：

- [ ] **微距主体正确**：是细节（水珠/气泡/纹理），不是整个产品
- [ ] **产品形状标准**：瓶身/罐身比例正确，无拉伸或压缩
- [ ] **标签清晰可读**：品牌logo可识别，文字无扭曲
- [ ] **透视自然**：产品呈现符合正常视角，无夸张透视
- [ ] **分层清晰**：前景（微距）→ 中景（产品）→ 背景（环境）三层明确

## 案例对比

### 优秀案例特征

- ✅ 前景有超清晰的微距细节（视觉吸引力）
- ✅ 产品在中景完美呈现（品牌识别度）
- ✅ 整体画面有景深层次感（专业摄影质感）
- ✅ 产品无任何变形（商业可用性）

### 失败案例特征

- ❌ 产品占据整个画面且被微距拉近（透视变形）
- ❌ 瓶身或罐身比例失调（不可识别）
- ❌ 标签扭曲（品牌损害）
- ❌ 缺乏前景微距细节（不算真正的微距拍摄）

## 总结

**微距特写型的正确理解**：
- 不是"把产品拍得很近"
- 而是"拍摄产品相关的微观细节，产品本身保持标准呈现"

**执行要点**：
1. 明确微距主体（水珠、气泡、冰晶、纹理）
2. 产品保持安全距离（30-60cm，正常透视）
3. Prompt中明确分层描述
4. 强调"no distortion, perfect shape, label readable"
5. 生成后检查产品形状和比例

**避免踩坑**：
- 永远不要让AI把整个产品作为"macro subject"
- 永远不要用"extreme close-up of entire bottle/can"
- 永远在Prompt中明确"product at safe distance, no distortion"

---

**应用到SKILL**：
- ✅ 已在技法2定义中增加"防变形保护"说明
- ✅ 已在组合示例3中增加详细的构图和AVOID说明
- ✅ 已在通用技术关键词中增加"微距拍摄防变形指南"
- ✅ 已在质量控制检查清单中增加"特别检查项：微距特写型场景"

用户今后使用SKILL生成微距特写型场景时，AI将自动应用这些防变形保护机制。
