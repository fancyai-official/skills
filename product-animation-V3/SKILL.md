---
name: product-animation-fancyai
description: Use Seedance or Kling to batch generate animation clips from multiple static product images and stitch them into a complete video. Use this skill when the user mentions product animations, image-to-video, animating static images, Seedance, Kling, animation prompts, or product video generation.
---

# Product Animation Generation Skill

> All execution functions, prompt dictionaries, and script templates can be found in [code-snippets.md](references/code-snippets.md), read them when needed.

## Instructions

### Workflow Checklist

```
- [ ] Step 0 (Optional): Fetch images from admin backend -> Both modes use ListAssetsImage (available assets) + tagNameList filtering
                      Use group_images_by_product() to create folders by product for merchant batch mode
- [ ] Step 1: Get image sources -> image_sources
- [ ] Step 2: Visual analysis of each image -> image_analyses (image_desc / motion_hint / has_model / shot_type / focus_point)
              -> Admin backend source: ListAssetsImage is filtered server-side, skip _is_product_shot
              -> Local folder source: User has manually selected, use all images directly, skip _is_product_shot
              -> has_model -> Select tool (kling / seedance)
- [ ] Step 3: Conversational confirmation of category + output ratio
- [ ] Step 4: pick_music + calc_clip_durations -> audio_path / clip_durations
- [ ] Step 5: prepare_image + get_prompt -> image_list; write prompt logs
- [ ] Step 6: Concurrent API calls (with retry) -> all_clip_urls
- [ ] Step 7: merge_videos stitch and mix audio -> Final video
```

> **Only 4 variables are passed to the video models: source image URL, prompt, duration, and ratio.**
> Among them, `image_desc` (Step 2) is the only variable bound to the image semantics, directly determining the upper limit of the video quality.

### Step 0: Admin Backend Assets (Optional)

| API Purpose | URL | Method |
|---|---|---|
| Login | `https://ccapi.fancybos.com/admin/login` | POST |
| Merchant Search | `https://ccapi.fancybos.com/cms-merchant/searchNoPage` | POST `{"name":"..."}` |
| Product List (parse internal fancyItemId) | `https://hubapi.fancybos.com/hub-assets/assets/product/queryProductList` | POST |
| **Available Assets** (corresponds to "Available Assets" page in admin) | `https://hubapi.fancybos.com/hub-assets/assets/image/ListAssetsImage` | POST |

> Warning: `ListAssetsImage` requires the full `assetsTagCategoryDTOList` (6 tagCategory items, each containing complete null fields), the simplified version returns empty. The return key is `data` (not `result`).

**Two Modes (Both use ListAssetsImage available assets + tagNameList filtering):**

| Mode | Trigger Condition | Images Returned per Product |
|---|---|---|
| Specific Product | Pass `fancy_item_ids` (platform itemId) | All valid available assets |
| Merchant Batch | Pass `merchant_name/merchant_id` | All valid available assets (can be limited by `max_images_per_product`) |

**Available Asset Filtering Rules (`tagNameList` field, server-side has already excluded unavailable images):**

| Condition | Action |
|---|---|
| `tagNameList` contains **Model Shot** | Keep |
| `tagNameList` contains **Scene Shot** | Keep |
| `tagNameList` contains **Detail Shot** | Keep |
| `imageRatio < 0.3` or `> 3.0` | Discard (abnormal ratio) |
| Others (product on white background, untagged, etc.) | Discard |

> In merchant batch mode, use `group_images_by_product()` to group by product, creating a separate folder for each product.
> Folder naming: `{itemId}/` (pure numbers, no Chinese characters, cross-platform compatible)
> **Minimum image count:** Products with < 3 images after filtering are automatically skipped (`min_images=3`, adjustable).

### Step 2: Visual Analysis of Key Variables

> **Only variables marked with * truly affect video content, others are auxiliary variables for the workflow.**

| Variable | Purpose | Impact |
|---|---|---|
| `image_desc` * | prompt layer1, bound to image semantics | Goes directly into prompt, quality upper limit |
| `has_model` * | Determines whether to use Kling or Seedance | Engine selection |
| `motion_hint` * | Routes to material animation base prompt | Animation style |
| `focus_point` * | Centers subject when cropping | Takes effect only when cropping |
| `shot_type` | Image type annotation (for reference only, currently neither source filters based on this) | Does not enter prompt |
| `is_dual` | Dual-panel image judgment (two products/views stitched horizontally or vertically) -> Filter if True | Does not enter prompt |
| `is_visual_duplicate` | Highly visually similar to other images in the same group -> Filter if True, keep the richest one | Does not enter prompt |
| `category_guess` | Provided for user confirmation in Step 3 | Does not enter prompt |

#### image_desc Format
```
[Brand] [color] [product name], [material/form], [background], <=20 words, English
Example: "NEI WAI model in coral T-shirt, white studio background"
         "MAC coral-red lipstick, matte metallic tube, white background"
```

#### motion_hint Values

