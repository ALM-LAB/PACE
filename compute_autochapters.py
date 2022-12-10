import pandas as pd
import requests
import time
import os
from tqdm import tqdm


# Read the data
df = pd.read_csv('data/news_episodes.csv')
# select episodes based on podcast_name == "The Daily Good" or podcast_name == "The Daily Show"
df = df[(df['podcast_name'] == 'The Daily Good') | (df['podcast_name'] == 'Daily News Brief')]
# drop columns
drop_cols = ['episode_description', 'episode_pub_date', 'episode_artwork_link', 'podcast_creator', 'podcast_main_genre']
df = df.drop(drop_cols, axis=1)
# cast episode_duration to int
df['episode_duration'] = df['episode_duration'].astype(int)
# sort by episode_duration
df = df.sort_values(by='episode_duration', ascending=True)

print("Total episodes:", len(df))
print("Total hours:", df['episode_duration'].sum()/3600) 

already_computed_episodes = os.listdir('data/transcriptions')

for index, row in tqdm(df.iterrows(), total=len(df)):

    if str(row['episode_id']) + '.json' in already_computed_episodes:
        print("Already computed:", row['episode_id'])
        continue

    endpoint = "https://api.assemblyai.com/v2/transcript"
    audio_url = row['episode_audio_link']
    json_request = {
        "audio_url": audio_url,
        "auto_chapters": True
    }
    # create the headers
    headers = {
        "authorization": "<API KEY>",
        "content-type": "application/json"
    }   

    response = requests.post(endpoint, json=json_request, headers=headers)
    response = response.json()
    polling_endpoint = endpoint + "/" + response['id']
    while True:
        response = requests.get(polling_endpoint, headers=headers)
        response_json = response.json()
        if response_json["status"] == 'completed':
            break
        time.sleep(5)
    
    with open('data/transcriptions/' + str(row["episode_id"]) + '.json', 'w') as f:
        f.write(response.text)

