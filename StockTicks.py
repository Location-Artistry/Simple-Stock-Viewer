import yfinance as yf
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
today = dt.date.today()

# Simple streamlit app using python & yfinance to get information on stock highlighted in selectbox
# Working as a streamlit app test deploy to Heroku

st.write("""
# Stock Selector

""","""Date:""",today)
tickerSymbols = ['JD','BABA','AAPL','TSLA','PFE','XLNX','CLNE','AAPL','NVDA','MAT','AMD','UPWK','ZNGA','ROBO','WORK','GOOGL']

option = st.sidebar.selectbox(
    'CHOOSE STOCK TO SHOW INFO',
     tickerSymbols)

tickerDatas = []
tickerDFs = []

def getStock(tickName):
    stockData = yf.Ticker(tickName)
    stockHistory = stockData.history(period='ytd')
    st.write("""
     ## SYMBOL: **""", stockData.info['symbol'], """**    NAME: **""", stockData.info['shortName'],"""**""")
    st.write(""" ## Closing Price:  """,stockData.info['regularMarketPreviousClose'], """Current Price:""",stockData.info['regularMarketPrice']) 
    st.line_chart(stockHistory.Close)  
    st.write("""Website: """,stockData.info['website'],"""        City: """,stockData.info['city'], """        Country: """,stockData.info['country'])
    st.write("""**RECOMMENDATIONS: **""",
    stockData.recommendations)
    st.sidebar.image(stockData.info['logo_url'])
    #st.sidebar("""**RECOMMENDATIONS: **""")
    #st.write(stockData.info)

getStock(option)
