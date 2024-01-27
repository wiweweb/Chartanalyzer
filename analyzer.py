"""
TODO:   - gedanken über Speicherung der Daten machen
            -> Tageskerze notwendig?
            -> wie sicherstellen, dass regelmäßig die daten aus den netzt gezogen werden?
        - verbinden aller Indikatoren??? auch separat betrachten? für starke Aussage 
            -> Fibonacci retracement
            -> aufwärstrend abwärtstrend
            -> Kerzenanalyse
            -> gleitender Mittelwert
        - Stop loss?
"""

import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import yfinance as yf
from dateutil.relativedelta import relativedelta
import time, os, pickle
import tkinter as tk
# import FrontEnd

dir_path = os.path.dirname(os.path.realpath(__file__))
filesInData = os.listdir(f"{dir_path}/data")
currentdate = date.today()


currentStocks = {"Varta":    "VAR1.DE", 
          "Tesla":    "TSLA", 
          "Etherium": "ETH-USD",
          "Bitcoin":  "BTC-USD"}

def save_data(data, key, interval):
    data.to_pickle(f"{dir_path}/data/{key}{interval}.pkl")

def is_data_already_read(key, interval):
    '''kind of load data pared with the check of existance
        takes:
                       - key(name of the Stock)
                       - interval (day or min) 
        returns: 
            descission - if file is already excisting
            lastdate   - last saved date is existing
            data       - whole data if existing'''
    try:
        descission = False
        lastdate = None
        data = None
        data = pd.read_pickle(f"{dir_path}/data/{key}{interval}.pkl")
        lastdate = datetime.strptime(str(data.index[-1])[0:10], '%Y-%m-%d').date()
        descission = True
        print(f"Data is existing and will be handled. Stock: {key}")
    except FileNotFoundError: # for trying to access the data pkl for current stock
        print(f"File for the Stock is not existing! Stock: {key}")
    except IndexError: # for geting specific data out of the stocks pkl for lastdade
        print(f"{key} is empty and will be removed!")
        handleStocks(key.replace("_","/"), single=True)
    return (descission, lastdate, data)
    
def relativeDelta(key, interval):
    '''calculates the days between today and the last saved date or 7years ago.
        takes: stock name
        returns: delta in days'''
    currentdate = date.today()
    result = is_data_already_read(key, interval)
    print(currentdate, result[1])
    if result[0]:
        dateinthepast = result[1]
    else:
        if interval == "":
            dateinthepast = currentdate - relativedelta(years=7)
        else:
            dateinthepast = currentdate - relativedelta(days=7)
    delta = (currentdate-dateinthepast).days
    print(delta)
    return (delta, result)

def set_interval(is_interval_min):
    interval = ""
    if is_interval_min:
        interval = "_min"
    return interval

def get_data(Stock, key, is_interval_min):
    interval = set_interval(is_interval_min)
    time_delta_more = relativeDelta(key, interval)
    time_delta = time_delta_more[0]
    dateInThePast = currentdate - relativedelta(days=time_delta)
    key = key.replace("/", "_")
    if time_delta_more[1][0]: #replace with time_delta_more[1] <-> is_data_already_read(key, interval)
        data_old = pd.read_pickle(f"{dir_path}/data/{key}{interval}.pkl")
        data_new = yf.download(Stock, end=str(currentdate), start=str(dateInThePast))
        frames = [data_old, data_new]
        data = pd.concat(frames)
        print("data red and merged")
    elif time_delta_more[1] != None:
        data = yf.download(Stock, end=str(currentdate), start=str(dateInThePast))
        print("data loaded the first time")
    save_data(data, key, interval)
    

def get_indicators(data):    # Get MACD
    
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])
    
    # Get MA10 and MA30
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma20"] = talib.MA(data["Close"], timeperiod=20)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)
    data["ma50"] = talib.MA(data["Close"], timeperiod=50)
    
    # Get SMA20 and SMA50
    data["sma20"] = talib.SMA(data["Close"], timeperiod=20)
    data["sma50"] = talib.SMA(data["Close"], timeperiod=50)
    
    # Get RSI
    data["rsi"] = talib.RSI(data["Close"])  
    return data

