import snscrape.modules.twitter as sntwitter
import pandas as pd

# Define the search query and tweet limit
query = "mental health OR depression OR anxiety lang:en"
limit = 1000

tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    tweets.append([
        tweet.date,
        tweet.user.username,
        tweet.content,
        tweet.likeCount,
        tweet.retweetCount
    ])

# Create DataFrame and save to CSV
df = pd.DataFrame(tweets, columns=['date', 'username', 'content', 'likes', 'retweets'])
df.to_csv("mental_health_tweets.csv", index=False)

print("✅ Collected and saved 1000 tweets.")