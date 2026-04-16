<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 质量保证与验证系统

## 核心质量标准

基于90+张顶级摄影师作品分析，每张生成的大片必须达到以下标准：

### 必达标准（Must Have）

**0. 原创性** ⭐⭐⭐⭐⭐ 🆕
- 场景必须100%原创，不模仿参考案例画面
- 基于用户纯净产品图策划
- 运用学习的技法但场景独特；子文档中的品牌/作品案例**仅可学习光影与结构**，不得复刻构图与成片
- 参考案例仅用于学习，不用于生成输入

**1. 产品清晰度** ⭐⭐⭐⭐⭐
- 产品主体清晰可辨，无模糊
- 标签/瓶身细节可见
- 材质质感真实（玻璃、金属、液体）

**2. 光影专业度** ⭐⭐⭐⭐⭐
- 逆光/侧光/柔光运用正确
- 高光不过曝，阴影有细节
- 散景/氛围光效果自然

**3. 构图平衡性** ⭐⭐⭐⭐⭐
- 主体位置符合三分法或黄金比例
- 视觉重心稳定
- 留白和呼吸感适当

**4. 色彩和谐度** ⭐⭐⭐⭐⭐
- 色彩搭配符合品牌调性
- 互补色/渐变色运用得当
- 整体色调统一

**5. 商业适用性** ⭐⭐⭐⭐⭐
- 符合商业摄影规范
- 可直接用于营销推广
- 视觉冲击力强

### 卓越标准（Nice to Have）

**6. 创意独特性** ⭐⭐⭐⭐
- 有独特的视角或创意
- 超越常规拍摄思路

**7. 情感共鸣** ⭐⭐⭐⭐
- 能引发情感联想
- 讲述品牌故事

**8. 细节精致度** ⭐⭐⭐⭐
- 冰块、气泡、水珠等细节完美
- 装饰物摆放精准

---

## 质量验证流程

### 阶段1：生成前验证

**Prompt质量检查清单**
```
生成前必检：
□ 使用的是用户纯净产品图，不是参考案例
□ 包含产品类型明确描述
□ 光影方案具体（光源/角度/色温）
□ 场景元素完整（背景/道具/材质）
□ 氛围描述清晰（情绪/色调）
□ 技术参数明确（景深/角度/比例）
□ 关键词库中的专业术语使用正确
□ 参考了对应风格的prompt模板
□ 场景设计原创，不照搬参考案例
```

### 阶段2：生成中监控

```python
# 生成时记录参数（与 SKILL.md 一致：nano-banana-pro，4K；默认比例场景1为 16:9，场景2~5 为 3:4）
generation_log = {
    "scene_type": "动态飞溅型",
    "prompt": "完整prompt内容",
    "model": "nano-banana-pro",
    "ratio": "16:9",  # 或 "3:4"，依场景序号而定
    "resolution": "4K",
    "reference_image": "product_url",
    "generation_time": "25s",
    "task_id": "xxx"
}
```

### 阶段3：生成后评估

**自动评估指标**
```python
def evaluate_result(generated_image_url, standards):
    """
    评估生成结果质量
    返回：分数 (0-100) 和改进建议
    """
    scores = {
        "product_clarity": 0,      # 产品清晰度
        "lighting_quality": 0,     # 光影质量
        "composition": 0,          # 构图
        "color_harmony": 0,        # 色彩和谐度
        "commercial_usability": 0  # 商业适用性
    }
    
    # 评估逻辑
    # ...
    
    total_score = sum(scores.values()) / len(scores)
    return total_score, scores
```

**人工评估清单**
```
视觉评估（1-5分）：
□ 第一眼印象（视觉冲击力）      _/5
□ 产品呈现（清晰度和美观度）    _/5
□ 光影效果（专业度和艺术性）    _/5
□ 构图布局（平衡性和创意）      _/5
□ 色彩运用（和谐度和品牌匹配）  _/5
□ 细节处理（精致度和真实感）    _/5
□ 整体质感（高端感和商业性）    _/5

总分：_/35  评级：________
30-35分：卓越 ⭐⭐⭐⭐⭐
25-29分：优秀 ⭐⭐⭐⭐
20-24分：良好 ⭐⭐⭐
15-19分：合格 ⭐⭐
<15分：需改进 ⭐
```

