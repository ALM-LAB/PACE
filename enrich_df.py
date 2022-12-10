import pandas as pd
import numpy as np
import os
import xmltodict
import urllib
from bs4 import BeautifulSoup
from ftfy import fix_text
from tqdm import tqdm


## Function to clean text from html tags
def clean_text_from_html(text):
    """Remove html tags from text"""
    return BeautifulSoup(text, "lxml").text


## Function to parse podcast rss links
def parse_podcast_rss(xml_link, main_genre=None):
    """Parse podcast rss links and return a list of dictionaries, one for each podcast episode"""
    try:
        response = urllib.request.urlopen(xml_link)
        data = response.read()
        doc = xmltodict.parse(data)
        list_of_episodes = []
    except Exception as e:
        # print (e)
        # print ("Invalid link: ", xml_link)
        return None

    invalid_episodes = 0

    for i, item in enumerate(doc["rss"]["channel"]["item"]):
        
        try:
            title = item["title"]                               # Get episode title
            description = item["description"]                   # Get episode description
            description = clean_text_from_html(description)     # Clean description from html tags
            pub_date = item["pubDate"]                          # Get episode publication date
            duration = item["itunes:duration"]                  # Get episode duration
            link = item["enclosure"]["@url"]                    # Get episode link [mp3]
            try:
                artwork = item["itunes:image"]["@href"]         # Get episode artwork
            except Exception as e:
                try:
                    artwork = doc["rss"]["channel"]["itunes:image"]["@href"] # Get episode artwork from podcast
                except Exception as e:
                    artwork = ""
            episode_id = doc["rss"]["channel"]["title"] + "_" + str(i)  # Get episode id = podcast name + _ + i
            creator = doc["rss"]["channel"]["itunes:author"]    # Get podcast creator from podcast
            podcast_name = doc["rss"]["channel"]["title"]       # Get podcast name from podcast
            
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


## Function to enrich the dataframe with podcast episodes
def enrich_df(df=None):
    
    # Remove podcasts without rss links
    df = df[df["Feed URL"].notnull()]
    
    # Get rss links
    rss_links = df["Feed URL"].tolist()
    primary_genres = df["Primary Genre"].tolist()
    
    # Parse rss links
    complete_list = []
    for i, rss_link in enumerate(tqdm(rss_links)):
        list_episodes = parse_podcast_rss(rss_link, primary_genres[i])
        if list_episodes is not None:
            complete_list.extend(list_episodes)
    
    # create dataframe from list of dictionaries
    df_enriched = pd.DataFrame(complete_list)

    return df_enriched


if __name__ == "__main__":

    ## Read the dataframe with podcast information
    df = pd.read_csv("data/news_podcast.csv")

    ## Enrich the dataframe with podcast episodes
    enriched_df = enrich_df(df)

    ## Save enriched dataframe to csv
    enriched_df.to_csv("data/news_episodes.csv", index=False)