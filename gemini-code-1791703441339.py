import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def export_comic_to_pdf(panel_images: list[Image.Image], output_filename: str = "comic_output.pdf") -> str:
    """
    Compiles PIL panel images into a nicely formatted printable PDF comic book.
    """
    c = canvas.Canvas(output_filename, pagesize=letter)
    page_width, page_height = letter

    temp_files = []
    for i, img in enumerate(panel_images):
        temp_path = f"temp_panel_{i}.png"
        img.save(temp_path)
        temp_files.append(temp_path)

    # Arrange 2 panels per page layout or 1 per page
    for i, temp_path in enumerate(temp_files):
        # Draw comic title/header
        c.drawString(54, page_height - 40, "ComicCraft AI Production")
        
        # Center image on page
        img_w, img_h = 450, 450
        x = (page_width - img_w) / 2
        y = (page_height - img_h) / 2 - 20
        
        c.drawImage(temp_path, x, y, width=img_w, height=img_h)
        c.showPage()

    c.save()

    # Clean up temporary panel files
    for path in temp_files:
        if os.path.exists(path):
            os.remove(path)

    return output_filename