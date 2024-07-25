import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def main():
    st.subheader('Explore Financial Statements')
    selected_data_type = st.selectbox('Select Data Type', ['Financial Statements', 'Time Series Data'])
    # Define the mapping of names to function calls
    function_mapping = {
        'Income Statement': 'get_income_stmt',
        'Balance Sheet': 'get_balance_sheet',
        'Cash Flow Statement': 'get_cashflow'
    }

    if selected_data_type == 'Financial Statements':
        #selected_function = st.selectbox('Select Financial Statement',  ['get_income_stmt', 'get_balance_sheet', 'get_cashflow'])
        selected_function_Array = st.selectbox('Select Financial Statement', list(function_mapping.keys()))

        selected_function = function_mapping[selected_function_Array]

        selected_stock = st.selectbox('Select Stock', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])
        
        if selected_stock:
            st.subheader(f"{selected_stock} Data")
            stock = yf.Ticker(selected_stock)
            financial_data_function = getattr(stock, selected_function)
            financial_data = financial_data_function().T  # Transpose the DataFrame

            if financial_data is not None:
                # Convert index to datetime and format to date only if applicable
                if isinstance(financial_data.index, pd.DatetimeIndex):
                    financial_data.index = financial_data.index.date
                st.dataframe(financial_data.style.format("{:,.2f}"))

            else:
                st.warning(f"No {selected_function} data available for {selected_stock}")

    elif selected_data_type == 'Time Series Data':
        st.subheader('Explore Time Series Data')
        selected_time_series_type = st.selectbox('Select Time Series Data Type', ['History', 'Dividends', 'Splits', 'Returns'])
        selected_stock = st.selectbox('Select Stock', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])

        if selected_stock:
            st.subheader(f"{selected_stock}'s {selected_time_series_type}")  # Hybrid sub-header
            stock = yf.Ticker(selected_stock)

            if selected_time_series_type == 'History':
                hist = stock.history(period="1mo").T  # Transpose the DataFrame
                if isinstance(hist.index, pd.DatetimeIndex):
                    hist.index = hist.index.date  # Convert index to datetime and format to date only if applicable
                st.dataframe(hist.T.style.format("{:,.2f}"))  # Transpose back to original orientation before displaying

            elif selected_time_series_type == 'Dividends':
                dividends = stock.dividends.to_frame().T  # Transpose the DataFrame
                if isinstance(dividends.index, pd.DatetimeIndex):
                    dividends.index = dividends.index.date  # Convert index to datetime and format to date only if applicable
                st.dataframe(dividends.T.style.format("{:,.2f}"))  # Transpose back to original orientation before displaying

            elif selected_time_series_type == 'Splits':
                splits = stock.splits.to_frame().T  # Transpose the DataFrame
                if isinstance(splits.index, pd.DatetimeIndex):
                    splits.index = splits.index.date  # Convert index to datetime and format to date only if applicable
                st.dataframe(splits.T.style.format("{:,.2f}"))  # Transpose back to original orientation before displaying

            elif selected_time_series_type == 'Returns':
                hist = stock.history(period="1y")
                
                if hist is not None:
                    hist['Simple Return'] = hist['Close'].pct_change()
                    hist['Log Return'] = np.log(hist['Close'] / hist['Close'].shift(1))
                    average_return = hist['Simple Return'].mean() * 252
                    volatility = hist['Simple Return'].std() * np.sqrt(252)
                    st.write(f"Average Annual Return: {average_return:.2%}")
                    st.write(f"Annual Volatility: {volatility:.2%}")
                    st.dataframe(hist[['Close', 'Simple Return', 'Log Return']].dropna().style.format({"Close": "{:,.2f}", "Simple Return": "{:.2%}", "Log Return": "{:.2%}"}))

if __name__ == "__main__":
    main()
