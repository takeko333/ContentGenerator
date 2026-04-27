import os
import shutil
from dotenv import load_dotenv
from glob import glob
from tqdm import tqdm
from PIL import Image
from utils import tti, tts, video

load_dotenv()
input_video_dir = os.getenv("INPUT_VIDEO_DIR")
output_video_dir = os.getenv("OUTPUT_VIDEO_DIR")
font_path = os.getenv("FONT_PATH")
background_image_file_path = os.getenv("BACKGROUND_IMAGE_FILE_PATH")

if __name__ == "__main__":

    speaker = 14
    background = Image.open(background_image_file_path)

    for input_path in glob(input_video_dir + "*.txt"):
        save_dir = output_video_dir + os.path.basename(input_path).replace(".txt", "")
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
        video.concat_audios(audio_path_list, concat_audio_data_path)
        video_path = output_video_dir + os.path.basename(input_path).replace(".txt", ".mp4")
        video.add_static_audio_to_video(concat_audio_data_path, concat_image_data_path, video_path)
        # shutil.rmtree(save_dir)