# Text to Voice with AI Female

### Run App
- run in WSL2
- create a folder named `static` in the root for the output.wav to be saved to
- create/start a `tts-env` virtual environment
  - source tts-env/bin/activate if the virtual environment has already been created
- run `pip install -r requirements.txt` if first time running app
- run `uvicorn main:app --reload` to start the app

### On MacOS
- Enable MPS Backend in `main.py`
- brew install portaudio libsndfile ffmpeg
- folder structure below
tts-ai/
├── main.py
├── requirements.txt
├── en_sample.wav
├── static/
│   └── (empty or output.wav)
├── templates/
│   └── index.html

- cd path/to/tts-ai
- python3 -m venv tts-env
- source tts-env/bin/activate
- pip install -r requirements.txt
- uvicorn main:app --reload

### Files
1. `voice.py` was the first iteration of this app. It used `en_sample.wav` to know what kind of voice to use. Then created an `output.wav` of the text being read.
2. `main.py`, `requirements.txt`, `en_sample.wav`, `/static`, `/templates` all needed to run a basic web UI

### TODOs
- Add a web audio player that buffers while playing
- Add file input support (PDF, DOCX)
- Add a real-time progress bar