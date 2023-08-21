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
    ticker_list = ['PLTR','SPY','QQQ','TQQQ','SQQQ','A','AAL','AAP','AAPL','ABBV','ABC','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP',
                   'AZO','BA','BAC','BAX','BBWI','BBY','BDX','BEN','BF.B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK.B','BRO','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT'
                   'B','COE','CBRE','CCI','CCL','CDAY','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNC','CNP','COF','COO',
                   'COP','COST','CPB','CPRT','CRL','CRM','CSCO','CSX','CTAS','CTLT','CTRA','CTSH','CTVA','CTXS','CVS','CVX','CZR','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS',
                   'DISCA','DISCK','DISH','DLR','DLTR','DOV','DOW','DPZ','DRE','DRI','DTE','DUK','DVA','DVN','DXC','DXCM','EA','EBAY','ECL','ED','EFX','EIX','EL','EMN','EMR','ENPH','EOG','EQIX',
                   'EQR','ES','ESS','ETN','ETR','ETSY','EVRG','EW','EXC','EXPD','EXPE','EXR','F','FANG','FAST','FB','FBHS','FCX','FDX','FE','FFIV','FIS','FISV','FITB','FLT','FMC','FOX','FOXA',
                   'FRC','FRT','FTNT','FTV','GD','GE','GILD','GIS','GL','GLW','GM','GNRC','GOOG','GOOGL','GPC','GPN','GPS','GRMN','GS','GWW','HAL','HAS','HBAN','HBI','HCA','HD','HES','HIG',
                   'HII','LT','HOLX','HON','HPE','HPQ','HRL','HSIC','HST','HSY','HUM','HWM','IBM','ICE','IDXX','IEX','IFF','ILMN','INCY','INFO','INTC','INTU','IP','IPG','IPGP','IQV','IR',
                   'IRM','ISRG','IT','ITW','IVZ','J','JBHT','JCI','JKHY','JNJ','JNPR','JPM','K','KEY','KEYS','KHC','KIM','KLAC','KMB','KMI','KMX','KO','KR','KSU','L','LDOS','LEG','LEN','LH',
                   'LHX','LIN','LKQ','LLY','LMT','LNC','LNT','LOW','LRCX','LUMN','LUV','LVS','LW','LYB','LYV','MA','MAA','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MGM','MHK',
                   'MKC','KTX','MLM','MMC','MMM','MNST','MO','MOS','MPC','MPWR','MRK','MRNA','MRO','MS','MSCI','MSFT','MSI','MTB','MTCH','MTD','MU','NCLH','NDAQ','NEE','NEM','NFLX','NI','NKE',
                   'NLOK','NLSN','NOC','NOW','NRG','NSC','NTAP','NTRS','NUE','NVDA','NVR','NWL','NWS','NWSA','NXPI','O','ODFL','OGN','OKE','OMC','ORCL','ORLY','OTIS','OXY','PAYC','PAYX','PBCT',
                   'PCAR','PEAK','PEG','PENN','PEP','PFE','PFG','PG','PGR','PH','PHM','PKG','PKI','PLD','PM','PNC','PNR','PNW','POOL','PPG','PPL','PRU','PSA','PSX','PTC','PVH','PWR','PXD','PYPL',
                   'QCOM','QRVO','RCL','RE','REG','REGN','RF','RHI','RJF','RL','RMD','ROK','ROL','ROP','ROST','RSG','RTX','SBAC','SBUX','SCHW','SEE','SHW','SIVB','SJM','SLB','SNA','SNPS','SO',
                   'SPG','SPGI','SRE','STE','STT','STX','STZ','SWK','SWKS','SYF','SYK','SYY','T','TAP','TDG','TDY','TECH','TEL','TER','TFC','TFX','TGT','TJX','TMO','TMUS','TPR','TRMB','TROW','TRV','TSCO','TSLA','TSN','TT','TTWO',
                   'TXN','TXT','TYL','UA','UAA','UAL','UDR','UHS','ULTA','UNH','UNP','UPS','URI','USB','V','VFC','VIAC','VLO','VMC','VNO','VRSK','VRSN','VRTX','VTR','VTRS','VZ','WAB','WAT','WBA','WDC','WEC','WELL','WFC','WHR','WLTW','WM','WMB','WMT','WRB','WRK','WST','WU','WY','WYNN','XEL','XLNX','XOM','XRAY','XYL','YUM','ZBH','ZBRA','ZION','ZTS']
                 
    list_consolidated = []

    #function to check if the Stock has been consolidating for last 15 days
    def is_consolidating(ticker,df,percentage = 2):
        threshhold = 1 - (percentage / 100)
        recent_closes = df[-15:]['Close']
        recent_volume = df[-15:] ['Volume']
        recent_volume_avg = recent_volume.mean()
        recent_closes_max = recent_closes.max()
        recent_closes_min = recent_closes.min()
        current_price = df['Close'].iloc[-1]
        print(current_price)
        
        if recent_closes_min > (recent_closes_max * threshhold):
            Cons_Dictionary = {'Ticker':ticker,'range':recent_closes_min/recent_closes_max,'Max':recent_closes_max,'Min':recent_closes_min,
                               'Current':current_price,'Volume':recent_volume_avg,'Max-Current':recent_closes_max-current_price }
            list_consolidated.append(Cons_Dictionary)

    # Email
    def send_mail(body):
        message = MIMEMultipart()
        message['Subject'] = 'Consolidating Stocks for the day'
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
    
    def send_consolidation_list():
        consolidated_stocks_df = pd.DataFrame.from_records(list_consolidated)
        consolidated_stocks_df.sort_values(by="range",ascending=True)
        output = build_table(consolidated_stocks_df, 'blue_light')
        send_mail(output)
    
    for ticker in ticker_list:
        start = dt.datetime.now() + dt.timedelta(days= -15) 
        now = dt.datetime.now()  
        data = yf.download(ticker, start=start, end=now)
        
        if not data.empty:
            is_consolidating(ticker,data,2)
    
    send_consolidation_list()
