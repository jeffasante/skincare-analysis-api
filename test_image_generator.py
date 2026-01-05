"""
Generate test images for the Skincare Analysis API
Run: python generate_test_images.py
"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_test_image(filename, size=(800, 600), color=None):
    """Generate a simple test image with random colors or specified color."""
    if color is None:
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
    
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size[0] // 2, size[1] // 2
    
    face_radius = min(size) // 3
    draw.ellipse(
        [center_x - face_radius, center_y - face_radius,
         center_x + face_radius, center_y + face_radius],
        fill=(255, 220, 200),
        outline=(200, 180, 160),
        width=3
    )
    
    eye_y = center_y - face_radius // 3
    eye_offset = face_radius // 3
    eye_radius = 20
    
    draw.ellipse(
        [center_x - eye_offset - eye_radius, eye_y - eye_radius,
         center_x - eye_offset + eye_radius, eye_y + eye_radius],
        fill=(100, 70, 50)
    )
    
    draw.ellipse(
        [center_x + eye_offset - eye_radius, eye_y - eye_radius,
         center_x + eye_offset + eye_radius, eye_y + eye_radius],
        fill=(100, 70, 50)
    )
    
    mouth_y = center_y + face_radius // 3
    draw.arc(
        [center_x - 50, mouth_y - 20,
         center_x + 50, mouth_y + 20],
        start=0, end=180,
        fill=(150, 80, 80),
        width=3
    )
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = f"Test Image - {size[0]}x{size[1]}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) // 2
    
    draw.text((text_x, 20), text, fill=(255, 255, 255), font=font)
    
    img.save(filename)
    print(f"✓ Generated: {filename} ({size[0]}x{size[1]}, {os.path.getsize(filename) / 1024:.1f} KB)")

def main():
    """Generate various test images."""
    print("Generating test images...\n")
    
    os.makedirs("test_images", exist_ok=True)
    
    generate_test_image("test_images/test_small.jpg", size=(400, 300))
    generate_test_image("test_images/test_medium.jpg", size=(800, 600))
    generate_test_image("test_images/test_large.jpg", size=(1920, 1080))
    
    img = Image.new('RGB', (800, 600), (200, 150, 100))
    img.save("test_images/test_image.png")
    print(f"✓ Generated: test_images/test_image.png (800x600, {os.path.getsize('test_images/test_image.png') / 1024:.1f} KB)")
    
    generate_test_image("test_images/test_portrait.jpg", size=(600, 800))
    
    generate_test_image("test_images/test_skin_light.jpg", size=(800, 600))
    generate_test_image("test_images/test_skin_medium.jpg", size=(800, 600))
    generate_test_image("test_images/test_skin_dark.jpg", size=(800, 600))
    
    generate_test_image("test_images/test_tiny.jpg", size=(100, 100))
    
    generate_test_image("test_images/test_hires.jpg", size=(2400, 1800))
    
    print(f"\n✓ All test images generated in 'test_images/' directory")
    print("\nYou can now use these images to test the API!")
    print("\nExample usage:")


if __name__ == "__main__":

    '''
    curl -X POST "http://localhost:8000/upload" \
    -H "X-API-Key: dev-api-key-12345" \
    -F "file=@test_images/test_medium.jpg"

    '''

    main()

