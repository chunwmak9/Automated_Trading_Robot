from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

from datetime import date
import datetime
import yahoo_fin.stock_info as stock_info
import time
import math
from datetime import datetime
import ssl
import re
import requests



from bs4 import BeautifulSoup

from typing import List

import re

import quandl



try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class HKStock_Getter:
    def __init__(self):
        pass

    def get_codes(self)-> List[int]:
        #http://billylkc.com/2021/06/21/getting-hkex-data-with-quandl-in-python/
        

        regex = re.compile(r"\s*(\d{5})(.*)")  # Get 5 digit codes only
        #re_chinese = re.compile(r"(\d{5})")#Get HK stock Chinese Name


        url = "https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate={}".format(
            datetime.today().strftime("%Y%m%d")
        ) # derive url, e.g. https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate=20210621

        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        
        codes = []
        count = 0
        for s in soup.select("table.table > tbody > tr"):
            count+=1
            
            text = s.get_text().replace(" ", "").strip()  # Replace extra spaces
            matchResult = regex.search(text)
            
            if matchResult:
                code = int(matchResult.group(1).lstrip("0"))  # Convert to int, e.g. 00005 to 5

                if code <= 10000:  # main board only
                    codes.append((code,text.split()[1]))
      
        tickers = []
        for c in codes:
            c0 = c[0]#HK tickers code
            c1 = c[1]#HK tickers name
            if len(str(c0)) <4:
                c0 = "0"*(4-len(str(c0)))+str(c0)+".HK"
                tickers.append([c0 ,c1])
            else:
                c0 = str(c0)+".HK"
                tickers.append([c0,c1])
        return tickers 
        #All tickers are tested for availability with Yahoo Finance

class StockGetter(object):
    def __init__(self): #initial setup parameters here e.g year ,duration,number of data
        pass
    #You can input the start to end date of certain stock token to get the data from yahoo finance online
    def get_data(self,s,e,stock):
        self.start_date = s
        self.end_date = e
        self.token = stock #stock name
        self.data = yf.download(self.token,self.start_date,self.end_date,interval = "1d")
        #1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo and 3mo (m refers to minute, h refers to hour, d refers to day, wk refers to week and mo refers to month)
        return self.data
    def get_rt_data(self,stock):
        self.ticker_yahoo = yf.Ticker(stock)
        self.data = self.ticker_yahoo.history(period = "1d", interval="1m")
        return self.data
    def get_all_tokens(self):
        #Stock_data
        naq = stock_info.tickers_nasdaq()
        dow = stock_info.tickers_dow()
        sp500 = stock_info.tickers_sp500()
        other_stocks = stock_info.tickers_other()
        hkex_stocks = HKStock_Getter().get_codes()
        hkex_tickers = [hkex_stocks[i][0] for i in range(len(hkex_stocks))]
        #hkex_names= [hkex_stocks[i][1] for _ in range(len(hkex_stocks))]
        tokens = naq+dow+sp500+other_stocks+hkex_tickers # all stock data input
        return tokens
                
if __name__ == "__main__":
    sg = StockGetter()
    today = date.today()
    now = today.strftime('%Y-%m-%d')
    data = sg.get_data('2020-9-1',now,"NNDM")
    print(data)
    
    
        







    """
    i = 0

    sg = sdata.StockGetter()
    today = date.today()
    now = today.strftime('%Y-%m-%d')
    tickers =  stock_info.get_day_gainers()['Symbol']    #stock_info.tickers_other()
    #stock_info: tickers_dow(),tickers_nasdaq(),tickers_other(),tickers_sp500()
    #Daily_stock: get_day_gainers(),get_day_most_active(),get_day_losers(),get_top_crypto()
    print(tickers)
    np.random.shuffle(tickers)
    
    while i < len(tickers): 
        try:
            data = sg.get_data('2020-9-1',now,tickers[i]).keys()
            data = sg.get_data('2020-9-1',now,tickers[i])
            methods= ['scatter','line']
            functions = ['regression','mean','volatility']
            plt.figure(figsize=(15,7))
            plt.subplot(1,2,1)
            sg.price_plot_data(data,methods,functions,'Open')
            plt.subplot(1,2,2)
            sg.price_plot_data(data,methods,functions,'Volume')
            plt.show()
            
        except KeyboardInterrupt:
            exit()

    """

    """
    while True:
        sg = StockGetter()
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        print(now)
        print(sg.get_data('2021-1-12',now,'NNDM').keys())
        token = str(input("Input the Stock Code: ")) #e.g NNDM 
        try:
            key = str(input("Input the type of data(NA=>Default Key): ")) #e.g Open
        except ValueError:
            key = "Open"
        data = sg.get_data('2020-1-12',now,token)
        print(data)
        methods= ['scatter','line']
        functions = ['regression','mean','volatility']
        sg.price_plot_data(data,methods,functions,key)
        """

#Reference: https://algotrading101.com/learn/yahoo-finance-api-guide/