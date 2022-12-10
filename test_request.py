from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import torch
import sys

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)
encoder_model.to(device)

query_string = sys.argv[1]
semantic = sys.argv[2] == "semantic"

es = Elasticsearch()
query_vector = encoder_model.encode(query_string)

# add an highligher to the title and description fields

if semantic:
    query = {
        "query": {
            "script_score": {
                "query": {
                    "multi_match": {
                        "query": query_string,
                        "fields": ["episode_title", "episode_description_clean"]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'episode_embedding') + 1",
                    "params": {"query_vector": query_vector}
                }
            }
        },
        "highlight": {
            "fields": {
                "episode_title": {},
                "episode_description_clean": {}
            }
        }
    }
else:
    query = {
        "query": {
            "multi_match": {
                "query": query_string,
                "fields": ["episode_title", "episode_description_clean"]
            }
        },
        "highlight": {
            "fields": {
                "episode_title": {},
                "episode_description_clean": {}
            }
        }
    }




res = es.search(index="podmagic-episodes", body=query)

print("Got %d Hits:" % res['hits']['total']['value'])

# print the score, id, title and link of the first 5 hits
for hit in res['hits']['hits'][:5]:
    # print score, id, and title and link and highlights
    print(f"Title: {hit['_source']['episode_title']} - score: {hit['_score']}")
    print(f"Description: {hit['_source']['episode_description_clean']}")
    try:
        print(f"Highlights: {hit['highlight']}")
    except:
        print ("No highlights")
    print("------------------------------------------------------------------")