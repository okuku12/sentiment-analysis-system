import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

# Define the search query and tweet limit
query = "mental health OR depression OR anxiety lang:en"
limit = 1000

tweets = []

print("🔍 Starting tweet collection...")

# Collect tweets
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
    if i % 100 == 0 and i != 0:
        print(f"✅ Collected {i} tweets...")

# Create DataFrame
df = pd.DataFrame(tweets, columns=['date', 'username', 'content', 'likes', 'retweets'])

# Add timestamp to filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"data/mental_health_tweets_{timestamp}.csv"
df.to_csv(filename, index=False)

print(f"\n📁 Saved {limit} tweets to {filename}")
print("📄 Sample tweet:")
print(df.head(1).to_string(index=False))
