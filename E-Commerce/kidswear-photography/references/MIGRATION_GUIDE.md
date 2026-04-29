# ⚠️ Important Update: Unified Prompt Structure

## 📋 Change Notes

### Previous Method (Deprecated)

**Example A and Example B separated:**
```
The user needed to choose:
- If Korean model / mass brand → Use Example A
- If European model / luxury → Use Example B

Problems:
❌ Required human judgment
❌ Two different structures
❌ Limited flexibility
```

### Current Method (Recommended)

**Unified Automated Workflow:**
```
Just provide a white-background image →
Automatically analyze garment →
Automatically select model type and generation model →
Automatically construct 9-layer precise prompt →
Generate five 3:4 vertical images

Advantages:
✅ Fully automated
✅ Unified 9-layer structure  
✅ Flexible expression matching
✅ Easy to maintain
```

---

## 📚 New Document System

### Core Documents

1. **[UNIFIED_PROMPT_BUILDER.md](UNIFIED_PROMPT_BUILDER.md)** ⭐
   - Unified 9-layer prompt building system
   - Automated decision logic
   - Complete template library

2. **[PROMPT_CONFIGURATIONS.md](PROMPT_CONFIGURATIONS.md)** ⭐
   - Configuration examples for different garment types
   - Complete configuration for 5 scenes
   - Quick reference comparison table

3. **[EXPRESSION_GUIDE.md](EXPRESSION_GUIDE.md)**
   - Complete expression option library
   - Flexibly chosen based on garment
   - No longer fixed "smile" or "serious"

### Support Documents

- **[COMMERCIAL_PHOTOGRAPHY_STANDARDS.md](COMMERCIAL_PHOTOGRAPHY_STANDARDS.md)** - Commercial editorial standards
- **[CURRENT_WORKFLOW_STATUS.md](CURRENT_WORKFLOW_STATUS.md)** - Current workflow status
- **[REFERENCES.md](REFERENCES.md)** - 23 sets of reference cases

---

## 🚀 Quick Start (New Method)

### Step 1: Analyze Garment
```python
garment_analysis = analyze_garment(garment_url)
# Auto-identifies: category/style/brand tier/colors etc.
```

### Step 2: Auto-Generate Configuration
```python
config = auto_config_from_garment(garment_analysis)
# Auto-selects: model type/generation model/expression/scene etc.
```

### Step 3: Construct Prompt
```python
for shot in [shot1, shot2, shot3, shot4, shot5]:
    prompt = build_9_layer_prompt(config, shot)
    # Uniformly uses 9-layer precise structure
```

### Step 4: Generate Images
```python
if config["generation_model"] == "image_gen":
    result = image_gen_sync(prompt, ...)
else:
    result = seedream_gen_image_sync(prompt, ...)
```

---

## 🔄 Migration Guide

### If you previously used Example A

**Before:**
```python
# Example A: Korean fashion model
korean_model_base = "..."
# Manually write 8-layer prompt
```

**Now:**
```python
# Auto-judged as Asian model
config = auto_config_from_garment(garment_analysis)
# config["model_race"] = "asian"
# config["generation_model"] = "seedream"

# Use unified 9-layer structure
prompt = build_9_layer_prompt(config, shot_config)
```

### If you previously used Example B

**Before:**
```python
# Example B: Luxury tier model  
luxury_model_character = "..."
# Manually define 9-layer variables
```

**Now:**
```python
# Auto-judged as European model
config = auto_config_from_garment(garment_analysis)
# config["model_race"] = "european"
# config["generation_model"] = "image_gen"

# Use unified 9-layer structure (same building method)
prompt = build_9_layer_prompt(config, shot_config)
```

---

## ❓ FAQ

### Q1: Can I still manually choose the model type?

**A: Yes!**
```python
config = auto_config_from_garment(garment_analysis)

# You can manually override
config["model_race"] = "european"  # Force European model
config["expression"] = "luxury_serious"  # Force specific expression
```

### Q2: Will expressions be selected automatically?

**A: Yes!**

The system automatically matches based on garment type:
- Luxury → serious calm / composed confidence
- Sportswear → focused determination / energetic vitality  
- Princess dress → gentle sweetness / dreamy elegance
- Casual wear → bright cheerful smile / relaxed ease
- Streetwear → cool edgy vibe / confident swagger

But you can also manually specify it.

### Q3: Will the composition of the 5 images be configured automatically?

**A: Yes!**

Uniformly uses 5 shot types:
1. Full-body standard stance
2. Dynamic frozen moment (or 2nd full-body pose)
3. Side profile garment display
4. 3/4 body top details
5. Half-body garment close-up

### Q4: Do I need to learn new code?

**A: Basically no!**

The core logic is already encapsulated. You just need to:
1. Provide the white-background image URL
2. Call the generation function
3. Get the results of the 5 images

---

## 📖 Recommended Reading Order

**First-time use:**
1. Read this document (MIGRATION_GUIDE.md)
2. Check [PROMPT_CONFIGURATIONS.md](PROMPT_CONFIGURATIONS.md) to understand configuration examples
3. Refer to [UNIFIED_PROMPT_BUILDER.md](UNIFIED_PROMPT_BUILDER.md) to understand technical details

**Daily use:**
1. Directly refer to [PROMPT_CONFIGURATIONS.md](PROMPT_CONFIGURATIONS.md) for quick configuration
2. When needing to adjust expressions, check [EXPRESSION_GUIDE.md](EXPRESSION_GUIDE.md)

---

## ✅ Core Advantages Summary

### Previous Problems
- ❌ Needed to choose between Example A or B
- ❌ Two different prompt structures
- ❌ Korean models couldn't wear luxury
- ❌ Fixed expressions

### Current Advantages
- ✅ Fully automated, no need to choose
- ✅ Unified 9-layer precise structure
- ✅ Any model can wear any clothes
- ✅ Expressions flexibly match garments
- ✅ Easier to maintain and expand

---

**Start using the new unified system!** 🚀
