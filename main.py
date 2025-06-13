import torch
import asyncio
import gc
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.api import TTS

# Add required globals for torch >= 2.6
add_safe_globals([XttsConfig, XttsAudioConfig, XttsArgs, BaseDatasetConfig])

# Init FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load TTS model once
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
# not enough GPU memory, so using CPU instead
#tts.to("cuda") 

# Move TTS model to CPU, slower but avoids GPU memory issues
tts.to("cpu") 

# Option to use GPU if available and has enough memory
# explor if cpu takes too long
# device = "cuda" if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory > 5000000000 else "cpu"
# tts.to(device)

# MPS Backend for Apple Silicon
# Enable when running on Mac with Apple Silicon
# device = "mps" if torch.backends.mps.is_available() else "cpu"
# print(f"Using device: {device}")
# tts.to(device)

# --- Background TTS task with timeout ---
def generate_tts(text: str):
    tts.tts_to_file(
        text=text,
        speaker_wav="en_sample.wav",
        language="en",
        file_path="static/output.wav"
    )
    torch.cuda.empty_cache()
    gc.collect()

async def run_tts_with_timeout(text: str, timeout: int = 30):
    loop = asyncio.get_event_loop()
    try:
        await asyncio.wait_for(
            loop.run_in_executor(None, generate_tts, text),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise RuntimeError("TTS generation timed out")

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/speak", response_class=HTMLResponse)
async def speak(request: Request, text: str = Form(...)):
    if len(text) > 500:
        return HTMLResponse("❌ Input too long. Please limit to 500 characters.", status_code=400)

    try:
        await run_tts_with_timeout(text, timeout=30)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "audio_url": "/static/output.wav",
            "text": text
        })
    except RuntimeError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e),
            "text": text
        })