import sys
import os 

working_dir=os.getcwd()
sys.path.insert(0,str(working_dir)+'/tradingautomationindicators')

from  lib.load import *
from lib.indicators import *
from datetime import *
import datetime as dt
import time as times
import threading

time=datetime.time()  

authenticate()

set_access_token()


class alerts:
    close=list()
    dis=list()
    sma_7=list()
    from_date=date.today()
    now=date.today()
    strike=""
    instrument_token=""
    event1=0
    initial=1
    thread_two= threading.Thread()
    thread_one= threading.Thread()

    index=""
    ind_name=""
    
    def ind(self, indx,indname):
        global index,ind_name
        index=indx
        ind_name=indname
        

    def di(self):
        global close,dis,sma_7,instrument_token,thread_two,thread_one,index,ind_name
        now=date.today()
        pre=date.today()-(dt.timedelta(10))

        instrument_token=kite.ltp("NSE:"+index)["NSE:"+index]["instrument_token"]

        df_last=kite.historical_data(instrument_token,pre,now,"day",oi=1)

        from_date=df_last[len(df_last)-5]['date']
        df=kite.historical_data(instrument_token,from_date,now,"30minute",oi=1)

        df=pd.DataFrame(df)
        disperative_index=get_di(pd.DataFrame({"disperative":list(df['close'])}),21)
        moving_average_7= disperative_index.rolling(7).mean()
        moving_average_7.rename(columns = {'disperative':'sma_7'}, inplace = True)

        xl=pd.concat([df,moving_average_7,disperative_index],axis=1)

        close=list(xl.tail(30)['close'])
        dis=list(xl.tail(7)['disperative'])
        sma_7=float(xl.tail(1)['sma_7']) 
        
        while True:
            now_time = datetime.now_time()
            if (now_time.hour==9 and now_time.minute==29 and now_time.second==58):
                breakout=self.di_breakout()
                if(breakout==1):
                    #ce
                    strike=get_strike("CE",index,ind_name)
                    self.opt_cret(strike,from_date,now_time)
                    break
                elif(breakout==0):
                    # pe
                    strike=get_strike("PE",index,ind_name)
                    self.sma_7opt_cret(strike,from_date,now_time)
                    break
                elif(breakout==10):
                    break

        thread_one = threading.Thread(target=self.di_break_condition)
        thread_two = threading.Thread(target=self.opt_cret,args=(strike,))

        thread_one.start()
        
    def di_breakout(self):
        global close,dis,sma_7,instrument_token
        
        df=kite.historical_data(instrument_token,self.from_date,self.now,"30minute",oi=1)
        df=pd.DataFrame(df)
        d=df.tail(1)
        close.append(d['close'])
        close.pop(0)
        temp=get_di(pd.DataFrame({"close":close}),21)
        temp=temp.values.tolist()
        dis.pop(0)
        dis.append(temp[len(temp)-1][0])
        dis_temp=pd.DataFrame({"sma" :dis})
        sma_7_temp=dis_temp.rolling(7).mean()
        sma_7_temp=sma_7_temp.values.tolist()
        sma_7=sma_7_temp[len(sma_7_temp)-1][0]
        # ce
        if(dis[len(dis)-1]<0):
            if(sma_7>dis[len(dis)-1]):
                return 1
            else:
                return 10
        # pe
        elif(dis[len(dis)-1]>0):
            if(sma_7<dis[len(dis)-1]):
                return 0
            else:
                return 10
            
    def di_break_condition(self):
        while True:
            global strike,thread_two,event1,initial,thread_two,index,ind_name
            times.sleep(1800)
            breakout=self.di_breakout()
            
            if(initial==1):
                if(breakout==1):
                    strike=get_strike("CE",index,ind_name)
                    thread_two = threading.Thread(target=self.opt_cret,args=(strike,))
                    thread_two.start(strike)
                elif(breakout==0):
                    strike=get_strike("PE",index,ind_name)
                    thread_two = threading.Thread(target=self.opt_cret,args=(strike,))
                    thread_two.start(strike)
                elif(breakout==10):
                    pass
                initial=0
                
            else:    
                if(breakout==1):
                    strike=get_strike("CE",index,ind_name)
                    event1=1
                    while(event1==0):
                        thread_two = threading.Thread(target=self.opt_cret,args=(strike,))
                        thread_two.start(strike)
                elif(breakout==0):
                    strike=get_strike("PE",index,ind_name)
                    event1=1
                    while(event1==0):
                        thread_two = threading.Thread(target=self.opt_cret,args=(strike,))
                        thread_two.start(strike)
                elif(breakout==10):
                    pass
            
    def opt_cret(self,strike_p,from_date_p=from_date,now_p=now):
            global event1
            df=kite.historical_data(kite.ltp('NSE:'+strike_p)['NSE:'+strike_p]["instrument_token"],from_date_p,now_p,"5minute",oi=1)
            df=pd.DataFrame(df)
            x=0
            
            # vwap
            while(event1==0):
                data=df.tail(1)
                vwap_data=[data['high'],data['low'],data['close'],data['volume']]
                vwap=vwap_ind(vwap_data)
                if(vwap<data['high'] and vwap<data['low'] and vwap<data['close'] and vwap<data['open']):
                    x=x+1
                    break
                else:
                    pass
                times.sleep(300)
                df=kite.historical_data(kite.ltp('NSE:'+strike_p)['NSE:'+strike_p]["instrument_token"],from_date_p,now_p,"5minute",oi=1)
                df=pd.DataFrame(df)
            
            #rsi
            rsi=calculate_rsi(df['close'])
            if(rsi[len(rsi)-1]>60):
                x=x+1
            else:
                pass
            if(event1==0):
                times.sleep(300)
                df=kite.historical_data(kite.ltp('NSE:'+strike_p)['NSE:'+strike_p]["instrument_token"],from_date_p,now_p,"5minute",oi=1)
                df=pd.DataFrame(df)
                
            #oi
            while(event1==0):
                oi=df.tail(1)['oi']
                sma_oi=df.rolling(20).mean()['oi']
                sma_oi=sma_oi.tail(1)['oi']

                if(oi>sma_oi):
                    x=x+1
                    break
                else:
                    pass
                times.sleep(300)
                df=kite.historical_data(kite.ltp('NSE:'+strike_p)['NSE:'+strike_p]["instrument_token"],from_date_p,now_p,"5minute",oi=1)
                df=pd.DataFrame(df)
                
            # volume
            while(event1==0): 
                volume=df.tail(1)['volume']
                sma_v=df.rolling(20).mean()['volume']
                sma_v=sma_v.tail(1)['volume']

                if(volume>1.9(sma_v)):
                    x=x+1
                    break
                else:
                    pass
                times.sleep(300)
                df=kite.historical_data(kite.ltp('NSE:'+strike_p)['NSE:'+strike_p]["instrument_token"],from_date_p,now_p,"5minute",oi=1)
                df=pd.DataFrame(df)
            
            if(event1==1):
                event1=0
        
            if(x==4):
                email_alert("alter",str(strike_p)+"nifty","")
        



nifty=alerts()
nifty.ind('NIFTY 50','NIFTY')

banknifty=alerts()
banknifty.ind('NIFTY BANK','BANKNIFTY')

finnifty=alerts()
finnifty.ind('NIFTY FIN SERVICE','FINNIFTY')


def nifty_50():
    while(True):
        nifty.di()

def bank_nifty():
    while(True):
        banknifty.di()
  
def fin_nifty():        
    while(True):
        finnifty.di()
        
        
thread_nifty=threading.Thread(target=nifty_50)
thread_banknifty=threading.Thread(target=bank_nifty)
thread_finnifty=threading.Thread(target=fin_nifty)

thread_nifty.start()
thread_banknifty.start()
thread_finnifty.start()
    