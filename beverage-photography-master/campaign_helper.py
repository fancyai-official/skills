#!/usr/bin/env python3
# Copyright 2026 FancyAI
# SPDX-License-Identifier: Apache-2.0

"""
酒水大片生成辅助工具
提供图片压缩、项目文件夹创建等功能
"""

import os
from datetime import datetime
from PIL import Image
import io


def create_campaign_folder(product_name, output_root=None):
    """
    创建项目文件夹

    :param product_name: 产品名称
    :param output_root: 输出根目录。
        优先使用环境变量 BEVERAGE_OUTPUT_DIR；
        未设置时 fallback 到 os.getcwd()/酒水大片输出（适配任意机器）。
    :return: 文件夹路径
    """
    if output_root is None:
        output_root = os.environ.get(
            "BEVERAGE_OUTPUT_DIR",
            os.path.join(os.getcwd(), "酒水大片输出")
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 清理产品名称中的特殊字符
    clean_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in product_name)
    clean_name = clean_name.replace(' ', '_').lower()

    folder_name = f"{clean_name}_campaign_{timestamp}"
    folder_path = os.path.join(output_root, folder_name)

    os.makedirs(folder_path, exist_ok=True)
    print(f"✅ 已创建项目文件夹: {folder_path}")

    return folder_path


def compress_image_to_target_size(image_data, target_size_mb=5):
    """
    将图片压缩到指定大小以下
    
    :param image_data: 图片二进制数据（bytes）
    :param target_size_mb: 目标文件大小（MB）
    :return: 压缩后的图片数据（bytes）
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    original_size_mb = len(image_data) / 1024 / 1024
    
    # 如果已经小于目标大小，直接返回
    if len(image_data) <= target_size_bytes:
        print(f"  📦 无需压缩: {original_size_mb:.2f}MB (已小于{target_size_mb}MB)")
        return image_data
    
    # 打开图片
    img = Image.open(io.BytesIO(image_data))
    
    # 二分查找最佳quality参数
    quality = 95
    low, high = 50, 95
    best_buffer = None
    
    while low <= high:
        quality = (low + high) // 2
        buffer = io.BytesIO()
        
        # 处理透明通道
        if img.mode in ('RGBA', 'LA', 'P'):
            # 转换透明图片为白底
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        
        # 保存为JPEG格式（更好的压缩）
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
        # 如果所有quality都太大，使用最低quality
        best_buffer = io.BytesIO()
        img.save(best_buffer, format='JPEG', quality=50, optimize=True)
        quality = 50
    
    best_buffer.seek(0)
    compressed_data = best_buffer.read()
    compressed_size_mb = len(compressed_data) / 1024 / 1024
    
    print(f"  📦 压缩完成: {original_size_mb:.2f}MB → {compressed_size_mb:.2f}MB (quality={quality})")
    
    return compressed_data


def save_image_to_campaign(image_data, campaign_folder, scene_number, technique_name):
    """
    保存图片到项目文件夹（自动压缩）
    
    :param image_data: 图片数据（bytes）
    :param campaign_folder: 项目文件夹路径
    :param scene_number: 场景编号（1-5）
    :param technique_name: 技法名称
    :return: 保存的文件路径
    """
    # 压缩到5MB以下
    compressed_data = compress_image_to_target_size(image_data, target_size_mb=5)
    
    # 生成文件名
    technique_slug = technique_name.lower().replace(' ', '_').replace('/', '_')
    filename = f"scene_{scene_number}_{technique_slug}.jpg"
    filepath = os.path.join(campaign_folder, filename)
    
    # 保存文件
    with open(filepath, 'wb') as f:
        f.write(compressed_data)
    
    file_size_mb = len(compressed_data) / 1024 / 1024
    print(f"  ✅ 已保存: {filename} ({file_size_mb:.2f}MB)")
    
    return filepath


def save_campaign_info(campaign_folder, product_name, aesthetic_style, techniques, prompts, liquid_color):
    """
    保存项目信息文件
    
    :param campaign_folder: 项目文件夹路径
    :param product_name: 产品名称
    :param aesthetic_style: 美学风格
    :param techniques: 技法列表
    :param prompts: Prompt列表
    :param liquid_color: 液体颜色
    """
    info_path = os.path.join(campaign_folder, "campaign_info.txt")
    
    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(f"# {product_name} 商业大片拍摄项目\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 美学风格\n{aesthetic_style}\n\n")
        f.write(f"## 产品液体颜色\n{liquid_color}\n\n")
        f.write(f"## 技法组合\n")
        for i, tech in enumerate(techniques, 1):
            f.write(f"{i}. {tech}\n")
        f.write(f"\n## 详细Prompt\n\n")
        for i, (tech, prompt) in enumerate(zip(techniques, prompts), 1):
            f.write(f"### 场景{i}: {tech}\n")
            f.write(f"```\n{prompt}\n```\n\n")
    
    print(f"  📄 已保存项目信息: campaign_info.txt")


if __name__ == "__main__":
    # 测试代码
    print("酒水大片生成辅助工具")
    print("=" * 60)
    
    # 测试创建文件夹
    folder = create_campaign_folder("Red Bull Peach Edition")
    print(f"项目文件夹: {folder}")
    
    # 测试压缩（需要实际图片数据）
    # test_image_path = "/path/to/test/image.png"
    # if os.path.exists(test_image_path):
    #     with open(test_image_path, 'rb') as f:
    #         img_data = f.read()
    #     compressed = compress_image_to_target_size(img_data, target_size_mb=5)
    #     print(f"压缩结果: {len(img_data)/1024/1024:.2f}MB → {len(compressed)/1024/1024:.2f}MB")
