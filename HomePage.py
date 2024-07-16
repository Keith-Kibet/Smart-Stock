import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pages import Comparison, Finances, News, Prediction, Risk, Technical_Indicators

# Page selection
page = st.sidebar.selectbox("Select a page", ["Comparison", "Finances", "News", "Prediction", "Risk", "Technical_Indicators"])

# Display selected page
if page == "Comparison":
    Comparison.app()
elif page == "Finances":
    Finances.app()
elif page == "News":
    News.app()
if page == "Prediction":
    Prediction.app()
elif page == "Risk":
    Risk.app()
elif page == "Technical_Indicators":
    Technical_Indicators.app()

def main():
    st.set_page_config(page_title='Stock Data Dashboard', layout='wide')
    st.markdown("<h1 style='text-align: center;'>📈 Stock Data Dashboard</h1>", unsafe_allow_html=True)

    st.header('Select Options')
    col1, col2 = st.columns(2)
    
    with col1:
        selected_function = st.selectbox('Statement Type', ['Income Statement', 'Balance Sheet', 'Cash Flow'])
    with col2:
        selected_stock = st.selectbox('Select Stock', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'NFLX'])

    if selected_stock:
        st.write(f"{selected_stock} Data")
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
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        # Summary cards with pie charts for Revenue vs Expenses
        st.subheader('Summary')
        col1, col2, = st.columns(2)

        with col1:
            st.write('Revenue vs Expenses')
            revenue = data['Total Revenue'].iloc[-1]
            expenses = data['Total Expenses'].iloc[-1]
            labels = ['Revenue', 'Expenses']
            values = [revenue, expenses]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write('Net Income vs Expenses')
            net_income = data['Net Income'].iloc[-1]
            labels = ['Net Income', 'Expenses']
            values = [net_income, expenses]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        # Line chart of Net Income
        col3, col4, = st.columns(2)

        with col3:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Net Income'], mode='lines', name='Net Income'))
            fig.update_layout(title='Net Income Over Time')
            st.plotly_chart(fig, use_container_width=True)

        # Area chart of Interest Income
        with col4:
            if 'Total Revenue' in data.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Total Revenue'], mode='lines', fill='tozeroy', name='Interest Income'))
                fig.update_layout(title='Total Revenue Over Time')
                st.plotly_chart(fig, use_container_width=True)

def plot_balance_sheet(data):
    st.subheader('Balance Sheet')
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        st.subheader("Summary")

        col1, col2 = st.columns(2)
        with col1:
            st.write('Total Assets vs Liabilities')
            assets = data['Total Assets'].iloc[-1]
            liabilities = data['Current Liabilities'].iloc[-1]
            labels = ['Total Assets', 'Liabilities']
            values = [assets, liabilities]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write('Long vs Short term debt')
            long_term = data['Long Term Debt'].iloc[-1]
            short_debt = (data['Total Debt'] - long_term) .iloc[-1]
            labels = ['Long Term', 'Short_Term']
            values = [long_term, short_debt]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        # Line chart of Net Income
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Net Debt'], mode='lines', fill='tozeroy', name='Net Debt'))
        fig.update_layout(title='Net Income Over Time')
        st.plotly_chart(fig, use_container_width=True)

        # Area chart of Interest Income
        if 'Interest Income' in data.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Interest Income'], mode='lines', fill='tozeroy', name='Interest Income'))
            fig.update_layout(title='Interest Income Over Time')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No Income Statement data available for selected stock")

def plot_cash_flow(data):
    if data is not None and not data.empty:
        st.dataframe(data.style.format("{:,.2f}"))

        # Area chart of Free Cash Flow
        if 'Free Cash Flow' in data.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Free Cash Flow'], mode='lines', fill='tozeroy', name='Free Cash Flow'))
            fig.update_layout(title='Free Cash Flow Over Time')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No Cash Flow data available for selected stock")

if __name__ == "__main__":
    main()
