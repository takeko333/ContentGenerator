import os
import shutil
from dotenv import load_dotenv
from glob import glob

load_dotenv()
output_video_dir = os.getenv("OUTPUT_VIDEO_DIR")

if __name__ == "__main__":

    common_parts_dir = "inputs/edit-video/common-parts/"
    target_parts = []
    target_parts.append(common_parts_dir + "導入A.mp4")
    target_parts.append(common_parts_dir + "導入B.mp4")

    main_parts = glob("inputs/edit-video/main-parts/*.mp4")
    main_parts.sort()
    for item in main_parts:
        target_parts.append(item)
        if item != main_parts[-1]:
            target_parts.append(common_parts_dir + "挿入.mp4")
        else:
            target_parts.append(common_parts_dir + "フェードアウト.mp4")

    idx = 1
    save_dir = "outputs/edit-video/"
    for item in target_parts:
        filename = os.path.basename(item)
        new_path = save_dir + str(idx).zfill(2) + "_" + filename
        shutil.copy(item, new_path)
        idx += 1