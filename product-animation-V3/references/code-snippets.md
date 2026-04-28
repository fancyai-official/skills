# Execution Code Library

All functions and data dictionaries referenced in the SKILL.md main workflow, read as needed.

---

## Admin Backend Assets Download Functions

### content_hub_login — Login to get token

```python
import requests, os, time as _time
from datetime import datetime

CCAPI_BASE      = "https://ccapi.fancybos.com"
HUB_ASSETS_BASE = "https://hubapi.fancybos.com/hub-assets"

# Type translation mapping using Unicode escapes to avoid Chinese characters in file
# Maps backend returns (Chinese) to internal English constants
_CH_TO_EN = {
    "\u6a21\u7279\u56fe": "Model Shot",
    "\u573a\u666f\u56fe": "Scene Shot",
    "\u7ec6\u8282\u56fe": "Detail Shot",
    "\u670d\u88c5/\u670d\u9970": "Clothing/Accessories",
    "\u7f8e\u5986\u62a4\u80a4": "Beauty/Skincare",
    "\u98df\u54c1\u996e\u6599": "Food/Beverages",
    "\u6570\u78013C": "Digital/3C",
    "\u73e0\u5b9d/\u914d\u9970": "Jewelry/Accessories",
    "\u5bb6\u5c45/\u5bb6\u5177": "Home/Furniture",
    "\u5ba0\u7269\u7528\u54c1": "Pet Supplies",
    "\u6bcd\u5a74\u7528\u54c1": "Maternity/Baby",
    "\u670d\u52a1": "Service",
    "\u865a\u62df\u5546\u54c1": "Virtual Product",
    "\u7535\u5b50\u4e66": "E-book",
    "\u8bfe\u7a0b": "Course",
    "\u8f6f\u4ef6": "Software"
}

# Confirmed real endpoints:
#   Merchant Search: GET  {CCAPI_BASE}/cms-merchant/searchNoPage
#   Product List: POST {HUB_ASSETS_BASE}/assets/product/queryProductList
#   Both APIs use ccapi_token (same account login)

def content_hub_login(phone: str = None, password: str = None) -> dict:
    """
    Login to the admin backend, return token dictionary.
    Credential priority: function arguments > config.json > interactive input.
    After initial input, ask whether to save to config.json, auto-read next time.
    ccapi_token is valid for both ccapi.fancybos.com and hubapi.fancybos.com/hub-assets.
    """
    import json as _json, os as _os, getpass as _gp

    # 1. Read config.json (prefer in SKILL_DIR/assets, then current directory)
    # SKILL_DIR is defined at the top of the generated script; __file__ points to the script itself (under scripts/)
    _skill_dir = globals().get("SKILL_DIR", _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    _cfg = {}
    for _p in [
        _os.path.join(_skill_dir, "assets", "config.json"),
        _os.path.join(_os.getcwd(), "config.json"),
    ]:
        if _os.path.exists(_p):
            with open(_p, encoding="utf-8") as _f:
                _cfg = _json.load(_f)
            _cfg_path = _p
            break
    else:
        _cfg_path = _os.path.join(_skill_dir, "assets", "config.json")

    phone    = phone    or _cfg.get("hub_phone")
    password = password or _cfg.get("hub_password")

    # 2. Interactive input if credentials are incomplete
    if not phone or not password:
        print("\n Admin Backend Login (Initial Setup)")
        if not phone:
            phone = input("  Enter phone number: ").strip()
        if not password:
            password = _gp.getpass("  Enter password (hidden): ").strip()
        if not phone or not password:
            raise ValueError("Phone number and password cannot be empty")

        # 3. Ask whether to save
        save = input("  Save to config.json to avoid entering again? (y/n, default y): ").strip().lower()
        if save != "n":
            with open(_cfg_path, "w", encoding="utf-8") as _f:
                _json.dump({"hub_phone": phone, "hub_password": password}, _f,
                           ensure_ascii=False, indent=2)
            print(f"  Saved to {_cfg_path}")

    resp = requests.post(
        f"{CCAPI_BASE}/admin/login",
        json={"phone": phone, "password": password},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    token = f"{data['tokenHead']}{data['token']}".strip()
    print("Admin backend login successful")
    return {"ccapi_token": token}
```

---

### fetch_assets_from_content_hub — Search and download product images

