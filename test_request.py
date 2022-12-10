from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)
encoder_model.to(device)

query_string = "How to get a job in tech"

es = Elasticsearch()
# match the string "Russia war" in the "title" or "description" fields
query = {
    "query": {
        "multi_match": {
            "query": query_string,
            "fields": ["episode_title", "episode_description"]
        }
    }
}

query_vector = encoder_model.encode(query_string)

# rewrite the query with a custom score that compute the cosine similarity using the "episode_embedding" field and the query vector
# use a mix of the cosine similarity and the original score to get a better result
query = {
    "query": {
        "script_score": {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": ["episode_title", "episode_description"]
                }
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'episode_embedding') + _score",
                "params": {"query_vector": query_vector}
            }
        }
    }
}





res = es.search(index="podmagic-episodes", body=query)

print("Got %d Hits:" % res['hits']['total']['value'])

for hit in res['hits']['hits']:
    # print score, id, and title
    print(hit["_score"], hit["_id"], hit["_source"]["episode_title"])