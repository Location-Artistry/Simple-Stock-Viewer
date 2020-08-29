import yfinance as yf
import streamlit as st
import pandas as pd
import datetime as dt
today = dt.date.today()

st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Selected Stocks

""",today)

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
#tickerSymbols = ['TSLA','PFE','AAPL']
#tickerSymbols = ['AAPL','GOOGL','TSLA','PFE']
tickerSymbols = ['JD','BABA','AAPL','TSLA','PFE','XLNX','CLNE','AAPL','NVDA','MAT','AMD','UPWK','ZNGA','ROBO','WORK','GOOGL']
#currentSymbol = yf.Ticker("YVR")
#stockInfo = currentSymbol.info
#stockInfo
#print(stockInfo['regularMarketPrice'])
tickerDatas = []
tickerDFs = []
z = 0
for symbol in tickerSymbols:
    tickerDatas.append(yf.Ticker(symbol))
    tickerDFs.append(tickerDatas[z].history(period='ytd'))
    z += 1
x = 0
for stocks in tickerDFs:
    st.write(""" ## Closing Price """, tickerSymbols[x], """Current Price:""",tickerDatas[x].info['regularMarketPrice']) 
    st.line_chart(stocks.Close)
    #st.write(""" ## Volume Price """, tickerSymbols[x]) 
    #st.line_chart(stocks.Volume)
    print(tickerSymbols[x],x)
    x += 1
    

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