```python
def fetch_assets_from_content_hub(
    tokens: dict,
    download_dir: str = None,       # Local download directory; None = do not download, return OSS/CDN URL directly
    merchant_name: str = None,      # Merchant name (fuzzy match), mutually exclusive with merchant_id
    merchant_id: int = None,        # Merchant ID (direct specification, higher priority than merchant_name)
    item_name: str = None,          # Search by SKU name / product name keywords
    category: str = None,           # Filter by category, e.g., "Clothing", "Beauty/Skincare" (client-side filtering)
    start_date: str = None,         # Created time start, format "2024-01-01"
    end_date: str = None,           # Created time end, format "2024-12-31"
    fancy_item_ids: list = None,    # List of product IDs input by user (platform itemId / Taobao ID)
    max_images_per_product: int = None,  # Max images per product; None=unlimited
    page_size: int = 50,
) -> list:
    """
    Fetch product images from admin backend "Product Assets Management", return list of image paths/URLs.

    Two modes (Both use ListAssetsImage to fetch "Available Assets" + tagNameList type filtering):
      1. Specific Product Mode (fancy_item_ids is not empty):
         -> Use queryProductList to parse platform itemId -> internal fancyItemId
         -> Call ListAssetsImage for the specific product (returns only available assets), filter by tagNameList and return

      2. Merchant Batch Mode (only provide merchant_name/merchant_id):
         -> Use queryProductList to paginate through all products of the merchant
         -> Call ListAssetsImage for each product, keep Model Shot / Scene Shot / Detail Shot
         -> max_images_per_product controls the maximum number of images per product (unlimited by default)

    ListAssetsImage returns the images displayed on the "Available Assets" page in the admin backend (unavailable ones already filtered),
    no need to check labelDeleted again, the tagNameList field replaces the labelAttr type tag.

    download_dir=None (default): return OSS/CDN URL directly, prepare_image() can use it directly.
    download_dir="/path/..." : download to local and return local path (use when network is unstable).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
    token = tokens.get("ccapi_token", "")
    headers = {"Authorization": token, "Content-Type": "application/json"}

    # ── Step 1: Parse Merchant ID ──────────────────────────────────────────────────
    if merchant_id is None:
        if not merchant_name and not fancy_item_ids:
            raise ValueError("Must provide one of merchant_name, merchant_id, or fancy_item_ids")
        if merchant_name:
            # searchNoPage must POST + JSON body {"name": ...}, GET will 500
            # If only fancy_item_ids is provided, skip this step, merchant_id remains None for API to match
            resp = requests.post(
                f"{CCAPI_BASE}/cms-merchant/searchNoPage",
                json={"name": merchant_name},
                headers=headers, timeout=15,
            )
            resp.raise_for_status()
            merchants = resp.json().get("data", [])
            if not merchants:
                raise ValueError(f"Merchant not found: {merchant_name}, please check if the name matches the admin backend")
            if len(merchants) > 1:
                # Prioritize exact match when multiple results, otherwise take the first
                exact = [m for m in merchants if m.get("name") == merchant_name]
                chosen = exact[0] if exact else merchants[0]
                print(f"  Warning: Found {len(merchants)} merchants, selecting: '{chosen['name']}'")
            else:
                chosen = merchants[0]
            merchant_id = chosen["id"]
            print(f"Merchant '{chosen['name']}' -> merchantId={merchant_id}")

    # ── Step 2: Paginate through product list (Parse internal fancyItemId) ─────────────────────
    all_products = []
    page_num = 1
    while True:
        payload = {
            "merchantId":        merchant_id,
            "pageNum":           page_num,
            "pageSize":          page_size,
            "platformSkuIds":    [],
            "fancyItemIdList":   fancy_item_ids or [],   # Pass platform itemId, API matches internally
            "makeVideoTypeList": [],
            "unAbleMakeVideoTypeList": [],
            "featureSearchList": [],
            "createTimeStart":   f"{start_date} 00:00:00" if start_date else "",
            "createTimeEnd":     f"{end_date} 23:59:59"   if end_date   else "",
            "videoMaxCreatedStart": "",
            "videoMaxCreatedEnd":   "",
        }
        if item_name:
            payload["itemName"] = item_name

        resp = requests.post(
            f"{HUB_ASSETS_BASE}/assets/product/queryProductList",
            json=payload, headers=headers, timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        data = body.get("data", {})
        items = data.get("list", []) if isinstance(data, dict) else []
        
        # Translate category names to English immediately upon receiving
        for it in items:
            cat = it.get("fancyCategoryName")
            if cat in _CH_TO_EN: it["fancyCategoryName"] = _CH_TO_EN[cat]
            cat_name = it.get("categoryName")
            if cat_name in _CH_TO_EN: it["categoryName"] = _CH_TO_EN[cat_name]
            
        all_products.extend(items)

        total = data.get("total", 0) if isinstance(data, dict) else 0
        print(f"  Page {page_num}: Fetched {len(items)} items, accumulated {len(all_products)}/{total}")
        if len(all_products) >= total or len(items) < page_size:
            break
        page_num += 1

    # ── Step 3: Category client-side filtering ───────────────────────────────────────────────
    if category:
        before = len(all_products)
        all_products = [
            it for it in all_products
            if category in (it.get("fancyCategoryName") or "")
            or category in (it.get("categoryName") or "")
        ]
        print(f"Category filter '{category}': {before} -> {len(all_products)} items")

    # ── Step 3.5: Product-level quick pre-filtering (Reduce invalid API requests) ────────────────────────
    all_products = _prefilter_product_shots(all_products)

    mode_label = "Specific Product Mode" if fancy_item_ids else "Merchant Batch Mode"
    print(f"\n {mode_label}: Total {len(all_products)} products, concurrently fetching available assets (ListAssetsImage)...")

    # ── Step 4: Concurrently fetch "Available Assets" per product (ListAssetsImage) + Type Filtering ─────
    # Complete assetsTagCategoryDTOList (Simplified version returns empty, must use this format)
    _ALL_TAGS = [
        {"tagCategory": tc, "tagCategoryName": name, "assetsTagList": [
            {"id": 0, "categoryId": None, "tagName": "\u5168\u90e8", "type": None,
             "parentId": None, "level": None, "createTime": None, "deleted": 0,
             "deletedTime": None, "tagCategory": 0, "totalCount": None,
             "statColName": None, "videoTagForType": None, "relationType": None,
             "isCustomTag": None, "checked": True}
        ]}
        for tc, name in [
            (1, "\u7c7b\u578b"), (2, "\u80cc\u666f"), (3, "\u89c6\u89d2"),
            (4, "\u6a21\u7279\u7c7b\u578b"), (5, "\u5c55\u793a\u4fe1\u606f"), (0, "\u5305\u542b\u63cf\u8ff0")
        ]
    ]
    _KEEP_TYPES = {"Model Shot", "Scene Shot", "Detail Shot"}

    def _fetch_product_images(prod):
        """Single product: ListAssetsImage fetch available assets -> tagNameList type filtering -> return (urls, metas)"""
        internal_fid  = prod.get("fancyItemId")
        prod_merchant = prod.get("merchantId", merchant_id)
        prod_title    = prod.get("productTitle", "")
        prod_category = prod.get("fancyCategoryName", "")
        item_id       = prod.get("itemId", "")

        if not internal_fid:
            return [], []

        try:
            # Paginate through available assets (pageSize=100, loop until exhausted)
            all_imgs, page = [], 1
            while True:
                ori_resp = requests.post(
                    f"{HUB_ASSETS_BASE}/assets/image/ListAssetsImage",
                    json={"pageNum": page, "pageSize": 100,
                          "merchantId": prod_merchant, "fancyItemId": internal_fid,
                          "assetsTagCategoryDTOList": _ALL_TAGS, "hasDesc": None},
                    headers=headers, timeout=30,
                )
                ori_resp.raise_for_status()
                body  = ori_resp.json()
                data  = body.get("data") or {}
                lst   = data.get("list") or [] if isinstance(data, dict) else []
                total = (data.get("total") or 0) if isinstance(data, dict) else 0
                all_imgs.extend(lst)
                if len(all_imgs) >= total or len(lst) < 100:
                    break
                page += 1

            for img in all_imgs:
                # Translate tags from Chinese to English mapping
                tags = img.get("tagNameList") or []
                img["tagNameList"] = [_CH_TO_EN.get(t, t) for t in tags]

            # Type filtering: keep only Model Shot / Scene Shot / Detail Shot, and reasonable ratio
            good_imgs = [
                img for img in all_imgs
                if any(t in _KEEP_TYPES for t in (img.get("tagNameList") or []))
                and 0.3 <= (img.get("imageRatio") or 1.0) <= 3.0
            ]

            if max_images_per_product:
                good_imgs = good_imgs[:max_images_per_product]

            urls = [img["imageUrl"] for img in good_imgs]
            metas = [
                {
                    "fancyItemId":       internal_fid,
                    "itemId":            item_id,
                    "productTitle":      prod_title,
                    "fancyCategoryName": prod_category,
                    "imageUrl":          img["imageUrl"],
                    "imageRatio":        img.get("imageRatio"),
                    "tagNameList":       img.get("tagNameList") or [],
                    # Compatibility with _has_model_from_label: construct labelAttr.type from tagNameList
                    "labelAttr": {
                        "type":       [t for t in (img.get("tagNameList") or [])
                                       if t in ("Model Shot", "Detail Shot")],
                        "background": [t for t in (img.get("tagNameList") or [])
                                       if t == "Scene Shot"],
                    },
                }
                for img in good_imgs
            ]
            print(f"  OK '{prod_title[:18]}' -> {len(all_imgs)} available assets, kept {len(urls)} images")
            return urls, metas
        except Exception as e:
            print(f"  Warning: Fetch failed fancyItemId={internal_fid}: {e}")
            return [], []

    image_sources: list = []
    _last_metas_list: list = []
    _global_seen_urls: set = set()   # Cross-product deduplication

    # Concurrency: Batch mode uses 5, specific product mode uses 3 (usually fewer products)
    workers = 5 if not fancy_item_ids else 3
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_fetch_product_images, prod): prod for prod in all_products}
        for fut in as_completed(futures):
            urls, metas = fut.result()
            for url, meta in zip(urls, metas):
                if url in _global_seen_urls:
                    print(f"  Config: Cross-product duplicate, skipping: {url[-40:]}")
                    continue
                _global_seen_urls.add(url)
                image_sources.append(url)
                _last_metas_list.append(meta)

    print(f"\n Total acquired {len(image_sources)} valid images (from {len(all_products)} products, cross-product duplicates removed)")

    # ── Step 5: Download to local if required ──────────────────────────────────────────────
    if download_dir and image_sources:
        # Inline download logic to avoid depending on external _download_images function
        local_paths = []
        for idx, url in enumerate(image_sources):
            ext = url.split("?")[0].rsplit(".", 1)[-1].lower() or "jpg"
            local_path = os.path.join(download_dir, f"img_{idx:04d}.{ext}")
            try:
                _r = requests.get(url, timeout=30)
                _r.raise_for_status()
                with open(local_path, "wb") as _f:
                    _f.write(_r.content)
                local_paths.append(local_path)
            except Exception as e:
                print(f"  Warning: Download failed [{idx}]: {e}")
        image_sources = local_paths

    fetch_assets_from_content_hub._last_metas = _last_metas_list
    return image_sources


def _prefilter_origin_images(ori_items: list, prod_title: str = "") -> list:
    """
    [Deprecated] Originally used for client-side filtering of queryAssetsImageOriginList.
    The new flow uses ListAssetsImage to directly get available assets, this function is no longer called.
    Kept for reference only, do not call in new scripts.

    Retention rules (Must satisfy both "do not discard" and "hit retention"):
      Do not discard conditions:
        1. imageUrl is not empty
        2. labelDeleted != 1 (top-level field) -> Not marked as unavailable (core filtering of available assets page)
        3. labelAttr.delete is empty           -> Inner labelAttr not marked as deleted
        4. imageRatio within [0.3, 3.0]        -> Not ultra-wide/ultra-tall banner

      Hit retention conditions (Satisfy any):
        A. labelAttr.type contains "Model Shot"      -> Model wear shot
        B. labelAttr.background contains "Scene Shot" -> Shot with scene background
        C. labelAttr.type contains "Detail Shot"     -> Material/local close-up

    Deduplication: Only keep the first entry for identical imageUrls within the same product.
    """
    import json as _json

    kept, dropped = [], []
    seen_urls: set = set()          # Intra-product deduplication
    for img in ori_items:
        url = img.get("imageUrl", "")
        reason = None

        if not url:
            reason = "No imageUrl"
        elif url in seen_urls:
            reason = "Intra-product duplicate URL"
        else:
            seen_urls.add(url)
            label = img.get("labelAttr") or {}
            if isinstance(label, str):
                try:
                    label = _json.loads(label)
                except Exception:
                    label = {}

            delete_flags = label.get("delete", [])
            type_tags    = label.get("type", [])
            bg_tags      = label.get("background", [])
            ratio        = img.get("imageRatio") or 0

            # Do not discard conditions
            if img.get("labelDeleted") == 1:
                reason = "labelDeleted=1 (Marked deleted on available assets page)"
            elif delete_flags:
                reason = f"labelAttr.delete not empty: {delete_flags[0]}"
            elif ratio and (ratio < 0.3 or ratio > 3.0):
                reason = f"Abnormal ratio {ratio}"
            else:
                # Hit retention conditions
                is_model    = "Model Shot" in type_tags
                is_scene    = "Scene Shot" in bg_tags
                is_detail   = "Detail Shot" in type_tags
                # Untagged (type and background are empty) -> Conservatively keep, labelDeleted=0 guarantees availability
                is_untagged = not type_tags and not bg_tags
                if not (is_model or is_scene or is_detail or is_untagged):
                    type_str = "/".join(type_tags) or "No type"
                    bg_str   = "/".join(bg_tags)   or "No background"
                    reason   = f"Not target type (type={type_str}, bg={bg_str})"

        if reason:
            dropped.append(reason)
        else:
            kept.append(img)

    if dropped:
        print(f"    Config: Original image pre-filtering: Dropped {len(dropped)} images, kept {len(kept)} images")
        for r in dropped[:3]:
            print(f"       Skipped: {r}")
    return kept


def _prefilter_product_shots(items: list) -> list:
    """
    Product-level quick pre-filtering: Before fetching original images, filter out obviously unsuitable products (e.g., no original images, pure video products).
    Can be called in both modes after Step 2, before _fetch_product_images, to reduce unnecessary API requests.

    Filtering rules (Discard if any condition is met):
      1. imageOriginCount == 0 and imageCount == 0  -> No asset images at all
      2. fancyCategoryName hits blacklist           -> Services/virtual products etc. not suitable for animation
    """
    CATEGORY_BLACKLIST = {"Service", "Virtual Product", "E-book", "Course", "Software"}

    kept, dropped = [], []
    for it in items:
        reason = None

        # imageCount corresponds to the number of "available assets" in the admin backend; if 0, ListAssetsImage will definitely return empty, skip directly
        if it.get("imageCount", 1) == 0:
            reason = "No available asset images (imageCount=0)"
        elif any(bl in (it.get("fancyCategoryName") or "") for bl in CATEGORY_BLACKLIST):
            reason = f"Category blacklist: {it.get('fancyCategoryName')}"

        if reason:
            dropped.append((it.get("fancyItemId"), reason))
        else:
            kept.append(it)

    if dropped:
        print(f"Config: Product-level pre-filtering: Dropped {len(dropped)} items (kept {len(kept)} items)")
        for fid, r in dropped[:5]:
            print(f"    Skipped fancyItemId={fid}: {r}")
    return kept


def group_images_by_product(image_sources: list, metas: list, base_output_dir: str,
                            min_images: int = 3) -> list:
    """
    Group the flat list of images returned by fetch_assets_from_content_hub by product,
    and create independent output folders for each product.

    Return value: list of dict, each item corresponding to a product:
      {
        "folder":       str,   # Output directory for this product (created)
        "item_id":      str,   # Platform product ID
        "fancy_item_id": int,  # Admin backend internal ID
        "product_title": str,  # Product title
        "category":     str,   # Category
        "image_sources": list, # List of image URLs/paths for this product
      }

    Folder naming rule: {base_output_dir}/{itemId}_{sanitized_title}/
    """
    import re as _re
    from collections import OrderedDict

    # Orderly grouping by fancyItemId (preserve API return order)
    grouped = OrderedDict()
    for src, meta in zip(image_sources, metas):
        fid = meta.get("fancyItemId") or meta.get("itemId")
        if fid not in grouped:
            grouped[fid] = {
                "fancy_item_id":  fid,
                "item_id":        str(meta.get("itemId", fid)),
                "product_title":  meta.get("productTitle", ""),
                "category":       meta.get("fancyCategoryName", ""),
                "image_sources":  [],
                "image_metas":    [],   # Same order as image_sources, for has_model inference
            }
        grouped[fid]["image_sources"].append(src)
        grouped[fid]["image_metas"].append(meta)

    os.makedirs(base_output_dir, exist_ok=True)
    result, skipped = [], []
    for fid, prod in grouped.items():
        n = len(prod["image_sources"])
        if n < min_images:
            skipped.append(f"{prod['product_title'][:20]} ({n} images, less than {min_images})")
            continue
        # Folder name: itemId (pure numbers, no Chinese), ensuring it opens correctly across platforms
        folder_name = str(prod["item_id"])
        folder_path = os.path.join(base_output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        prod["folder"] = folder_path
        result.append(prod)
        print(f"  Folder {folder_name}  ->  {n} images")

    if skipped:
        print(f"\nSkip {len(skipped)} products (images less than {min_images}):")
        for s in skipped: print(f"    - {s}")
    print(f"\nTotal {len(result)} products entered generation queue, output dir: {base_output_dir}")
    return result


def _is_product_shot(image_desc: str, shot_type: str = None) -> bool:
    """
    Second layer filtering: Called after Step 2 visual analysis, determines if the image is a product shot.
    image_desc: Image description output by Step 2 analysis (English)
    shot_type:  Shot type tag output by Step 2 analysis (optional)

    Product shot features (returns True):
      - Product is the main subject, background is simple (white, gradient, solid color)
      - Detail close-ups (material, texture)
      - Hand-held / partial frame product showcase

    Filtered out types (returns False):
      - Lifestyle scenes: People-dominated, complex indoor/outdoor environments
      - Pure design posters: Large areas of text, event banners
      - No product subject: Pure background, decorative images
    """
    # shot_type has highest priority: Explicit AI judgment is more reliable than keyword matching
    if shot_type:
        if shot_type in ("product_shot", "detail_shot", "packshot", "model_shot"):
            return True
        if shot_type in ("lifestyle_scene", "graphic_poster", "scene_only"):
            return False
        # shot_type unknown -> fall back to image_desc keyword check

    if not image_desc:
        return True   # Conservatively keep when no description

    desc_lower = image_desc.lower()

    # Explicit scene/poster keywords -> filter
    REJECT_SIGNALS = [
        "poster", "banner", "advertisement", "promotional text",
        "lifestyle scene", "outdoor scene", "people walking",
        "crowded", "street scene", "large text overlay",
        "infographic", "chart", "diagram",
        "no product", "background only", "abstract pattern",
    ]
    for sig in REJECT_SIGNALS:
        if sig in desc_lower:
            return False

    # Explicit product shot keywords -> keep
    KEEP_SIGNALS = [
        "product", "item", "white background", "clean background",
        "gradient background", "studio shot", "close-up", "detail shot",
        "packshot", "isolated", "centered product",
    ]
    if any(sig in desc_lower for sig in KEEP_SIGNALS):
        return True

    return True   # Conservatively keep for other cases


def _download_images(items: list, url_extractor, download_dir: str) -> list:
    """[Deprecated] Download logic has been inlined to fetch_assets_from_content_hub. Kept for reference only."""
    local_paths = []
    seen_urls = set()

    for item in items:
        for img_url in url_extractor(item):
            if not img_url or img_url in seen_urls:
                continue
            seen_urls.add(img_url)
            try:
                ext = img_url.split("?")[0].rsplit(".", 1)[-1].lower()
                if ext not in ("jpg", "jpeg", "png", "webp"):
                    ext = "jpg"
                uid = img_url.rsplit("/", 1)[-1].split(".")[0]
                fpath = os.path.join(download_dir, f"{uid}.{ext}")
                if os.path.exists(fpath):
                    print(f"Already exists skipping: {uid}.{ext}")
                    local_paths.append(fpath)
                    continue
                r = requests.get(img_url, timeout=30)
                r.raise_for_status()
                with open(fpath, "wb") as f:
                    f.write(r.content)
                local_paths.append(fpath)
                print(f"Downloaded: {uid}.{ext}")
            except Exception as e:
                print(f"Warning: Download failed {img_url}: {e}")

    print(f"Total downloaded {len(local_paths)} images -> {download_dir}")
    return local_paths
```

