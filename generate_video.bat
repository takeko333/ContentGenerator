@echo off
set PYTHONPATH=%cd%\src
python src/scripts/generate_video.py
python src/scripts/delete_files_after_generating_video.py