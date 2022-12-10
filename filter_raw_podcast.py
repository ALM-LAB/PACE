import pandas as pd

df = pd.read_csv('data/df_popular_podcasts.csv')

# get unique Main Genres
genres = df['Primary Genre'].unique()

# get count of podcasts for each genre and print it ordered by count
genre_counts = {}
for genre in genres:
    genre_counts[genre] = len(df[df['Primary Genre'] == genre])

for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=False):
    if "news" in genre.lower():
        print(f"{genre}: {count}") 

print(f"Unique genres: {len(genres)}")

# leave only news podcasts
df = df[df['Primary Genre'].str.contains("News", na=False)]

# drop duplicates
df = df.drop_duplicates(subset=['Feed URL'])

# count number of podcasts
print(f"Number of news podcasts: {len(df)}")

# save filtered dataframe to csv
df.to_csv('data/news_podcast.csv', index=False)




