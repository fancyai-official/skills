# API Parameter Reference

Both interfaces are located in the `scripts/` directory, using an asynchronous submission + polling mode. The `_sync` version blocks until the result returns, returning a list of video URLs.

---

## Seedance 2.0 — `seedance20_video_gen_sync`

**File**: `http_seedance20_video_gen.py`

```python
seedance20_video_gen_sync(
    prompt: str = "",                           # Animation prompt
    first_img_url: str = None,                  # First frame image URL (product image)
    last_img_url: str = None,                   # Last frame image URL (requires first_img_url)
    reference_image_urls: List[str] = None,     # Multimodal reference images (0~9 images)
    reference_video_urls: List[str] = None,     # Multimodal reference videos (0~3 videos, each 2~15s)
    reference_audio_urls: List[str] = None,     # Multimodal reference audios (0~3 audios, each 2~15s)
    duration: int = 5,                          # Duration (seconds), range 4~15, or -1 for model auto-select
    ratio: str = "adaptive",                    # Aspect ratio, see enum; adaptive automatically follows input image
    resolution: str = "720p",                   # Resolution, see enum
    vid_num: int = 1,                           # Number to generate, default 1
    generate_audio: bool = True,                # Whether to generate ambient audio (False recommended for product animations)
    model: str = "doubao-seedance-2-0-260128",  # Model version, see enum
    enable_web_search: bool = False,            # Web search (only for text-to-video)
)
```

**ratio Enum**: `"adaptive"` `"1:1"` `"3:4"` `"4:3"` `"9:16"` `"16:9"` `"21:9"`

**resolution Enum**: `"480p"` `"720p"`

**model Enum**: `"doubao-seedance-2-0-260128"` (Standard) / `"doubao-seedance-2-0-fast-260128"` (Fast)

> Recommendation for product animations: `ratio="adaptive"` (auto-follow image), `generate_audio=False` (bring your own BGM)

---

## Kling Multi-Shot — `kling_multi_shot_sync`

**File**: `http_kling_multi_shot.py`
**Applicable**: Model walking, wearing showcase, multi-scene narrative.

```python
kling_multi_shot_sync(
    prompt: str,                                        # Required, overall description
    shot_type: str = "customize",                       # Shot mode, see enum
    multi_prompt: List[dict] = None,                    # Custom shots list (required when customize)
    image_urls: List[str] = None,                       # Reference image URL list
    model: str = "kling_3.0-Omni_multi_shot",           # Model version
    resolution: str = "1080P",                          # Resolution, see enum
    aspect_ratio: str = None,                           # Aspect ratio, see enum (None determined by model)
    enhance_prompt: str = "Disabled",                   # Model enhanced prompt: Enabled / Disabled
    audio_generation: str = None,                       # Generate audio: Enabled / Disabled
    enhance_switch: str = None,                         # Super-resolution enhancement: Enabled / Disabled
)
```

**shot_type Enum**:
- `"customize"` — Manually specify the prompt and duration for each shot, requires multi_prompt
- `"intelligence"` — Model automatically generates shots based on prompt, no multi_prompt required

**multi_prompt Format** (required when customize, up to 6 shots):
```python
multi_prompt = [
    {"index": 1, "prompt": "Shot 1 scene description", "duration": 5},
    {"index": 2, "prompt": "Shot 2 scene description", "duration": 3},
]
```

**resolution Enum**: `"720P"` `"1080P"` `"2K"` `"4K"`

**aspect_ratio Enum**: `"16:9"` `"9:16"` `"1:1"` (pass `None` to let model decide)

**Toggle Parameters** (all strings):
- `enhance_prompt`: `"Enabled"` / `"Disabled"` (Default Disabled)
- `audio_generation`: `"Enabled"` / `"Disabled"` (Default not passed = not generated)
- `enhance_switch`: `"Enabled"` / `"Disabled"` (Super-resolution, default not passed)

---

## Quick Reference for Common Parameters

| Scenario | Interface | ratio | duration | resolution |
|------|------|-------|----------|------------|
| Static product image (auto ratio) | Seedance 2.0 | `"adaptive"` | 5 | `"720p"` |
| Forced vertical (9:16) | Seedance 2.0 | `"9:16"` | 5 | `"720p"` |
| Forced square (1:1) | Seedance 2.0 | `"1:1"` | 5 | `"720p"` |
| Model showcase vertical | Kling | `"9:16"` | — | `"1080P"` |
| Multi-scene narrative | Kling | `"16:9"` | — | `"1080P"` |
