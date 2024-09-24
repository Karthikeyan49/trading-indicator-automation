import sys
import os 
working_dir=os.getcwd()
sys.path.insert(0,str(working_dir)+'/tradingautomationindicators')

from  lib.load import *
from lib.indicators import *
from datetime import *
import datetime as dt
import time as times
from yahoo_fin import stock_info as si 

def opt_cret(strike,from_date,now):
    
    df=kite.historical_data(kite.ltp('NSE:'+strike)['NSE:'+strike]["instrument_token"],from_date,now,"5minute",oi=1)
    df=pd.DataFrame(df)
    x=0
    time=1
    
    # vwap
    while(True):
        data=df.tail(1)
        vwap_data=[data['High'],data['Low'],data['Close'],data['Volume']]
        vwap=vwap_ind(vwap_data)
        if(vwap<data['High'] and vwap<data['Low'] and vwap<data['Close'] and vwap<data['open']):
            x=x+1
            break
        else:
            pass
        times.sleep(300)
        time=time+1
        df=kite.historical_data(kite.ltp('NSE:'+strike)['NSE:'+strike]["instrument_token"],from_date,now,"5minute",oi=1)
        df=pd.DataFrame(df)
    
    
    #rsi
    rsi=calculate_rsi(df['Close'])
    if(rsi[len(rsi)-1]>60):
        x=x+1
    else:
        pass
    df=kite.historical_data(kite.ltp('NSE:'+strike)['NSE:'+strike]["instrument_token"],from_date,now,"5minute",oi=1)
    df=pd.DataFrame(df)
         
    #oi
    while(True):
        oi=df.tail(1)['oi']
        sma_oi=df.rolling(20).mean()['oi']
        sma_oi=sma_oi.tail(1)['oi']

        if(oi>sma_oi):
            x=x+1
            break
        else:
            pass
        df=kite.historical_data(kite.ltp('NSE:'+strike)['NSE:'+strike]["instrument_token"],from_date,now,"5minute",oi=1)
        df=pd.DataFrame(df)
        
    # volume
    while(True): 
        volume=df.tail(1)['volume']
        sma_v=df.rolling(20).mean()['volume']
        sma_v=sma_v.tail(1)['volume']

        if(volume>1.9(sma_v)):
            x=x+1
            break
        else:
            pass
        df=kite.historical_data(kite.ltp('NSE:'+strike)['NSE:'+strike]["instrument_token"],from_date,now,"5minute",oi=1)
        df=pd.DataFrame(df)
    
    
    if(x==5):
        email_alert("alter",str(strike)+"nifty","")
    
    
    
    
def di_breakout():
    global close,dis,sma_7
    close.append(si.get_live_price("^NSEI"))
    close.pop(0)
    temp=get_di(pd.DataFrame({"close":close}),14)
    temp=temp.values.tolist()
    dis.pop(0)
    dis.append(temp[29][0])
    dis_temp=pd.DataFrame({"sma" :dis})
    sma_7=dis_temp.rolling(7).mean()
    sma_7=sma_7.values.tolist()
    if(dis[13]<0):
        if(sma_7[13][0]>dis[13]):
            return 1
        else:
            return 10
    elif(dis[13]>0):
        if(sma_7[13][0]<dis[13]):
            return 0
        else:
            return 10
    

now=date.today()
pre=date.today()-(dt.timedelta(8))
df=yf.download("^NSEI", start=pre, end=now, interval="1d").reset_index()
from_date=str(df['Date'][(len(df.index))-3])
from_date=from_date[0:10]

set_access_token()
authenticate()

df = yf.download("^NSEI", start=from_date, end=now, interval="30m").reset_index()

disperative_index=get_di(pd.DataFrame({"disperative" :list(df['Close'])}),14)
moving_average_9= disperative_index.rolling(9).mean()
moving_average_7= disperative_index.rolling(7).mean()
moving_average_7.rename(columns = {'disperative':'sma_7'}, inplace = True)
moving_average_9.rename(columns = {'disperative':'sma_9'}, inplace = True)

xl=pd.concat([df,moving_average_7,moving_average_9,disperative_index],axis=1)

close=list(xl.tail(30)['Close'])
dis=list(xl.tail(14)['disperative'])
sma_7=float(xl.tail(1)['sma_7']) 
sma_9=float(xl.tail(1)['sma_9'])

while True:
    now = datetime.now()
    if now.hour==9 and now.minute==29 and now.second==58:
        breakout=di_breakout()
        if(breakout==1):
            break
        elif(breakout==0):
            break
        elif(breakout==10):
            break

def main():
   while True:
        di_breakout()
        times.sleep(1800)  

if __name__ == "__main__":
    main()