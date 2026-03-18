from transformers import pipeline
import os
import torch

MODEL_DIR = os.getenv('MODEL_DIR')
device = "cuda:0" if torch.cuda.is_available() else "cpu"

transcriber = pipeline(
    "automatic-speech-recognition",
    model=MODEL_DIR,
    tokenizer=MODEL_DIR,
    device=device,
    chunk_length_s=50,
    generate_kwargs={"num_beams": 5}
)
