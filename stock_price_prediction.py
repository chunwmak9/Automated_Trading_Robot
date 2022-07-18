#This is written from Benny Mak 
#GitHub: r93042004@gmail.com


#Based on financial statements,technical indicator,balance sheet
#*Stock Price Prediction => Up/Down , continuous values

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stock_data as sd

from datetime import date
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import requests
import re
import pandas as pd
import numpy as np
import quandl

import streamlit as st
import time

#import altair as alt
#import threading

class HKStock_Getter:
    def __init__(self):
        pass
    def get_codes(self):
        #http://billylkc.com/2021/06/21/getting-hkex-data-with-quandl-in-python/
        
        """
        Get all the codes from the listed companies in HK main board from HKEX page
        Args:
            None

        Returns:
            codes ([]int): List of codes in HKEX main board

        Example:
            codes = get_codes()

        Data preview:
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ..]
        """

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
        








#Machine Learning 
class Regression:
    pass


class KNN:
    def __init__(self):
        pass
    def fit(self):
        pass
    def predict(self):
        pass
class LSTM:
    def __init__(self):
        pass

class Finance_Algorithms:
    def __init__(self):
        pass
   


    def EMA(self,ema_yesterday=0 ,close_price=None):
        smoothing = 2
        multiplier = 2/(1+len(close_price))
        if ema_yesterday == 0:
            ema_yesterday = sum(close_price)/len(close_price)
        res = close_price[-1] *multiplier  + ema_yesterday*(1-multiplier)
        return res
    def Normalize(self,ref,data):
        MAX = np.max(ref)
        normalized_data = (data -np.min(data)) / (np.max(data)-np.min(data)) *MAX
        return normalized_data
    def Gain(self,close_price=None): #Gain and Loss % between close price of two days 
        ans = []
        for i in range(len(close_price)):
            if i>0:
                ans.append(((close_price[i]-close_price[i-1])/close_price[i-1]))
            else:
                ans.append(0)
        return ans

    def Next_Price(self,close_price=None): #Create a next day price column
        ans = []
        for i in range(len(close_price)):
            if i<len(close_price)-1:
                ans.append(close_price[i+1])
            else:
                ans.append(np.nan)
        return ans
    def Average_Gain_Loss(self,gain,days=14):
        avg_gains = []
        avg_loss = []
        for g in range(len(gain)):
            if g == days-1:
                
                gains_0 = np.sum(gain[g-days-1:g+1][gain[g-days-1:g+1]>0]) /days
                loss_0 =  np.sum(gain[g-days-1:g+1][gain[g-days-1:g+1]<0]) /days
                avg_gains.append(gains_0)
                avg_loss.append(abs(loss_0))
            elif g>days-1:
                G = gain[g] if gain[g]>0 else 0
                L = gain[g] if gain[g]<0 else 0
                average_gains = ((avg_gains[-1]*(days-1) + G)/days)
                average_loss =  ((avg_loss[-1]*(days-1) + L)/days)
                avg_gains.append(average_gains)
                avg_loss.append(abs(average_loss))

            else:
                average_gains = 0
                average_loss = 0
                avg_gains.append(average_gains)
                avg_loss.append(average_loss)
        return (avg_gains,avg_loss)

    def RSI(self,gain,loss,days=14):
        rsi = []
        count=0
        for _ in gain:
            if count>=days:
                #ratio = gain[count]/loss[count]
                #print(ratio)
                #RSI = 100-(100/(1+ratio))
                try:
                    RSI =( gain[count]/(gain[count]+loss[count]) )* 100
                except:
                    RSI = 0
                rsi.append(RSI)
            else:
                rsi.append(0)
            count+=1
        return rsi
    def Bollinger_Band(self,close_price=None,days=30):
        sma = 0
        std = 0
        Upper_Band = []
        Lower_Bnad = []
        SMA = []
        STD = []
        #Default 9 days simple moving average
        for i in range(len(close_price)):
            if i >= days:
                val = close_price[i-days:i]
                sma = sum(val)/len(val)
            else:
                val = close_price[:i+1]
                sma = sum(val)/len(val)
            std = val.std()
            STD.append(std)
            Upper_Band.append(sma+(2*std))
            Lower_Bnad.append(sma-(2*std))
            SMA.append(sma)
        return Upper_Band,Lower_Bnad,SMA,STD
    


    def Technical_Automated(self,data):
        #0 => Inaction
        #1 => Entry
        #2 => Exit
        decision = 0 #0 => Wait for entry , 1 => Wait for exit
        auto_entry = []
        auto_exit = []
        add_point = 0  # 0,1,2 
        buy = 0
        entry_coor = []
        exit_coor = []
        EMA_count = 0
        cut_off_loss = 2 #Default = 100% (No cutoff for loss)
        for i in range(len(data)):
            add_point = 0
            
            if i>3:
                #buy_condition_2 = (data["Volume"][i] > data["Volume"][i-1]*10 and data["MACD"][i-2] < data["MACD"][i] and data["MACD"][i-1] < data["MACD"][i-2] and data["SMA"][i] > data["Close"][i])
                #buy_condition_2 = data["Volume"][i] > data["Volume"][i-1]*10 and data["DIFF"][i-1] + data["DIFF"][i] >0 and data["SMA"][i] < data["Close"][i]

                #buy_condition_2 = data["Close"][i-1] < data["BOLL_LB"][i-1] and data["Close"][i] > data["BOLL_LB"][i]  and data["MACD"][i-2] < data["MACD"][i] and data["Signal"][i] >= data["MACD"][i] and data["DIFF"][i-1] < data["DIFF"][i] 
                #Buy the Dig
                #buy_condition_1 = data["Volume"][i] > data["Volume"][i-1]*2 and data["DIFF"][i-1] + data["DIFF"][i] >0 and data["Close"][i]< data["BOLL_LB"][i]
                buy_condition_1_risky = data["Volume"][i] > data["Volume"][i-1]*2 and (data["DIFF"][i-1]>0 and data["DIFF"][i] >0 and data["DIFF"][i-1]<data["DIFF"][i] ) and (data["Close"][i]<= data["BOLL_LB"][i]+data["BOLL_STD"][i] ) and data["Close"][i-1] <data["Close"][i] and data["SMA"][i-1]<=data["SMA"][i]#and data["DIFF"][i]<=data["DIFF"][i-1])
                
                buy_condition_2_risky = data["SMA"][i-1]<=data["SMA"][i] and data["Close"][i-1]<data["Close"][i] and ( data["DIFF"][i]>=0 ) and (data["Close"][i]<= data["BOLL_LB"][i]+data["BOLL_STD"][i]  or (data["Close"][i]> data["SMA"][i]+ data["BOLL_STD"][i] and data["Close"][i]<data["SMA"][i]+ data["BOLL_STD"][i] and data["DIFF"][i]>0 and data["SMA"][i-1]<=data["SMA"][i] and  data["SMA"][i-2]<data["SMA"][i-1]) ) # and (data["Close"][i-1]<data["Close"][i] and data["Close"][i-2]>data["Close"][i-1]) 
                buy_condition_3_risky = data["Close"][i]<data["BOLL_LB"][i]  and data["DIFF"][i] >0 and data["Close"][i-1]<data["Close"][i]
                #buy_condition_3_risky = data["Close"][i-1]<data["BOLL_LB"][i-1]+data["BOLL_STD"][i-1] and data["Close"][i]<data["BOLL_LB"][i]+data["BOLL_STD"][i]
                buy_condition_4_risky = data["Close"][i] < data["SMA"][i]-data["BOLL_STD"][i] and data["SMA"][i-1]<=data["SMA"][i]
                normal_buy_condition = data["Close"][i-1] <= data["BOLL_LB"][i-1] and data["Close"][i] > data["BOLL_LB"][i]#data["Close"][i-1] <= data["BOLL_LB"][i-1] and data["Close"][i] > data["BOLL_LB"][i] 
                base_condition = data["Close"][i-1] < data["BOLL_LB"][i-1] and data["Close"][i] > data["BOLL_LB"][i] and  data["DIFF"][i-1] + data["DIFF"][i] >0
                buy_condition_5_risky = data["DIFF"][i-1]<data["DIFF"][i] and data["DIFF"][i]<0 and data["Close"][i-1] <data["Close"][i] and (data["Close"][i]<data["BOLL_LB"][i])


                #buy_condition_6_risky = 2* abs(data["DIFF"][i-1]) < data["DIFF"][i] and 0>data["DIFF"][i-1]  and data["DIFF"][i-1]<data["DIFF"][i] and data["DIFF"][i]  >0 and  ( data["Close"][i]<data["BOLL_LB"][i] + 0.5*data["BOLL_STD"][i] or data["SMA"][i-1]<data["SMA"][i])
                #condition_2 = (data["Volume"][i] > data["Volume"][i-1]*10 and data["MACD"][i])
                if decision == 0:
                    #if data["Close"][i-5] < data["BOLL_LB"][i-5] and 
                    #if data["Close"][i-4] < data["BOLL_LB"][i-4] and data["Close"][i-3] < data["BOLL_LB"][i-3] and data["Close"][i-2] < data["BOLL_LB"][i-2] and 
                    #and data["MACD"][i-1]<data["MACD"][i]
                    if ((data["Close"][i-2] <= data["BOLL_LB"][i-1] and data["Close"][i-1] > data["BOLL_LB"][i] and  data["DIFF"][i] > 0 ) or buy_condition_1_risky or buy_condition_3_risky  or buy_condition_2_risky or buy_condition_5_risky or buy_condition_4_risky): #or normal_buy_condition: 
                        
                        # or  buy_condition_3_risky : 
                        #and ( data["SMA"][i-1] - data["SMA"][i-2] > data["SMA"][i] - data["SMA"][i-1] ) :
                    # or buy_condition_1 or buy_condition_2 :
                    #and data["DIFF"][i-1] > data["DIFF"][i] and data["DIFF"][i-1] >0 and data["MACD"][i] > data["Signal"][i]:

                    
                        #and data["DIFF"][i]>data["DIFF"][i-1]:#and data["DIFF"][i-2]>data["DIFF"][i-1] and data["DIFF"][i]>data["DIFF"][i-1]:#(data["MACD"][i-1] <= data["Signal"][i-1] and data["MACD"][i] > data["Signal"][i]):
                        #Entry point
                        decision = 1
                        add_point = 1
                        buy = data["Close"][i]
                       

                elif decision == 1:
                    #if data["Close"][i-5] > data["BOLL_UB"][i-5] and 
                    #if data["Close"][i-4] >data["BOLL_UB"][i-4] and data["Close"][i-3] > data["BOLL_UB"][i-3] and data["Close"][i-2] > data["BOLL_UB"][i-2] and 
                    if data["Close"][i]<data["SMA"][i]:
                        EMA_count+=1
                    #if  (data["Close"][i] <= data["SMA"][i] and data["MACD"][i] < data["Signal"][i]):
                    if (data["Close"][i] > data["BOLL_UB"][i] or  ( data["MACD"][i] < data["Signal"][i] and data["SMA"][i]<=data["SMA"][i-1]) ) : #or (data["Close"][i]<data["SMA"][i]+data["BOLL_STD"][i] and data["SMA"][i-1]>data["SMA"][i]):
                    
                     #or ( data["Close"][i-1] > data["SMA"][i-1] ):
                    #or data["Close"][i-1] > data["Close"][i]:#or  data["Close"][i] <= data["BOLL_LB"][i] : #and data["MACD"][i-1] > data["MACD"][i]:#and 
                    #if data["DIFF"][i-2]<data["DIFF"][i-1] and data["DIFF"][i]<data["DIFF"][i-1]:#(data["MACD"][i-1] >= data["Signal"][i-1] and data["MACD"][i] < data["Signal"][i]):
                        #Exit point
                        if data["Close"][i] >= buy and data["Close"][i-1]>data["Close"][i]: 
                            EMA_count = 0
                            decision = 0
                            add_point = 2
                            buy = 0
                        elif data["Close"][i] <= data["BOLL_LB"][i]:
                            EMA_count = 0
                            decision = 0
                            add_point = 2
                            buy = 0
                    if buy!=0: #If the stock is not sold and it is below the buying price, then we need to cut the loss
                        if abs(((data["Close"][i] - buy)/buy))*100 >cut_off_loss:
                            EMA_count = 0
                            decision = 0
                            add_point = 2
                            buy = 0

                    
                    if add_point==0 and EMA_count>2:
                            if  data["Close"][i] >=buy:
                                EMA_count = 0
                                decision = 0
                                add_point = 2
                                buy = 0
                    

                            elif EMA_count ==2 and  data["Close"][i] <= buy:
                                EMA_count = 0
                                decision = 0
                                add_point = 2
                                buy = 0

                    ####*************CUT LOSS => for stocks like SOS, RUN
                    # elif data["Close"][i-1] > data["Close"][i] and data["Close"][i] < data["SMA"][i] and data["DIFF"][i] < 0:
                    #     if data["Close"][i] >= buy:
                    #         decision = 0
                    #         add_point = 2
                    #         buy = 0

                
                
                if add_point == 0:
                    auto_entry.append(np.nan)
                    auto_exit.append(np.nan)
                    
                elif add_point==1:
                    auto_entry.append(data["Close"][i])
                    auto_exit.append(np.nan)

                    entry_coor.append((i,data["Close"][i]))
                elif add_point==2:
                    auto_entry.append(np.nan)
                    auto_exit.append(data["Close"][i])
                    exit_coor.append((i,data["Close"][i]))


            else:
                auto_entry.append(np.nan)
                auto_exit.append(np.nan)
            



        data["Auto_Entry"] = auto_entry
        data["Auto_Exit"] = auto_exit
        return data,entry_coor,exit_coor