---

## Prompt Dictionaries

### SEEDANCE_PROMPTS — Category Default Base Prompt

```python
SEEDANCE_PROMPTS = {
    "Clothing/Accessories": (
        "The garment hangs in a minimal studio. Warm diffused light filters through "
        "a half-open window from camera left, casting soft directional shadows. "
        "Structured silhouette transitions to fluid drape as the fabric moves with "
        "realistic weight and momentum. Physically-based cloth simulation, no fabric morphing. "
        "Fashion editorial aesthetic, cinematic quality, 4K, no text, no watermark, "
        "no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
        "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Beauty/Skincare": (
        "A premium skincare bottle on a white velvet pedestal. Soft key light from "
        "45° above and camera left caresses the curved packaging, creating refined "
        "specular highlights without overexposure. "
        "Elegant and minimal, La Mer editorial style. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
        "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Food/Beverages": (
        "The product sits on a dark stone surface. "
        "Warm amber volumetric side light, cozy premium atmosphere. "
        "Nespresso-inspired editorial style. "
        "4K, no text, no watermark, "
        "no condensation, no water droplets, no moisture, no steam, "
        "no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
        "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Digital/3C": (
        "The product rests on a matte black surface, emerging from darkness. "
        "Precise specular highlight traces the chamfered edge. Studio three-point lighting "
        "with hard shadow definition on one side and soft fill on the other. "
        "No lens flare. Apple-inspired minimalist precision aesthetic. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Jewelry/Accessories": (
        "A luxury jewelry piece resting on a cool gray gradient surface. "
        "Single soft key light from 45° above and camera left. "
        "All light originates from material surface reflection and ambient environment only. "
        "The gemstone reveals its inner depth and quiet luminosity through the interplay "
        "of ambient light and metal reflection — not from added sparkle or artificial effects. "
        "No artificial sparkle, no sudden light bursts, no added light rays, "
        "no lens flare, no over-saturated reflections. "
        "Tiffany-inspired high-end editorial style, restrained and material-honest. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Home/Furniture": (
        "The product rests in a minimal interior setting. Warm afternoon light enters "
        "from a window at camera left, casting long gentle shadows across the surface. "
        "Wood grain, fabric weave, or metal sheen are revealed in precise detail. "
        "Muji-inspired calm and honest aesthetic. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Pet Supplies": (
        "The product sits centered on a clean white or light gray background. "
        "Soft even three-point lighting with no harsh shadows, building a sense "
        "of trust and clarity. Approachable eye-level observation feel. "
        "Royal Canin-inspired product-first style. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
    "Maternity/Baby": (
        "The product sits on a soft cream-white background. Ultra-soft wrap-around "
        "fill light from all sides eliminates harsh shadows, creating a gentle "
        "cotton-soft and pure atmosphere. Very slow pace. "
        "Warm white color temperature, safe and tender feel. "
        "Johnson & Johnson-inspired pure and caring aesthetic. "
        "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
    ),
}
```

---

### CATEGORY_VARIANT_PROMPTS — motion_hint Routed Variant Prompts

When motion_hint hits MOTION_VARIANT_MAP, use the corresponding value from this dictionary to replace the default base color of SEEDANCE_PROMPTS.

```python
CATEGORY_VARIANT_PROMPTS = {
    "Beauty/Skincare": {
        "Liquid Flowing": (
            "on a smooth obsidian reflective surface. "
            "A single bead of liquid slowly descends the exterior surface of the sealed bottle "
            "with realistic surface tension and gravity. "
            "The product remains sealed and in the exact same state as shown in the source image — "
            "no cap opening, no lid removal, no revealing interior. "
            "Shallow depth of field, soft backlight with subtle chromatic aberration rim. "
            "Slow motion, luxury feel. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
            "no ghosting, temporal coherence, stabilized."
        ),
        "Product Rotation": (
            "on a white velvet pedestal. "
            "Soft key light from 45° above and camera left caresses the curved packaging, "
            "creating refined specular highlights without overexposure. "
            "Smooth 90° clockwise arc from front to side, shallow depth of field. "
            "Medium close-up texture reveal, keeping the full product in frame, showing surface luminosity and material quality. "
            "Elegant and minimal, La Mer editorial style. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Food/Beverages": {
        "Steam Rising": (
            "on a dark stone surface. "
            "Gentle steam rising with realistic fluid simulation. "
            "Static medium shot with full product visible in frame, warm amber volumetric side light, cozy premium atmosphere. "
            "Nespresso-inspired editorial style. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
        "Water Droplets": (
            "on a dark wet reflective surface. "
            "Condensation droplets slowly form and run down the surface with realistic "
            "surface tension and gravity. Cool dramatic rim lighting, slow dolly-in stopping at medium close-up with full product visible in frame, "
            "refreshing advertisement style. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Jewelry/Accessories": {
        "Light Sparkling": (
            "resting on a cool gray gradient surface. "
            "Single soft key light from 45° above and camera left. "
            "All light originates from material surface reflection and ambient environment only. "
            "The gemstone reveals its inner depth and quiet luminosity through the interplay "
            "of ambient light and metal reflection — not from added sparkle or artificial effects. "
            "No artificial sparkle, no sudden light bursts, no added light rays, "
            "no lens flare, no over-saturated reflections. "
            "Tiffany-inspired high-end editorial style, restrained and material-honest. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
        "Slow Motion Close-up": (
            "on a black obsidian pedestal. "
            "Soft sweeping key light reveals fine engraving and metal texture. "
            "Smooth 90° arc from front to side, rack focus from overall form to detail. "
            "Soft focused background, sharp foreground, jewelry catalog style. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Digital/3C": {
        "Light Effect Scan": (
            "on a dark surface. A soft light beam slowly sweeps across the surface, "
            "revealing fine material texture and craftsmanship. "
            "Physically accurate metal sheen, chromatic aberration rim on edges. "
            "Dramatic studio lighting, slow dolly-in stopping at medium close-up with full product form visible in frame. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
            "no ghosting, temporal coherence, stabilized."
        ),
        "Mechanical Rotation": (
            "The mechanical product is shown in its natural environment or against a clean studio background. "
            "All rotating parts — such as propellers, fans, wheels, or gears — spin continuously at realistic "
            "physical speed throughout the entire clip, with accurate motion blur and rotational momentum. "
            "The product body remains stationary and stable; only the designated rotating components move. "
            "Preserve the original background exactly as shown in the source image. "
            "Slow dolly-in from medium shot to medium close-up, full product always visible in frame. "
            "Physically accurate aerodynamics or mechanical motion, no speed ramp, no sudden stop. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
            "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Pet Supplies": {
        "Texture Close-up": (
            "Medium close-up, full product visible in frame. Slow dolly-in stopping before extreme close-up, revealing fluffy texture and stitching detail. "
            "Soft sweeping key light from the side, warm diffused fill light. "
            "Cozy and gentle atmosphere. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Maternity/Baby": {
        "Material Sense of Security": (
            "Medium close-up, full product visible in frame. Slow dolly-in stopping before extreme close-up, soft sweeping key light gently highlights "
            "the smooth and safe texture. Warm pastel tones, minimalist background, "
            "tender and caring atmosphere. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
    "Home/Furniture": {
        "Material Light Effect": (
            "Medium close-up, full product visible in frame. A soft sweeping key light slowly moves across, "
            "revealing fine grain and texture detail without pushing to extreme close-up. "
            "Warm studio lighting with physically accurate material sheen. "
            "Slow dolly-in stopping at medium close-up, lifestyle photography style. "
            "4K, no text, no watermark, no floating, no levitation, no anti-gravity, all subjects and products stay grounded, obeys real-world physics, "
            "no morphing, no shape distortion, preserve exact product form and packaging, "
        "no ghosting, temporal coherence, stabilized."
        ),
    },
}
```

