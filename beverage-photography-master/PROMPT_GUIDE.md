<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Prompt 构建详细指南

> **与 [SKILL.md](SKILL.md) 一致**：进入第三步、**构建每条 Prompt 之前**必须阅读本文件（及 `KEYWORD_LIBRARY.md`），获取「美学风格 × 拍摄技法」的组合示例与完整模板。

---

## 📋 Prompt组合示例（美学风格 × 拍摄技法）

**理念**：每张图的Prompt = 美学风格基调 + 拍摄技法元素

---

### 组合示例1：柔和自然风格 × 场景叙事型（场景4标杆）

```
Lifestyle commercial photography: [Product] in elegant celebration scene.

AESTHETIC STYLE: Soft natural style
- Background: Naturally blurred with soft pastel tones, gentle depth of field
- Colors: Soft pastel pink, peach, white, gold accents, harmonious gentle tones
- Lighting: Soft natural daylight, warm gentle illumination, no harsh shadows

SHOOTING TECHNIQUE: Lifestyle narrative
- Setting: Elegant terrace scene with complete story
- Props: Fresh fruits scattered, flower petals, decorative ornaments, cocktail glass
- Mood: Warm, inviting, celebratory atmosphere

STYLE: Lifestyle commercial photography, natural authentic, editorial beverage shot
```

---

### 组合示例2：柔和自然风格 × 动态飞溅型

```
Lifestyle commercial photography: [Product] with gentle liquid pour moment.

AESTHETIC STYLE: Soft natural style
- Background: Soft blurred backdrop with pastel tones
- Colors: Gentle harmonious tones, soft lighting
- Lighting: Soft diffused light, warm feel

SHOOTING TECHNIQUE: Dynamic splash
- Element: Gentle liquid pouring into glass, soft splash effect
- Motion: Frozen moment (1/8000s) with graceful flow

⚠️ PHYSICAL REALISM - Choose ONE approach:
OPTION A (Full bottle visible pouring):
- Hand gracefully holding bottle, tilting to pour liquid
- Hand can be: female hand with manicured nails, or masculine hand, or partially visible
- Hand position: natural grip on bottle neck/body, relaxed and elegant
- Avoid: floating bottle with no support (physically impossible)

OPTION B (Partial pour without hand):
- Close-up of bottle neck/opening, liquid flowing out
- Bottle appears to continue beyond frame (implication: held outside frame)
- Focus on liquid stream and splash in glass

OPTION C (Splash focus, bottle static):
- Liquid splash frozen mid-air (ice cubes, liquid droplets)
- [Product] bottle/can placed statically on surface beside glass
- Focus on dynamic splash moment, not pouring action

✅ RECOMMENDED: Option A or B for dynamic pour, Option C for pure splash impact

STYLE: Lifestyle commercial, soft romantic aesthetic, gentle motion capture, natural hand interaction
```

---

### 组合示例3：柔和自然风格 × 微距特写型

```
Macro commercial photography: [Product] with extreme detail focus on surface condensation.

AESTHETIC STYLE: Soft natural style
- Background: Soft bokeh with pastel tones
- Colors: Delicate gentle hues
- Lighting: Soft natural light highlighting details

SHOOTING TECHNIQUE: Macro close-up
- ⚠️ CRITICAL: Focus on SURFACE DETAILS, not entire bottle
- Macro subject: Condensation droplets on bottle surface (0.5-2mm water beads)
- Secondary focus: Bubble details in glass, ice cube texture
- Product placement: [Product] bottle clearly visible in background (sharp, no distortion)
- Depth: Shallow depth of field, dreamy bokeh

COMPOSITION:
- Foreground: Extreme macro of droplets/bubbles (pin-sharp)
- Mid-ground: Product bottle in perfect condition (clear label, no distortion)
- Background: Soft blurred elements

AVOID: 
- ❌ Extreme close-up of entire bottle (causes distortion)
- ❌ Macro of bottle cap or label text (causes warping)
- ✅ CORRECT: Macro of surface condensation with bottle visible behind

STYLE: Macro lifestyle photography, soft detail focus, gentle aesthetic, product remains recognizable and undistorted
```

---

### 组合示例4：高饱和建筑风格 × 动态飞溅型（改进版测试图方向）

