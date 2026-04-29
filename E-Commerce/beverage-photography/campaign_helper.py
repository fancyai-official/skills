#!/usr/bin/env python3
"""
Beverage commercial photography helper
Provides image compression and project folder creation utilities
"""

import os
from datetime import datetime
from PIL import Image
import io


def create_campaign_folder(product_name):
    """
    Create a project folder with timestamp

    :param product_name: product name
    :return: folder path
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # sanitize special characters from product name
    clean_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in product_name)
    clean_name = clean_name.replace(' ', '_').lower()
    
    folder_name = f"{clean_name}_campaign_{timestamp}"
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    folder_path = os.path.join(base_dir, folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    print(f"✅ Campaign folder created: {folder_path}")
    
    return folder_path


def compress_image_to_target_size(image_data, target_size_mb=5):
    """
    Compress image to below the specified size

    :param image_data: image binary data (bytes)
    :param target_size_mb: target file size (MB)
    :return: compressed image data (bytes)
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    original_size_mb = len(image_data) / 1024 / 1024
    
    # return early if already under target size
    if len(image_data) <= target_size_bytes:
        print(f"  📦 No compression needed: {original_size_mb:.2f}MB (already under {target_size_mb}MB)")
        return image_data
    
    img = Image.open(io.BytesIO(image_data))
    
    # binary search for the best quality value
    quality = 95
    low, high = 50, 95
    best_buffer = None
    
    while low <= high:
        quality = (low + high) // 2
        buffer = io.BytesIO()
        
        # handle transparency — composite onto white background
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        
        # save as JPEG for better compression ratio
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        size = buffer.tell()
        
        if size <= target_size_bytes:
            best_buffer = buffer
            if high - low <= 1:
                break
            low = quality + 1
        else:
            high = quality - 1
    
    if best_buffer is None:
        # fallback to lowest quality if all attempts exceed target size
        best_buffer = io.BytesIO()
        img.save(best_buffer, format='JPEG', quality=50, optimize=True)
        quality = 50
    
    best_buffer.seek(0)
    compressed_data = best_buffer.read()
    compressed_size_mb = len(compressed_data) / 1024 / 1024
    
    print(f"  📦 Compressed: {original_size_mb:.2f}MB → {compressed_size_mb:.2f}MB (quality={quality})")
    
    return compressed_data


def save_image_to_campaign(image_data, campaign_folder, scene_number, technique_name):
    """
    Save image to project folder with automatic compression

    :param image_data: image data (bytes)
    :param campaign_folder: project folder path
    :param scene_number: scene index (1-5)
    :param technique_name: shooting technique name
    :return: saved file path
    """
    compressed_data = compress_image_to_target_size(image_data, target_size_mb=5)
    
    # build filename
    technique_slug = technique_name.lower().replace(' ', '_').replace('/', '_')
    filename = f"scene_{scene_number}_{technique_slug}.jpg"
    filepath = os.path.join(campaign_folder, filename)
    
    with open(filepath, 'wb') as f:
        f.write(compressed_data)
    
    file_size_mb = len(compressed_data) / 1024 / 1024
    print(f"  ✅ Saved: {filename} ({file_size_mb:.2f}MB)")
    
    return filepath


def save_campaign_info(campaign_folder, product_name, aesthetic_style, techniques, prompts, liquid_color):
    """
    Save project metadata to a text file

    :param campaign_folder: project folder path
    :param product_name: product name
    :param aesthetic_style: chosen aesthetic style
    :param techniques: list of shooting techniques
    :param prompts: list of prompts
    :param liquid_color: liquid color
    """
    info_path = os.path.join(campaign_folder, "campaign_info.txt")
    
    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(f"# {product_name} — Commercial Photography Campaign\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Aesthetic Style\n{aesthetic_style}\n\n")
        f.write(f"## Liquid Color\n{liquid_color}\n\n")
        f.write(f"## Shooting Techniques\n")
        for i, tech in enumerate(techniques, 1):
            f.write(f"{i}. {tech}\n")
        f.write(f"\n## Prompts\n\n")
        for i, (tech, prompt) in enumerate(zip(techniques, prompts), 1):
            f.write(f"### Scene {i}: {tech}\n")
            f.write(f"```\n{prompt}\n```\n\n")
    
    print(f"  📄 Project info saved: campaign_info.txt")


if __name__ == "__main__":
    print("Beverage Commercial Photography Helper")
    print("=" * 60)
    
    folder = create_campaign_folder("Red Bull Peach Edition")
    print(f"Campaign folder: {folder}")
    
