import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import spacy
from sentence_transformers import SentenceTransformer

from clean_descriptions import description_cleaner
from episodes_encoding import episodes_encoding
from elasticsearch_index_episodes import elasticsearch_index_episodes 

cleaner_model = AutoModelForSequenceClassification.from_pretrained('morenolq/spotify-podcast-advertising-classification')
tokenizer = AutoTokenizer.from_pretrained('morenolq/spotify-podcast-advertising-classification')
nlp = spacy.load("en_core_web_sm")
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)

df_episodes = pd.read_csv("data/episodes.csv")
for index in df_episodes.index:
    description = df_episodes.loc[index,"description"]
    description = description_cleaner(cleaner_model, tokenizer, nlp, description)
    episode_embedding = episodes_encoding(description, encoder_model)
    df_episodes.loc[index,"embedding"] = episode_embedding

dense_dim = len(episode_embedding)
elasticsearch_index_episodes(df_episodes, dense_dim)
