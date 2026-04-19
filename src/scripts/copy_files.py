import os
import shutil
from dotenv import load_dotenv
from glob import glob

load_dotenv()
generated_data_dir = os.getenv("GENERATED_DATA_DIR")
generated_text_filename = os.getenv("GENERATED_TEXT_FILENAME")
input_tts_dir = os.getenv("INPUT_TTS_DIR")

if __name__ == "__main__":

    for sub_dir in glob(os.path.join(generated_data_dir, "*")):
        load_path = os.path.join(sub_dir, generated_text_filename)
        save_path = os.path.join(input_tts_dir, sub_dir.split("\\")[-1] + ".txt")
        if not os.path.exists(save_path):
            try:
                _ = shutil.copy(load_path, save_path)
                print("コピー成功：", save_path)
            except Exception as e:
                print("エラー：", e)