---

### SEEDANCE_SHOT_VARIANTS — Camera Movement Variants (Cycled by shot_index)

```python
SEEDANCE_SHOT_VARIANTS = {
    "Clothing/Accessories": [
        "Slow dolly-in from wide shot to mid-body close-up, emphasizing fabric weave and surface texture throughout the continuous move.",
        "Camera holds at a slight high angle and slowly tilts down, scanning from neckline to hem, revealing the full garment drape.",
        "Camera drifts slowly sideways with subtle parallax, soft-focus background separating from the sharp garment surface.",
        "Camera holds low and slowly cranes upward at eye level, scanning from hem to neckline in one continuous vertical reveal, warm diffused side light tracking with the camera.",
    ],
    "Beauty/Skincare": [
        "Camera drifts slowly left with subtle parallax, foreground soft-focus bokeh separates from the sharp product surface. Rack focus pull from packaging surface into logo detail.",
        "Camera at a low angle slowly cranes upward, continuously tilting down to reveal the full bottle from base to cap.",
        "Slow direct push-in from front, arriving at a medium close-up with the full product label clearly visible in frame.",
        "Static overhead shot with a soft key-light sweep slowly crossing the bottle surface from left to right.",
    ],
    "Food/Beverages": [
        "Static medium shot with a very slow push-in toward the product label stopping at medium close-up, warm side light gradually revealing surface material and texture detail with full product visible in frame.",
        "Camera slowly cranes upward from a low front angle, revealing the full product height against the dark stone surface.",
        "Camera drifts gently sideways at eye level, foreground surface texture creating soft parallax depth.",
        "Slow push-in from a 3/4 front angle, arriving at a medium close-up with the full product label remaining in frame.",
    ],
    "Digital/3C": [
        "Camera performs a slow low-angle tilt up, revealing the full form from base to top.",
        "Slow direct push-in from front, arriving at a medium close-up with the full product form visible in frame.",
        "Camera drifts slowly left from a 3/4 angle, subtle parallax separating product from dark background.",
        "Camera cranes upward from near the surface, wide reveal of the product standing against studio lighting.",
    ],
    "Jewelry/Accessories": [
        "Camera at a low angle slowly cranes upward while continuously tilting down, a soft specular trail tracing the metal edge throughout the single fluid move.",
        "Camera drifts slowly left with subtle parallax, foreground bokeh separating from the sharp gemstone surface.",
        "Slow direct push-in arriving at a medium close-up with the full jewelry piece visible in frame, revealing gemstone depth and facets.",
        "Camera holds at a low 3/4 side angle and slowly tilts upward, light raking across the metal surface.",
    ],
    "Home/Furniture": [
        "Camera performs a slow direct push-in stopping at medium close-up with the full product visible in frame, continuously revealing wood grain, fabric weave, or metal sheen throughout the single uninterrupted move.",
        "Camera starts at a low side angle and slowly cranes up, warm window light shifting across the surface.",
        "Camera drifts slowly sideways at mid-height, subtle parallax separating product from interior backdrop.",
        "Camera holds overhead and slowly tilts down, scanning the top surface texture and material finish.",
    ],
    "Pet Supplies": [
        "Camera drifts gently and continuously from left to right at eye level in a slow arc, one unbroken direction throughout the shot.",
        "Slow direct push-in from front, arriving at a medium close-up with the full product label visible in frame.",
        "Camera begins low and slowly cranes upward, revealing the full product height against the clean background.",
        "Static composed shot with a very subtle breathing zoom — imperceptibly slow zoom-in — giving a calm, steady feel.",
    ],
    "Maternity/Baby": [
        "Camera drifts gently from front-left to front-right at eye level, staying within the frontal 60-degree viewing zone, warm wrap-around light following the camera.",
        "Camera drifts slowly left at eye level, soft-focus background separating from the sharp product surface.",
        "Slow direct push-in from front, arriving at a medium close-up with the full product packaging visible in frame.",
        "Camera begins slightly high and slowly tilts down, scanning from top to base of the product.",
    ],
}
```

---

### KLING_SHOT_ANGLES — Kling Shot Camera Movement Descriptions

```python
# Each item <= 40 chars, leaving enough space for desc / base / guard
KLING_SHOT_ANGLES = [
    "Slow push-in to full product reveal",
    "Orbit 90° right to side profile",
    "Slow arc left to right, 60° frontal",
    "Slow dolly-in to medium close-up",
    "Crane back and up, reveal full scene",
    "Pull back from close-up to wide shot",
]
```

### KLING_BASE_PROMPTS — Kling Category Scene Base Colors (Layer 3)

```python
# Each item <= 70 chars
KLING_BASE_PROMPTS = {
    "Clothing/Accessories": "Studio, soft overhead light, fashion editorial. No extra people.",
    "Beauty/Skincare": "Studio, 45° key light, luxury beauty. No hands, no label shifts.",
    "Food/Beverages": "Dark stone, warm side light, food photography. No people.",
    "Digital/3C":   "Matte black, studio lighting, minimal. No screen content.",
    "Jewelry/Accessories": "Dark velvet, spotlight, shallow depth. No extra hands.",
    "Home/Furniture": "Warm interior, afternoon light, lifestyle. No people.",
    "Pet Supplies":  "White background, soft lighting, product-first. No animals.",
    "Maternity/Baby":  "Cream-white background, soft wrap light, tender. No infants.",
}

def get_kling_shot_prompt(shot_index: int, category: str, image_desc: str = "") -> str:
    """
    Three-layer stitched Kling prompt, hard limit 512 chars (Kling API limit):
      layer1: image_desc  — Semantic description, align with image content (<= 90 chars)
      layer2: angle       — Camera angle (<= 40 chars)
      layer3: base        — Category scene base color (<= 70 chars)
      guard:  Safety Guard — Prevent frame distortion/background disappearance (<= 180 chars)
    """
    angle = KLING_SHOT_ANGLES[shot_index % len(KLING_SHOT_ANGLES)]
    base  = KLING_BASE_PROMPTS.get(category, "Clean studio, professional product photography.")
    desc  = f"A {image_desc}. " if image_desc else ""
    guard = (
        "No state change, no pour; "
        "animate only visible surfaces; "
        "keep original background intact; "
        "single continuous shot, no cuts; "
        "full product in frame; no morphing; real-world physics."
    )
    prompt = f"{desc}{angle}. {base} {guard}"
    # Truncation insurance: trim from guard tail if exceeds 512
    if len(prompt) > 512:
        prompt = prompt[:512].rsplit(" ", 1)[0]
    return prompt
```

---

## Image Processing Functions

### detect_ratio — Auto Detect Ratio (fallback under adaptive mode)

| Aspect Ratio r | Seedance ratio | Kling aspect_ratio |
|---------|---------------|-----------------|
| r < 0.65 | `9:16` | `9:16` |
| 0.65 <= r < 0.85 | `3:4` | `9:16` |
| 0.85 <= r < 1.15 | `1:1` | `1:1` |
| 1.15 <= r < 1.6 | `4:3` | `16:9` |
| 1.6 <= r < 2.2 | `16:9` | `16:9` |
| r >= 2.2 | `21:9` | `16:9` |

```python
from PIL import Image
import requests
from io import BytesIO

def detect_ratio(image_source: str, tool: str = "seedance") -> str:
    if image_source.startswith("http"):
        _r = requests.get(image_source, timeout=15); _r.raise_for_status()
        img = Image.open(BytesIO(_r.content))
    else:
        img = Image.open(image_source)
    w, h = img.size
    r = w / h
    if tool == "kling":
        if r < 0.85: return "9:16"
        if r < 1.15: return "1:1"
        return "16:9"
    if r < 0.65: return "9:16"
    if r < 0.85: return "3:4"
    if r < 1.15: return "1:1"
    if r < 1.6:  return "4:3"
    if r < 2.2:  return "16:9"
    return "21:9"
```

### crop_to_ratio + prepare_image — Crop + Upload

```python
from PIL import Image
import requests, base64, os
from io import BytesIO
from http_nano_banana import file_upload_to_obs_sync

def crop_to_ratio(img: Image.Image, ratio_str: str, focus_point: tuple = (0.5, 0.5)) -> Image.Image:
    """
    Crop to specified ratio centered around focus_point, e.g., '9:16', '1:1'.
    focus_point: (cx, cy) normalized coordinates (0-1), representing the visual center of the main product; default (0.5, 0.5) is geometric center.
    """
    rw, rh = map(int, ratio_str.split(":"))
    target = rw / rh
    w, h = img.size
    current = w / h
    cx, cy = focus_point

    if current > target:          # Image wider than target -> crop left/right
        new_w = int(h * target)
        left = int(cx * w - new_w / 2)
        left = max(0, min(left, w - new_w))   # Prevent out of bounds
        return img.crop((left, 0, left + new_w, h))
    elif current < target:        # Image taller than target -> crop top/bottom
        new_h = int(w / target)
        top = int(cy * h - new_h / 2)
        top = max(0, min(top, h - new_h))     # Prevent out of bounds
        return img.crop((0, top, w, top + new_h))
    return img

def prepare_image(image_source: str, target_ratio: str = None, tool: str = "seedance",
                  focus_point: tuple = (0.5, 0.5)):
    """
    Read local path or URL image, crop if needed and upload, return (url, ratio).
    - target_ratio is not None: crop to target ratio centered around focus_point and upload to OBS
    - target_ratio is None (adaptive): upload original image, ratio returned by detect_ratio actual ratio
      Seedance supports adaptive ratio string; Kling unifies to None in Step 6
    - focus_point: (cx, cy) normalized coordinates provided by Step 2 visual analysis; default (0.5, 0.5) geometric center as fallback
    """
    MAX_SIDE = 2048  # Seedance / Kling API max pixel limit per side

    if image_source.startswith("http"):
        _r = requests.get(image_source, timeout=15); _r.raise_for_status()
        img = Image.open(BytesIO(_r.content))
        original_url = image_source
    else:
        img = Image.open(image_source)
        original_url = None

    # Scale down super large images proportionally, avoid API rejection or generation quality drop
    if max(img.size) > MAX_SIDE:
        orig_w, orig_h = img.size
        scale = MAX_SIDE / max(orig_w, orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        original_url = None   # Force re-upload scaled version
        print(f"  Warning: Image dimensions {orig_w}x{orig_h} exceeded limit, scaled down proportionally to {new_w}x{new_h}")

    # Need to unify to RGB when uploading (crop/scale/transparent PNG handled here)
    def _to_jpeg_b64(image: Image.Image) -> str:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        buf = BytesIO()
        image.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()

    if target_ratio:
        img = crop_to_ratio(img, target_ratio, focus_point=focus_point)
        b64 = _to_jpeg_b64(img)
        url = file_upload_to_obs_sync(file_bytes_or_base64=b64, file_extension="jpg")
        ratio = target_ratio
        print(f"Cropped and uploaded (focus {focus_point[0]:.2f},{focus_point[1]:.2f}): {ratio} -> {url}")
    else:
        # adaptive path: Calculate ratio directly from loaded img.size, avoid re-downloading URL
        w, h = img.size
        r = w / h
        if tool == "kling":
            ratio = "9:16" if r < 0.85 else ("1:1" if r < 1.15 else "16:9")
        else:
            if r < 0.65:   ratio = "9:16"
            elif r < 0.85: ratio = "3:4"
            elif r < 1.15: ratio = "1:1"
            elif r < 1.6:  ratio = "4:3"
            elif r < 2.2:  ratio = "16:9"
            else:           ratio = "21:9"

        if original_url and img.mode not in ("RGBA", "P"):
            # URL source + no transparency + no scaling -> reuse original URL directly, save upload
            url = original_url
        else:
            # Local file, scaled URL, or contains alpha channel -> unify convert to JPEG and upload
            b64 = _to_jpeg_b64(img)
            url = file_upload_to_obs_sync(file_bytes_or_base64=b64, file_extension="jpg")
        print(f"Ratio: adaptive -> actual detection is {ratio}")
    return url, ratio
```

