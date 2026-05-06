@echo off
set PYTHONPATH=%cd%\..\..\src
python ../../src/scripts/05_import_footage/import_footage.py
python ../../src/scripts/05_import_footage/generate_timestamp.py
pause