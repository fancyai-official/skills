import os
import sys
import re
import datetime
import json
import random
import requests
import subprocess
import time
import imageio_ffmpeg
from PIL import Image
from io import BytesIO
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
SKILL_DIR = os.environ.get("SKILL_DIR", "/Users/fancy/Desktop/product-animation-fancyai")
FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "product_animation_output")

sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
catalog_path = os.path.join(SKILL_DIR, "assets", "pixabay_bgm_catalog.json")
os.makedirs(FOLDER, exist_ok=True)

from http_seedance20_video_gen import seedance20_video_gen_sync
from http_kling_multi_shot import kling_multi_shot_sync
from http_nano_banana import file_upload_to_obs_sync

# --- Dictionaries ---
CATEGORY_BGM_TAGS = {
    "Jewelry/Accessories": ["Luxury", "Elegant", "Classical Piano", "Dreamy", "Solo Piano", "Classical String Quartet", "Sacred Choral", "Bossa Nova", "Jazz Cafe"],
}

SEEDANCE_PROMPTS = {
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
}

CATEGORY_VARIANT_PROMPTS = {
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
    },
}

SEEDANCE_SHOT_VARIANTS = {
    "Jewelry/Accessories": [
        "Camera at a low angle slowly cranes upward while continuously tilting down, a soft specular trail tracing the metal edge throughout the single fluid move.",
        "Camera drifts slowly left with subtle parallax, foreground bokeh separating from the sharp gemstone surface.",
        "Slow direct push-in arriving at a medium close-up with the full jewelry piece visible in frame, revealing gemstone depth and facets.",
        "Camera holds at a low 3/4 side angle and slowly tilts upward, light raking across the metal surface.",
    ],
}

MOTION_VARIANT_MAP = {
    "Jewelry/Accessories": {"shiny_gem": "Light Sparkling", "metal": "Slow Motion Close-up"},
}

# --- Functions ---
def pick_music(category_tags: list, folder: str = ".", catalog_path: str = None) -> str:
    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)
    matched = [
        item for item in catalog["items"]
        if any(any(query.lower() in tag.lower() for tag in item["tags"]) for query in category_tags)
    ]
    if not matched: matched = catalog["items"]
    for _ in range(2):
        chosen = random.choice(matched)
        print(f"Selected music: {chosen['title']} -> {chosen['url']}")
        audio_url = chosen.get("downloadUrl")
        audio_path = os.path.join(folder, "bgm.mp3")
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(audio_url, headers=headers, timeout=10)
            resp.raise_for_status()
            with open(audio_path, "wb") as f:
                f.write(resp.content)
            print(f"Downloaded audio: {audio_url}")
            return audio_path
        except Exception as e:
            print(f"Failed to download audio {audio_url}: {e}, trying another...")
    print("Warning: Failed to download background music, proceeding without audio.")
    return None

