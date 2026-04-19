import textwrap
from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, font_path, font_size=40, image_size=(1280, 720), background=None):
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    if background is not None:
        image.paste(background)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size) # Windowsのパス指定は、raw文字列(r"")にするかスラッシュを使う
    except IOError:
        print("フォントが見つかりません。")
        return
    full_text = wrap_text(draw, text, width, font_size)
    bbox = draw.multiline_textbbox((0, 0), full_text, font=font, stroke_width=3.5)
    block_w = bbox[2] - bbox[0]
    block_h = bbox[3] - bbox[1]
    x = (width - block_w) / 2
    y = (height - block_h) / 2
    draw.multiline_text(
        (x, y), 
        full_text, 
        font=font, 
        fill=(255, 255, 255, 255), 
        stroke_width=5, 
        stroke_fill=(0, 0, 0, 100),
        align="left", 
        spacing=10
    )
    return image

def wrap_text(draw, text, width, font_size, display_rate=0.8):
    lines = []
    max_text_width = width * display_rate
    wrap_width = int(max_text_width // font_size)    
    for paragraph in text.split("\n"):
        if paragraph != "":
            if draw.textlength(paragraph, font=font) > max_text_width:
                lines.extend(textwrap.wrap(paragraph, width=wrap_width))
            else:
                lines.append(paragraph)    
    return "\n".join(lines)