import os
from dotenv import load_dotenv
from glob import glob
from tqdm import tqdm
from utils import tti, tts

load_dotenv()
input_video_dir = os.getenv("INPUT_VIDEO_DIR")
output_video_dir = os.getenv("OUTPUT_VIDEO_DIR")
font_path = os.getenv("FONT_PATH")

if __name__ == "__main__":

    for input_path in glob(input_video_dir + "*"):
        save_dir = output_video_dir + os.path.basename(input_path).replace(".txt", "")
        os.makedirs(save_dir, exist_ok=True)
        with open(input_path, "r", encoding="utf-8") as f:
            lines = []
            for line in f.readlines():
                if line != "\n":
                    lines.append(line.strip())
        idx = 1
        for line in tqdm(lines):
            save_path_without_ext = f"{save_dir}/{str(idx).zfill(3)}"
            image = tti.text_to_image(line, font_path)
            image.save(save_path_without_ext + ".png")
            audio = tts.text_to_audio(line)
            audio.export(save_path_without_ext + ".wav", format="wav")
            idx += 1