def plot_chart(n: list, ticker: str, is_interval_min):
    interval = set_interval(is_interval_min)
    data = is_data_already_read(ticker, interval)[2]
    # Filter number of observations to plot
    if n[1] == None:
        data = data.iloc[-int(n[0]):]
    else:
        data = data.iloc[-int(n[0]):-int(n[1])]
    
    # Create figure and set axes for subplots
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    fig.suptitle(f"This is the Analysis of {ticker}.")
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)
    
    # Format x-axis ticks as dates
    ax_candle.xaxis_date()
    
    # Get nested list of date, open, high, low and close prices
    ohlc = []
    dates = []
    for date, row in data.iterrows():
        # print(row[:5])
        openp, highp, lowp, closep = row[:4]
        # print(date)
        # date = datetime.strptime(date, "%Y-%m-%d")
        dates.append(date2num(date))
        ohlc.append([date2num(date), openp, highp, lowp, closep])
 
    # Plot candlestick chart
    # ax_candle.plot(dates, data["ma10"], label="MA10")
    # ax_candle.plot(dates, data["ma20"], label="MA20")
    # ax_candle.plot(dates, data["ma30"], label="MA30")
    # ax_candle.plot(dates, data["ma50"], label="MA50")
    ax_candle.plot(dates, data["sma20"], label="SMA20")
    ax_candle.plot(dates, data["sma50"], label="SMA50")
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)
    ax_candle.legend()
    
    # Plot MACD
    ax_macd.plot(dates, data["macd"], label="macd")
    ax_macd.bar(dates, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(dates, data["macd_signal"], label="signal")
    ax_macd.legend()
    
    # Plot RSI
    # Above 70% = overbought, below 30% = oversold
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(dates, [70] * len(data.index), label="overbought")
    ax_rsi.plot(dates, [30] * len(data.index), label="oversold")
    ax_rsi.plot(dates, data["rsi"], label="rsi")
    ax_rsi.legend()
    
    # Show volume in millions
    ax_vol.bar(dates, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")
   
    # Save the chart as SVG
    fig.savefig(f"{dir_path}/charts/{ticker}{interval}.svg", bbox_inches="tight")
    
    plt.show()

def handleStocks(add = False, single = False, inputSingle = "", inputList="empty"):
    currentStocks = load_stocks()
        
    newStocks = []
    if single == False:
        if inputList != "empty":
            print("using List generated by the Program -> inputList")
            newStocks = [(i + "; ").split(";") for i in inputList]
            print(newStocks, len(newStocks))
            input("Press enter to continue!")
        else:
            with open(f"{dir_path}/data/Yahoo_Ticker.txt","r") as f:
                for line in f:
                    stock = [i.strip() for i in line.split(";")]
                    newStocks.append(stock)
    else:
        stock = [i.strip() for i in inputSingle.split(";")]
        newStocks.append(stock)
    saveIsNeeded = False
    if add == True:
        for newStock in newStocks:
            if newStock[0] == "":
                print(f"Stock include no name. Stock: {newStock}")
            elif newStock[0] not in currentStocks:                              
                currentStocks[newStock[0]] = newStock[1]
                print(f"added: {newStock}")
                saveIsNeeded = True                         
            else:
                print(f"Stock is already included. Stock: {newStock}")
    else:
        for newStock in newStocks:
            if newStock[0] == "":
                pass
            elif newStock[0] not in currentStocks:
                print(f"stock: {newStock} can't be deleted. It is not included.")
            else:
                currentStocks.pop(newStock[0])
                for interval in ["", "_min"]:
                    try:
                        os.remove(f"{dir_path}/data/{newStock[0].replace('/', '_')}{interval}.pkl")
                        print(f"removed file. Stock: {newStock} interval: {interval}")
                    except FileNotFoundError:
                        print(f"file is not existing. Stock: {newStock} interval: {interval}")
                print(f"removed: {newStock}")
                saveIsNeeded = True
    if saveIsNeeded:
        print(f"Saving Stocks!")
        save_stocks(currentStocks)

def amount_of_stocks():
    currentStocks = load_stocks()
    amountOfStocks = len(currentStocks)
    return amountOfStocks

def checkIfFileForStock():
    currentStocks = load_stocks()
    readyToDelete = []
    for key in currentStocks:
        check = key.replace("/", "_")
        delete = True
        for fileInData in filesInData:
            if check == fileInData.replace(".pkl", ""):
                delete = False
                break
        if delete:
            print(f"add {key} to delete list!")
            readyToDelete.append(key)
    print(readyToDelete)
    handleStocks(inputList=readyToDelete)
    
def check_loaded_files():
    countEmptyFiles = 0
    stocksToDelete = []
    startTime = time.time()
    for file in filesInData:
        # print(".txt".lower() not in file or ".pickl".lower() not in file.lower())
        if ".pkl".lower() in file:
            try:
                data = pd.read_pickle(f"{dir_path}/data/{file}")
                datetime.strptime(str(data.index[-1])[0:10], '%Y-%m-%d').date()
                if os.path.getsize(f"{dir_path}/data/{file}") <= 700:
                    print(f"File is not empty: {file}")
                    print(os.path.getsize(f"{dir_path}/data/{file}"))
            except IndexError:
                countEmptyFiles += 1
                print(f"File is empty: {file}")
                print(os.path.getsize(f"{dir_path}/data/{file}"))
                key = file.replace("_", "/").replace(".pkl", "")
                stocksToDelete.append(key)
                
            except AttributeError:
                print(f"AttributeError cached!")
                print(f"file: {file}, size: " + str(os.path.getsize(f"{dir_path}/data/{file}")))
            except:
                print(f"_pickle.UnpicklingError: invalid load key file: {file}")
        else:
            print(f"file: {file}")
    handleStocks(inputList=stocksToDelete)
    print(f"Ammount of empty Files: {countEmptyFiles}")
    print(time.time() - startTime)    
        
def save_stocks(stocks):
    '''saves'''   
    with open(f"{dir_path}/data/stocks.pickl","wb") as f:   
        pickle.dump(stocks, f)

def load_stocks():
    try:
        with open(f"{dir_path}/data/stocks.pickl","rb") as f:
                stocks = pickle.load(f) 
    except:
        save_stocks(currentStocks)
        with open(f"{dir_path}/data/stocks.pickl","rb") as f:
                stocks = pickle.load(f) 
    # print(stocks)
    return stocks
    
print("hallo World")