import os
import shutil
from dotenv import load_dotenv
from glob import glob
from tqdm import tqdm
from PIL import Image
from utils import tti, tts, video
# from utils import connect_browser, generate

def get_inputs(display_lines, save_path="", generate_reading=False):
    if generate_reading:
        outputs = generate.generate_txt(
            connect_browser.page, 
            prompt + "\n" + "\n".join(display_lines),
            save_path
        )
        reading_lines = []
        for line in outputs.split("\n"):
            if line != "":
                reading_lines.append(line.strip())
        return zip(display_lines, reading_lines)
    else:
        return zip(display_lines, display_lines)

if __name__ == "__main__":

    load_dotenv()
    input_dir = os.getenv("INPUT_DIRNAME")
    output_dir = os.getenv("OUTPUT_DIRNAME")
    background_image_filename = os.getenv("BACKGROUND_IMAGE_FILENAME")
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    font_path = os.getenv("FONT_PATH")

    speaker = 14
    background = Image.open(os.path.join(input_dir, background_image_filename))

    prompt_path = os.path.join(input_dir, os.getenv("PROMPT_DIRNAME"))
    prompt_path = os.path.join(prompt_path, "generate_reading.txt")
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt = f.read()

    for input_path in glob(os.path.join(input_dir, "*.txt")):
        save_dir = os.path.join(output_dir, os.path.basename(input_path).replace(".txt", ""))
        video_path = save_dir + ".mp4"
        if not os.path.exists(video_path):
            os.makedirs(save_dir, exist_ok=True)
            with open(input_path, "r", encoding="utf-8") as f:
                display_lines = [line.strip() for line in f.readlines() if line.strip()]
            inputs = get_inputs(display_lines, os.path.join(save_dir, "reading.csv"))
            idx = 1
            image_path_list = []
            audio_path_list = []
            for display_line, reading_line in tqdm(inputs):
                save_path_without_ext = f"{save_dir}/{str(idx).zfill(3)}"
                image_path = save_path_without_ext + ".png"
                image_path_list.append(image_path)
                image = tti.text_to_image(display_line, font_path, background=background)
                image.save(image_path)
                audio_path = save_path_without_ext + ".wav"
                audio_path_list.append(audio_path)
                audio = tts.text_to_audio(reading_line, speaker=speaker)
                audio.export(audio_path, format="wav")
                idx += 1

            concat_image_data_path = f"{save_dir}/concat_image_data.mp4"
            video.concat_images(image_path_list, audio_path_list, concat_image_data_path)

            concat_audio_data_path = f"{save_dir}/concat_audio_data.wav"
            base_dir = os.path.dirname(os.path.dirname(os.getcwd()))
            ffmpeg_path = os.path.join(base_dir, ffmpeg_path)
            video.concat_audios(audio_path_list, concat_audio_data_path, ffmpeg_path)
            video.add_static_audio_to_video(concat_audio_data_path, concat_image_data_path, video_path)