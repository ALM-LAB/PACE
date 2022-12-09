from episodes_encoding import episodes_encoding
import pandas as pd

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


def elasticsearch_index_episodes(dict_episodes, dense_dim):

    ## Create mapping
    index_properties = {}
    index_properties['settings'] = { "number_of_shards": 2, 
                                     "number_of_replicas": 1 }
    index_properties['mappings'] = { "dynamic": "true", 
                                     "_source": {"enabled": "true"}, 
                                     "properties": {} }

    for t in ['episode_title', 'episode_description', 'episode_pub_date', 'podcast_creator', 'podcast_name']: 
        index_properties['mappings']['properties'][t] = { "type": "text" }
    for t in ['episode_duration']: 
        index_properties['mappings']['properties'][t] = { "type": "float" }
    for d in ["episode_embedding"]: 
        index_properties['mappings']['properties'][d] = { "type": "dense_vector", 
                                                          "dims": dense_dim }

    es = Elasticsearch()
    es.indices.delete(index="wiki-semantic-search", ignore=[404])
    es.indices.create(index="podmagic", body=index_properties)

    from tqdm import tqdm
    for k, v in tqdm(dict_episodes.items()): 
        temp_dict = {
            "episode_title"         : v["episode_title"],
            "episode_description"   : v["episode_description"],
            "episode_pub_date"      : v["episode_pub_date"],
            "podcast_creator"       : v["podcast_creator"],
            "podcast_name"          : v["podcast_name"],
            "episode_duration"      : v["episode_duration"],
            "episode_embedding"     : v["episode_embedding"],
        }

        res = es.index(index="wiki-semantic-search", id=v["ID"], body=temp_dict)

    search_term = "The capital of Italy"
    search_vector = model.encode(search_term)
    old_script_score = "(doc['pagerank_score'].value * 250) + _score"
    script_computing_score = "cosineSimilarity(params.q_vector, doc['embedding_bert']) + 1.0"
    template_query: dict = {
        "query": {
            "function_score": {
                "query": {
                    "match": { "full_text" : search_term }
                },
                "script_score": {
                    "script": {
                        "params": {"q_vector" : search_vector},
                        "source": script_computing_score
                    }
                }
            }
        }
    }

    res = es.search(index="wiki-semantic-search", body=template_query)
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print (hit["_score"], " - ", hit["_source"]["ID"])


text_1 = "How big is London"
text_2 = "London has 9,787,426 inhabitants at the 2011 census"
text_3 = "London is known for its finacial district"
list_text = [text_1, text_2, text_3]
sentence_encodings = episodes_encoding(list_text)

df_episodes = pd.read_csv("data/episodes.csv")
for index in df_episodes.index:
    df_episodes.loc[index,"episode_embedding"] = sentence_encodings[i].tolist()

dense_dim = len(sentence_encodings[0])
elasticsearch_index_episodes(df_episodes, dense_dim)