---

## Category Configuration + Interactive Confirmation

```python
CATEGORIES = [
    "Clothing/Accessories", "Beauty/Skincare", "Food/Beverages", "Digital/3C",
    "Jewelry/Accessories", "Home/Furniture", "Pet Supplies", "Maternity/Baby",
]

CATEGORY_BGM_TAGS = {
    "Clothing/Accessories":  ["Fashion", "Upbeat", "Pop"],
    "Beauty/Skincare":  ["Luxury", "Elegant", "Upbeat Bright", "Bossa Nova", "Jazz Cafe", "Classical String Quartet"],
    "Food/Beverages":  ["Cheerful", "Upbeat", "Acoustic", "Folk", "Background Music", "Positive", "Pop"],
    "Digital/3C":    ["Technology", "Electronic", "Corporate"],
    "Jewelry/Accessories": ["Luxury", "Elegant", "Classical Piano", "Dreamy", "Solo Piano", "Classical String Quartet", "Sacred Choral", "Bossa Nova", "Jazz Cafe"],
    "Home/Furniture": ["Ambient", "Relax", "Background Music"],
    "Pet Supplies":  ["Cheerful", "Upbeat", "Acoustic", "Folk", "Happy", "Positive", "Cute", "Fun"],
    "Maternity/Baby":  ["Classical Piano", "Relax", "Solo Piano", "Happy Childrens Tunes", "Hap Kids Music", "Calm"],
}

def ask_setup(auto_guess: str = "") -> tuple[str, str | None]:
    """
    Show category + ratio options at once, two inputs to confirm.
    Only used for CLI / local script environments.
    In Cursor, completed through AI dialogue, this function is not called.
    """
    print(f"\n[1/2] Please confirm the product category:")
    for i, c in enumerate(CATEGORIES):
        hint = " (AI Inference)" if c == auto_guess else ""
        print(f"  {i+1}. {c}{hint}")
    default_hint = f'Enter for default "{auto_guess}"' if auto_guess else "Must enter number"
    cat_choice = input(f"Enter number ({default_hint}): ").strip()
    if cat_choice:
        if not cat_choice.isdigit() or not (1 <= int(cat_choice) <= len(CATEGORIES)):
            raise ValueError(f"Invalid number: {cat_choice}, please enter 1-{len(CATEGORIES)}")
        category = CATEGORIES[int(cat_choice) - 1]
    elif auto_guess in CATEGORIES:
        category = auto_guess
    else:
        raise ValueError("Category not inferred, please manually enter the number")

    print(f"\n[2/2] Please select output ratio:")
    print("  A. adaptive (follow original, no cropping) [Default]")
    print("  B. 9:16 (Vertical)  C. 1:1 (Square)  D. 16:9 (Horizontal)  E. 3:4 (Wide Vertical, Seedance only)")
    ratio_choice = input("Enter option (A-E, Enter for default A): ").strip().upper()
    ratio = {"B": "9:16", "C": "1:1", "D": "16:9", "E": "3:4"}.get(ratio_choice)
    return category, ratio
```

---

## Background Music Functions

```python
import json, random, requests, os

def pick_music(category_tags: list, folder: str = ".", catalog_path: str = None) -> str:
    """
    Randomly pick a track from Pixabay catalog based on English category tags, and use downloadUrl direct link to download.
    catalog_path should explicitly be passed by the caller (os.path.join(SKILL_DIR, "assets", "pixabay_bgm_catalog.json")).
    Only when catalog_path=None and running in project root, will it try to auto-locate (os.getcwd() fallback).
    """
    if catalog_path is None:
        import os as _os
        catalog_path = _os.path.join(_os.getcwd(), ".cursor", "skills", "product-animation-fancyai", "assets", "pixabay_bgm_catalog.json")
    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)

    # Fuzzy match: any word in category_tags appears in any word of item tags (case-insensitive)
    matched = [
        item for item in catalog["items"]
        if any(
            any(query.lower() in tag.lower() for tag in item["tags"])
            for query in category_tags
        )
    ]
    if not matched:
        matched = catalog["items"]   # Pick randomly from full library if no match

    chosen = random.choice(matched)
    print(f"Selected music: {chosen['title']} -> {chosen['url']}")

    audio_url = chosen.get("downloadUrl")
    if not audio_url:
        raise ValueError(f"Missing downloadUrl in catalog, please update catalog: {chosen['title']}")

    audio_path = os.path.join(folder, "bgm.mp3")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    resp = requests.get(audio_url, headers=headers, timeout=30)
    resp.raise_for_status()
    with open(audio_path, "wb") as f:
        f.write(resp.content)
    print(f"Downloaded audio: {audio_url}")
    return audio_path
```

---

## BPM Beat Analysis Functions

```python
import librosa
import numpy as np

def calc_clip_durations(audio_path: str, n_clips: int,
                        min_duration: int = 4, max_duration: int = 5,
                        target_duration: float = None) -> tuple[list[int], float]:
    """
    Allocate duration for each clip based on actual beat timestamps, transition points strictly hit the beat.
    Returns (clip_durations, audio_offset):
      - clip_durations: List of integer seconds of length n_clips
      - audio_offset:   BGM mixed starting from this second (skip intro, align with first beat)

    Parameters:
      - min_duration / max_duration: Duration clamping range
      - target_duration: Target duration (seconds). If specified, algorithm auto-selects closest integer beats for
        beats_per_clip per segment, ensuring in/out points land strictly on beat timestamps, while duration stays close
        to target_duration. Applicable for Kling (target_duration=3).
        When not specified, degrades to previous equal division logic (Applicable for Seedance, min=4, max=5).

    Recommended Tool Parameters:
      - Seedance: min=4, max=5 (API min 4s, trim to first 3s when stitching)
      - Kling:    min=2, max=4, target_duration=3 (Auto-find closest 3s beat point by tempo)
    Dependencies: pip install librosa
    """
    if n_clips == 0:
        return [], 0.0

    y, sr = librosa.load(audio_path, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # Protection: When beat_times is empty (very short or silent audio), directly degrade to equal division
    if len(beat_times) == 0:
        d = max(min_duration, min(max_duration, round(target_duration or max_duration)))
        print(f"  Warning: No beats detected, equally allocating {d}s/clip")
        return [d] * n_clips, 0.0

    audio_offset = float(beat_times[0])   # Skip intro silence, start from first beat

    # Calculate number of beats allocated per clip
    if target_duration is not None and len(beat_times) > 1:
        # Use average beat interval to deduce closest integer beat count to target_duration
        beat_interval = float(np.mean(np.diff(beat_times)))
        beats_per_clip = max(1, round(target_duration / beat_interval))
    else:
        beats_per_clip = max(1, len(beat_times) // n_clips)

    if len(beat_times) < n_clips + 1:
        # Degrade to equal division if beats are too few
        bar = (60.0 / float(tempo)) * 4
        bars = max(1, round((target_duration or max_duration) / bar))
        d = max(min_duration, min(max_duration, round(bar * bars)))
        print(f"  Warning: Insufficient beats, equally allocating {d}s/clip")
        return [d] * n_clips, 0.0

    durations = []
    _max_idx = len(beat_times) - 1
    for i in range(n_clips):
        start_idx = min(i * beats_per_clip, _max_idx - 1)  # Ensure at least 1 smaller than end_idx
        end_idx   = min((i + 1) * beats_per_clip, _max_idx)
        if start_idx >= end_idx:
            # Exceeds beat range, reuse last duration or fallback to max_duration
            d = durations[-1] if durations else max_duration
        else:
            d = round(float(beat_times[end_idx]) - float(beat_times[start_idx]))
        d = max(min_duration, min(max_duration, d))
        durations.append(d)

    bpm = float(tempo)
    _target_info = f", Target Duration: {target_duration}s" if target_duration else ""
    print(f"BPM: {bpm:.1f}, BGM Align Offset: {audio_offset:.2f}s{_target_info}, Clip Durations: {durations}")
    return durations, audio_offset
```

---

## Prompt Routing + Assembly

