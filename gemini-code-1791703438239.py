import io
import requests
from PIL import Image, ImageDraw, ImageFont

def create_comic_panel_image(visual_prompt: str, caption: str, dialogue: str, panel_num: int) -> Image.Image:
    """
    Creates a styled comic panel image layout with caption boxes and speech text overlays.
    """
    # 1. Base Panel Image Generation placeholder (integrate Imagen 3 via Gemini or Stable Diffusion here)
    # For demonstration, we generate a clean stylized canvas background representing the panel artwork.
    width, height = 600, 600
    panel_img = Image.new("RGB", (width, height), color=(245, 245, 240))
    draw = ImageDraw.Draw(panel_img)
    
    # Draw a comic panel border outline
    draw.rectangle([10, 10, width - 10, height - 10], outline="black", width=5)
    
    # Render visual prompt text description inside the drawing area as placeholder art text
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text((30, 50), f"[Artwork Scene {panel_num}]\n{visual_prompt[:120]}...", fill="darkgray", font=font)
    
    # 2. Add Caption Box (Top)
    if caption:
        draw.rectangle([20, 20, width - 20, 80], fill=(255, 255, 220), outline="black", width=2)
        draw.text((30, 30), f"Caption: {caption}", fill="black", font=font)

    # 3. Add Speech Dialogue Bubble / Box (Bottom)
    if dialogue:
        draw.rectangle([40, height - 120, width - 40, height - 30], fill="white", outline="black", width=2)
        draw.text((50, height - 110), f"Dialogue: {dialogue}", fill="black", font=font)

    return panel_img