---

## 对标顶级案例

### 标杆案例库

从90张参考案例中选出各风格的"标杆"：

**动态飞溅型标杆**
- Stella Rosa 红酒液体飞溅
- 关键指标：液体S型曲线、液滴晶莹、纯黑背景、高对比

**静物氛围型标杆**
- Glenfiddich 威士忌酒吧场景
- 关键指标：散景效果、暖色调、木质质感、奢华氛围

**微距特写型标杆**
- 血橙鸡尾酒微距
- 关键指标：细节极致、色彩鲜艳、渐变背景、清爽感

**场景叙事型标杆**
- Tecate 啤酒户外场景
- 关键指标：真实场景、自然光、生活化、故事感

**创意概念型标杆**
- BRAE 几何金属场景
- 关键指标：几何元素、金属质感、艺术性、现代感

### 对标评估方法

```python
def benchmark_comparison(generated_url, reference_url, style_type):
    """
    将生成结果与标杆案例对比
    """
    comparison = {
        "visual_impact": 0,      # 视觉冲击力对比
        "technical_quality": 0,  # 技术质量对比
        "creativity": 0,         # 创意水平对比
        "commercial_value": 0    # 商业价值对比
    }
    
    # 对比分析
    # 100%：达到或超越标杆
    # 80-99%：接近标杆
    # 60-79%：有差距但可用
    # <60%：需要重新生成
    
    return comparison
```

---

## 迭代改进机制

### 不达标时的改进策略

**问题1：产品不够清晰**
```python
# 改进方案
improved_prompt = original_prompt + """
, product in ultra sharp focus, crystal clear details, 
high definition product photography, pristine clarity
"""

# 参数调整
resolution = "4K"  # 提升分辨率
model = "nano-banana-pro"  # 使用顶级模型
```

**问题2：光影不够专业**
```python
# 改进方案
improved_prompt = original_prompt + """
, professional studio lighting, three-point lighting setup,
dramatic rim lighting, controlled highlights, soft shadows
"""

# 增加光影关键词密度
lighting_keywords = [
    "backlit", "rim lighting", "soft diffused light",
    "dramatic lighting", "ambient glow"
]
```

**问题3：构图失衡**
```python
# 改进方案
improved_prompt = original_prompt + """
, rule of thirds composition, balanced layout,
professional commercial photography composition,
centered product with negative space
"""
```

**问题4：色彩不和谐**
```python
# 改进方案
improved_prompt = original_prompt + """
, harmonious color palette, [互补色] color scheme,
professional color grading, cinematic color treatment
"""
```

**问题5：缺乏商业感**
```python
# 改进方案
improved_prompt = original_prompt + """
, high-end commercial photography, advertising quality,
luxury product shot, premium brand aesthetic,
professional marketing photography
"""
```

### 批量A/B测试

```python
def ab_test_generation(prompt_a, prompt_b, product_image):
    """
    同时生成两个版本对比
    """
    # 版本A：当前prompt
    result_a = nano_banana_image_gen_sync(
        prompt=prompt_a,
        img_urls=[product_image],
        app_model_type="nano-banana-pro",
        ratio="3:4",
        image_size="4K"
    )
    
    # 版本B：改进prompt
    result_b = nano_banana_image_gen_sync(
        prompt=prompt_b,
        img_urls=[product_image],
        app_model_type="nano-banana-pro",
        ratio="3:4",
        image_size="4K"
    )
    
    return {
        "version_a": result_a,
        "version_b": result_b,
        "comparison": compare_results(result_a, result_b)
    }
```

---

## 实战验证案例

### 验证测试1：红酒液体飞溅

**目标标杆**: Stella Rosa 红酒案例

