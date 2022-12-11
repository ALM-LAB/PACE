# 🎧 PACE: Podcast AI for Chapters and Episodes

<p align="center">
  <img src="readme_images/pace_horizontal_orange.png" alt="logo" width="300">
</p>

**DEMO**: Try it out for limited time on our [demo page](http://130.192.163.139:9000/).

## 📝 Table of Contents

- [🎯 Our IDEA](#-our-idea)
- [🔎 How does it work?](#-how-does-it-work)
- [📺 Demo](#-demo)
- [⏳ Pipeline](#-pipeline)
- [🙏🏻 Acknowledgements](#-acknowledgements)
- [🤌🏻 About the project](#-about-the-project)

---

## 🎯 Our IDEA
How many times have you been listening to a podcast and you wanted to go back to a specific part, but you don't remember the exact time? We have all been there. Now we got you covered!

We present **PACE, Podcast AI for Chapters and Episodes**, which allows you to search for podcasts at your own *pace*.  
PACE is a ***semantic search engine*** that helps you find the information you need, in a fast and easy way.

To get more superpowers and let the magic begin, switch the checkbox on. PACE will use the power of AI to search inside the podcasts and give you back the ***exact*** part you're looking for. 

In addition to providing fast and easy access to information within podcasts, PACE also uses advanced ***text-to-image generative models*** to automatically create chapter covers for each podcast episode. This makes it easy for listeners to quickly identify and navigate to the specific information they are looking for within an episode. 

With PACE, accessing the information you need within podcasts has never been easier.  
Get ready to experience the ***future of podcasting***. Everything you need, just a click away!

--- 

## 🔎 How does it work?
Podcasts usually are long-form audio content. They could contain many interesting topics, but you may be interested in only one or some of them.  

***PACE*** got you covered!

- 🔈 *Speech Processing*: generate chapters from audio tracks
- 📃 *NLP*: search for episodes or chapters using natural language
- 🎨 *Computer Vision*: generate artwork for chapters using text-to-image models
- 💻 *Web*: Flask + Elasticsearch to build a web app

---

## 📺 Demo & Slides
[![Watch the video](readme_images/video.png)](https://youtu.be/1Z7Z8Z8Z8Z8)  

Find the slides of our project [here](readme_images/PACE_Slides.pptx).

---

## ⏳ Pipeline
This is the pipeline of our project. 

We ingest podcast rss feeds, and we enrich the dataframe with episodes and related metadata. We then filter episodes' description using [BERT Podcast Classifier](https://huggingface.co/morenolq/spotify-podcast-advertising-classification).

We encode episodes' description using [sentence BERT](https://sbert.net/docs/pretrained_models.html), and we index them in [Elasticsearch](https://www.elastic.co/).

We then select a bunch of podcasts for intra-podcast search, and we use [AssemblyAI](https://www.assemblyai.com/) to transcribe podcasts and retrieve chapters inside episodes. We index episodes' chapters in elasticsearch, using [cohere](www.cohere.ai) to embed the chapters.

We finally leverage [stable diffusion models](https://huggingface.co/CompVis/stable-diffusion-v1-4) to create an image/gif for each of the generated chapter.

---

**🕒 PHASE 1**

1. [x] Ingest podcasts rss 
2. [x] Enrich dataframe with episodes and related metadata 
3. [x] Filter episodes' description using [BERT](https://huggingface.co/morenolq/spotify-podcast-advertising-classification) 
4. [x] Encode episodes' description using [sentence BERT](https://sbert.net/docs/pretrained_models.html) 
5. [x] Index episodes in elasticsearch 
6. [x] **TEST: Query elasticsearch using [sentence BERT](https://sbert.net/docs/pretrained_models.html)** 

**END OF PHASE 1**

---

**🕕 PHASE 2**

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
    - [x] Implement intra-podcast search
    
**END OF PHASE 2**

---

**🕘 PHASE 3**

11. [x] Generative models (generate gifs for chapters)
12. [x] Implement storage mechanism for images/gifs 
13. [x] Implement image/gif retrieval in web app
14. [x] **TEST: Test the overall correct behavior of the web app, in all its parts**

**END OF PHASE 3**

 ---

**🕛 PHASE 4**

15. [x] Slides & Demo 
16. [ ] Add a "search by voice" button to the web app -- Future Work
17. [ ] Add "Fake News" detection to the web app - Future Work


**END OF PHASE 4**

---

## 🙏🏻 Acknowledgements

- [AssemblyAI](https://www.assemblyai.com/) for the outstanding experience (and the free credits)
- [Cohere](www.cohere.ai) for the amazing API
- 🎬 [plyr.io](https://github.com/sampotts/plyr) for the media player design
- 🤗 [Huggingface](https://huggingface.co/) for the amazing models
- ☕️ ☕️ 🧃 for the energy

---

## 🤌🏻 About the project 
PACE is a project created by [Alkis Koudounas](https://koudounasalkis.github.io), [Lorenzo Vaiani](https://twitter.com/VaianiLorenzo), and [Moreno La Quatra](https://www.mlaquatra.me). It is part of the ***AssemblyAI 50K Hackathon - Winter 2022***.

<p align="center">
  <img src="readme_images/ALM.png" alt="logo" width="300"/>
</p>