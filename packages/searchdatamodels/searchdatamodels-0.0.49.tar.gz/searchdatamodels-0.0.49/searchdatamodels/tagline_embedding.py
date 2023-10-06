from sentence_transformers import SentenceTransformer
import deepl
import os
from langdetect import detect

translator = deepl.Translator(os.environ["DEEPL_API_KEY"])

def translate_to_english(text:str)-> str:
    if detect(text) !='en':
        return translator.translate_text(text, target_lang="EN-US").text.lower()
    else:
        return text




#https://www.sbert.net/docs/pretrained_models.html

#these were chosen for their speed and decent performance
MINI_LM_12='all-MiniLM-L12-v2'
MINI_LM_L6='all-MiniLM-L6-v2'
PARAPHRASE_LM_L3='paraphrase-MiniLM-L3-v2'

SENTENCE_EMBEDDING_MODELS=[MINI_LM_12, MINI_LM_L6, PARAPHRASE_LM_L3]

DEFAULT_SENTENCE_TRANSFORMER_MODEL=MINI_LM_L6
model_dict={
    model_name: SentenceTransformer(model_name) for model_name in SENTENCE_EMBEDDING_MODELS
} #preload the models

def create_embedding(text: str, model_name: str=DEFAULT_SENTENCE_TRANSFORMER_MODEL):
    model=model_dict[model_name]
    en_text=translate_to_english(text)
    embedding_list = model.encode([en_text])
    return embedding_list[0].tolist()