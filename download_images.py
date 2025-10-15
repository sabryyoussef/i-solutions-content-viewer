#!/usr/bin/env python3
"""
Download and organize images from Tharwah Academy website for Streamlit app
"""

import requests
import os
from pathlib import Path
from PIL import Image
import io

# Create directories
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Key images from Tharwah Academy website
IMAGES_TO_DOWNLOAD = {
    "hero_bg.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/hero-bg.jpg",
    "logo.png": "https://academy.tharwah.net/wp-content/uploads/2024/06/tharwah-academy-logo.png",
    "cert_cybersecurity.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/cybersecurity-course.jpg",
    "cert_shrm.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/shrm-certificate.jpg",
    "cert_accounting.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/accounting-course.jpg",
    "cert_pmp.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/pmp-course.jpg",
    "cert_ai.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/ai-course.jpg",
    "cert_training.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/professional-training.jpg",
    "stats_bg.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/stats-background.jpg",
    "about_us.jpg": "https://academy.tharwah.net/wp-content/uploads/2024/06/about-tharwah.jpg"
}

def download_and_resize_image(url, filename, max_width=800, max_height=600):
    """Download image and resize it for web use"""
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Open image with PIL
        image = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize while maintaining aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        output_path = IMAGES_DIR / filename
        image.save(output_path, 'JPEG', quality=85, optimize=True)
        
        print(f"✅ Saved {filename} ({image.size[0]}x{image.size[1]})")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {str(e)}")
        return False

def create_placeholder_images():
    """Create placeholder images if downloads fail"""
    placeholder_images = {
        "hero_bg.jpg": "Create a gradient background",
        "logo.png": "Create Tharwah Academy logo",
        "cert_cybersecurity.jpg": "Cybersecurity course image",
        "cert_shrm.jpg": "SHRM certificate image", 
        "cert_accounting.jpg": "Accounting course image",
        "cert_pmp.jpg": "PMP course image",
        "cert_ai.jpg": "AI course image",
        "cert_training.jpg": "Professional training image",
        "stats_bg.jpg": "Statistics background",
        "about_us.jpg": "About us image"
    }
    
    for filename, description in placeholder_images.items():
        if not (IMAGES_DIR / filename).exists():
            print(f"Creating placeholder for {filename} - {description}")
            # Create a simple colored placeholder
            img = Image.new('RGB', (400, 300), color='#f0f0f0')
            try:
                img.save(IMAGES_DIR / filename)
                print(f"✅ Created placeholder {filename}")
            except Exception as e:
                print(f"❌ Failed to create placeholder {filename}: {str(e)}")

def main():
    print("🖼️  Downloading Tharwah Academy Images for Streamlit App")
    print("=" * 60)
    
    # Download images
    success_count = 0
    for filename, url in IMAGES_TO_DOWNLOAD.items():
        if download_and_resize_image(url, filename):
            success_count += 1
    
    print(f"\n📊 Download Summary:")
    print(f"✅ Successfully downloaded: {success_count}/{len(IMAGES_TO_DOWNLOAD)} images")
    
    # Create placeholders for failed downloads
    print(f"\n🔄 Creating placeholder images for missing files...")
    create_placeholder_images()
    
    # List all images
    print(f"\n📁 Images available in {IMAGES_DIR}:")
    for img_file in sorted(IMAGES_DIR.glob("*")):
        if img_file.is_file():
            size = img_file.stat().st_size
            print(f"  - {img_file.name} ({size:,} bytes)")
    
    print(f"\n🎉 Image setup complete!")
    print(f"Images are ready to use in the Streamlit app at: static/images/")

if __name__ == "__main__":
    main()
