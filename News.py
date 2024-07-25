import streamlit as st
import nltk
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Function to fetch news table for a given ticker
def fetch_news_table(ticker):
    finviz_url = 'https://finviz.com/quote.ashx?t='
    url = finviz_url + ticker
    try:
        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)
        html = BeautifulSoup(response, features='html.parser')
        return html.find(id='news-table')
    except Exception as e:
        st.error(f"Failed to fetch news table for the selected ticker: {e}")
        return None

# Function to filter DataFrame for the past week and calculate average sentiment scores
def sentiment_analysis_weekly(df):
    df['date'] = pd.to_datetime(df['date'], format='%b-%d-%y')
    last_week = datetime.now() - timedelta(days=7)
    df_last_week = df[df['date'] >= last_week]
    daily_sentiment = df_last_week.groupby(df_last_week['date'].dt.date)['Sent_Score'].mean().reset_index()
    daily_sentiment.columns = ['Date', 'Average Sentiment Score']
    return daily_sentiment

# Function to update DataFrame based on selected ticker
def update_df(ticker):
    news_table = fetch_news_table(ticker)
    if news_table:
        parsed_data = []
        for row in news_table.findAll('tr'):
            if row.a and row.td:
                title = row.a.text
                url = row.a.get('href')
                date_data = [elem.strip() for elem in row.td.text.split(' ') if elem.strip()]
                today_date = datetime.now().strftime('%b-%d-%y')
                if len(date_data) == 1:
                    time = date_data[0]
                    date = today_date
                else:
                    date = date_data[0]
                    time = date_data[1]
                date = today_date if date.lower() == 'today' else date
                parsed_data.append([ticker, date, time, title, url])
        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title', 'url'])
        vader = SentimentIntensityAnalyzer()
        df['Sent_Score'] = df['title'].apply(lambda title: vader.polarity_scores(title)['compound'])
        return df
    else:
        return None

# Main function for the News page
def main():
    st.header("Financial News")
    ticker = st.selectbox("Select Ticker", ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX', 'NIO', 'SIRI', 'GOLD'])
    df = update_df(ticker)
    if df is not None:
        st.write(df)
        daily_sentiment = sentiment_analysis_weekly(df)
        st.subheader("Average Sentiment Scores for the Past 7 Days")
        st.write(daily_sentiment)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_sentiment['Date'], y=daily_sentiment['Average Sentiment Score'],
                                  mode='lines+markers',
                                  line_shape='spline',
                                  name='Average Sentiment Score'))
        fig.update_layout(title=f'Average Sentiment Score for {ticker}',
                          xaxis_title='Date',
                          yaxis_title='Average Sentiment Score')
        st.plotly_chart(fig)
        st.subheader("News Article URLs")
        for index, row in df.iterrows():
            st.markdown(f"[{row['title']}]({row['url']})")
    else:
        st.error("Failed to fetch news table for the selected ticker.")

if __name__ == "__main__":
    main()
