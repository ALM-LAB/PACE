from episodes_encoding import episodes_encoding
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm import tqdm

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

def elasticsearch_index_episodes(dict_episodes, episode_embedding_dict, dense_dim):

    ## Create mapping
    index_properties = {}
    index_properties['settings'] = { "number_of_shards": 2, 
                                     "number_of_replicas": 1 }
    index_properties['mappings'] = { "dynamic": "true", 
                                     "_source": {"enabled": "true"}, 
                                     "properties": {} }

    for t in ['episode_title', 'episode_description', 'podcast_creator', 'podcast_name']: 
        index_properties['mappings']['properties'][t] = { "type": "text" }
    for t in ['episode_pub_date', 'episode_id', 'episode_audio_link', 'episode_artwork_link']: 
        index_properties['mappings']['properties'][t] = { "type": "text", "index" : "false" }
    for t in ['episode_duration']: 
        index_properties['mappings']['properties'][t] = { "type": "float"}
    for t in ["episode_embedding"]: 
        index_properties['mappings']['properties'][t] = { "type": "dense_vector", 
                                                          "dims": dense_dim }
    
    es = Elasticsearch()
    es.indices.delete(index="podmagic-episodes", ignore=[404])
    es.indices.create(index="podmagic-episodes", body=index_properties)
    
    for _, v in tqdm(dict_episodes.items()): 
        v["episode_embedding"] = episode_embedding_dict[v["episode_id"]]
        res = es.index(index="podmagic-episodes", id=v["episode_id"], body=v)
        print(res['result'])

    es.indices.refresh(index="podmagic-episodes")
