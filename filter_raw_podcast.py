import pandas as pd


if __name__ == "__main__":

    ## Read data 
    df = pd.read_csv('data/df_popular_podcasts.csv')

    ## Get unique Main Genres
    genres = df['Primary Genre'].unique()

    ## Get count of podcasts for each genre and print it, ordered by count
    genre_counts = {}
    for genre in genres:
        genre_counts[genre] = len(df[df['Primary Genre'] == genre])

    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=False):
        if "news" in genre.lower():
            print(f"{genre}: {count}") 

    print(f"Unique genres: {len(genres)}")

    ## Leave only news podcasts
    df = df[df['Primary Genre'].str.contains("News", na=False)]

    ## Drop possible duplicates
    df = df.drop_duplicates(subset=['Feed URL'])

    ## Count number of remaining news podcasts
    print(f"Number of news podcasts: {len(df)}")

    ## Save filtered dataframe to a new csv
    df.to_csv('data/news_podcast.csv', index=False)




