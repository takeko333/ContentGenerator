import os
import shutil
from dotenv import load_dotenv
from glob import glob

if __name__ == "__main__":

    load_dotenv()
    input_dir = os.getenv("INPUT_DIRNAME")
    output_dir = os.getenv("OUTPUT_DIRNAME")
    generated_data_dir = os.getenv("01_DIR")
    generated_text_filename = os.getenv("GENERATED_TEXT_FILENAME")

    current_path = os.getcwd()
    parent_dir = os.path.dirname(current_path)
    target_dir = os.path.join(parent_dir, generated_data_dir)
    target_dir = os.path.join(target_dir, output_dir)

    generated_text_basename = generated_text_filename.replace(".txt", "")
    for sub_dir in glob(os.path.join(target_dir, "*")):
        for load_path in glob(os.path.join(sub_dir, "*.txt")):
            if generated_text_basename in load_path:
                save_path = os.path.join(input_dir, sub_dir.split("\\")[-1] + os.path.basename(load_path.replace(generated_text_basename, "")))
                if not os.path.exists(save_path):
                    try:
                        _ = shutil.copy(load_path, save_path)
                        print("コピー成功：", save_path)
                    except Exception as e:
                        print("エラー：", e)
                else:
                    print("コピー済み：", save_path)