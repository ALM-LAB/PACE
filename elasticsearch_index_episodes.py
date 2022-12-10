from episodes_encoding import episodes_encoding
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm import tqdm
from copy import deepcopy

"""
episode_dict = {
            "episode_title": title,
            "episode_description": description,
            "episode_pub_date": pub_date,
            "episode_duration": duration,
            "episode_audio_link": link,
            "episode_artwork_link": artwork,
            "episode_id": episode_id,
            "podcast_creator": creator,
            "podcast_name": podcast_name,
        }
"""

def elasticsearch_index_episodes(df_episodes, episode_embedding_dict, description_clean_dict, dense_dim):

    ## Create mapping
    index_properties = {}
    index_properties['settings'] = { "number_of_shards": 2, 
                                     "number_of_replicas": 1 }
    index_properties['mappings'] = { "dynamic": "true", 
                                     "_source": {"enabled": "true"}, 
                                     "properties": {} }

    for t in ['episode_title', 'episode_description', 'episode_description_clean', 'podcast_creator', 'podcast_name']: 
        index_properties['mappings']['properties'][t] = { "type": "text" }
    for t in ['episode_pub_date', 'episode_id', 'episode_audio_link', 'episode_artwork_link', 'episode_duration']: 
        index_properties['mappings']['properties'][t] = { "type": "text", "index" : "false" }
    for t in ["episode_embedding"]: 
        index_properties['mappings']['properties'][t] = { "type": "dense_vector", 
                                                          "dims": dense_dim }
    
    es = Elasticsearch()
    es.indices.delete(index="podmagic-episodes", ignore=[404])
    es.indices.create(index="podmagic-episodes", body=index_properties)
    
    for row in tqdm(df_episodes.iterrows(), total=df_episodes.shape[0]):
        try:
            # convert the entire row to a dictionary
            v = row[1].to_dict()
            v["episode_embedding"] = episode_embedding_dict[v["episode_id"]]
            v["episode_description_clean"] = description_clean_dict[v["episode_id"]]
            res = es.index(index="podmagic-episodes", id=v["episode_id"], body=v)
            #print(res['result'])
        except Exception as e:
            print(e)
            print("Error with episode_id: ", v["episode_id"])

    es.indices.refresh(index="podmagic-episodes")
