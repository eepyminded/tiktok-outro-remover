# ⚠️ EARLY WIP! ⚠️

# Tiktok Outro Remover

This tool allows you to automate removing tiktok annoying outro at the end, specify your directories where video files are, script will detect & remove them,  for your convenience.

## Requirements

- openCV
- numpy 
- ffmpeg
- tkinter
- Python

## Setting it up and running:
```bash
git clone -b development https://github.com/eepyminded/tiktok-outro-remover.git
cd tiktok-outro-remover
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python appUi.py
```

## TODO
- ✅ Function  detecting what frame does the ending start
- ✅ Checking videos in a chosen folder, saving the original ones
- ✅ Program functioning correctly
- 🔄 Proper error handling
- 🔄 Proper tests
- 🔄 Elegant GUI
- 🔄 Changing tolerance (models?) of detection