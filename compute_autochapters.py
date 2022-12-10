import pandas as pd
import requests
import time
import os
from tqdm import tqdm


## Read data
df = pd.read_csv('data/news_episodes.csv')

## Select episodes based on 
# (podcast_name == "The Daily Good") or (podcast_name == "The Daily Show")
df = df[(df['podcast_name'] == 'The Daily Good') | (df['podcast_name'] == 'Daily News Brief')]

## Drop columns
drop_cols = ['episode_description', 'episode_pub_date', \
    'episode_artwork_link', 'podcast_creator', 'podcast_main_genre']
df = df.drop(drop_cols, axis=1)

## Cast episode_duration to int
df['episode_duration'] = df['episode_duration'].astype(int)

## Sort by episode_duration
df = df.sort_values(by='episode_duration', ascending=True)

print("Total episodes:", len(df))
print("Total hours:", df['episode_duration'].sum()/3600) 

## Check if the episode has already been computed
already_computed_episodes = os.listdir('data/transcriptions')

## Bad URLs
bad_urls = ["https://app.dropwave.io/episode/86906ecb-db12-4c65-a235-b083de87d0a0/daily-news-brief-for-monday-july-11th-2022.mp3",
            "https://app.dropwave.io/episode/eab07d8f-7a0b-4f80-8e6e-c6a87e30e47f/daily-news-brief-for-monday-june-27th-2022.mp3"]

for index, row in tqdm(df.iterrows(), total=len(df)):

    ## If the episode has already been computed, skip it
    if str(row['episode_id']) + '.json' in already_computed_episodes:
        print("Already computed:", row['episode_id'])
        continue

    ## If the episode has a bad URL, skip it
    if row['episode_audio_link'] in bad_urls:
        print("Bad URL:", row['episode_id'])
        continue

    ## AssemblyAPI endpoint 
    endpoint = "https://api.assemblyai.com/v2/transcript"
    audio_url = row['episode_audio_link']
    json_request = {
        "audio_url": audio_url,
        "auto_chapters": True
    }
    
    ## Create headers
    headers = {
        "authorization": "125ffb9a861340b0a636c646f9e6d6a1",
        "content-type": "application/json"
    }   

    ## Send request
    response = requests.post(endpoint, json=json_request, headers=headers)
    response = response.json()
    polling_endpoint = endpoint + "/" + response['id']
    
    ## Poll for completion
    while True:
        response = requests.get(polling_endpoint, headers=headers)
        response_json = response.json()
        if response_json["status"] == 'completed':
            break
        time.sleep(5)
    
    ## Save the response
    with open('data/transcriptions/' + str(row["episode_id"]) + '.json', 'w') as f:
        f.write(response.text)

