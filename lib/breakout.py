from load import *
import pandas as pd
import openpyxl

def find_hundrend(price):
    strike=[]
    if(price%100 >51):
        strike.append((price-(price%100))+100)
        strike.append(price-(price%100))
    elif(price%100 <=51):
        strike.append((price-(price%100)))
        strike.append((price-(price%100))+100)
    return strike
    
break_above=0
break_down=0

var=pd.read_excel("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
wb_obj = openpyxl.load_workbook("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
sheet_obj = wb_obj.active
if(var['disperative'][24]<var['sma_7'][24] and var['disperative'][24]<var['sma_7'][24]):
    break_above=1
else:
    break_down=1

for i in range(25,len(var.index)-1):
    if (break_above==1 and var['disperative'][i]>var['sma_7'][i] and var['disperative']>0):
        break_down=1
        break_above=0
        sheet_obj["L"+str(i+2)].value=var['disperative'][i]
        # 5min indicators
        
    elif (break_down==1 and var['disperative'][i]<var['sma_7'][i] and var['disperative']>0):
        break_down=0
        break_above=1
        sheet_obj["L"+str(i+2)].value=var['disperative'][i]
        #5min indicator
        
wb_obj.save("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
        
