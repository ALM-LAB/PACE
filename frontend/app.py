from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import torch
import cohere
import numpy as np
from datetime import datetime, date, timedelta
from flask import url_for, redirect, make_response, jsonify
import random


device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
encoder_model = SentenceTransformer(model_name)
encoder_model.to(device)

static_folder = 'static'


app = Flask(__name__, static_folder=static_folder)
es = Elasticsearch('127.0.0.1', port=9200)
cohere_api_key = "c8ES1KWN9nd8uObqxiBvBWEQ450asuAkoF61EYCg"
co = cohere.Client(cohere_api_key)

COHERE = True

@app.route('/')
def home():
    return render_template('search.html')

@app.template_filter('ctime')
# convert milliseconds to MM:SS
def timectime(s):
    s = datetime.fromtimestamp(s/1000).strftime('%M:%S')
    return f"{s}"

@app.template_filter('random_artwork')
def random_artwork(s):
    # get a random number between 0 and 2 without a seed
    #n = random.randint(0, 2)
    n = 1
    return f"{n}.png"

@app.template_filter('uniform_duration')
def uniform_duration(duration):
    try:
        if isinstance(duration, float) or (":" not in duration and '"' not in duration and "'" not in duration):
                value =  int(duration)
        else:
            parts = duration.split(":")
            if len(parts) == 1:
                parts = parts[0].split("'")
                if len(parts) == 1:
                    value =  int(parts[0])
                elif len(parts) == 2:
                    if parts[1] == '':
                        parts[1] = '0"'
                    value =  int(parts[0])*60 + int(parts[1][:-1])
            elif len(parts) == 2:
                minutes, seconds = parts
                value =  int(minutes)*60 + int(seconds)
            elif len(parts) == 3:
                hours, minutes, seconds = parts
                value =  int(hours)*3600 + int(minutes)*60 + int(seconds)
    except Exception as e:
        print(e)
        value =  0

    return str(int(value/60)) + " min"

@app.template_filter('truncate_if_longer_than')
def truncate_if_longer_than(s, n=25):
    # truncate string if longer than n words
    s = s.split(" ")
    if len(s) > n:
        s = s[:n]
        s.append("...")
        s = " ".join(s)
    else:
        s = " ".join(s)
    return s


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():

    try:
        is_semantic = True
        search_term = request.form["input"]
        is_magic = request.form.get("magic")
        print (f"Magic search: {is_magic}")
        is_magic = True if is_magic == "on" else False
        print (f"Magic search: {is_magic}")
    except Exception as e:
        is_semantic = True # Always True for now
        search_term = request.args.get('input')
        is_magic = request.args.get('magic')
        is_magic = True if is_magic == "on" else False
        search_term = search_term.replace("+", " ")

    if is_semantic:

        if is_magic:
            fields = ["chapter_gist", "chapter_summary"]
            dense_field = "chapter_embedding"
            if COHERE:
                query_vector = co.embed(texts=[search_term], model="small").embeddings[0]
                query_vector = np.array(query_vector)
            else:
                query_vector = encoder_model.encode(search_term)
                
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
                        "source": f"cosineSimilarity(params.query_vector, '{dense_field}') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
        }

        print (f"Searching for {search_term} in {fields} using {dense_field} with vector {query_vector.shape}") 
        

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
        try:
            res = es.search(
                index="podmagic-chapters", 
                size=20, 
                body=query
            )
        except Exception as e:
            print (e)
    else:
        res = es.search(
            index="podmagic-episodes", 
            size=20, 
            body=query
        )

    # rerank results boosting results that are more recent
    scores_before = [hit['_score'] for hit in res['hits']['hits']]
    scores_after = []
    for i, hit in enumerate(res['hits']['hits']):
        pubdate = hit['_source']['episode_pub_date'][:25]
        if pubdate[-1] == " ": pubdate = pubdate[0:5] + "0" + pubdate[5:-1]
        time_delta = datetime.now() - datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S")
        # convert time_delta to float number of days
        time_delta = time_delta.days
        # compute a score between 0 and 1 - it spans over 10 years
        time_delta = 1.0 - (time_delta / 3650.0)
        res['hits']['hits'][i]['_score'] = res['hits']['hits'][i]['_score'] + 0.1 * time_delta
        scores_after.append(res['hits']['hits'][i]['_score'])
    
    # print aligned list of scores before and after
    for i in range(len(scores_before)):
        print (f"{scores_before[i]} -> {scores_after[i]}")

    # reorder results by score
    res['hits']['hits'] = sorted(res['hits']['hits'], key=lambda x: x['_score'], reverse=True)
    return render_template('results.html', res=res, input=search_term, is_magic=is_magic)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=9000, debug=True)