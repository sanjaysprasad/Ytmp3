@echo off
REM Path to Python executable — WRAPPED IN QUOTES
set "PYTHON_PATH=C:\Users\Sanjay New\AppData\Local\Programs\Python\Python312\python.exe"

REM Path to your Python script — ALSO WRAPPED
set "SCRIPT_PATH=C:\Users\Sanjay New\Documents\SSP CODES\YT to MP3\ytmp3.py"

echo Running YouTube to MP3 Converter...
"%PYTHON_PATH%" "%SCRIPT_PATH%"
pause
