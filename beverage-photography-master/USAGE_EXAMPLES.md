<!-- Copyright 2026 FancyAI -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 使用示例

本文档演示如何使用酒水饮料商业大片拍摄技能。

**默认批量参数**（与 [SKILL.md](SKILL.md) 一致）：模型 `nano-banana-pro`，分辨率 `4K`；**比例**在用户未指定时为场景 1 → `16:9`，场景 2～5 → `3:4`。下文代码若未另作说明，应优先遵循该默认值。

## ⚠️ 重要：产品图要求

### 正确的产品图

用户必须提供**纯净的产品图**：
- ✅ 白底或简单纯色背景
- ✅ 产品清晰完整可见
- ✅ 无复杂场景元素
- ✅ 电商产品图、官方产品照均可

### 错误的输入

❌ **严禁使用**：
- 参考案例库中的完整场景图
- 已经包含创意拍摄的图片
- 复杂背景的营销大片

### 为什么要用纯净产品图？

**原因**：AI需要基于纯产品图原创策划场景，而不是模仿现有场景。

**参考案例的正确用途**：
- 学习光影技巧
- 学习构图原则
- 学习色彩搭配
- 不作为生成输入

---

## 快速开始

### 示例1：威士忌产品拍摄

**用户输入**
```
帮我拍摄这瓶威士忌的商业大片
[附带产品图：纯净的产品照，白底或简单背景]
```

**AI工作流程**

**1. 产品分析**
```
产品类型: 威士忌（烈酒类）
液体颜色: 琥珀色
包装风格: 奢华高端
瓶身设计: 玻璃瓶，标签精致
品牌定位: 高端奢侈
目标场景: 酒吧、高端会所
```

**2. 场景策划**
选择5个风格：
1. 静物氛围型（主推）- 温暖酒吧场景
2. 动态飞溅型 - 冰块溅射
3. 微距特写型 - 液体细节
4. 场景叙事型 - 壁炉边享受
5. 创意概念型 - 金属几何空间

**3. 生成大片**

每个场景调用生图工具：

```python
import sys
sys.path.append('/Users/mac/py')
from http_nano_banana import nano_banana_image_gen_sync

# 场景1：静物氛围型
prompt_1 = """
Atmospheric lifestyle beverage photography, premium whiskey bottle and glass 
on wooden bar counter, warm ambient lighting, soft bokeh background with 
blurred lights, shallow depth of field, golden hour glow, cozy bar atmosphere, 
professional product photography, amber liquid in glass, luxury setting, 
cinematic mood, high-end commercial shot
"""

# 重要：这里传入的是用户的纯产品图，不是参考案例
result_urls = nano_banana_image_gen_sync(
    prompt=prompt_1,
    img_urls=["用户的威士忌产品图URL"],  # 纯净产品图
    app_model_type="nano-banana-pro",
    ratio="16:9",  # 批量场景1默认比例
    image_size="4K",  # 文件约10-15MB
    pic_num=1
)
print(f"场景1生成成功: {result_urls[0]}")
```

**4. 输出结果**
```
✅ 场景1/5：静物氛围型
描述：温暖的酒吧环境，威士忌瓶和酒杯置于木质吧台，散景效果
图片：https://ccdn.fancybos.com/result_1.jpg

✅ 场景2/5：动态飞溅型
描述：威士忌瓶和酒杯，冰块飞溅，琥珀色液体，深色背景
图片：https://ccdn.fancybos.com/result_2.jpg

✅ 场景3/5：微距特写型
描述：超近距离拍摄冰块和威士忌液体，展现晶莹剔透质感
图片：https://ccdn.fancybos.com/result_3.jpg

✅ 场景4/5：场景叙事型
描述：壁炉边的威士忌，温暖火光映照，营造冬日氛围
图片：https://ccdn.fancybos.com/result_4.jpg

✅ 场景5/5：创意概念型
描述：金色几何框架中的威士忌瓶，现代奢华艺术表达
图片：https://ccdn.fancybos.com/result_5.jpg
```

---

## 示例2：鸡尾酒拍摄

**用户输入**
```
这是我们新推出的粉色鸡尾酒，需要社交媒体宣传图
[本地图片：/Users/mac/products/pink_cocktail.png]
```

**AI工作流程**

**1. 产品分析**
```
产品类型: 鸡尾酒
液体颜色: 粉红色
装盛方式: 鸡尾酒杯
品牌定位: 年轻时尚
目标场景: 社交媒体、年轻聚会
```

**2. 场景策划**
选择5个风格：
1. 微距特写型（主推）- 社交媒体友好
2. 动态飞溅型 - 倾倒瞬间
3. 创意概念型 - 渐变背景
4. 场景叙事型 - 派对桌面
5. 静物氛围型 - 精致摆拍

**3. 生成参数**

```python
# 场景1：微距特写型（适合社交媒体的方形构图）
prompt = """
Macro beverage photography, extreme close-up of pink cocktail, 
crystal clear ice cubes with pristine details, fresh berry garnish, 
tiny bubbles and condensation droplets, pink to purple gradient background, 
soft diffused lighting, shallow depth of field, ultra sharp focus on details, 
fresh and vibrant colors, commercial product photography
"""

result_urls = nano_banana_image_gen_sync(
    prompt=prompt,
    img_urls=["/Users/mac/products/pink_cocktail.png"],  # 本地路径自动上传
    app_model_type="nano-banana-pro",
    ratio="3:4",  # 批量场景2~5默认；若需竖屏可改为 9:16
    image_size="4K",
    pic_num=1
)
```

