import os
import shutil
from dotenv import load_dotenv
from glob import glob
from tqdm import tqdm
from PIL import Image
from utils import tti, tts, video
# from utils import connect_browser, generate

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

    try:
        with open(prompt_path, "r", encoding='utf-8') as f:
            prompt = f.read()
    except Exception as e:
        print("プロンプトの読み込みに失敗しました。")
        raise ValueError(f"Error: {e}")

    try:
        with open(os.path.join(input_dir, "display.txt"), "r", encoding="utf-8") as f:
            display_lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print("入力テキスト（表示用）に失敗しました。")
        raise ValueError(f"Error: {e}")

    try:
        with open(os.path.join(input_dir, "speech.txt"), "r", encoding="utf-8") as f:
            reading_lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(display_lines) != len(reading_lines):
            raise ValueError()
    except Exception as e:
        print("入力テキスト（読み上げ用）に失敗しました。⇒入力テキスト（表示用）で代用します。")
        reading_lines = display_lines

    save_dir = os.path.join(output_dir, "video")
    video_path = save_dir + ".mp4"
    if not os.path.exists(video_path):
        os.makedirs(save_dir, exist_ok=True)
        idx = 1
        image_path_list = []
        audio_path_list = []
        inputs = zip(display_lines, reading_lines)
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