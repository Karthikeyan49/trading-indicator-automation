from yahoo_fin import stock_info
import yfinance as yf
import matplotlib.pyplot as plt
df = yf.download("^NSEI", start="2024-05-15", end="2023-07-08", interval="30m")
df.to_csv('file1.csv')
import pandas as pd
df_new = pd.read_csv('file1.csv')
 
# saving xlsx file
GFG = pd.ExcelWriter('nifty.xlsx')
df_new.to_excel(GFG, index=False)
 
GFG.save()

path = "/home/karthikeyan/vscode/python/5-15 TO 7-8.xlsx"
wb_obj = openpyxl.load_workbook(path)
sheet_obj = wb_obj.active
import openpyxl
sheet_obj["C"+str(i)].value
wb_obj.save(path)

var=pd.read_excel("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
plt.plot(var['Datetime'],var['Close'])
plt.title('AAPL Closing Prices')
plt.show()