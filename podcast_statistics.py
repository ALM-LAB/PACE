import pandas as pd
from tqdm import tqdm
import math

def uniform_duration(duration):
    #try:
    try:
        if isinstance(duration, float) or (":" not in duration and '"' not in duration and "'" not in duration):
                return int(duration)
        else:
            parts = duration.split(":")
            if len(parts) == 1:
                parts = parts[0].split("'")
                if len(parts) == 1:
                    return int(parts[0])
                elif len(parts) == 2:
                    if parts[1] == '':
                        parts[1] = '0"'
                    return int(parts[0])*60 + int(parts[1][:-1])
            elif len(parts) == 2:
                minutes, seconds = parts
                return int(minutes)*60 + int(seconds)
            elif len(parts) == 3:
                hours, minutes, seconds = parts
                return int(hours)*3600 + int(minutes)*60 + int(seconds)
    except Exception as e:
        print(e)
        return 0

#read the data
df = pd.read_csv('data/news_episodes.csv')
print(df.columns)

ud = []
for i, d in enumerate(tqdm(list(df.episode_duration))):
    ud.append(uniform_duration(d))
df["uniform_duration"] = ud

# sum uniform duration group by podcast_name
print("grouping...")
groups = df.groupby("podcast_name")
for i, tuple in enumerate(groups):
    name, group = tuple
    print(i, " - ", name, " - ", group.uniform_duration.sum()/3600)