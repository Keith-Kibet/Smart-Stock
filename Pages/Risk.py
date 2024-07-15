import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def calculate_risk_metrics(stock_ticker, risk_free_rate=0.01, confidence_level=0.95):
    stock = yf.Ticker(stock_ticker)
    hist = stock.history(period="1y")
    if not hist.empty:
        hist['Simple Return'] = hist['Close'].pct_change()
        avg_return = hist['Simple Return'].mean() * 252  # Annualized average return
        volatility = hist['Simple Return'].std() * np.sqrt(252)  # Annualized volatility
        beta = stock.info.get('beta', np.nan)
        sharpe_ratio = (avg_return - risk_free_rate) / volatility  # Sharpe ratio calculation
        
        # VaR Calculation
        sorted_returns = hist['Simple Return'].dropna().sort_values()
        var_index = int((1 - confidence_level) * len(sorted_returns))
        var = sorted_returns.iloc[var_index] * np.sqrt(252) if var_index < len(sorted_returns) else np.nan  # Annualized VaR
        
        return volatility, beta, sharpe_ratio, var
    return None, None, None, None

def main():
    st.subheader('Stock Risk Metrics Visualization')

    # List of stocks to evaluate
    stock_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX']
    
    risk_metrics = {}
    
    # Calculate risk metrics for each stock
    for stock in stock_list:
        volatility, beta, sharpe_ratio, var = calculate_risk_metrics(stock)
        if volatility is not None and beta is not None and sharpe_ratio is not None and var is not None:
            risk_metrics[stock] = {
                'Volatility': volatility,
                'Beta': beta,
                'Sharpe Ratio': sharpe_ratio,
                'Value at Risk (VaR)': var
            }
    
    if risk_metrics:
        risk_metrics_df = pd.DataFrame.from_dict(risk_metrics, orient='index')
        risk_metrics_df.sort_values(by='Sharpe Ratio', ascending=False, inplace=True)
        
        st.dataframe(risk_metrics_df.style.format({
            "Volatility": "{:.2%}",
            "Beta": "{:.2f}",
            "Sharpe Ratio": "{:.2f}",
            "Value at Risk (VaR)": "{:.2%}"
        }))
        
        # Allow user to select which metrics to visualize
        selected_metrics = st.multiselect(
            'Select Metrics to Visualize',
            ['Volatility', 'Beta', 'Sharpe Ratio', 'Value at Risk (VaR)'],
            default=['Volatility', 'Beta', 'Sharpe Ratio', 'Value at Risk (VaR)']
        )
        
        if selected_metrics:
            st.bar_chart(risk_metrics_df[selected_metrics])

if __name__ == "__main__":
    main()
