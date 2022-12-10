from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import torch
import cohere

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)
encoder_model.to(device)

static_folder = 'static'


app = Flask(__name__, static_folder=static_folder)
es = Elasticsearch('127.0.0.1', port=9200)
cohere_api_key = "c8ES1KWN9nd8uObqxiBvBWEQ450asuAkoF61EYCg"
co = cohere.Client(cohere_api_key)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    is_semantic = True

    is_magic = request.form.get("magic")
    print (f"Magic search: {is_magic}")
    is_magic = True if is_magic == "on" else False
    print (f"Magic search: {is_magic}")
    

    if is_semantic:

        if is_magic:
            fields = ["chapter_gist", "chapter_summary"]
            dense_field = "chapter_embedding"
            query_vector = co.embed(texts=[search_term], model="small").embeddings[0]
            print (len(query_vector))
        else:
            fields = ["episode_title", "episode_description_clean"]
            dense_field = "episode_embedding"
            query_vector = encoder_model.encode(search_term)

        query = {
            "query": {
                "script_score": {
                    "query": {
                        "multi_match": {
                            "query": search_term,
                            "fields": fields
                        }
                    },
                    "script": {
                        "source": f"cosineSimilarity(params.query_vector, '{dense_field}') + 1",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
        }

    else:
        query = {
            "query": {
                "multi_match": {
                    "query": search_term,
                    "fields": ["episode_title", "episode_description_clean"]
                }
            },
        }

    if is_magic:
        res = es.search(
            index="podmagic-chapters", 
            size=20, 
            body=query
        )
    else:
        res = es.search(
            index="podmagic-episodes", 
            size=20, 
            body=query
        )
    return render_template('results.html', res=res, input=search_term, is_magic=is_magic)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=9000, debug=True)