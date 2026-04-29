@echo off
set PYTHONPATH=%cd%\src
python src/scripts/generate_components_for_video_editing.py
python src/scripts/generate_timestamp.py