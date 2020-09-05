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

option = st.selectbox(
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
    st.image(stockData.info['logo_url'])
    st.write("""Website: """,stockData.info['website'],"""        City: """,stockData.info['city'], """        Country: """,stockData.info['country'])
    st.write("""**RECOMMENDATIONS: **""",
    stockData.recommendations)
    #st.write(stockData.info)

getStock(option)
    
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol

#z = 0
#for symbol in tickerSymbols:
#    tickerDatas.append(yf.Ticker(symbol))
#    tickerDFs.append(tickerDatas[z].history(period='ytd'))
#    z += 1
#x = 0
#for stocks in tickerDFs:
#    st.write(""" ## Closing Price """, tickerSymbols[x], """Current Price:""",tickerDatas[x].info['regularMarketPrice']) 
#    st.line_chart(stocks.Close)
#    #st.write(""" ## Volume Price """, tickerSymbols[x]) 
#    #st.line_chart(stocks.Volume)
#    print(tickerSymbols[x],x)
#    x += 1
    

#ickerSymbol = 'GOOGL'
#get data on this ticker
#tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
#tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-8-7')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

#st.write(""" ## Closing Price """) 
#st.line_chart(tickerDf.Close)
#st.write(""" ## Volume Price """) 
#st.line_chart(tickerDf.Volume)