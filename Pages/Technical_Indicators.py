import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Simple Moving Average 
def calculate_SMA(data, ndays): 
    SMA = pd.Series(data['Close'].rolling(ndays).mean(), name='SMA') 
    data = data.join(SMA) 
    return data

# Exponentially-weighted Moving Average 
def calculate_EWMA(data, ndays): 
    EMA = pd.Series(data['Close'].ewm(span=ndays, min_periods=ndays - 1).mean(), 
                    name='EWMA_' + str(ndays)) 
    data = data.join(EMA) 
    return data

# Function to calculate ATR values
def atr(high, low, close, n=14):
    tr = np.amax(np.vstack(((high - low).to_numpy(), 
                            (abs(high - close)).to_numpy(), 
                            (abs(low - close)).to_numpy())).T, axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

# Compute the Bollinger Bands 
def calculate_BBANDS(data, window):
    MA = data['Close'].rolling(window=window).mean()
    SD = data['Close'].rolling(window=window).std()
    data['MiddleBand'] = MA
    data['UpperBand'] = MA + (2 * SD)
    data['LowerBand'] = MA - (2 * SD)
    return data

# Function to calculate RSI values
def rsi(close, periods=14):
    close_delta = close.diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi

# Function to calculate Force Index
def force_index(data, ndays):
    FI = pd.Series(data['Close'].diff(ndays) * data['Volume'], name='ForceIndex')
    data = data.join(FI)
    return data

# Function to calculate MFI values
def mfi(high, low, close, volume, n=14):
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    mf_sign = np.where(typical_price > typical_price.shift(1), 1, -1)
    signed_mf = money_flow * mf_sign

    # Calculate gain and loss using vectorized operations
    positive_mf = np.where(signed_mf > 0, signed_mf, 0)
    negative_mf = np.where(signed_mf < 0, -signed_mf, 0)

    mf_avg_gain = pd.Series(positive_mf).rolling(n, min_periods=1).sum()
    mf_avg_loss = pd.Series(negative_mf).rolling(n, min_periods=1).sum()

    return (100 - 100 / (1 + mf_avg_gain / mf_avg_loss)).to_numpy()

# Function to fetch historical stock data and calculate various indicators
def fetch_stock_data(symbol):
    data = yf.download(symbol, start="2020-01-01", end="2024-12-31")
    data['ATR'] = atr(data['High'], data['Low'], data['Close'], 14)
    data['RSI'] = rsi(data['Close'])
    data = force_index(data, 1)
    data['MFI'] = mfi(data['High'], data['Low'], data['Close'], data['Volume'], 14)
    return data

def main():
    st.subheader('Technical Indicators')

    selected_time_series_type = st.selectbox('Select an Indicator', ['History', 'Bollinger Bands', 'ATR', 'RSI', 'Force Index', 'MFI', 'SMA', 'EWMA'])
    selected_stock = st.selectbox('Select Stock', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])

    if selected_stock:
        st.subheader(f"{selected_stock}'s {selected_time_series_type}")
        stock = yf.Ticker(selected_stock)

        if selected_time_series_type == 'History':
            hist = stock.history(period="1mo").T
            if isinstance(hist.index, pd.DatetimeIndex):
                hist.index = hist.index.date
            st.dataframe(hist.T.style.format("{:,.2f}"))

        elif selected_time_series_type == 'Bollinger Bands':
            st.subheader('Bollinger Bands')
            window = st.number_input('Enter window size:', min_value=1, max_value=100, value=20)
            data = yf.download(selected_stock, start="2020-01-01", end="2024-12-31")
            data_with_bbands = calculate_BBANDS(data, window)

            fig, ax = plt.subplots(figsize=(10, 7))
            ax.set_title('Bollinger Bands')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.plot(data_with_bbands['Close'], lw=1, label='Close Price')
            ax.plot(data_with_bbands['UpperBand'], 'g', lw=1, label='Upper Band')
            ax.plot(data_with_bbands['MiddleBand'], 'r', lw=1, label='Middle Band')
            ax.plot(data_with_bbands['LowerBand'], 'g', lw=1, label='Lower Band')
            ax.legend()
            st.pyplot(fig)

        elif selected_time_series_type == 'ATR':
            st.subheader("Average True Range")
            data = fetch_stock_data(selected_stock)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
            ax1.set_title(f'{selected_stock} Price Chart')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Close Price')
            ax1.plot(data['Close'], label='Close price')
            ax1.legend()
            ax2.set_title('Average True Range (ATR)')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('ATR values')
            ax2.plot(data['ATR'], 'm', label='ATR')
            ax2.legend()
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_time_series_type == 'RSI':
            st.subheader("Relative Strength Index")
            data = fetch_stock_data(selected_stock)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
            ax1.set_title(f'{selected_stock} Price Chart')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Close Price')
            ax1.plot(data['Close'], label='Close price')
            ax1.legend()
            ax2.set_title('Relative Strength Index (RSI)')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('RSI values')
            ax2.plot(data['RSI'], 'm', label='RSI')
            ax2.legend()
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_time_series_type == 'Force Index':
            data = fetch_stock_data(selected_stock)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
            ax1.set_title(f'{selected_stock} Price Chart')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Close Price')
            ax1.plot(data['Close'], label='Close price')
            ax1.legend()
            ax2.set_title('Force Index')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Force Index values')
            ax2.plot(data['ForceIndex'], 'm', label='Force Index')
            ax2.legend()
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_time_series_type == 'MFI':
            st.subheader('Money Flow Index')
            data = fetch_stock_data(selected_stock)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
            ax1.set_title(f'{selected_stock} Price Chart')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Close Price')
            ax1.plot(data['Close'], label='Close price')
            ax1.legend()
            ax2.set_title('Money Flow Index (MFI)')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('MFI values')
            ax2.plot(data['MFI'], 'm', label='MFI')
            ax2.legend()
            plt.tight_layout()
            st.pyplot(fig)
        
        elif selected_time_series_type == 'SMA':
            st.subheader('Simple Moving Average')
            window = st.number_input('Enter window size:', min_value=1, max_value=100, value=50)
            data = yf.download(selected_stock, start="2020-01-01", end="2024-12-31")
            data_with_sma = calculate_SMA(data, window)

            fig, ax = plt.subplots(figsize=(10, 7))
            ax.set_title('Simple Moving Average')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.plot(data['Close'], lw=1, label='Close Price')
            ax.plot(data_with_sma['SMA'], 'g', lw=1, label=f'{window}-day SMA')
            ax.legend()
            st.pyplot(fig)
        
        elif selected_time_series_type == 'EWMA':
            st.subheader('Exponentially Weighted Moving Average')
            window = st.number_input('Enter window size:', min_value=1, max_value=100, value=50)
            data = yf.download(selected_stock, start="2020-01-01", end="2024-12-31")
            data_with_ewma = calculate_EWMA(data, window)

            fig, ax = plt.subplots(figsize=(10, 7))
            ax.set_title('Exponentially Weighted Moving Average')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.plot(data['Close'], lw=1, label='Close Price')
            ax.plot(data_with_ewma[f'EWMA_{window}'], 'r', lw=1, label=f'{window}-day EWMA')
            ax.legend()
            st.pyplot(fig)

if __name__ == '__main__':
    main()
