import torch
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.api import TTS

add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cuda")

# List all available built-in voices
#print(tts.speakers)  # This will show something like ["default", "en_female_0", "en_male_1", etc.]

# Female voice from chatGPT
# tts.tts_to_file(
#     text="This is a test using one of the built-in female voices.",
#     speaker_wav="en_sample.wav",  # <- or another name from the printed list
#     language="en",
#     file_path="output.wav"
# )

# Built in Female voice
tts.tts_to_file(
    text="This is a female voice speaking through Coqui XTTS v2.",
    speaker_idx="Ana Florence",  # one of the built-in female voices
    language="en",
    file_path="output_female.wav"
)