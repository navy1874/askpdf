"""
Create an icon for the PDF Reader application
Red background with white "aPDF" text
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with red background
    size = 256
    img = Image.new('RGB', (size, size), color='#DC143C')  # Crimson red
    draw = ImageDraw.Draw(img)
    
    # Try to use a bold font, fallback to default if not available
    try:
        # Try to find a bold font on Windows
        font_paths = [
            'C:/Windows/Fonts/arialbd.ttf',  # Arial Bold
            'C:/Windows/Fonts/calibrib.ttf',  # Calibri Bold
            'C:/Windows/Fonts/verdanab.ttf',  # Verdana Bold
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 72)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Draw the text "aPDF" in white
    text = "aPDF"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position to center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10  # Slight adjustment
    
    # Draw white text
    draw.text((x, y), text, fill='white', font=font)
    
    # Save as ICO file with multiple sizes
    icon_path = 'icon.ico'
    # Create multiple sizes for better display at different resolutions
    img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    print(f"Icon created successfully: {icon_path}")
    return icon_path

if __name__ == '__main__':
    create_icon()
