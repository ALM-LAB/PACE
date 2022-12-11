# PodMAGIC

A Project by ***ALM LAB (Audio, Language and Multimedia Lab)***.


## Pipeline
This is the pipeline of our project. 

We ingest podcast rss feeds, and we enrich the dataframe with episodes and related metadata. We then filter episodes' description using [BERT Podcast Classifier](https://huggingface.co/morenolq/spotify-podcast-advertising-classification).

We encode episodes' description using [sentence BERT](https://sbert.net/docs/pretrained_models.html), and we index them in [Elasticsearch](https://www.elastic.co/).

We then select a bunch of podcasts for intra-podcast search, and we use [AssemblyAI](https://www.assemblyai.com/) to transcribe podcasts and retrieve chapters inside episodes. We index episodes' chapters in elasticsearch, using [cohere](www.cohere.ai) to embed the chapters.

We finally leverage [stable diffusion models](https://huggingface.co/CompVis/stable-diffusion-v1-4) to create an image/gif for each of the generated chapter.



---

**PHASE 1**

1. [x] Ingest podcasts rss 
2. [x] Enrich dataframe with episodes and related metadata 
3. [x] Filter episodes' description using [BERT](https://huggingface.co/morenolq/spotify-podcast-advertising-classification) 
4. [x] Encode episodes' description using [sentence BERT](https://sbert.net/docs/pretrained_models.html) 
5. [x] Index episodes in elasticsearch 
6. [x] **TEST: Query elasticsearch using [sentence BERT](https://sbert.net/docs/pretrained_models.html)** 

**END OF PHASE 1**

---

**PHASE 2**

7. [x] Select a bunch of podcasts for intra-podcast search (limited by AssemblyAI API)
8. [x] Index episodes' chapters in elasticsearch 

    - Podcast name
    - Chapter description
    - Start & End time
    - Original episode (mp3 link)

9. [x] **TEST: Query elasticsearch using [cohere](www.cohere.ai)**

10. [x] Web app

    - [x] Implement flask-based web app
    - [x] Implement search bar
    - [x] Implement search results
    - [x] Implement player
    - [ ] Implement intra-podcast search
    
**END OF PHASE 2**

---

**PHASE 3**

11. [x] Generative models (generate gifs for chapters)
12. [x] Implement storage mechanism for images/gifs 
13. [x] Implement image/gif retrieval in web app
14. [ ] **TEST: Test the overall correct behavior of the web app, in all its parts**

**END OF PHASE 3**

 ---

**PHASE 4**

15. [ ] Add ASR (Whisper) to the pipeline, to allow for search directly by recording a query
16. [ ] Slides & Demo 

**END OF PHASE 4**

---
## Acknowledgements

- plyr.io https://github.com/sampotts/plyr
