#!/usr/bin/env python
# coding: utf-8

# In[41]:


import requests
from bs4 import BeautifulSoup
from FinMind.data import DataLoader
import datetime
from dateutil.relativedelta import relativedelta

def line(data, stockid, name):
    url = 'https://notify-api.line.me/api/notify'
    token = '4wYKot7VvCa57AyWpakDh8i8YpklEdzD8ncTOahmUPw'
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    requests.post(url, headers=headers, data=data)
    
def stock(stockid,name):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockid}.TW'
        resp = requests.get(url)
    except:
        url = f'https://tw.stock.yahoo.com/quote/{stockid}.TWO'
        resp = requests.get(url)
        
    soup = BeautifulSoup(resp.text, "html.parser")    
    a = soup.select('.Fz\(32px\)')[0]
    y = float(a.text)

    x=datetime.datetime.now()
    start=(x- relativedelta(months=11)).strftime("%Y-%m-%d")

    dl = DataLoader()
    df = dl.taiwan_stock_daily(stock_id=stockid ,start_date=start)

    x = list(df["close"])

    ma = max(x)
    mi = min(x)
    high = ((ma-mi)/4+mi)*1.1
    low = ((ma-mi)/4+mi)*0.9
    if y >= high :
        data = {
            'message': 
            "\n"+
            f'{stockid}{name}'+'\n'+
            f'股價已漲至{y}元'
        }
        line(data, stockid, name)
    elif y <= low :
        data = {
            'message': 
            "\n"+
            f'{stockid}{name}'+'\n'+
            f'股價已跌至{y}元'
        }
        line(data, stockid, name)

#stock('2313','華通')
#stock('6415','矽力KY')
