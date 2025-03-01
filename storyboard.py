import os
import argparse
from PIL import Image, ImageDraw

def create_llama_optimized_storyboard(image_paths, output_path='llama_storyboard.jpg', 
                                     padding=2, quality=95):
    """
    Create a captionless storyboard optimized for Llama 3.2-11B-Vision-Preview.
    
    Parameters:
    -----------
    image_paths : list
        List of paths to the 6 images to include in the storyboard
    output_path : str
        Path where the output storyboard will be saved
    padding : int
        Minimal padding between panels (pixels)
    quality : int
        JPEG quality for output image (1-100)
    """
    # Validate inputs
    if len(image_paths) != 6:
        raise ValueError("This function requires exactly 6 images for Llama 3.2 storyboard")
    
    # Load images
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    # Set up the grid - 2x3 grid layout (3 across, 2 down)
    cols = 3
    rows = 2
    
    # Llama's optimal panel size
    panel_width = 336
    panel_height = 336
    
    # Calculate the size of the entire storyboard
    board_width = cols * (panel_width + padding) + padding
    board_height = rows * (panel_height + padding) + padding
    
    # Create the storyboard canvas with white background
    storyboard = Image.new('RGB', (board_width, board_height), (255, 255, 255))
    draw = ImageDraw.Draw(storyboard)
    
    # Place each image
    for i, img in enumerate(images):
        # Calculate position
        row = i // cols
        col = i % cols
        x = padding + col * (panel_width + padding)
        y = padding + row * (panel_height + padding)
        
        # Resize and crop to exactly 336x336
        img_aspect = img.width / img.height
        
        if img_aspect > 1:  # Image is wider than tall
            resize_height = 336
            resize_width = int(336 * img_aspect)
        else:  # Image is taller than wide
            resize_width = 336
            resize_height = int(336 / img_aspect)
        
        resized_img = img.resize((resize_width, resize_height), Image.LANCZOS)
        
        # Center crop to 336x336
        left = (resized_img.width - 336) // 2
        top = (resized_img.height - 336) // 2
        right = left + 336
        bottom = top + 336
        
        cropped_img = resized_img.crop((left, top, right, bottom))
        
        # Paste the cropped image
        storyboard.paste(cropped_img, (x, y))
        
        # Add thin border around panel (optional - comment out to save a few pixels)
        draw.rectangle([x, y, x + panel_width, y + panel_height], outline=(100, 100, 100), width=1)
        
        # Add tiny panel number in corner for reference
        draw.text((x + 4, y + 4), str(i+1), fill=(0, 0, 0))
    
    # Save the optimized storyboard with high quality to preserve details
    storyboard.save(output_path, quality=quality)
    print(f"Llama-optimized storyboard saved to {output_path}")
    
    # Print estimated token usage
    estimated_tokens = 6 * 1000  # 6 panels at ~1K tokens each - max context window is 8192
    print(f"Estimated token usage: ~{estimated_tokens} tokens (rough estimate)")
    
    return storyboard

if __name__ == "__main__":
    image_paths = ['/Users/justintimo/RonaldMcDonald/src/1.png','/Users/justintimo/RonaldMcDonald/src/2.png',
                   '/Users/justintimo/RonaldMcDonald/src/3.png','/Users/justintimo/RonaldMcDonald/src/4.png','/Users/justintimo/RonaldMcDonald/src/5.png',
                    '/Users/justintimo/RonaldMcDonald/src/6.png' ]
    create_llama_optimized_storyboard(image_paths, output_path='llama_storyboard.jpg', 
                                     padding=2, quality=95)