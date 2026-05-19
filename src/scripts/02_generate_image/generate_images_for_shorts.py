import os
from dotenv import load_dotenv
from utils import connect_browser, extract, generate, path
from datetime import datetime
from PIL import Image

def crop_image(image, position='center', target_size=(1280, 720)):
    w, h = image.size
    crop_w = w
    crop_h = w * 9 // 16
    if position == 'top':
        upper = 0
    elif position == 'bottom':
        upper = h - crop_h
    else:
        upper = (h - crop_h) // 2
    lower = upper + crop_h
    image = image.crop((0, upper, w, lower))
    image = image.resize(target_size, Image.LANCZOS)
    return image

if __name__ == "__main__":

    ng_list = ["Gemini の回答"]

    load_dotenv()
    input_dir = os.getenv("INPUT_DIRNAME")
    output_dir = os.getenv("OUTPUT_DIRNAME")

    input_text_path = os.path.join(input_dir, "text.txt")
    with open(input_text_path, "r", encoding='utf-8') as f:
        text = "\n".join([line.strip() for line in f.readlines() if line.strip()])

    prompt_dir = os.path.join(input_dir, os.getenv("PROMPT_DIRNAME"))
    with open(os.path.join(prompt_dir, "generate_image_ideas_for_shorts.txt"), "r", encoding='utf-8') as f:
        prompt_for_image_ideas = f.read()
    with open(os.path.join(prompt_dir, "generate_images_for_shorts.txt"), "r", encoding='utf-8') as f:
        prompt_for_images = f.read()

    generated_text_filename = os.getenv("GENERATED_TEXT_FILENAME")
    log_filename = os.getenv("LOG_FILENAME")
    try:
        timeinfo = "20260520082330" # datetime.now().strftime("%Y%m%d%H%M%S")
        save_dir = os.path.join(output_dir, timeinfo)
        save_text_path = os.path.join(save_dir, generated_text_filename)
        generate.generate_txt(
            connect_browser.page, 
            prompt_for_image_ideas + "\n" + "\n".join(lines), 
            save_text_path
        )
        with open(save_text_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            lines = [line for line in lines if line not in ng_list]
        for idx, line in enumerate(lines):
            filename = f"{str(idx).zfill(3)}.png"
            save_image_path = os.path.join(save_dir, filename)
            generate.generate_img(
                connect_browser.page, 
                prompt_for_images + "\n" + line, 
                save_image_path
            )
            image = Image.open(save_image_path)
            for pos in ["top", "center", "bottom"]:
                save_pos_dir = os.path.join(save_dir, pos)
                os.makedirs(save_pos_dir, exist_ok=True)
                crop_image(image, position=pos).save(os.path.join(save_pos_dir, filename))
    finally:
        print("done.")
