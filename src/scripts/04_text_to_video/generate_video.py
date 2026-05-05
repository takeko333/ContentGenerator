import os
import shutil
from dotenv import load_dotenv
from glob import glob
from tqdm import tqdm
from PIL import Image
from utils import tti, tts, video

if __name__ == "__main__":

    load_dotenv()
    input_dir = os.getenv("INPUT_DIRNAME")
    output_dir = os.getenv("OUTPUT_DIRNAME")
    background_image_filename = os.getenv("BACKGROUND_IMAGE_FILENAME")
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    font_path = os.getenv("FONT_PATH")

    speaker = 14
    background = Image.open(os.path.join(input_dir, background_image_filename))

    for input_path in glob(os.path.join(input_dir, "*.txt")):
        save_dir = os.path.join(output_dir, os.path.basename(input_path).replace(".txt", ""))
        video_path = save_dir + ".mp4"
        if not os.path.exists(video_path):
            os.makedirs(save_dir, exist_ok=True)
            with open(input_path, "r", encoding="utf-8") as f:
                lines = []
                for line in f.readlines():
                    if line != "\n":
                        lines.append(line.strip())
            idx = 1
            image_path_list = []
            audio_path_list = []
            for line in tqdm(lines):
                save_path_without_ext = f"{save_dir}/{str(idx).zfill(3)}"
                image_path = save_path_without_ext + ".png"
                image_path_list.append(image_path)
                image = tti.text_to_image(line, font_path, background=background)
                image.save(image_path)
                audio_path = save_path_without_ext + ".wav"
                audio_path_list.append(audio_path)
                audio = tts.text_to_audio(line, speaker=speaker)
                audio.export(audio_path, format="wav")
                idx += 1

            concat_image_data_path = f"{save_dir}/concat_image_data.mp4"
            video.concat_images(image_path_list, audio_path_list, concat_image_data_path)

            concat_audio_data_path = f"{save_dir}/concat_audio_data.wav"
            base_dir = os.path.dirname(os.path.dirname(os.getcwd()))
            ffmpeg_path = os.path.join(base_dir, ffmpeg_path)
            video.concat_audios(audio_path_list, concat_audio_data_path, ffmpeg_path)
            video.add_static_audio_to_video(concat_audio_data_path, concat_image_data_path, video_path)