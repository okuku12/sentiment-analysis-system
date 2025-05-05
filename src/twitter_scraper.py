import tweepy
import pandas as pd

# Replace with your own bearer token from Twitter Developer Portal
bearer_token = "YOUR_BEARER_TOKENAAAAAAAAAAAAAAAAAAAAAIgn1AEAAAAAQ5cmVfDERIRGfwqNX6GThU0U1LE%3D0Rqzkb1jSDYRmXWOTm30uoUKvMArkAjmaemjWRgkFk5vB1qANI"

client = tweepy.Client(bearer_token=bearer_token)

def get_tweets(query, max_results=100):
    tweets = client.search_recent_tweets(query=query, tweet_fields=["created_at", "lang"], max_results=max_results)
    data = [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets.data if tweet.lang == "en"]
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = get_tweets("mental health", max_results=100)
    df.to_csv("data/tweets.csv", index=False)
    print(df.head())
