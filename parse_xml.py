import xmltodict

f_name = "example_lex.xml"
with open(f_name, "r") as f:
    xml_string = f.read()

xml_dict = xmltodict.parse(xml_string)

podcast_title = xml_dict["rss"]["channel"]["title"]
podcast_description = xml_dict["rss"]["channel"]["description"]
podcast_link = xml_dict["rss"]["channel"]["link"]

print(f"Title: {podcast_title}")
print(f"Description: {podcast_description}")
print(f"Link: {podcast_link}")

episodes = xml_dict["rss"]["channel"]["item"]
episodes_links = [episode["link"] for episode in episodes]
episode_mp3_links = [episode["enclosure"]["@url"] for episode in episodes]
eposides_descriptions = [episode["description"] for episode in episodes]
print (f"Found {len(episodes)} episodes")
for episode in episodes[:5]:
    print (f"Title: {episode['title']}")
    print (f"Link: {episode['link']}")
    print (f"Description: {episode['description']}")
    print (f"MP3: {episode['enclosure']['@url']}")

print (xml_dict["rss"]["channel"].keys())


'''
- rss
    - channel
'''