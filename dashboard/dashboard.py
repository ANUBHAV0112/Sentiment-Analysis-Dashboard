# dashboard/dashboard.py

import streamlit as st # type: ignore
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh # type: ignore
import plotly.express as px
from wordcloud import WordCloud # type: ignore
import matplotlib.pyplot as plt

API_URL = "http://localhost:5000/analyze"

# Page config and theme
st.set_page_config(page_title="Sentiment Dashboard", layout="wide", page_icon="📰")
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .css-1d391kg {
        background-color: #1f1f1f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Auto-refresh every 30 seconds
st_autorefresh(interval=30 * 1000, key="refresh")

st.title("📰 Real-Time Sentiment Dashboard")
st.markdown("Live sentiment analysis of top headlines.")

try:
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data)

    # Metrics summary
    total_headlines = len(df)
    positive_count = df['sentiment'].value_counts().get('positive', 0)
    negative_count = df['sentiment'].value_counts().get('negative', 0)
    neutral_count = df['sentiment'].value_counts().get('neutral', 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📰 Total Headlines", total_headlines)
    col2.metric("😊 Positive %", f"{(positive_count / total_headlines) * 100:.1f}%")
    col3.metric("😠 Negative %", f"{(negative_count / total_headlines) * 100:.1f}%")
    col4.metric("😐 Neutral %", f"{(neutral_count / total_headlines) * 100:.1f}%")

    # Sentiment filter
    sentiment_filter = st.selectbox("Filter by sentiment", ["All", "positive", "negative", "neutral"])
    if sentiment_filter != "All":
        df = df[df["sentiment"] == sentiment_filter]

    # Headlines table
    st.write("### Latest Headlines and Sentiment")
    st.dataframe(df[['text', 'sentiment', 'score']])

    # Sentiment distribution bar chart
    sentiment_counts = df['sentiment'].value_counts()
    st.write("### Sentiment Distribution")
    st.bar_chart(sentiment_counts)

    # Pie chart
    st.write("### Sentiment Proportions")
    fig_pie = px.pie(df, names='sentiment', title='Sentiment Proportions', hole=0.4)
    st.plotly_chart(fig_pie)

    # Word cloud
    st.write("### Word Cloud of Headlines")
    text = ' '.join(df['text'])
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error fetching data from API: {e}")
