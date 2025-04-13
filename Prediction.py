import streamlit as st
import yfinance as yf
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Permute, Reshape, Multiply, Flatten, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard, CSVLogger
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error
import plotly.graph_objects as go


# Function to fetch news table for a given ticker
def fetch_news_table(ticker):
    finviz_url = 'https://finviz.com/quote.ashx?t='
    url = finviz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, features='html.parser')
    return html.find(id='news-table')

# Streamlit app definition
def main():
    st.title('Stock Prediction')
    
    # Select stock ticker
    ticker = st.selectbox("Select Ticker", ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])
    
    # Fetch stock data
    stock_data = yf.download(ticker, start='2024-01-01', end='2025-02-13')
    
    if stock_data.empty:
        st.error("Failed to fetch data. Please try again later.")
        return
    
    st.write(f"{ticker} Stock Data")
    st.dataframe(stock_data)
    
    # Normalization
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Check if data is not empty
    if stock_data['Close'].empty:
        st.error("No data available for normalization.")
        return
    
    closing_prices = stock_data['Close'].values.reshape(-1, 1)
    stock_data_scaled = scaler.fit_transform(closing_prices)
    
    # Creating sequences
    X, y = [], []
    for i in range(30, len(stock_data_scaled)):
        X.append(stock_data_scaled[i-30:i, 0])
        y.append(stock_data_scaled[i, 0])
    
    # Train-test split
    train_size = int(len(X) * 0.8)
    test_size = len(X) - train_size
    
    X_train, X_test = np.array(X[:train_size]), np.array(X[train_size:])
    y_train, y_test = np.array(y[:train_size]), np.array(y[train_size:])
    
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    
    # Define the model
    inputs = Input(shape=(X_train.shape[1], 1))

    x = LSTM(units=50, return_sequences=True)(inputs)
    x = Dropout(0.2)(x)
    x = BatchNormalization()(x)

    x = LSTM(units=50, return_sequences=True)(x)
    x = Dropout(0.2)(x)
    x = BatchNormalization()(x)

    attention = tf.keras.layers.AdditiveAttention(name='attention_weight')
    x = Permute((2, 1))(x)
    x = Reshape((50, X_train.shape[1]))(x)
    attention_result = attention([x, x])
    x = Multiply()([x, attention_result])
    x = Permute((2, 1))(x)
    x = Flatten()(x)
    outputs = Dense(1)(x)  # Output layer directly after the Flatten layer

    model = Model(inputs=inputs, outputs=outputs)

    model.compile(optimizer='adam', loss='mean_squared_error')
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss')
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)
    tensorboard = TensorBoard(log_dir='./logs')
    csv_logger = CSVLogger('training_log.csv')
    callbacks_list = [early_stopping, model_checkpoint, reduce_lr, tensorboard, csv_logger]
    
    with st.spinner('Training the model...'):
        history = model.fit(X_train, y_train, epochs=100, batch_size=25, validation_split=0.2, callbacks=callbacks_list)

    st.success('Model trained successfully!')
    
    # Evaluate the model
    test_loss = model.evaluate(X_test, y_test)
    st.write(f"Test Loss: {test_loss}")
    
    # Making predictions
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    st.write(f"Mean Absolute Error: {mae}")
    
    # Predicting the next 2 days using the last 30 days of data
    if len(stock_data_scaled) < 30:
        st.warning("Insufficient data available for prediction.")
        return
        
    closing_prices = stock_data['Close'].values.reshape(-1, 1)
    scaled_data = scaler.fit_transform(closing_prices)

    predicted_prices = []
    current_batch = scaled_data[-30:].reshape(1, 30, 1)  # Adjusted to use the last 60 days

    for i in range(2):  # Change from 4 to 2
        next_prediction = model.predict(current_batch)
        next_prediction_reshaped = next_prediction.reshape(1, 1, 1)
        current_batch = np.append(current_batch[:, 1:, :], next_prediction_reshaped, axis=1)
        predicted_prices.append(scaler.inverse_transform(next_prediction)[0, 0])


    st.write(f"Predicted Stock Prices for the next 2 days: {predicted_prices}")

    # Visualization of predictions
    last_date = stock_data.index[-1]
    next_day = last_date + pd.Timedelta(days=1)
    prediction_dates = pd.date_range(start=next_day, periods=2)

    predictions_df = pd.DataFrame(index=prediction_dates, data=predicted_prices, columns=['Close'])

    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index[-30:], stock_data['Close'][-30:], linestyle='-', marker='o', color='blue', label='Actual Data')  # Adjusted to use the last 60 days
    plt.plot(prediction_dates, predicted_prices, linestyle='-', marker='o', color='red', label='Predicted Data')
    plt.title(f"{ticker} Stock Price: Last 30 Days and Next 2 Days Predicted")  # Adjusted title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)
    
    # Display candlestick chart with prediction markers
    st.subheader("Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'],
                                         increasing_line_color='green',
                                         decreasing_line_color='red')])
    
    fig.add_trace(go.Scatter(x=prediction_dates, y=predicted_prices, mode='markers+lines',
                             name='Predicted Prices', marker=dict(color='orange', size=8),
                             line=dict(color='orange', dash='dash')))
    
    fig.update_layout(title=f"{ticker} Stock Price Candlestick Chart with Predictions", 
                      xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)
    # Auto-refresh every 10 seconds
    page_refresh = """
    <script>
    const interval = setInterval(() => {
      window.location.reload();
    }, 10000);
    </script>
    """
    st.markdown(page_refresh, unsafe_allow_html=True)

if __name__ == "__main__":
    main()