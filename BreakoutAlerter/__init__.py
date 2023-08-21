import datetime as dt
import logging

import azure.functions as func
import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
import numpy as np

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pretty_html_table import build_table

def main(mytimer: func.TimerRequest) -> None:
    shortlist = pd.read_csv('https://mkcstocks.blob.core.windows.net/mkcstocks/consolidated.csv?sp=r&st=2023-08-21T00:49:40Z&se=2026-08-21T08:49:40Z&spr=https&sv=2022-11-02&sr=b&sig=JpoEQJ%2BCTFIgVswuuOPqJ98QasLw6xaa4gSUdv60VI8%3D')
    print(shortlist[['Ticker','Min','Max']])

    listalerts=[]
   
    def send_mail(body):
        message = MIMEMultipart()
        message['Subject'] = 'Breakout Stocks for the day'
        message['From'] = 'kc.milan.it@gmail.com'
        message['To'] = 'kc.milan.it@gmail.com'

        body_content = body
        message.attach(MIMEText(body_content, "html"))
        msg_body = message.as_string()

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], 'dzzlkoqqswozcdtl')
        server.sendmail(message['From'], message['To'], msg_body)
        server.quit()

    for index, row in shortlist.iterrows():
        start = dt.datetime.now() + dt.timedelta(days= -4) 
        now = dt.datetime.now()  

        data = yf.download(row['Ticker'], start=start, end=now)
        current_price = data.tail(1)['Close'].item()

        if (row['Min']>current_price):
            Cons_Dictionary = {'Ticker':row['Ticker'],'MinMax':row['Min'],'Current':current_price,'Direction':'Down'}
            listalerts.append(Cons_Dictionary)
        
        if (row['Max']<current_price):
            Cons_Dictionary = {'Ticker':row['Ticker'],'MinMax':row['Max'],'Current':current_price,'Direction':'Up'}
            listalerts.append(Cons_Dictionary)
    
    def send_breakout_list():
        if(len(listalerts)) > 0:
            breakout_stocks_df = pd.DataFrame.from_records(listalerts)
            output = build_table(breakout_stocks_df, 'blue_light')
            send_mail(output)

    send_breakout_list()   