```
Modern commercial photography: [Product] with dramatic splash on vibrant backdrop.

AESTHETIC STYLE: High-saturation architectural style
- Background: Corrugated wall with highly saturated [color], texture clearly visible
- Colors: Vibrant bold tones, pure saturated colors
- Lighting: Directional hard light from 45° creating clear cast shadows

SHOOTING TECHNIQUE: Dynamic splash
- Element: Powerful liquid splashing, ice cubes flying
- Motion: Frozen at peak moment, high energy
- Impact: Strong visual punch, dynamic composition

STYLE: Modern commercial, bold architectural aesthetic, high-impact splash photography
```

---

### 组合示例5：高饱和建筑风格 × 场景叙事型

```
Lifestyle commercial photography: [Product] in vibrant summer pool party scene.

AESTHETIC STYLE: High-saturation architectural style
- Background: Bold saturated color backdrop, geometric elements visible
- Colors: Highly saturated primary colors, vivid tones
- Lighting: Hard directional light, clear shadows

SHOOTING TECHNIQUE: Lifestyle narrative
- Setting: Poolside party with vivid atmosphere
- Props: Fresh fruits, modern geometric props
- Story: Energetic summer celebration

STYLE: Modern lifestyle commercial, vibrant color treatment, party atmosphere
```

---

### 组合示例6：戏剧氛围风格 × 静物氛围型

```
Cinematic commercial photography: [Product] in dramatic atmospheric setting.

AESTHETIC STYLE: Dramatic atmospheric style
- Background: Dark gradient with colored smoke, volumetric lighting
- Colors: Deep dark tones with dramatic accents
- Lighting: Single spotlight, high contrast, rim lighting

SHOOTING TECHNIQUE: Still life atmosphere
- Composition: Carefully arranged elegant setup
- Props: Minimal refined elements
- Mood: Mysterious, luxurious, cinematic feel

STYLE: Cinematic advertising photography, dramatic atmospheric, film noir aesthetic
```

---

## 🎬 完整Prompt模板（5种美学风格）

### 模板A：柔和自然风格 🌸

```
Lifestyle commercial photography: [Product] in [温馨场景故事].

SCENE: [优雅环境描述]. [台面材质] with [柔和色调]. [自然氛围].

BACKGROUND:
- Surface: [材质] in soft [淡雅色系]
- Backdrop: naturally blurred background with gentle [氛围色] tones, creating depth
- Atmosphere: warm, inviting, [节日/季节] celebration feel

PROPS & ELEMENTS:
- [Product] as hero with natural condensation
- Cocktail glass with [饮品], ice cubes, [herb/flower] garnish
- Fresh [水果] scattered naturally ([具体数量])
- Decorative [装饰元素] ([颜色] ornaments, flower petals, [材质] accents)
- Organic asymmetric placement

LIGHTING:
- Soft natural daylight from [方向]
- Gentle even illumination, no harsh shadows
- Warm [色温]K lighting creating cozy atmosphere
- Light window glow feel

COLOR PALETTE:
- Primary: Soft pastel [主色] (product + surface harmony)
- Secondary: [辅助色] (gentle complementary tones)
- Accent: [点缀色] (subtle highlights)
- Overall: harmonious gentle color scheme, muted elegant tones

MOOD: [情绪关键词] (e.g., fresh, inviting, celebratory, elegant yet approachable)

STYLE: Lifestyle commercial photography, natural authentic look, editorial beverage advertising, soft romantic aesthetic, shot on Canon EOS R5, not 3D render, organic placement with natural beauty
```

**成功案例参考**：场景4（Red Bull清新风格）、Aperol粉色台面、桃子鸡尾酒

---

### 模板B：高饱和建筑风格 🎨