```python
MOTION_VARIANT_MAP = {
    "Beauty/Skincare": {"liquid": "Liquid Flowing", "solid": "Product Rotation"},
    "Food/Beverages": {"hot": "Steam Rising", "cold": "Water Droplets"},
    "Jewelry/Accessories": {"shiny_gem": "Light Sparkling", "metal": "Slow Motion Close-up"},
    "Digital/3C":   {"metal": "Light Effect Scan", "mechanical": "Mechanical Rotation"},
    "Pet Supplies":  {"plush": "Texture Close-up"},
    "Maternity/Baby":  {"soft": "Material Sense of Security"},
    "Home/Furniture": {"material": "Material Light Effect"},
}

def get_seedance_prompt(category: str, shot_index: int = 0,
                        image_desc: str = "", motion_hint: str = "") -> str:
    """
    Three-layer complete Seedance prompt stitching:
      layer1: image_desc  — Semantic description, align prompt with image
      layer2: shot_desc   — Camera variant (cycles by shot_index)
      layer3: base        — Category/Variant base color (motion_hint routing)
    """
    variant_key = MOTION_VARIANT_MAP.get(category, {}).get(motion_hint)
    if variant_key:
        base = CATEGORY_VARIANT_PROMPTS.get(category, {}).get(variant_key, "")
    else:
        base = ""
    if not base:
        base = SEEDANCE_PROMPTS.get(
            category,
            "Product slowly rotates on a clean background. 4K, no text, no watermark."
        )
    variants = SEEDANCE_SHOT_VARIANTS.get(category, [])
    if variants:
        shot_desc = variants[shot_index % len(variants)]
        base = shot_desc + " " + base
    _state_guard = (
        "No cap opening, no lid opening, no unboxing, no pouring, no product state change. "
        "Do not invent or hallucinate any product detail, texture, color, label, or surface "
        "that is not clearly visible in the source image. "
        "Animate only the visible state and surfaces shown in the source image; "
        "do not show any part of the product that is outside the frame of the source image. "
        "Preserve the original background exactly as shown in the source image — "
        "do not replace, simplify, remove, or alter any background elements; "
        "no sudden background color change, no background disappearing to solid color. "
        "Single continuous shot with no internal cuts, no scene transitions, no sudden camera jumps; "
        "the entire clip is one uninterrupted camera movement from start to finish. "
        "Do not push closer than a medium close-up; the complete product must remain fully visible "
        "within the frame at all times — never crop or cut off any part of the product."
    )
    result = f"A {image_desc}. {base}" if image_desc else base
    return f"{result} {_state_guard}"
```

---

## pHash Perceptual Deduplication Function

```python
def _dedup_by_phash(analyses: list, threshold: int = 8) -> list:
    """
    Apply pHash perceptual deduplication on image_analyses list, keep only first copy of similar images within product.
    threshold=8 corresponds to "basically identical"; increase to filter more loosely; decrease for stricter.
    Dependencies: pip install imagehash Pillow (Pillow already available)
    """
    try:
        import imagehash as _ih
    except ImportError:
        print("  Warning: imagehash not installed, skipping perceptual deduplication. Please run: pip install imagehash")
        return analyses

    from PIL import Image as _PILImg
    from io import BytesIO as _BIO

    kept, seen_hashes = [], []
    for a in analyses:
        src = a.get("source", "")
        try:
            if src.startswith("http"):
                _r = requests.get(src, timeout=15); _r.raise_for_status()
                img = _PILImg.open(_BIO(_r.content))
            else:
                img = _PILImg.open(src)
            h = _ih.phash(img)
            if any(h - s <= threshold for s in seen_hashes):
                print(f"  Config: pHash dedup: Skipping visually similar image {src.split('/')[-1][:40]}")
                continue
            seen_hashes.append(h)
            kept.append(a)
        except Exception as e:
            print(f"  Warning: pHash calculation failed, keeping original image: {e}")
            kept.append(a)
    removed = len(analyses) - len(kept)
    if removed:
        print(f"  Config: pHash dedup: Removed {removed} similar images, kept {len(kept)} images")
    return kept
```

---

## API Retry Wrapper

```python
import time

def call_with_retry(fn, max_retries: int = 3, delay: float = 10, **kwargs):
    """Call fn(**kwargs), retry up to max_retries times on failure, interval delay seconds."""
    for attempt in range(1, max_retries + 1):
        try:
            return fn(**kwargs)
        except Exception as e:
            if attempt == max_retries:
                raise
            print(f"Attempt {attempt} failed: {e}, retrying in {delay}s...")
            time.sleep(delay)
```

---

## Video Stitching Functions

```python
import subprocess, requests, os, re
import imageio_ffmpeg

def get_clips_duration(clip_paths: list, ffmpeg_exe: str = None) -> float:
    if ffmpeg_exe is None:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    total = 0.0
    for path in clip_paths:
        result = subprocess.run([ffmpeg_exe, "-i", path], capture_output=True, text=True)
        # ffmpeg writes file info to stderr; try stdout as well for compatibility with different versions
        output = result.stderr or result.stdout
        match = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", output)
        if match:
            h, m, s = int(match.group(1)), int(match.group(2)), float(match.group(3))
            total += h * 3600 + m * 60 + s
        else:
            raise RuntimeError(
                f"Cannot parse video duration from ffmpeg output ({path}), "
                f"please ensure file is complete and ffmpeg version is normal.\nffmpeg output: {output[:300]}"
            )
    return total

def merge_videos(urls: list, audio_path: str = None, output_path: str = "final.mp4",
                 bgm_fadeout: bool = True, video_fadeout: bool = True,
                 fade_duration: int = 1, audio_offset: float = 0.0,
                 trim_per_clip: float = None):
    """
    trim_per_clip: If specified (e.g. 3.0), trim first N seconds of each video segment after downloading before stitching.
    Suitable for scenarios where Seedance minimum is 4s but final clip needs to be 3s per shot.
    """
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    out_dir = os.path.dirname(os.path.abspath(output_path))
    clips = []
    raw_paths = []   # Track raw files separately to ensure cleanup on exceptions
    list_file = os.path.join(out_dir, "clips.txt")
    try:
        for i, url in enumerate(urls):
            raw_path = os.path.join(out_dir, f"clip_{i}_raw.mp4")
            path     = os.path.join(out_dir, f"clip_{i}.mp4")
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            with open(raw_path, "wb") as f:
                f.write(resp.content)
            raw_paths.append(raw_path)   # Record for finally cleanup
            if trim_per_clip:
                subprocess.run(
                    [ffmpeg_exe, "-y", "-i", raw_path,
                     "-t", str(trim_per_clip), "-c", "copy", path],
                    check=True
                )
                os.remove(raw_path)
                raw_paths.remove(raw_path)   # Removed manually, drop from track list
            else:
                os.rename(raw_path, path)
                raw_paths.remove(raw_path)   # Original path doesn't exist after rename
            clips.append(path)
        with open(list_file, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        # Calculate total duration in advance if fadeout needed (avoid redundant calls)
        fade_start = None
        if (bgm_fadeout or video_fadeout) and (audio_path or video_fadeout):
            total = get_clips_duration(clips, ffmpeg_exe=ffmpeg_exe)
            fade_start = max(0, total - fade_duration)

        if audio_path:
            cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", list_file]
            # Skip BGM intro if audio_offset > 0, align first beat with first cut point
            if audio_offset > 0:
                cmd += ["-ss", f"{audio_offset:.3f}"]
            cmd += ["-i", audio_path, "-map", "0:v", "-map", "1:a"]

            if video_fadeout and fade_start is not None:
                # Video fadeout requires re-encoding, cannot use copy
                cmd += [
                    "-vf", f"fade=t=out:st={fade_start:.2f}:d={fade_duration}",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                ]
            else:
                cmd += ["-c:v", "copy"]

            cmd += ["-c:a", "aac"]
            if bgm_fadeout and fade_start is not None:
                cmd += ["-af", f"afade=t=out:st={fade_start:.2f}:d={fade_duration}"]
            cmd += ["-shortest", output_path]
            subprocess.run(cmd, check=True)
        else:
            if video_fadeout and fade_start is not None:
                subprocess.run([
                    ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", list_file,
                    "-vf", f"fade=t=out:st={fade_start:.2f}:d={fade_duration}",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    output_path,
                ], check=True)
            else:
                subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0",
                                "-i", list_file, "-c", "copy", output_path], check=True)
    finally:
        # Only clean temporary intermediate files; bgm.mp3 kept for debugging/retry
        for c in clips + raw_paths:   # raw_paths fallback: clean residual raw files if trim fails
            if os.path.exists(c):
                os.remove(c)
        if os.path.exists(list_file):
            os.remove(list_file)
    return output_path

def make_output_path(project_name: str = "product", folder: str = ".") -> str:
    """Return video path at the same level as input images, e.g., /path/to/folder/projectname_final.mp4"""
    return os.path.join(folder, f"{project_name}_final.mp4")
```

---

## Script Templates

> AI reads this section on demand when generating scripts. Contains: config header, single product full flow, merchant batch (create folders by product), local multi-folder batch.

### Script Config Header (Must be placed at the top of all scripts)

```python
import os, sys, re, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Note: Hardcoded for test environment below, change to actual skill installation directory for production
SKILL_DIR = os.environ.get("SKILL_DIR", "/Users/fancy/Desktop/cursor/product-animation-fancyai")
FOLDER    = os.path.join(os.path.expanduser("~"), "Downloads", "product_animation_output")

sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
catalog_path = os.path.join(SKILL_DIR, "assets", "pixabay_bgm_catalog.json")
os.makedirs(FOLDER, exist_ok=True)

from http_seedance20_video_gen import seedance20_video_gen_sync
from http_kling_multi_shot import kling_multi_shot_sync
```

### Single Product Full Flow (Steps 1-7)

