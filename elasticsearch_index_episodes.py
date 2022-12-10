from episodes_encoding import episodes_encoding
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm import tqdm
from copy import deepcopy

"""
Example of episode_dict:

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

## Function for indexing episodes in Elasticsearch
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
    
    ## Create Elasticsearch index
    es = Elasticsearch()
    es.indices.delete(index="podmagic-episodes", ignore=[404])
    es.indices.create(index="podmagic-episodes", body=index_properties)
    
    ## Index episodes
    for row in tqdm(df_episodes.iterrows(), total=df_episodes.shape[0]):
        try:
            ## Convert the entire row to a dictionary
            v = row[1].to_dict()
            v["episode_embedding"] = episode_embedding_dict[v["episode_id"]]
            v["episode_description_clean"] = description_clean_dict[v["episode_id"]]
            res = es.index(index="podmagic-episodes", id=v["episode_id"], body=v)
        except Exception as e:
            print(e)
            print("Error with episode_id: ", v["episode_id"])

    ## Refresh index
    es.indices.refresh(index="podmagic-episodes")


"""
Example of chapter_df:

    df["episode_id"] = episode_ids
    df["chapter_id"] = chapter_ids
    df["chapter_gist"] = chapter_gists
    df["chapter_summary"] = chapter_summaries
    df["audio_url"] = audio_urls
    df["start"] = starts
    df["end"] = ends
    df["episode_title"] = episode_titles
    df["episode_pub_date"] = episode_pub_dates
    df["podcast_name"] = podcast_names

"""

## Function for indexing chapters in Elasticsearch
def elasticsearch_index_chapters(df_chapters, chapter_embedding_dict, dense_dim):

    ## Create mapping
    index_properties = {}
    index_properties['settings'] = { "number_of_shards": 2, 
                                     "number_of_replicas": 1 }
    index_properties['mappings'] = { "dynamic": "true", 
                                     "_source": {"enabled": "true"}, 
                                     "properties": {} }

    for t in ['chapter_gist', 'chapter_summary']: 
        index_properties['mappings']['properties'][t] = { "type": "text" }
    for t in ['episode_id', 'chapter_id', 'audio_url', 'episode_title', 'episode_pub_date', 'podcast_name']: 
        index_properties['mappings']['properties'][t] = { "type": "text", "index" : "false" }
    for t in ['start', 'end']: 
        index_properties['mappings']['properties'][t] = { "type": "integer" }
    for t in ["chapter_embedding"]: 
        index_properties['mappings']['properties'][t] = { "type": "dense_vector", 
                                                          "dims": dense_dim }
    
    ## Create Elasticsearch index
    es = Elasticsearch()
    es.indices.delete(index="podmagic-chapters", ignore=[404])
    es.indices.create(index="podmagic-chapters", body=index_properties)
    
    ## Index chapters
    for row in tqdm(df_chapters.iterrows(), total=df_chapters.shape[0]):
        try:
            ## Convert the entire row to a dictionary
            v = row[1].to_dict()
            v["chapter_embedding"] = chapter_embedding_dict[v["chapter_id"]]
            res = es.index(index="podmagic-chapters", id=v["chapter_id"], body=v)
        except Exception as e:
            print(e)
            print("Error with chapter_id: ", v["chapter_id"])

    ## Refresh index
    es.indices.refresh(index="podmagic-chapters")
