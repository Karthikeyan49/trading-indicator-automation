from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import webbrowser
import json
from datetime import *
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os
from dateutil.relativedelta import relativedelta, TH
import smtplib
from email.message import EmailMessage


working_dir=os.getcwd()
file=open(str(working_dir)+'/trading automation data/data.json','r')    
api_info=json.load(file)

kite = KiteConnect(api_key=api_info["api_key"])

def get_api_config(key):
    return api_info[key]

def set_access_token():
    kite.set_access_token(api_info["access_token"])

def set_kws():
    global kws
    kws = KiteTicker(api_info["api_key"], api_info["access_token"])
    
def authenticate():
    it=webbrowser.open_new_tab(kite.login_url())
    request_token=input("enter the token : ")
    data = kite.generate_session(request_token, api_secret=get_api_config("api_secret"))
    access_token=data['access_token']
    file=open(str(working_dir)+'/trading automation data/data.json','r')    
    api_info=json.load(file)
    file.close()
    api_info["access_token"]=access_token
    file=open(str(working_dir)+'/trading automation data/data.json','w')    
    json.dump(api_info,file)
    file.close()
    return access_token

def find_expire():
    days_ahead = 3 - date.today().weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    return  date.today() + datetime.timedelta(days_ahead)

def find_hundrend(price):
    strike=[]
    if(price%100 >51):
        strike.append((price-(price%100))+100)
        strike.append(price-(price%100))
    elif(price%100 <=51):
        strike.append((price-(price%100)))
        strike.append((price-(price%100))+100)
    return strike

def get_thurs(dt):
    return dt + relativedelta(day=31, weekday=TH(-1))

def get_strike(s,index,ind):
    set_access_token()

    expire=find_expire()
    day=""
    strike=""

    month={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}

    if(expire==get_thurs(date.today())):
        exp_last=month[expire.month]
        strike=ind+str(expire.year)[2:4]+str(exp_last)+str(find_hundrend(int(kite.ltp("NSE:"+index)["NSE:"+index]['last_price']))[0])+s
        return strike   
    else:
        if(expire.day<10):
            day="0"+str(expire.day)
        else:
            day=str(expire.day)    
        
        strike=ind+str(expire.year)[2:4]+str(expire.month)+day+str(find_hundrend(int(kite.ltp("NSE:"+index)["NSE:"+index]['last_price']))[0])+s
        return strike
    

    
def email_alert(subject, body, to):

    msg = EmailMessage()

    msg.set_content(body)

    msg['subject'] = subject

    msg['to'] = to

    user = "tradeproject.0342@gmail.com"

    password = "#$345/14"

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(user, password)

    server.quit()

    