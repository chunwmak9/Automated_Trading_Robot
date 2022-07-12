import os
import time
import sys
import subprocess


path = os.getcwd() +"\stock_price_prediction.py"
os.system(r"pip install streamlit")
os.system(r"pip install pandas")
os.system(r"pip install yfinance")
os.system(r"pip install pytreands")
os.system(r"pip install numpy")
os.system(r"pip install yahoo-fin")
os.system(r"pip install ssl")
os.system(r"pip install beautifulsoup4")
os.system(r"pip install typing")
os.system(r"pip install requests")
os.system(r"pip install quandl")
os.system(r"pip install regex")
os.system(r"pip install matplotlib")

try:
    from streamlit import cli as stcli
    import streamlit
    print('streamlit run '+path)
    #streamlit.run(path)
    subprocess.run(["streamlit", "run", path])
    #os.system('streamlit run '+path)
    
    #print(r'streamlit run {}'.format(path)
except:
    print("Failed to launch.")
while True:
    print("Running....")
    time.sleep(5)
