# PodMAGIC

## ALM LAB
Audio, Language and Multimedia Lab


## Pipeline

**PHASE 1**
1. Ingest podcasts rss
2. Enrich dataframe with episodes and related metadata
3. Filter episodes' description using [BERT](https://huggingface.co/morenolq/spotify-podcast-advertising-classification) 
4. Encode episodes' description using [sentence BERT](https://sbert.net/docs/pretrained_models.html)
5. Index episodes in elasticsearch
6. **TEST**: Query elasticsearch using [sentence BERT](https://sbert.net/docs/pretrained_models.html)

**END OF PHASE 1**

**PHASE 2**

7. Select a bunch of podcasts for intra-podcast search (limited by AssemblyAI API)
8. Index episodes' chapters in elasticsearch:

    - Podcast name
    - Chapter description
    - Start & End time
    - Original episode (mp3 link)

9. **TEST**: Query elasticsearch using [sentence BERT](https://sbert.net/docs/pretrained_models.html)

**END OF PHASE 2**

**PHASE 3**

10. Generative models (generate gifs for chapters)
11. How to store these gifs? Static files? Need a way to index the images/gifs.

**END OF PHASE 3**
