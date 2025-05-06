# app.py
import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import emoji
import plotly.express as px
import os
import time

# --- Utility Functions ---
def scrape_tweets(query, limit):
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
    df = pd.DataFrame(tweets, columns=['date', 'username', 'content', 'likes', 'retweets'])
    return df

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.05:
        return 'Positive'
    elif polarity < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def extract_emojis(text):
    return ''.join(c for c in text if c in emoji.EMOJI_DATA)

# --- Streamlit UI ---
st.set_page_config(page_title="Mental Health Tweet Sentiment Analysis", layout="wide")
st.title("💬 Mental Health Tweet Sentiment Analyzer")

# Sidebar Inputs
st.sidebar.header("🔧 Options")
query = st.sidebar.text_input("Enter hashtag or keyword:", value="#mentalhealth")
limit = st.sidebar.slider("Number of tweets to fetch:", min_value=100, max_value=2000, step=100, value=500)
live_mode = st.sidebar.checkbox("🔄 Enable Live Updates", value=False)
time_interval = st.sidebar.slider("Live Update Interval (secs)", 10, 300, 60) if live_mode else None

# Main Button
df = pd.DataFrame()
run_query = st.sidebar.button("🚀 Run Analysis")

if run_query or live_mode:
    if live_mode:
        st.info("Live update mode enabled. Fetching tweets every {} seconds...".format(time_interval))
    while True:
        with st.spinner("Scraping tweets..."):
            df = scrape_tweets(query, limit)
            df['sentiment'] = df['content'].apply(analyze_sentiment)
            df['emojis'] = df['content'].apply(extract_emojis)
            os.makedirs("data", exist_ok=True)
            df.to_csv("data/mental_health_tweets.csv", index=False)

        st.success("✅ Tweets scraped and analyzed!")

        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts().reset_index()
        fig = px.pie(sentiment_counts, names='index', values='sentiment', title='Sentiment Breakdown')
        st.plotly_chart(fig)

        st.subheader("☁️ Word Cloud")
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            st.markdown(f"**{sentiment} Tweets**")
            sentiment_text = ' '.join(df[df['sentiment'] == sentiment]['content'])
            if sentiment_text:
                wordcloud = generate_wordcloud(sentiment_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)

        st.subheader("😀 Emoji Frequency")
        all_emojis = ''.join(df['emojis'].tolist())
        emoji_series = pd.Series(list(all_emojis)).value_counts().head(10)
        st.bar_chart(emoji_series)

        st.subheader("📥 Download Dataset")
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="mental_health_tweets.csv")

        st.subheader("🔍 Filter Tweets by Sentiment")
        selected_sentiment = st.selectbox("Select sentiment to view tweets:", ['All', 'Positive', 'Neutral', 'Negative'])
        filtered_df = df if selected_sentiment == 'All' else df[df['sentiment'] == selected_sentiment]
        st.dataframe(filtered_df[['date', 'username', 'content', 'likes', 'retweets', 'sentiment']])

        if not live_mode:
            break
        else:
            time.sleep(time_interval)