| Value | Applicable Material/Scene |
|---|---|
| `liquid` | Serums, lotions (visible liquid in image) |
| `solid` | Lipsticks, compact powders, 3C products (sealed packaging) |
| `fabric` | Clothing, scarves |
| `shiny_gem` | Diamond rings, crystals (gemstone refraction) |
| `metal` | Metal chains, watches (light sweeps) |
| `hot` | Coffee, ramen (visible steam in image) |
| `cold` | Cold drinks (visible condensation droplets in image) |
| `plush` | Plush toys, mattresses |
| `soft` | Maternity/baby cotton products, silicone pacifiers |
| `material` | Furniture surfaces, rugs, lamps |
| `mechanical` | Drones, fans, camera lenses |
| `default` | Others |

> **Principle: Only animate materials/states already visible in the image, do not infer invisible states.**
> Sealed bottle -> `solid` (do not choose `liquid`); No visible steam -> do not choose `hot`

#### shot_type Reference Values

> `shot_type` is currently not used for any filtering, only as an auxiliary annotation to understand the image type.

| shot_type | Meaning |
|---|---|
| `product_shot` / `detail_shot` / `model_shot` | Product shot / detail shot / model shot |
| `lifestyle_scene` / `graphic_poster` / `scene_only` | Lifestyle scene / poster / background only |

### Step 3: Conversational Confirmation of Category + Ratio

**You MUST proactively ask the user** (using the AskQuestion tool or replying with text directly) to confirm the following two options:

1. **Product Category (Choose 1 of 8)**:
   (It is recommended to first give your inference based on the images, and let the user confirm)
   `Clothing/Accessories` | `Beauty/Skincare` | `Food/Beverages` | `Digital/3C` | `Jewelry/Accessories` | `Home/Furniture` | `Pet Supplies` | `Maternity/Baby`

2. **Output Ratio (Choose 1 of 5)**:
   - `adaptive` (Automatically follows source image, **recommended for horizontal products like home/digital**)
   - `9:16` (Vertical)
   - `1:1` (Square)
   - `16:9` (Horizontal)
   - `3:4` (Seedance only)

Only proceed with subsequent code execution and workflow after the user has answered and confirmed.

### Steps 4-7: Execution

> All execution code (script templates) can be found in [code-snippets.md §Script Templates](references/code-snippets.md), read them as needed.

| Step | Core Function | Key Parameters |
|---|---|---|
| Step 4 | `pick_music` + `calc_clip_durations` | Kling: target_duration=3; Seedance: min=4, max=5 |
| Step 5 | `prepare_image` + `get_seedance_prompt` / `get_kling_shot_prompt` | focus_point crop centering |
| Step 6 | `seedance20_video_gen_sync` / `kling_multi_shot_sync` + `call_with_retry` | Concurrent ThreadPoolExecutor; **Seedance max_workers=3, Kling max_workers=5**, exceeding will trigger rate limiting |
| Step 7 | `merge_videos` | Seedance: trim_per_clip=3; Kling: None |

**Acceptance Criteria:** Product subject has no deformation, no merging, no text watermarks, smooth animation, no black frames at stitching points.

> Stop **Anti-Disturbance Limit**: After script execution completes, only print the final video file path in the chat box. **Strictly forbidden** for AI to proactively use the terminal `open` command to automatically open and play the video, so as not to interrupt the user's workflow.

> **Deduplication Pipeline (Batch Mode):**
> 1. URL Layer (inside `fetch_assets_from_content_hub`) — Keep only one copy of identical URLs across products
> 2. AI Layer (`is_dual` / `is_visual_duplicate`) — Manually flagged during Step 2 visual analysis
> 3. pHash Layer (`_dedup_by_phash`, threshold 8) — Automatically filters visually similar images during runtime
>    ▸ Dependency: `pip install imagehash`; Automatically skipped if not installed, does not affect main flow
> 4. Recheck count after pHash, skip the product if < 3 images

## Examples

### Example 1: Animation Generation for a Single Product
**User says:** "Help me animate these lipstick images"
**Actions:**
1. Visually analyze the images, determine the `has_model` status and corresponding material `motion_hint` (e.g., `solid`).
2. Confirm the category (Beauty/Skincare) and output ratio (e.g., 9:16) with the user.
3. Select audio and calculate the duration for each clip.
4. Concurrently request the corresponding generation model (Kling or Seedance) based on the presence of a model.
5. After generation is complete, stitch the clips and mix the audio.
**Result:** Automatically outputs an animated product showcase video stitched from multiple lipstick images.

## Troubleshooting

### Error: API Concurrent Calls Trigger Rate Limiting
**Cause:** When processing a large number of images in batch, the concurrent worker threads are set too high.
**Solution:** Ensure that when using `ThreadPoolExecutor`, `max_workers` for Seedance is set to no more than 3, and for Kling is limited to no more than 5, and use `call_with_retry` for retry mechanisms with backoff.

### Error: Execution Function or Prompt Dictionary Not Found
**Cause:** Associated code snippets were not read before skill execution.
**Solution:** Always use the Read tool to read the contents of the `references/code-snippets.md` file before execution.

### Error: Batch Processing Fails Due to Insufficient Asset Quantity
**Cause:** After filtering invalid ratios and similar images, the total number of valid images for a product is less than 3.
**Solution:** When a product has fewer than 3 valid images, automatically record skipping that product and process the next one, while providing feedback to the user on the reason for skipping.
