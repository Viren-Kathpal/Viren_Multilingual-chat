import os
from transformers import MarianMTModel, MarianTokenizer
from itertools import permutations

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja"
}

def download_model(src, tgt):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    save_path = f"models/{src}-{tgt}"
    try:
        MarianMTModel.from_pretrained(model_name, cache_dir=save_path)
        MarianTokenizer.from_pretrained(model_name, cache_dir=save_path)
        print(f"Downloaded: {src} → {tgt}")
    except Exception as e:
        print(f"Model not available: {src} → {tgt}")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    pairs = permutations(SUPPORTED_LANGUAGES.values(), 2)
    for src, tgt in pairs:
        download_model(src, tgt)