import pandas as pd
import numpy as np
import os
import xmltodict
import urllib
from bs4 import BeautifulSoup
from ftfy import fix_text
from tqdm import tqdm

def clean_text_from_html(text):
    """Remove html tags from text"""
    return BeautifulSoup(text, "lxml").text

def parse_podcast_rss(xml_link, main_genre=None):
    """Parse podcast rss links and return a list of dictionaries, one for each podcast episode"""
    try:
        response = urllib.request.urlopen(xml_link)
        data = response.read()
        doc = xmltodict.parse(data)
        list_of_episodes = []
    except Exception as e:
        #print (e)
        #print ("Invalid link: ", xml_link)
        return None

    invalid_episodes = 0

    for i, item in enumerate(doc["rss"]["channel"]["item"]):
        try:
            # get episode title
            title = item["title"]
            # get episode description
            description = item["description"]
            # clean episode description from html tags
            description = clean_text_from_html(description)
            # get episode publish date
            pub_date = item["pubDate"]
            # get episode duration
            duration = item["itunes:duration"]
            # get episode episode link - mp3
            link = item["enclosure"]["@url"]
            try:
                # get episode artwork
                artwork = item["itunes:image"]["@href"]
            except Exception as e:
                # get episode artwork from podcast
                try:
                    artwork = doc["rss"]["channel"]["itunes:image"]["@href"]
                except Exception as e:
                    artwork = ""
            # get episode id = podcast name + _ + i
            episode_id = doc["rss"]["channel"]["title"] + "_" + str(i)
            # get podcast creator from podcast
            creator = doc["rss"]["channel"]["itunes:author"]
            # get podcast name from podcast
            podcast_name = doc["rss"]["channel"]["title"]
            episode_dict = {
                "episode_title": fix_text(title),
                "episode_description": fix_text(description),
                "episode_pub_date": pub_date,
                "episode_duration": duration,
                "episode_audio_link": link,
                "episode_artwork_link": artwork,
                "episode_id": episode_id,
                "podcast_creator": fix_text(creator),
                "podcast_name": fix_text(podcast_name),
                "podcast_main_genre": main_genre,
            }
            list_of_episodes.append(episode_dict)
        except Exception as e:
            invalid_episodes += 1
            continue
    
    if invalid_episodes > 0:
        print ("Invalid episodes: ", invalid_episodes)

    return list_of_episodes



def enrich_df(df=None):
    # remove podcasts without rss links
    df = df[df["Feed URL"].notnull()]
    # get rss links
    rss_links = df["Feed URL"].tolist()
    primary_genres = df["Primary Genre"].tolist()
    complete_list = []
    for i, rss_link in enumerate(tqdm(rss_links)):
        list_episodes = parse_podcast_rss(rss_link, primary_genres[i])
        if list_episodes is not None:
            complete_list.extend(list_episodes)
    # create dataframe from list of dictionaries
    df_enriched = pd.DataFrame(complete_list)
    return df_enriched

df = pd.read_csv("data/news_podcast.csv")
enriched_df = enrich_df(df)
# save enriched dataframe to csv
enriched_df.to_csv("data/news_episodes.csv", index=False)