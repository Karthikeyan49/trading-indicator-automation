import yfinance as yf
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
from matplotlib import style

def get_di(data, lookback):
    ma = data.rolling(lookback).mean()
    di = ((data - ma) / ma) * 100
    return di

# df = yf.download("^NSEI", start="2024-01-15", end="2024-01-30", interval="30m")
# df.to_csv('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/file1.csv')

# df_new = pd.read_csv('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/file1.csv')

# GFG = pd.ExcelWriter('/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx')
# df_new.to_excel(GFG, index=False)
# GFG.save()

# path = "/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx"
# wb_obj = openpyxl.load_workbook(path)
# sheet_obj = wb_obj.active

var=pd.read_excel("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
a=pd.DataFrame({"dis" :list(var['disperative']),"sma7" :list(var['sma_7']),"sma9" :list(var['sma_9'])})
# n=a.rolling(14).mean()
# r=pd.concat([a,n],axis=1)
# print(r)
plt.plot(var['Datetime'],a)
plt.plot(var['Datetime'],var['Unnamed: 11'],marker="x")
plt.title('nifty') 
plt.show()