import sys
sys.path.insert(0,'/home/karthikeyan/vscode/TA/tradingautomationindicators')

from  lib.load import *
from lib.indicators import *
from datetime import *
import datetime as dt
import time as times
from yahoo_fin import stock_info as si 

# def find_hundrend(price):
#     strike=[]
#     if(price%100 >51):
#         strike.append((price-(price%100))+100)
#         strike.append(price-(price%100))
#     elif(price%100 <=51):
#         strike.append((price-(price%100)))
#         strike.append((price-(price%100))+100)
#     return strike

# symbol=""
# kite.quote("NFO:"+symbol)

volume=[1,11,2,4,4,3,2,4,5,6,6,6,6,6,55,4,3,33,8,8,8,8,7,76,5,54,4,22,66,5,5,33,6,4,2,35,3,2]
volume=pd.DataFrame({"volume" :volume})
sma20=volume.rolling(20).mean()

vol_pt=volume['volume'][len(volume)-1]
sma20_pt=sma20['volume'][len(sma20)-1]
if(vol_pt>1.9(sma20_pt)):
    pass
else:
    pass