```
Modern commercial photography: [Product] in vibrant [年轻场景].

SCENE: [活力环境]. [建筑材质] with highly saturated [主色] clearly visible.

BACKGROUND ARCHITECTURE:
- Surface: [材质] with visible [纹理特征] texture, [色调] tone
- Wall: [建筑元素] in highly saturated [鲜艳色], bold color blocks, texture clearly showing (not blurred)
- Geometric elements: [几何装饰]
- Color: vibrant pure [颜色], bold saturated palette

PROPS & ELEMENTS:
- [Product] with perfect condensation
- [现代道具]
- Geometric decorations ([金属几何体])
- Minimalist modern placement

LIGHTING:
- Directional light from [角度] creating clear cast shadows on surface
- [光线性质] with defined shadow lines
- [色温] creating [氛围]

COLOR PALETTE:
- Primary: Highly saturated [主色] (vibrant bold tone)
- Secondary: [辅助色] (pure bright accent)
- Unified color theme across product-background-props

MOOD: [情绪] (e.g., energetic, youthful, vibrant, summer vibes)

STYLE: Modern commercial photography, bold architectural aesthetic, vibrant color treatment, editorial advertising, shot on professional camera, not CGI
```

**成功案例参考**：改进版测试图（波纹墙面）、芒果鸡尾酒橙红背景、Tecate蓝色场景

---

### 模板C：戏剧氛围风格 🎭

```
Cinematic commercial photography: [Product] with dramatic atmospheric effects.

SCENE: Moody [环境] with volumetric lighting. [深色材质]. Dramatic [色彩] smoke/mist creating mystical atmosphere.

BACKGROUND:
- Dark gradient background ([深色渐变])
- [彩色] colored smoke clouds swirling
- Volumetric light rays cutting through mist
- Ground mist effect

ELEMENTS:
- [Product] as focal point with rim lighting
- Minimal props ([精致道具])
- [Atmospheric elements]

LIGHTING:
- Single [方向] spotlight creating god rays
- Dramatic side rim light
- High contrast, moody cinematic look
- Smoke illuminated from within

COLOR PALETTE: Deep [深色调] + dramatic [重点色] accents

MOOD: Epic, powerful, mysterious, luxurious

STYLE: Cinematic advertising photography, dramatic atmospheric, inspired by perfume campaigns, film grain texture, shot on ARRI camera
```

**成功案例参考**：Nescafé咖啡烟雾、BRAE紫色氛围、场景3

---

### 模板D：场景叙事风格 📖

```
Lifestyle commercial photography: [Product] in authentic [生活场景].

SCENE: [真实环境描述]. Natural [材质]. [生活化氛围].

SETTING:
- Environment: [户外/室内真实场景]
- Surface: [自然材质]
- Background: [真实环境] naturally blurred
- Story: [具体故事情节]

PROPS:
- [Product] in real-use context
- [生活化道具组合]
- Natural placement as in real life

LIGHTING:
- Natural environmental lighting
- [时段] light feel
- Realistic shadows and reflections

MOOD: [生活情绪] (e.g., casual, social, joyful, relaxed)

STYLE: Lifestyle photography, real-world authentic setting, story-driven, natural documentary feel
```

**成功案例参考**：Tecate冰桶啤酒、场景1（泳池派对）

---

### 模板E：极简商业风格 ⚪

```
Clean commercial product photography: [Product] on [简洁背景].

SETUP:
- Background: Pure [颜色] or gradient, minimalist
- Surface: [简单材质] or suspended
- Focus: Product as sole hero

LIGHTING:
- Clean professional product lighting
- Even illumination highlighting product details
- Subtle shadows for dimension

STYLE: Professional commercial photography, minimalist aesthetic, high-end product shot, clean and focused
```

---

## 🎯 技法组合策略建议

**方案1：全面展示型**（适合新产品发布）
1. 场景叙事型 - 展现使用场景和生活方式
2. 动态飞溅型 - 视觉冲击和活力感
3. 微距特写型 - 产品质感和细节
4. 静物氛围型 - 品牌调性和高级感
5. 创意概念型 - 艺术化和记忆点

**方案2：生活方式主导型**（适合节日营销）
1. 场景叙事型（主KV）
2. 场景叙事型（不同场景）
3. 微距特写型
4. 静物氛围型
5. 动态飞溅型

**方案3：视觉冲击型**（适合年轻市场）
1. 动态飞溅型（主KV）
2. 创意概念型
3. 场景叙事型
4. 微距特写型
5. 动态飞溅型（不同角度）

**方案4：高端精致型**（适合奢华品牌）
1. 静物氛围型（主KV）
2. 微距特写型
3. 戏剧氛围静物
4. 创意概念型
5. 场景叙事型（精致场景）
