import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

# Streamlit app definition
def main():
    st.header('Stock Comparison')

    # Custom Date Range Selector
    start_date = st.date_input("Choose a Start Date", value=date(2020, 1, 1))
    end_date = st.date_input("Choose an End Date", value=date.today())

    # Select stock ticker(s)
    tickers = st.multiselect("Select Ticker(s)", ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'], default=['AAPL'])
    
    if not tickers:
        st.warning("Please select at least one ticker.")
        return

    # Fetch stock data
    stock_data = {}
    for ticker in tickers:
        stock_data[ticker] = yf.download(ticker, start=start_date, end=end_date)
    
    # Display stock data
    for ticker in tickers:
        st.write(f"{ticker} Stock Data")
        st.dataframe(stock_data[ticker])
    
    # Check if data is not empty
    if any(data.empty for data in stock_data.values()):
        st.error("No data available for normalization.")
        return

    # Variable selection for visualization
    variable_to_plot = st.selectbox("Select Variable to Visualize", ['Open', 'High', 'Low', 'Close'])

    # Visualization of selected variable
    fig = go.Figure()
    for ticker in tickers:
        fig.add_trace(go.Scatter(x=stock_data[ticker].index, y=stock_data[ticker][variable_to_plot], mode='lines', name=f"{ticker} {variable_to_plot}"))
    
    fig.update_layout(
        title=f"{variable_to_plot} Prices Over Time",
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis=dict(showline=True, showgrid=False),  # Customize axis appearance
        yaxis=dict(showline=True, showgrid=False),
        plot_bgcolor='white',  # Set background color
        paper_bgcolor='white',  # Set border and background color
        margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins
        hovermode='x'  # Set hovermode
    )
    
    fig.update_xaxes(showspikes=True)  # Enable spikes on x-axis
    
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
