import os
import shutil
import pathlib
from dotenv import load_dotenv
from glob import glob

load_dotenv()
output_video_dir = os.getenv("OUTPUT_VIDEO_DIR")

if __name__ == "__main__":

    for path in glob(os.path.join(output_video_dir, "*")):
        if pathlib.Path(path).is_dir():
            shutil.rmtree(path)