**测试prompt**:
```
Commercial beverage photography, premium red wine bottle with 
dramatic crimson liquid splash in elegant S-curve motion around 
the bottle, pure black background, strong backlighting creating 
glowing translucent liquid edges, frozen droplets suspended in 
mid-air with crystal clarity, high contrast dramatic lighting, 
liquid appears luminous and jewel-like, professional advertising 
photography, ultra sharp product details, 8k resolution, 
cinematic quality
```

**生成参数**:
```python
result = nano_banana_image_gen_sync(
    prompt=test_prompt,
    img_urls=["reference_wine_bottle.jpg"],
    app_model_type="nano-banana-pro",  # 使用顶级模型
    ratio="16:9",  # 批量流程中场景1默认；单张测试可改用 3:4
    image_size="4K",  # 最高分辨率
    pic_num=1
)
```

**评估标准**:
- 液体飞溅S型曲线 ✓ / ✗
- 液滴晶莹剔透 ✓ / ✗
- 纯黑背景纯净 ✓ / ✗
- 逆光效果明显 ✓ / ✗
- 高对比戏剧性 ✓ / ✗
- 产品清晰可见 ✓ / ✗

**期望达成率**: ≥80% (5/6项)

---

### 验证测试2：几何创意场景

**目标标杆**: BRAE 几何金属场景

**测试prompt**:
```
Creative concept beverage photography, rose gold beverage can 
and crystal cocktail glass arranged in geometric rose gold metal 
framework, modern minimalist aesthetic with clean lines, purple 
gradient background with soft bokeh effect, hard directional 
lighting creating metallic reflections, luxurious and futuristic 
atmosphere, high-end commercial photography, sharp focus on 
products, artistic composition, sophisticated and elegant
```

**评估标准**:
- 几何框架结构 ✓ / ✗
- 金属质感真实 ✓ / ✗
- 紫色背景渐变 ✓ / ✗
- 现代奢华感 ✓ / ✗
- 产品清晰突出 ✓ / ✗

**期望达成率**: ≥80% (4/5项)

---

## 持续优化机制

### 反馈收集

```python
feedback_template = {
    "generation_id": "xxx",
    "scene_type": "动态飞溅型",
    "quality_score": 85,
    "strengths": [
        "液体飞溅效果出色",
        "光影处理专业"
    ],
    "weaknesses": [
        "产品标签细节不够清晰",
        "背景不够纯黑"
    ],
    "improvement_actions": [
        "增加'ultra sharp product label'关键词",
        "强调'pure black background, no ambient light'"
    ]
}
```

### Prompt优化库

建立"成功案例-Prompt"数据库：

```
成功案例1：
风格：动态飞溅型
产品：红酒
质量评分：92/100
成功Prompt：[完整prompt内容]
关键因素：S-curve motion + backlit + crystal droplets

成功案例2：
风格：静物氛围型
产品：威士忌
质量评分：88/100
成功Prompt：[完整prompt内容]
关键因素：bokeh lights + warm ambient + wooden bar
```

### 版本迭代

```
V1.0 (当前版本)
- 基础5大风格
- 33个场景模板
- 标准prompt模板

V1.1 (计划改进)
- 增加质量验证系统
- 优化prompt关键词库
- 添加对标案例对比

V2.0 (未来规划)
- 自动质量评估
- AI prompt自优化
- 多轮迭代生成机制
```

---

## 质量保证承诺

**基线保证**：
- 产品清晰可见率：≥95%
- 光影专业度：≥80分（百分制）
- 商业可用率：≥85%
- 整体满意度：≥4.0/5.0

**卓越目标**：
- 达到标杆案例水平：≥80%场景
- 超越标杆案例：≥20%场景
- 零重拍率：<5%

**不达标补救**：
- 免费重新生成
- prompt优化建议
- 参数调整指导
- 直到满意为止

---

使用本技能时，请遵循质量验证流程，确保每张生成的大片都达到商业摄影标准！
