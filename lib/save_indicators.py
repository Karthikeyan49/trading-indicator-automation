import yfinance as yf
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import pandas as pd

def get_di(data, lookback):
    ma = data.rolling(lookback).mean()
    di = ((data - ma) / ma) * 100
    return di

df = yf.download("^NSEI", start="2024-01-25", end="2024-02-20", interval="30m").reset_index()

disperative_index=get_di(pd.DataFrame({"disperative" :list(df['Close'])}),14)
moving_average_9= disperative_index.rolling(9).mean()
moving_average_7= disperative_index.rolling(7).mean()
moving_average_7.rename(columns = {'disperative':'sma_7'}, inplace = True)
moving_average_9.rename(columns = {'disperative':'sma_9'}, inplace = True) 

xl=pd.concat([df,moving_average_7,moving_average_9,disperative_index],axis=1)

xl.to_csv('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/file1.csv')

df_new = pd.read_csv('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/file1.csv')

GFG = pd.ExcelWriter('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx')
df_new.to_excel(GFG, index=False)
GFG.save()


