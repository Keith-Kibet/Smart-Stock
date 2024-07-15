import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.title('Stock Data Dashboard')
    st.sidebar.subheader('Select Financial Statement')
    selected_function = st.sidebar.selectbox('Statement Type', ['Income Statement', 'Balance Sheet', 'Cash Flow'])
    selected_stock = st.sidebar.selectbox('Select Stock', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])

    if selected_stock:
        st.subheader(f"{selected_stock} - {selected_function}")
        stock = yf.Ticker(selected_stock)

        if selected_function == 'Income Statement':
            financial_data = stock.financials.T
            plot_income_statement(financial_data)

        elif selected_function == 'Balance Sheet':
            financial_data = stock.balance_sheet.T
            plot_balance_sheet(financial_data)

        elif selected_function == 'Cash Flow':
            financial_data = stock.cashflow.T
            plot_cash_flow(financial_data)

def plot_income_statement(data):
    st.subheader('Income Statement')
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        # Bar chart of Revenues and Expenses
        st.subheader('Revenue vs Expenses')
        st.bar_chart(data[['Total Revenue', 'Total Expenses']], 
                     use_container_width=True,
                     color=['#1f77b4', '#ff7f0e'])  # Blue for Revenue, Orange for Expenses

        # Line chart of Net Income
        st.subheader('Net Income')
        st.line_chart(data['Net Income'], 
                      use_container_width=True)

        # Area chart of Interest Income
        st.subheader('Interest Income')
        if 'Interest Income' in data.columns:
            st.area_chart(data['Interest Income'], 
                          use_container_width=True)
    else:
        st.warning(f"No Income Statement data available for selected stock")

def plot_balance_sheet(data):
    st.subheader('Balance Sheet')
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        # Pie chart of Total Assets and Liabilities
        st.subheader('Assets vs Liabilities')
        labels = ['Total Assets', 'Current Liabilities']
        values = data[['Total Assets', 'Current Liabilities']].fillna(0).iloc[-1]  # Fill NaN with 0
        values = values[values != 0]  # Remove 0 values
        labels = labels[:len(values)]
        labels = np.array(labels)  # Convert to numpy array for labels
        values = values.values.astype(float)  # Convert to numpy array of float values
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.warning(f"No Balance Sheet data available for selected stock")

def plot_cash_flow(data):
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        # Area chart of Free Cash Flow
        st.subheader('Free Cash Flow')
        if 'Free Cash Flow' in data.columns:
            st.area_chart(data['Free Cash Flow'], 
                          use_container_width=True)
    else:
        st.warning(f"No Cash Flow data available for selected stock")

if __name__ == "__main__":
    main()