class DataPreprocessor(Finance_Algorithms):
    #IN DF => OUT DF for Machine learning model
    def __init__(self):
        self.data = []
    def get_format_data(self,data): 
        #Add Gains = close_today - close_yesterday ,EMA,MACD,RSI,Bolling Band
        #Support data format in yfinance
        # if self.data!= []:
        #     return self.data
        EMA = [] #12 days EMA
        EMA_26 = [] #26 days EMA
        
        EMA_p = 0
        for n in range(len(data["Close"])):
            if n>=12:
                EMA_p = self.EMA(EMA_p,data["Close"][n-12:n])
                EMA.append(EMA_p)
            else:
                EMA_p = self.EMA(EMA_p,data["Close"][:n+1])
                EMA.append(EMA_p)
        EMA_p = 0
        for n in range(len(data["Close"])):
            if n>=26:
                EMA_p = self.EMA(EMA_p,data["Close"][n-26:n])
                EMA_26.append(EMA_p)
            else:
                EMA_p = self.EMA(EMA_p,data["Close"][:n+1])
                EMA_26.append(EMA_p)
       
        
                
        

        data["EMA_12"] = EMA
        data["EMA_26"] = EMA_26
        data["MACD"] = data["EMA_26"] - data["EMA_12"] #No need for absolute => MACD can be negative
        data["Gain"] = self.Gain(data["Close"])
        
        data["Avg_Gain"],data["Avg_Loss"] = self.Average_Gain_Loss(data["Gain"])
      
        data["RSI"] = self.RSI(data["Avg_Gain"],data["Avg_Loss"])
        data["BOLL_UB"],data["BOLL_LB"],data["SMA"],data["BOLL_STD"] = self.Bollinger_Band(data["Close"])


        Signal = []
        signal_p = 0
        for n in range(len(data["MACD"])):
            if n>=9:
                signal_p = self.EMA(signal_p,data["MACD"][n-9:n+1])
                Signal.append(signal_p)
            else:
                signal_p = self.EMA(signal_p,data["MACD"][:n+1])
                Signal.append(signal_p)


        data["Signal"] = Signal
        data["DIFF"] =data["Signal"] - data["MACD"] 


        #Normalization
        # MAX = np.max(data["Volume"])
        # MIN = np.min(data["MACD"])
        # RANGE  = np.max(data["MACD"])-np.min(data["MACD"])

        #data["MACD"] = self.Normalize(data["Close"],data["MACD"])
        #data["Volume"] = self.Normalize(data["Close"],data["Volume"])
        #data["Signal"] = self.Normalize(data["Close"],data["Signal"])
        data["Next Price"] = self.Next_Price(data["Close"])
        self.data = data
        return data
    def Normalize(self,ref,data):
        MAX = np.max(ref)
        normalized_data = (data -np.min(data)) / (np.max(data)-np.min(data)) *MAX
        return normalized_data
    def NormalizeAll(self,data):
        from sklearn.preprocessing import MinMaxScaler
        data_rescale = MinMaxScaler(feature_range = (0,1))
        try:
            
            for key in data.keys():
                data[key] = data_rescale.fit_transform(data[key].values.reshape(-1,1))
        except:
                data = data.to_numpy()   
                data = data_rescale.fit_transform(data.reshape(-1,1))
        return data
    """
    Default days: 5
    Input: days data 
    Output: prices for 23.6% ,38.2%,61.8%,78.6%
    """
    def Fibonacci_Retraction(self,data,days=5):
        fib = [0,0.236,0.382,0.5,0.618,0.786]
        res = []
        Price_MAX = data["High"].max()
        Price_MIN = data["High"].min()
        Diff = Price_MAX - Price_MIN 
        #Diff: Range between Max and Min

        level0 = Price_MAX - fib[0]*Diff
        level1 = Price_MAX - fib[1]*Diff
        level2 = Price_MAX - fib[2]*Diff
        level3 = Price_MAX - fib[3]*Diff
        level4 = Price_MAX - fib[4]*Diff
        level5 = Price_MAX - fib[5]*Diff
        res = [level0,level1,level2,level3,level4,level5]
        return res





        