```python
# ── Step 1: Get Images ──────────────────────────────────────────────────────────
image_sources = [
    os.path.join(FOLDER, f)
    for f in sorted(os.listdir(FOLDER))
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
]

# ── Step 2: Visual Analysis (AI analyzes images and fills in actual values) ────────────────────────────────
# image_desc format: [Brand] [color] [product name], [material/form], [background], <=20 words, English
# motion_hint: liquid/solid/fabric/shiny_gem/metal/hot/cold/plush/soft/material/mechanical/default
# shot_type: product_shot/detail_shot/model_shot/lifestyle_scene/graphic_poster/scene_only (For tagging only, no filtering)
# has_model: Contains real person -> True (Auto-switch to Kling)
# focus_point: Main subject visual center normalized coordinates (cx, cy), works only when cropping
# is_dual: Contains two independent products/angles stitched together (dual-panel) -> Filter if True, do not send to video model
# is_visual_duplicate: Visually highly similar to another image in the same group -> Filter if True, keep the one with richest visual info
image_analyses = [
    # {"source": path, "has_model": False, "image_desc": "...", "shot_type": "product_shot",
    #  "motion_hint": "default", "category_guess": "Beauty/Skincare", "focus_point": (0.5, 0.5),
    #  "is_dual": False, "is_visual_duplicate": False},
]

# Neither source calls _is_product_shot: Admin backend filtered by server, local folder manually selected by user

# Dual-panel + Visual duplicate filtering: Exclude at once after AI visual judgment
image_analyses = [a for a in image_analyses if not a.get("is_dual") and not a.get("is_visual_duplicate")]

# ── Circuit Breaker: No qualified image assets ──────────────────────────────────────────────────────
if not image_analyses:
    raise SystemExit(
        "Error: No qualified image assets, unable to generate video.\n"
        "   Local Source: Please ensure there are jpg/png/webp images in the folder.\n"
        "   Admin Backend Source: Please ensure the selected product has available assets of Model Shot, Scene Shot, or Detail Shot."
    )

has_model = any(a["has_model"] for a in image_analyses)
tool = "kling" if has_model else "seedance"

# ── Step 3: Category + Ratio (Filled after AI dialogue confirmation) ─────────────────────────────────
category     = "Clothing/Accessories"   # 1 of 8: Clothing/Accessories Beauty/Skincare Food/Beverages Digital/3C Jewelry/Accessories Home/Furniture Pet Supplies Maternity/Baby
target_ratio = "9:16"       # None=adaptive (recommended for horizontal products: Home/Furniture/Digital/3C) / "9:16" / "1:1" / "16:9" / "3:4"
category_tags = CATEGORY_BGM_TAGS.get(category, [])

# ── Step 4: BGM + Beats ───────────────────────────────────────────────────────
audio_path = pick_music(category_tags, folder=FOLDER, catalog_path=catalog_path)
_dur_args = ({"min_duration": 2, "max_duration": 4, "target_duration": 3}
             if tool == "kling" else {"min_duration": 4, "max_duration": 5})
clip_durations, audio_offset = calc_clip_durations(audio_path, n_clips=len(image_analyses), **_dur_args)

# ── Step 5: Assemble prompt + Crop & Upload ───────────────────────────────────────────
from PIL import Image as _PILImage
image_list = []
for i, a in enumerate(image_analyses):
    effective_ratio = target_ratio
    if tool == "kling" and target_ratio not in (None, "9:16", "1:1", "16:9"):
        effective_ratio = "9:16"
    url, ratio = prepare_image(a["source"], target_ratio=effective_ratio, tool=tool,
                               focus_point=a.get("focus_point", (0.5, 0.5)))
    prompt = (get_seedance_prompt(category=category, shot_index=i,
                                  image_desc=a["image_desc"], motion_hint=a["motion_hint"])
              if tool == "seedance"
              else get_kling_shot_prompt(i, category, image_desc=a["image_desc"]))
    image_list.append({"url": url, "prompt": prompt, "ratio": ratio, "duration": clip_durations[i]})

_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open(os.path.join(FOLDER, f"prompts_{_ts}.txt"), "w", encoding="utf-8") as _f:
    _f.write(f"Tool:{tool} Category:{category} Ratio:{target_ratio or 'adaptive'}\n{'='*80}\n")
    for _i, _item in enumerate(image_list):
        _f.write(f"[{_i+1}] {os.path.basename(image_analyses[_i]['source'])}\n"
                 f"  {_item['duration']}s | {_item['ratio']}\n  {_item['prompt']}\n\n")

# ── Step 6: Concurrent Generation ─────────────────────────────────────────────────────────
# Concurrency limit: Seedance max 3 streams, Kling max 5 streams, exceeding triggers API rate limit
VIDEO_CONCURRENCY = 3 if tool == "seedance" else 5

all_clip_urls, _failed = [], []

def _gen_one(item, idx):
    if tool == "seedance":
        return call_with_retry(seedance20_video_gen_sync,
                               prompt=item["prompt"], first_img_url=item["url"],
                               duration=item["duration"], ratio=item["ratio"],
                               resolution="720p", generate_audio=False)
    else:
        return call_with_retry(kling_multi_shot_sync,
                               prompt="Product showcase video, showing product details and dynamics.",
                               shot_type="customize",
                               multi_prompt=[{"index": 1, "prompt": item["prompt"],
                                              "duration": item["duration"]}],
                               image_urls=[item["url"]],
                               aspect_ratio=(item["ratio"] if item["ratio"] != "adaptive" else None),
                               resolution="1080P", enhance_prompt="Disabled")

results = [None] * len(image_list)
with ThreadPoolExecutor(max_workers=VIDEO_CONCURRENCY) as ex:
    futs = {ex.submit(_gen_one, item, i): i for i, item in enumerate(image_list)}
    for fut in as_completed(futs):
        idx = futs[fut]
        try:
            results[idx] = fut.result()
        except Exception as e:
            print(f"  Warning: [{idx+1}] Failed: {e}")
            _failed.append((idx+1, str(e)))
for urls in results:
    if urls: all_clip_urls.extend(urls)
if not all_clip_urls: raise RuntimeError("All clips failed to generate")

# ── Step 7: Stitching ─────────────────────────────────────────────────────────────
project_name = re.sub(r"[^a-zA-Z0-9_]", "_", image_analyses[0]["image_desc"])[:30]
output_path  = make_output_path(project_name=project_name, folder=FOLDER)
final_video  = merge_videos(all_clip_urls, audio_path=audio_path, output_path=output_path,
                            audio_offset=audio_offset,
                            trim_per_clip=3 if tool == "seedance" else None)
print(f"Done: {final_video}")
```

### Merchant Batch (Store Name/ID -> Create folders by product)

```python
import re
tokens = content_hub_login()

# Step 0: Fetch Images + Grouping
image_sources = fetch_assets_from_content_hub(
    tokens=tokens,
    merchant_name="Neiwai",        # Or merchant_id=1001039
    category="Clothing",             # Optional
    max_images_per_product=5,    # Optional, limit images per product
)
metas = fetch_assets_from_content_hub._last_metas

# ── Circuit Breaker 1: Image fetching result is empty ──────────────────────────────────────────────────────
if not image_sources:
    raise SystemExit(
        "Error: No qualified image assets found.\n"
        "   Possible reasons: Incorrect merchant name / No images matching filter rules for this merchant (Must include Model Shot, Scene Shot or Detail Shot).\n"
        "   Please check merchant name, or go to admin backend to confirm if products have tagged original images."
    )

BASE_OUTPUT = os.path.join(os.path.expanduser("~"), "Downloads", "product_animation_output")
products = group_images_by_product(image_sources, metas, BASE_OUTPUT)

# ── Circuit Breaker 2: All products have less than 3 images after filtering ──────────────────────────────────────
if not products:
    raise SystemExit(
        "Error: All products have less than 3 qualified images after filtering, unable to generate video.\n"
        "   Suggestion: Lower min_images threshold, or go to admin backend to add original image tags for products."
    )

# Ask user generation quantity this time
_total = len(products)
_inp = input(f"\nFound {_total} products, how many to generate this time? (Enter directly = All): ").strip()
if _inp.isdigit() and 0 < int(_inp) < _total:
    products = products[:int(_inp)]
    print(f"Selected first {len(products)} products to generate.")
else:
    print(f"Generating all {_total} products.")

# Ask output ratio (unified for batch)
print("\nPlease select output ratio (unified cropping for all products in batch):")
print("  1. 9:16 (Vertical)  2. 1:1 (Square)  3. 16:9 (Horizontal)  4. 4:3 (Wide Vertical)  5. Auto follow original [Default]")
_ratio_map = {"1": "9:16", "2": "1:1", "3": "16:9", "4": "4:3", "5": None}
_ratio_inp = input("Enter number (Enter defaults to Auto): ").strip()
BATCH_RATIO = _ratio_map.get(_ratio_inp)   # None = Auto (By product's main image mode ratio)
print(f"Output Ratio: {'Auto (By product main image mode)' if BATCH_RATIO is None else BATCH_RATIO}")

# _gen_one: Single clip generation (tool updates per for-loop before taking effect)
def _gen_one(item, idx):
    if tool == "seedance":
        return call_with_retry(seedance20_video_gen_sync,
                               prompt=item["prompt"], first_img_url=item["url"],
                               duration=item["duration"], ratio=item["ratio"],
                               resolution="720p", generate_audio=False)
    else:
        return call_with_retry(kling_multi_shot_sync,
                               prompt="Product showcase video, showing product details and dynamics.",
                               shot_type="customize",
                               multi_prompt=[{"index": 1, "prompt": item["prompt"],
                                              "duration": item["duration"]}],
                               image_urls=[item["url"]],
                               aspect_ratio=(item["ratio"] if item["ratio"] != "adaptive" else None),
                               resolution="1080P", enhance_prompt="Disabled")

# pHash Perceptual Deduplication (Inlined to avoid missing dependency during script generation)
def _dedup_by_phash(analyses: list, threshold: int = 8) -> list:
    """Apply pHash dedup to image_analyses, keep only first copy of similar images."""
    try:
        import imagehash as _ih
    except ImportError:
        print("  Warning: imagehash not installed, skipping perceptual deduplication. Please run: pip install imagehash")
        return analyses
    from PIL import Image as _PILImg
    from io import BytesIO as _BIO
    kept, seen_hashes = [], []
    for a in analyses:
        src = a.get("source", "")
        try:
            if src.startswith("http"):
                _r = requests.get(src, timeout=15); _r.raise_for_status()
                img = _PILImg.open(_BIO(_r.content))
            else:
                img = _PILImg.open(src)
            h = _ih.phash(img)
            if any(h - s <= threshold for s in seen_hashes):
                print(f"  Config: pHash dedup: Skipping similar image {src.split('/')[-1][:40]}")
                continue
            seen_hashes.append(h)
            kept.append(a)
        except Exception as e:
            print(f"  Warning: pHash calculation failed, keeping original image: {e}")
            kept.append(a)
    removed = len(analyses) - len(kept)
    if removed:
        print(f"  Config: pHash dedup: Removed {removed} images, kept {len(kept)} images")
    return kept

# Define helper functions once, reuse within loop
import json as _j
from collections import Counter as _Counter

def _has_model_from_label(lb_raw):
    lb = lb_raw or {}
    if isinstance(lb, str):
        try: lb = _j.loads(lb)
        except Exception: lb = {}
    return "Model Shot" in (lb.get("type") or [])

def _ratio_str(r, t):
    """Map imageRatio float value to video ratio string"""
    if t == "kling":
        return "9:16" if r < 0.85 else ("1:1" if r < 1.15 else "16:9")
    if r < 0.65: return "9:16"
    if r < 0.85: return "3:4"
    if r < 1.15: return "1:1"
    if r < 1.6:  return "4:3"
    if r < 2.2:  return "16:9"
    return "21:9"

# Run complete flow product by product
batch_results = []
for _prod_idx, prod in enumerate(products):
    FOLDER        = prod["folder"]
    image_sources = prod["image_sources"]
    category      = prod["category"] or "Clothing/Accessories"
    print(f"\n{'='*60}\n> {prod['product_title'][:30]}  ({_prod_idx+1}/{len(products)})")
    try:
        # Step 2: AI Visual Analysis (image_desc / motion_hint filled by AI after analyzing each image)
        # Admin Backend Source: ListAssetsImage already filtered, _is_product_shot not called anymore
        # has_model inferred from labelAttr.type (constructed from tagNameList by _fetch_product_images)

        if len(image_sources) < 3:
            batch_results.append((prod["product_title"], "Skip", f"Less than 3 images ({len(image_sources)} images)"))
            continue

        image_metas = prod.get("image_metas", [{}] * len(image_sources))
        image_analyses = [
            {"source": s, "image_desc": "", "motion_hint": "fabric",
             "shot_type": "model_shot", "category_guess": category, "focus_point": (0.5, 0.5),
             "has_model": _has_model_from_label(m.get("labelAttr")),
             "image_ratio": m.get("imageRatio") or 1.0,  # Keep original aspect ratio for unified output ratio
             "is_dual": False,
             "is_visual_duplicate": False}
            for s, m in zip(image_sources, image_metas)
        ]
        if not image_analyses:
            batch_results.append((prod["product_title"], "Warning Skip", "No usable images")); continue

        # Dual-panel + AI visual duplicate filtering
        image_analyses = [a for a in image_analyses if not a.get("is_dual") and not a.get("is_visual_duplicate")]
        # pHash perceptual deduplication (Executes automatically at runtime, doesn't rely on AI memory)
        image_analyses = _dedup_by_phash(image_analyses, threshold=8)
        # ── Circuit Breaker: Re-validate count after all filtering (pHash might reduce count below 3) ──────────
        if len(image_analyses) < 3:
            batch_results.append((prod["product_title"], "Skip",
                                  f"Only {len(image_analyses)} images left after dedup, less than 3, skipping"))
            continue

        tool = "kling" if any(a["has_model"] for a in image_analyses) else "seedance"

        # ── Unified Output Ratio ────────────────────────────────────────────────────────
        # User selected explicit ratio -> Use directly, smart crop all images to this ratio
        # User selected Auto (None) -> Take mode ratio of all images for this product, ensuring consistent clip resolution (prevent stretching)
        if BATCH_RATIO is not None:
            consistent_ratio = BATCH_RATIO
        else:
            _ratio_votes = [_ratio_str(a.get("image_ratio", 1.0), tool) for a in image_analyses]
            consistent_ratio = _Counter(_ratio_votes).most_common(1)[0][0] if _ratio_votes else "1:1"
        # Kling only supports 9:16 / 1:1 / 16:9, other ratios must map (to avoid API error)
        if tool == "kling" and consistent_ratio not in (None, "9:16", "1:1", "16:9"):
            _kling_map = {"3:4": "9:16", "4:3": "16:9", "21:9": "16:9"}
            _orig = consistent_ratio
            consistent_ratio = _kling_map.get(consistent_ratio, "9:16")
            print(f"  Info: Kling doesn't support {_orig}, auto-mapped to {consistent_ratio}")
        print(f"  Info: Output Ratio: {consistent_ratio}")

        category_tags = CATEGORY_BGM_TAGS.get(category, [])
        audio_path = pick_music(category_tags, folder=FOLDER, catalog_path=catalog_path)
        _dur_args = ({"min_duration": 2, "max_duration": 4, "target_duration": 3}
                     if tool == "kling" else {"min_duration": 4, "max_duration": 5})
        clip_durations, audio_offset = calc_clip_durations(audio_path, n_clips=len(image_analyses), **_dur_args)

        image_list = []
        for i, a in enumerate(image_analyses):
            # Crop to unified ratio then upload: If user picked ratio, crop to it; if auto mode, crop to mode ratio
            url, ratio = prepare_image(a["source"], target_ratio=consistent_ratio, tool=tool,
                                       focus_point=a.get("focus_point", (0.5, 0.5)))
            prompt = (get_seedance_prompt(category=category, shot_index=i,
                                          image_desc=a["image_desc"], motion_hint=a["motion_hint"])
                      if tool == "seedance"
                      else get_kling_shot_prompt(i, category, image_desc=a["image_desc"]))
            image_list.append({"url": url, "prompt": prompt, "ratio": ratio, "duration": clip_durations[i]})

        all_clip_urls = []
        results = [None] * len(image_list)
        _concurrency = 3 if tool == "seedance" else 5   # Seedance<=3, Kling<=5, prevent rate limit
        with ThreadPoolExecutor(max_workers=_concurrency) as ex:
            futs = {ex.submit(_gen_one, item, i): i for i, item in enumerate(image_list)}
            for fut in as_completed(futs):
                idx = futs[fut]
                try: results[idx] = fut.result()
                except Exception as e: print(f"  Warning: [{idx+1}] Failed: {e}")
        for urls in results:
            if urls: all_clip_urls.extend(urls)
        if not all_clip_urls: raise RuntimeError("All clips failed to generate")

        project_name = str(prod["item_id"])   # Use itemId to name, no Chinese
        final_video  = merge_videos(all_clip_urls, audio_path=audio_path,
                                    output_path=make_output_path(project_name, FOLDER),
                                    audio_offset=audio_offset,
                                    trim_per_clip=3 if tool == "seedance" else None)
        print(f"  Done: {final_video}")
        batch_results.append((prod["product_title"], "Success", final_video))
    except Exception as e:
        print(f"  Error: {e}")
        batch_results.append((prod["product_title"], "Failed", str(e)))

print(f"\nBatch Complete: {len(products)} products")
for t, s, _ in batch_results: print(f"  {s}  {t[:25]}")
```

