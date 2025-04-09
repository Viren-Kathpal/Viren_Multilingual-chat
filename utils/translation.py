from transformers import MarianMTModel, MarianTokenizer
from transformers.utils import logging

model_cache = {}
logging.set_verbosity_error()

def get_model(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    if model_name not in model_cache:
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            model_cache[model_name] = (tokenizer, model)
        except:
            return None
    return model_cache.get(model_name)

def translate(text, src_lang, tgt_lang):
    model_pair = get_model(src_lang, tgt_lang)
    if not model_pair:
        return None
    tokenizer, model = model_pair
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def translate_message(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text

    # Try direct translation
    result = translate(text, src_lang, tgt_lang)
    if result is not None:
        return result

    # Fallback: use English as bridge
    if src_lang != "en" and tgt_lang != "en":
        to_en = translate(text, src_lang, "en")
        if to_en:
            final = translate(to_en, "en", tgt_lang)
            if final:
                return final

    return f"[Translation Unavailable from {src_lang} to {tgt_lang}]"