if __name__ == "__main__":
    hkstock = HKStock_Getter()
    hk_tickers = hkstock.get_codes() #[[Ticker, Name]......]
    #print(len(hk_tickers))
    #print(hk_tickers)

    ####Stock Screener => Find a Day trade ETF models (US stock ), +% shold > 5% per day and percentage of earning > 90%
    # sg = sd.StockGetter()
    
    # today = date.today()
    # now = today.strftime('%Y-%m-%d')

    # #US Stocks
    # import ssl
  

    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     pass
   
    # ssl._create_default_https_context = _create_unverified_https_context
    # naq = sd.stock_info.tickers_nasdaq()
    # dow = sd.stock_info.tickers_dow()
    # sp500 = sd.stock_info.tickers_sp500()
    # other_stocks = sd.stock_info.tickers_other()
    # stocks = naq

    # for t in stocks:
    #     try:
    #         data = sg.get_data('2018-10-1',now,t)
    #     except:
    #         continue
    #     #streamlit
    #     name = t
        
    #     #data = sg.get_data('2018-10-1',now,"FB")
    #     algo = Finance_Algorithms()
        
    #     EMA = [] #12 days EMA
    #     EMA_26 = [] #26 days EMA

    #     EMA_p = 0
    #     for n in range(len(data["Close"])):
    #         if n>=12:
    #             EMA_p = algo.EMA(EMA_p,data["Close"][n-12:n])
    #             EMA.append(EMA_p)
    #         else:
    #             EMA_p = algo.EMA(EMA_p,data["Close"][:n+1])
    #             EMA.append(EMA_p)
    #     EMA_p = 0
    #     for n in range(len(data["Close"])):
    #         if n>=26:
    #             EMA_p = algo.EMA(EMA_p,data["Close"][n-26:n])
    #             EMA_26.append(EMA_p)
    #         else:
    #             EMA_p = algo.EMA(EMA_p,data["Close"][:n+1])
    #             EMA_26.append(EMA_p)
    #     data["EMA_12"] = EMA 
    #     data["EMA_26"] = EMA_26
    #     data["MACD"] = data["EMA_26"] - data["EMA_12"] #No need for absolute => MACD can be negative

    #     Signal = []
    #     signal_p = 0
    #     for n in range(len(data["MACD"])):
    #         if n>=9:
    #             signal_p = algo.EMA(signal_p,data["MACD"][n-9:n+1])
    #             Signal.append(signal_p)
    #         else:
    #             signal_p = algo.EMA(signal_p,data["MACD"][:n+1])
    #             Signal.append(signal_p)


    #     data["Signal"] = Signal
    



    #     #Normalization
    #     # MAX = np.max(data["Volume"])
    #     # MIN = np.min(data["MACD"])
    #     # RANGE  = np.max(data["MACD"])-np.min(data["MACD"])

    #     data["MACD"] = algo.Normalize(data["Close"],data["MACD"])
    #     data["Volume"] = algo.Normalize(data["Close"],data["Volume"])
    #     data["Signal"] = algo.Normalize(data["Close"],data["Signal"])
    #     try:
    #         #diff = ((data["Close"][-1] - data["Close"][-2]) /  data["Close"][-2]) *100
    #         if ((data["Signal"][-2] < data["MACD"][-2]) and (data["Signal"][-1] < data["MACD"][-1])) and (data["Signal"][-3] > data["MACD"][-3]) :
    #             st.write(name)
    #             st.write("The last price: {} \n The current price {}".format(data["Close"][-2],data["Close"][-1]))
    #             st.line_chart(data[["EMA_12","Close","EMA_26","MACD","Signal"]])
    #             data
    #     except:
    #         pass

    
    ####Signal Stock
    sg = sd.StockGetter()
    
    today = date.today()
    #print(today)
    now = today.strftime('%Y-%m-%d')


    
    #data = sg.get_data('2018-2-24',now,"2800.HK")
    
    
    #streamlit
    #name = [i[1] for i in hk_tickers if "2800.HK" in i ]
    #st.write(name[-1])
    
    
    #data = sg.get_data('2018-10-1',now,"FB")
    
    # x = [i for i in range(len(data))]
    def real_time_window(stock):
        
        data_preprocessor = DataPreprocessor()
        data = sg.get_rt_data(stock)
        data = data_preprocessor.get_format_data(data)
        algo = Finance_Algorithms()
        all_tokens = sg.get_all_tokens()

        fib_data = sg.get_rt_data(stock,5)
        
        option = st.selectbox(
                        'Select a Stock:',
                        tuple(all_tokens))
       


        
        if st.button('Select'):
            stock = option
            fib_data = sg.get_rt_data(stock,5)
            fib = data_preprocessor.Fibonacci_Retraction(fib_data)
            print("Fibonanci Retraction:{}".format(str(fib)))

        
        with st.sidebar:
            st.write("Trade Automation")
            option_tradebot = st.checkbox("Turn TradeBot On")
            
            st.write("Analytic Tools")
            option_fibonacci = st.checkbox("Fibonacci Retraction")
            option_boll = st.checkbox("Bollinger Bands")

            st.write("Other")
            option_tradetable = st.checkbox("Enable Trade Table")
            option_analytics =st.checkbox("Turn Analytics On")
        

        
            
    


        with st.empty():
            while True:
                with st.container():
                   
                    st.write(stock)
                    fig, ax = plt.subplots()
                    data = sg.get_rt_data(stock)
                    #data = sg.get_data('2018-2-24',now,"NNDM")
                    data = data_preprocessor.get_format_data(data)
                    #time.sleep(1)
                    #print(data["Close"].min())
                    
                    data,ENTRY,EXIT = algo.Technical_Automated(data)
                    #data
                    
                    

                    #Fibonanci_Retraction
                    if option_fibonacci == True:
                        colors = ["r","g","b","r","g","b"]
                        fib = data_preprocessor.Fibonacci_Retraction(fib_data)
                        print("Fibonanci Retraction:{}".format(str(fib)))
                        fib_ratios = [0,0.236,0.382,0.5,0.618,0.786]
                        for i in range(len(fib)):
                            plt.annotate("Level{} ({}%) : {}".format(i,round(fib_ratios[i]*100,3),round(fib[i],3)),(len(data.index)//50,fib[i]))
                            if i+1 <= len(fib) -1:
                                plt.axhspan(fib[i],fib[i+1],0,len(data.index),color=colors[i],alpha=0.1)
                                print(fib)
                            else:
                                plt.axhspan(fib[i],data["Close"].min(),0,len(data.index),color=colors[i],alpha=0.1)
                                print(fib)
                    



                    l1= ax.plot(range(len(data.index)),data["Close"])

                    #l2= ax.plot(range(len(data.index)),data["EMA_12"])
                    
                    #l3 = ax.plot(range(len(data.index)),data["EMA_26"])
                    if option_boll:
                        l4 = ax.plot(range(len(data.index)),data["BOLL_UB"])
                        l5 = ax.plot(range(len(data.index)),data["BOLL_LB"])
                        l6 = ax.plot(range(len(data.index)),data["SMA"])

                    #labels = ['Close',"BOLL_UB","BOLL_LB","SMA"] #,"EMA 12","EMA 26"
                    
                    #ax.legend(labels, loc ='lower left') 
                    if option_tradebot:
                        ax.scatter(range(len(data.index)),data["Auto_Entry"],color="green",marker='*',s=30)
                        ax.scatter(range(len(data.index)),data["Auto_Exit"],color="red",marker='*',s=30)
                        entry_price = []
                        exit_price = []
                        gains = []
                        for e in range(len(ENTRY)):

                            entry_price.append(round(ENTRY[e][1],3))
                            ax.annotate("Buy at {}".format(round(ENTRY[e][1],3)), (ENTRY[e][0], ENTRY[e][1]))
                        for ex in range(len(EXIT)):
                            exit_price.append(round(EXIT[ex][1],3))
                            ax.annotate("Sell at {}".format(round(EXIT[ex][1],3)) ,(EXIT[ex][0], EXIT[ex][1]))
                        if len(entry_price) == len(exit_price): 
                            for e,ex in zip(entry_price,exit_price):
                                gains.append(((ex-e)/e)*100)
                        else:
                            if len(entry_price) == 0:
                                gains.append(0)
                            else:
                                for e,ex in zip(entry_price[:len(entry_price)-1],exit_price):
                                    gains.append(((ex-e)/e)*100)
                        st.write("Total Gains: {}%".format(str(sum(gains))))

                      
                    st.pyplot(fig)
                    if option_tradetable:
                        st.table(data[::-1])

                    #st.line_chart(data[["BOLL_UB","BOLL_LB","SMA"]])

                    #st.line_chart(data[["EMA_12","Close","EMA_26"]])
                    if option_analytics:
                        analytics_expander = st.expander(label='Analytics')
                        with analytics_expander:
                            st.line_chart(data[["MACD","Signal"]])
                            st.bar_chart(data["DIFF"])
                            st.bar_chart(data["Volume"])
                            st.line_chart(data["RSI"])
                    #time.sleep(1)
                    
    real_time_window("NNDM")
    
    
    
    
        


    
    


    

    

    

