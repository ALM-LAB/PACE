import os
import json
import pandas as pd
from tqdm import tqdm
import cohere
import time
import numpy as np
import torch

from elasticsearch_index_episodes import elasticsearch_index_chapters

#import sentenceBERT
from sentence_transformers import SentenceTransformer
model_name = "all-mpnet-base-v2"
model = SentenceTransformer(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
model = model.to(device)

COHERE = False

'''
from elasticsearch import Elasticsearch
es = Elasticsearch()

resp = es.search(index="podmagic-chapters", body={"query": {"match_all": {}}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    # pring gist and summary
    print(hit["_source"]["chapter_gist"])
    print(hit["_source"]["chapter_summary"])

exit()
'''

cohere_api_key = 'c8ES1KWN9nd8uObqxiBvBWEQ450asuAkoF61EYCg'
co = cohere.Client(cohere_api_key)

selected_episodes = os.listdir(os.path.join("data", "transcriptions"))
selected_episodes = [episode for episode in selected_episodes if not episode.startswith(".")]

embedded_summaries = {}

episode_ids = []
chapter_ids = []
chapter_gists = []
chapter_summaries = []
audio_urls = []
starts = []
ends = []

counter = 0

for episode in tqdm(selected_episodes):
    episode_id = episode[:-4]
    #load json file
    with open(os.path.join("data", "transcriptions", episode), "r") as f:
        data = json.load(f)
    
    if COHERE:
        if counter > 90:
            time.sleep(45)
            counter = 0

    #get the chapters
    chapters = data["chapters"]
    audio_url = data["audio_url"]
    print("Episode:", episode)
    print("# chapters:", len(chapters))
    print("Chapters:")

    counter += len(chapters)

    for i, chapter in enumerate(chapters):
        chapter_id = episode_id + "_" + str(i)
        gist = chapter["gist"]
        summary = chapter["summary"]
        start = chapter["start"]
        end = chapter["end"]

        #store info
        chapter_ids.append(chapter_id)
        chapter_gists.append(gist)
        chapter_summaries.append(summary)
        episode_ids.append(episode_id)
        audio_urls.append(audio_url)
        starts.append(start)
        ends.append(end)

        if COHERE:
            #embed the summary
            response = co.embed(
                texts=[summary],
                model="small",
            )
        
            embedded_summary = response.embeddings[0]
            embedded_summary = np.array(embedded_summary)
        else:
            embedded_summary = model.encode(summary)

        #store the embedded summary
        embedded_summaries[chapter_id] = embedded_summary

        print("\t", i+1, "-", gist)
        print("\t  ", "-", summary)


df = pd.DataFrame()
df["episode_id"] = episode_ids
df["chapter_id"] = chapter_ids
df["chapter_gist"] = chapter_gists
df["chapter_summary"] = chapter_summaries
df["audio_url"] = audio_urls
df["start"] = starts
df["end"] = ends

dense_dim = len(embedded_summary)
elasticsearch_index_chapters(df, embedded_summaries, dense_dim)