### Local Multi-Folder Batch

```python
import re
from collections import Counter
ROOT_FOLDER  = os.path.join(os.path.expanduser("~"), "Downloads", "product_animation_output")
target_ratio = None   # Unified ratio; None=adaptive

# _gen_one: Single clip generation
def _gen_one(item, idx):
    if tool == "seedance":
        return call_with_retry(seedance20_video_gen_sync,
                               prompt=item["prompt"], first_img_url=item["url"],
                               duration=item["duration"], ratio=item["ratio"],
                               resolution="720p", generate_audio=False)
    else:
        return call_with_retry(kling_multi_shot_sync,
                               prompt="Product showcase video, showing product details and dynamics.",
                               shot_type="customize",
                               multi_prompt=[{"index": 1, "prompt": item["prompt"],
                                              "duration": item["duration"]}],
                               image_urls=[item["url"]],
                               aspect_ratio=(item["ratio"] if item["ratio"] != "adaptive" else None),
                               resolution="1080P", enhance_prompt="Disabled")

subfolders = sorted([os.path.join(ROOT_FOLDER, d) for d in os.listdir(ROOT_FOLDER)
                     if os.path.isdir(os.path.join(ROOT_FOLDER, d)) and not d.startswith(".")])

# Use Unicode escapes to avoid Chinese characters in file
KNOWN_CATEGORIES = {
    "\u670d\u88c5/\u670d\u9970": "Clothing/Accessories",
    "\u7f8e\u5986\u62a4\u80a4": "Beauty/Skincare",
    "\u98df\u54c1\u996e\u6599": "Food/Beverages",
    "\u6570\u78013C": "Digital/3C",
    "\u73e0\u5b9d/\u914d\u9970": "Jewelry/Accessories",
    "\u5bb6\u5c45/\u5bb6\u5177": "Home/Furniture",
    "\u5ba0\u7269\u7528\u54c1": "Pet Supplies",
    "\u6bcd\u5a74\u7528\u54c1": "Maternity/Baby",
}

def detect_category_from_folder(folder_name, category_guesses):
    for ch, en in KNOWN_CATEGORIES.items():
        if ch in folder_name or en in folder_name: return en
    votes = Counter(g for g in category_guesses if g)
    return votes.most_common(1)[0][0] if votes else "Beauty/Skincare"

# AI Pre-check: Infer category -> Present to user to confirm -> Fill into confirmed_categories
confirmed_categories = {}  # {folder_path: "Category Name"}

batch_results = []
for FOLDER in subfolders:
    folder_name = os.path.basename(FOLDER)
    try:
        image_sources = [os.path.join(FOLDER, f) for f in sorted(os.listdir(FOLDER))
                         if f.lower().endswith((".jpg",".jpeg",".png",".webp"))]
        if not image_sources:
            batch_results.append((folder_name, "Warning Skip", "No images")); continue

        # Step 2: AI Visual Analysis (Omitted, same as single product flow)
        # Local folder source: User manually filtered, use all images directly, no extra filtering
        image_analyses = []  # Filled by AI
        if not image_analyses:
            batch_results.append((folder_name, "Warning Skip", "No image analysis results")); continue

        tool = "kling" if any(a["has_model"] for a in image_analyses) else "seedance"
        category = confirmed_categories.get(FOLDER, "Beauty/Skincare")
        category_tags = CATEGORY_BGM_TAGS.get(category, [])
        audio_path = pick_music(category_tags, folder=FOLDER, catalog_path=catalog_path)
        _dur_args = ({"min_duration": 2, "max_duration": 4, "target_duration": 3}
                     if tool == "kling" else {"min_duration": 4, "max_duration": 5})
        clip_durations, audio_offset = calc_clip_durations(audio_path, n_clips=len(image_analyses), **_dur_args)

        image_list = []
        for i, a in enumerate(image_analyses):
            effective_ratio = target_ratio
            if tool == "kling" and target_ratio not in (None,"9:16","1:1","16:9"):
                effective_ratio = "9:16"
            url, ratio = prepare_image(a["source"], target_ratio=effective_ratio, tool=tool,
                                       focus_point=a.get("focus_point", (0.5, 0.5)))
            prompt = (get_seedance_prompt(category=category, shot_index=i,
                                          image_desc=a["image_desc"], motion_hint=a["motion_hint"])
                      if tool == "seedance"
                      else get_kling_shot_prompt(i, category, image_desc=a["image_desc"]))
            image_list.append({"url": url, "prompt": prompt, "ratio": ratio, "duration": clip_durations[i]})

        all_clip_urls = []
        results = [None] * len(image_list)
        _concurrency = 3 if tool == "seedance" else 5   # Seedance<=3, Kling<=5, prevent rate limit
        with ThreadPoolExecutor(max_workers=_concurrency) as ex:
            futs = {ex.submit(_gen_one, item, i): i for i, item in enumerate(image_list)}
            for fut in as_completed(futs):
                idx = futs[fut]
                try: results[idx] = fut.result()
                except Exception as e: print(f"  Warning: [{idx+1}] Failed: {e}")
        for urls in results:
            if urls: all_clip_urls.extend(urls)
        if not all_clip_urls: raise RuntimeError("All clips failed to generate")

        raw = image_analyses[0]["image_desc"] if image_analyses else folder_name
        final_video = merge_videos(all_clip_urls, audio_path=audio_path,
                                   output_path=make_output_path(re.sub(r"[^\w]","_",raw)[:30], FOLDER),
                                   audio_offset=audio_offset,
                                   trim_per_clip=3 if tool == "seedance" else None)
        print(f"  Done: {final_video}")
        batch_results.append((folder_name, "Success", final_video))
    except Exception as e:
        print(f"  Error: {e}")
        batch_results.append((folder_name, "Failed", str(e)))

print(f"\nBatch Complete: {len(subfolders)} folders")
for n, s, _ in batch_results: print(f"  {s}  {n}")
```

---

## Universal Prompt Formula Reference

```
[Camera Movement] + [Subject Action] + [Environment Atmosphere] + [Lighting Texture]
```

| Type | English |
|------|------|
| Camera | slow push in |
| Camera | slow orbit / 360 rotation |
| Camera | static shot |
| Action | gently swaying |
| Action | liquid flowing / dripping |
| Action | steam rising |
| Lighting | soft natural light |
| Lighting | studio lighting |
| Lighting | specular highlight glint |