def calc_clip_durations(audio_path: str, n_clips: int, min_duration: int = 4, max_duration: int = 5, target_duration: float = None):
    if n_clips == 0: return [], 0.0
    d = max(min_duration, min(max_duration, round(target_duration or max_duration)))
    return [d] * n_clips, 0.0
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    if len(beat_times) == 0:
        d = max(min_duration, min(max_duration, round(target_duration or max_duration)))
        return [d] * n_clips, 0.0
    audio_offset = float(beat_times[0])
    if target_duration is not None and len(beat_times) > 1:
        beat_interval = float(np.mean(np.diff(beat_times)))
        beats_per_clip = max(1, round(target_duration / beat_interval))
    else:
        beats_per_clip = max(1, len(beat_times) // n_clips)
    
    if len(beat_times) < n_clips + 1:
        bar = (60.0 / float(tempo)) * 4
        bars = max(1, round((target_duration or max_duration) / bar))
        d = max(min_duration, min(max_duration, round(bar * bars)))
        return [d] * n_clips, 0.0
        
    durations = []
    _max_idx = len(beat_times) - 1
    for i in range(n_clips):
        start_idx = min(i * beats_per_clip, _max_idx - 1)
        end_idx   = min((i + 1) * beats_per_clip, _max_idx)
        if start_idx >= end_idx:
            d = durations[-1] if durations else max_duration
        else:
            d = round(float(beat_times[end_idx]) - float(beat_times[start_idx]))
        d = max(min_duration, min(max_duration, d))
        durations.append(d)
    bpm = float(tempo)
    print(f"BPM: {bpm:.1f}, BGM Offset: {audio_offset:.2f}s, Durations: {durations}")
    return durations, audio_offset

def crop_to_ratio(img, ratio_str, focus_point=(0.5, 0.5)):
    rw, rh = map(int, ratio_str.split(":"))
    target = rw / rh
    w, h = img.size
    current = w / h
    cx, cy = focus_point
    if current > target:
        new_w = int(h * target)
        left = int(cx * w - new_w / 2)
        left = max(0, min(left, w - new_w))
        return img.crop((left, 0, left + new_w, h))
    elif current < target:
        new_h = int(w / target)
        top = int(cy * h - new_h / 2)
        top = max(0, min(top, h - new_h))
        return img.crop((0, top, w, top + new_h))
    return img

def prepare_image(image_source, target_ratio=None, tool="seedance", focus_point=(0.5, 0.5)):
    MAX_SIDE = 2048
    if image_source.startswith("http"):
        _r = requests.get(image_source, timeout=15)
        _r.raise_for_status()
        img = Image.open(BytesIO(_r.content))
        original_url = image_source
    else:
        img = Image.open(image_source)
        original_url = None

    if max(img.size) > MAX_SIDE:
        orig_w, orig_h = img.size
        scale = MAX_SIDE / max(orig_w, orig_h)
        img = img.resize((int(orig_w * scale), int(orig_h * scale)), Image.LANCZOS)
        original_url = None

    def _to_jpeg_b64(image):
        if image.mode in ("RGBA", "P"): image = image.convert("RGB")
        buf = BytesIO()
        image.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()

    if target_ratio:
        img = crop_to_ratio(img, target_ratio, focus_point)
        url = file_upload_to_obs_sync(file_bytes_or_base64=_to_jpeg_b64(img), file_extension="jpg")
        return url, target_ratio
    else:
        w, h = img.size
        r = w / h
        if tool == "kling": ratio = "9:16" if r < 0.85 else ("1:1" if r < 1.15 else "16:9")
        else:
            if r < 0.65: ratio = "9:16"
            elif r < 0.85: ratio = "3:4"
            elif r < 1.15: ratio = "1:1"
            elif r < 1.6: ratio = "4:3"
            elif r < 2.2: ratio = "16:9"
            else: ratio = "21:9"
        
        if original_url and img.mode not in ("RGBA", "P"): url = original_url
        else: url = file_upload_to_obs_sync(file_bytes_or_base64=_to_jpeg_b64(img), file_extension="jpg")
        return url, ratio

def get_seedance_prompt(category, shot_index=0, image_desc="", motion_hint=""):
    variant_key = MOTION_VARIANT_MAP.get(category, {}).get(motion_hint)
    base = CATEGORY_VARIANT_PROMPTS.get(category, {}).get(variant_key, "") if variant_key else ""
    if not base: base = SEEDANCE_PROMPTS.get(category, "Product slowly rotates on a clean background. 4K, no text, no watermark.")
    variants = SEEDANCE_SHOT_VARIANTS.get(category, [])
    if variants: base = variants[shot_index % len(variants)] + " " + base
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

def call_with_retry(fn, max_retries=3, delay=10, **kwargs):
    for attempt in range(1, max_retries + 1):
        try: return fn(**kwargs)
        except Exception as e:
            if attempt == max_retries: raise
            print(f"Attempt {attempt} failed: {e}, retrying in {delay}s...")
            time.sleep(delay)

def get_clips_duration(clip_paths, ffmpeg_exe=None):
    if not ffmpeg_exe: ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    total = 0.0
    for path in clip_paths:
        result = subprocess.run([ffmpeg_exe, "-i", path], capture_output=True, text=True)
        output = result.stderr or result.stdout
        match = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", output)
        if match:
            h, m, s = int(match.group(1)), int(match.group(2)), float(match.group(3))
            total += h * 3600 + m * 60 + s
    return total

def merge_videos(urls, audio_path=None, output_path="final.mp4", audio_offset=0.0, trim_per_clip=None):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    out_dir = os.path.dirname(os.path.abspath(output_path))
    clips = []
    raw_paths = []
    list_file = os.path.join(out_dir, "clips.txt")
    try:
        for i, url in enumerate(urls):
            raw_path = os.path.join(out_dir, f"clip_{i}_raw.mp4")
            path = os.path.join(out_dir, f"clip_{i}.mp4")
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            with open(raw_path, "wb") as f: f.write(resp.content)
            raw_paths.append(raw_path)
            if trim_per_clip:
                subprocess.run([ffmpeg_exe, "-y", "-i", raw_path, "-t", str(trim_per_clip), "-c", "copy", path], check=True)
                os.remove(raw_path)
                raw_paths.remove(raw_path)
            else:
                os.rename(raw_path, path)
                raw_paths.remove(raw_path)
            clips.append(path)
            
        with open(list_file, "w") as f:
            for c in clips: f.write(f"file '{c}'\n")
            
        fade_duration = 1
        fade_start = max(0, get_clips_duration(clips, ffmpeg_exe) - fade_duration)
        
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", list_file]
        if audio_path:
            if audio_offset > 0: cmd += ["-ss", f"{audio_offset:.3f}"]
            cmd += ["-i", audio_path, "-map", "0:v", "-map", "1:a"]
            cmd += ["-vf", f"fade=t=out:st={fade_start:.2f}:d={fade_duration}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"]
            cmd += ["-c:a", "aac", "-af", f"afade=t=out:st={fade_start:.2f}:d={fade_duration}"]
            cmd += ["-shortest", output_path]
        else:
            cmd += ["-vf", f"fade=t=out:st={fade_start:.2f}:d={fade_duration}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"]
            cmd += [output_path]
        subprocess.run(cmd, check=True)
    finally:
        for c in clips + raw_paths:
            if os.path.exists(c): os.remove(c)
        if os.path.exists(list_file): os.remove(list_file)
    return output_path

# --- Execution Flow ---
def main():
    image_analyses = [
        {"source": "/Users/fancy/.cursor/projects/Users-fancy-Desktop-product-animation-fancyai/assets/WechatIMG4665-f86d71ec-93e9-461b-be41-8c7ee269e0c5.png",
         "image_desc": "LV pink rose-gold earrings, mother-of-pearl flower shape, white textured background",
         "motion_hint": "shiny_gem", "has_model": False, "focus_point": (0.5, 0.5)},
        {"source": "/Users/fancy/.cursor/projects/Users-fancy-Desktop-product-animation-fancyai/assets/WechatIMG4667-91b86dbc-8fcc-4aff-b303-3923703acbe1.png",
         "image_desc": "LV pink rose-gold ring, mother-of-pearl flower and diamond, white textured background",
         "motion_hint": "shiny_gem", "has_model": False, "focus_point": (0.5, 0.5)},
        {"source": "/Users/fancy/.cursor/projects/Users-fancy-Desktop-product-animation-fancyai/assets/WechatIMG4666-52e9b486-a976-4f43-80a7-7cad6c61c584.png",
         "image_desc": "LV pink rose-gold bracelet, mother-of-pearl flowers and diamonds, white textured background",
         "motion_hint": "shiny_gem", "has_model": False, "focus_point": (0.5, 0.5)},
        {"source": "/Users/fancy/.cursor/projects/Users-fancy-Desktop-product-animation-fancyai/assets/WechatIMG4664-28b1fe25-789b-4917-b224-4142e3e64b8f.png",
         "image_desc": "LV pink rose-gold necklace, mother-of-pearl flower and diamond, white textured background",
         "motion_hint": "shiny_gem", "has_model": False, "focus_point": (0.5, 0.5)},
    ]

    tool = "seedance"
    category = "Jewelry/Accessories"
    target_ratio = None # adaptive

    print("Skipping music due to network timeout...")
    audio_path = None
    
    print("Calculating clip durations...")
    clip_durations, audio_offset = calc_clip_durations(audio_path, n_clips=len(image_analyses), min_duration=4, max_duration=5)

    image_list = []
    print("Preparing images and prompts...")
    for i, a in enumerate(image_analyses):
        url, ratio = prepare_image(a["source"], target_ratio, tool, a["focus_point"])
        prompt = get_seedance_prompt(category, i, a["image_desc"], a["motion_hint"])
        image_list.append({"url": url, "prompt": prompt, "ratio": ratio, "duration": clip_durations[i]})

    with open(os.path.join(FOLDER, f"prompts_{int(time.time())}.txt"), "w", encoding="utf-8") as f:
        for i, item in enumerate(image_list):
            f.write(f"[{i+1}] {item['duration']}s | {item['ratio']}\nURL: {item['url']}\n{item['prompt']}\n\n")

    print(f"Generating {len(image_list)} video clips with Seedance...")
    all_clip_urls = []
    def _gen_one(item):
        return call_with_retry(seedance20_video_gen_sync, prompt=item["prompt"], first_img_url=item["url"],
                               duration=item["duration"], ratio=item["ratio"], resolution="720p", generate_audio=False)

    results = [None] * len(image_list)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(_gen_one, item): i for i, item in enumerate(image_list)}
        for fut in as_completed(futs):
            idx = futs[fut]
            results[idx] = fut.result()
            print(f"Clip {idx+1} generated successfully.")
            
    for urls in results:
        if urls: all_clip_urls.extend(urls)
        
    print("Stitching videos...")
    output_path = os.path.join(FOLDER, "Louis_Vuitton_Jewelry_final.mp4")
    final_video = merge_videos(all_clip_urls, audio_path=audio_path, output_path=output_path, 
                               audio_offset=audio_offset, trim_per_clip=3)
    
    print(f"Finished: {final_video}")

if __name__ == "__main__":
    main()
