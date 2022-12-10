import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import spacy
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch

from clean_descriptions import description_cleaner
from episodes_encoding import episodes_encoding
from elasticsearch_index_episodes import elasticsearch_index_episodes 

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

cleaner_model = AutoModelForSequenceClassification.from_pretrained('morenolq/spotify-podcast-advertising-classification')
cleaner_model.to(device)
tokenizer = AutoTokenizer.from_pretrained('morenolq/spotify-podcast-advertising-classification')
nlp = spacy.load("en_core_web_sm")
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)
encoder_model.to(device)


df_episodes = pd.read_csv("data/news_episodes.csv")
episode_embedding_dict = {}
description_clean_dict = {}
episodes_id_to_remove = []
for index in tqdm(df_episodes.index):
    description = df_episodes.loc[index,"episode_description"]
    episode_id = df_episodes.loc[index,"episode_id"]
    try:
        description = description_cleaner(cleaner_model, tokenizer, nlp, description, device)
        episode_embedding = episodes_encoding(description, encoder_model)
        episode_embedding_dict[episode_id] = episode_embedding
        description_clean_dict[episode_id] = description
    except Exception as e:
        print (e)
        print("Error with episode_id: ", episode_id)
        # remove the episode from the dataframe
        episodes_id_to_remove.append(episode_id)

    if index == 15000:
        dense_dim = len(episode_embedding)
        elasticsearch_index_episodes(df_episodes.head(15000), episode_embedding_dict, description_clean_dict, dense_dim)

df_episodes = df_episodes[~df_episodes.episode_id.isin(episodes_id_to_remove)]

dense_dim = len(episode_embedding)
elasticsearch_index_episodes(df_episodes, episode_embedding_dict, description_clean_dict, dense_dim)