---

## 示例3：啤酒夏日主题

**用户输入**
```
拍摄我们的新款精酿啤酒，主题是夏日户外
[产品图URL]
```

**场景策划**
1. 场景叙事型（主推）- 海滩冰桶
2. 微距特写型 - 冰霜凝结
3. 动态飞溅型 - 泡沫爆发
4. 场景叙事型 - 泳池派对
5. 创意概念型 - 蓝色清凉风

**比例选择**（与 SKILL 默认一致）
- 场景1：`16:9`（首张横版）
- 场景2～5：`3:4`（竖构图友好）

---

## 示例4：高端葡萄酒

**用户输入**
```
这是一瓶陈年红酒，需要体现历史感和品质
[产品图]
```

**场景策划**
1. 静物氛围型（主推）- 酒窖场景
2. 动态飞溅型 - 红酒液体飞溅
3. 场景叙事型 - 餐桌红酒时光
4. 微距特写型 - 酒液质感
5. 创意概念型 - 镜面反射

**模型选择**
使用 `nano-banana-pro` 获得顶级质量：

```python
result_urls = nano_banana_image_gen_sync(
    prompt=prompt,
    img_urls=[product_image_url],
    app_model_type="nano-banana-pro",  # 顶级质量
    ratio="16:9",  # 或与当前场景序号匹配：场景1 用 16:9，2~5 用 3:4
    image_size="4K",
    pic_num=1
)
```

---

## 常见场景组合推荐

### 社交媒体推广
- 微距特写型 + 创意概念型 + 场景叙事型
- 比例：默认仍以 SKILL 为准（场景1 `16:9`，2～5 `3:4`）；若渠道要求可选用 9:16 或 1:1
- 色彩：高饱和、渐变背景

### 电商产品页
- 静物氛围型 + 微距特写型 + 动态飞溅型
- 比例：默认 `16:9` / `3:4`；若平台主图强制方形可再改为 1:1
- 重点：产品细节清晰

### 品牌形象宣传
- 静物氛围型 + 场景叙事型 + 创意概念型
- 比例：与 SKILL 默认一致；横版主视觉可优先场景1 的 `16:9`
- 氛围：高端、有故事感

### 季节性营销
- 夏季：场景叙事型（户外）+ 微距特写型（清爽）
- 冬季：静物氛围型（温暖）+ 场景叙事型（居家）
- 节日：创意概念型（节日元素）+ 场景叙事型（聚会）

---

## 高级技巧

### 1. 参考图最佳实践

**单一产品图**
```python
img_urls=["product_image.jpg"]
```

**多角度产品图**
```python
# 如果有多个角度，选择最清晰的一张
img_urls=["product_front_view.jpg"]
```

### 2. 分辨率选择指南

- **1K**: 快速预览、社交媒体小图（约1-2MB）
- **2K**: 网络使用、电商详情页（约2-5MB）
- **4K**: 超高清、印刷品、大尺寸展示（约10-15MB）**推荐**

### 3. 比例选择策略

- **本 Skill 批量默认**：场景1 → `16:9`，场景2～5 → `3:4`（见 SKILL.md）
- **1:1方形**: Instagram、产品展示、通用性强（用户明确要求时可改用）
- **16:9横版**: 网站Banner、电脑端展示
- **9:16竖版**: 手机端、竖屏视频封面、Story

### 4. 模型选择建议

**nano-banana-pro**（本 Skill 默认）
- 质量与细节最佳，与 SKILL 中「4K 大片」流程一致
- 速度相对较慢（约30-60秒）
- 适合商业出片与印刷延展

**其他模型**（若接入方提供）：仅作快速预览时可选用，成稿仍以 `nano-banana-pro` + `4K` 为准

---

## 故障排查

### 问题1：生成的图片产品不够清晰

**解决方案**
- 在prompt中强调：`ultra sharp focus on product`, `product in sharp detail`
- 提供更高清的参考图
- 使用 `nano-banana-pro` 模型

### 问题2：场景风格不符合预期

**解决方案**
- 检查prompt是否包含风格关键词
- 参考 `photography-styles.md` 中的prompt模板
- 增加更具体的场景描述

### 问题3：生成超时

**解决方案**
- 检查网络连接
- 增加 `timeout` 参数：`timeout=180.0`（3分钟）
- 降低分辨率：使用 `1K` 或 `2K` 代替 `4K` 做快速重试

### 问题4：本地图片上传失败

**解决方案**
- 确认文件路径正确
- 确认文件格式支持（jpg, png等）
- 检查文件大小（建议<10MB）
- 改用图片URL

---

## 最佳实践总结

1. **提供高质量产品图** - 清晰、光线好、背景干净
2. **明确使用场景** - 告知AI用途（社交媒体/电商/印刷品）
3. **批量生成** - 一次生成5张不同风格，提供选择空间
4. **保存prompt** - 满意的结果记录下prompt，后续复用
5. **灵活调整比例** - 根据最终用途选择合适比例
6. **合理选择模型** - 本 Skill 默认 `nano-banana-pro` + `4K`

---

现在就开始使用这个强大的酒水饮料大片拍摄技能吧！🍷✨
