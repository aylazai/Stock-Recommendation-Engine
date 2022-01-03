# %%
import sqlalchemy
import pymysql
import ta
import pandas as pd
import numpy as np
import yfinance as yf

# %%
pymysql.install_as_MySQLdb()

# %%

class Recommender:
    engine = sqlalchemy.create_engine('mysql://root:Shift777@localhost:3306/')

    #constructer that provides index
    def __init__(self, index):
        self.index = index

    #Takes tables from the MySQL Database
    def gettables(self):
        query = f"""SELECT table_name FROM information_schema.tables 
        WHERE table_schema = '{self.index}'"""
        df = pd.read_sql(query, self.engine)
        df['Schema'] = self.index 
        return df

    #Pulls prices
    def getprices(self):
        prices = [] #creates empty list
        for table, schema in zip(self.gettables().TABLE_NAME, self.gettables().Schema):
            sql = schema+'.'+f'`{table}`' #must account for dot inside tables names
            prices.append(pd.read_sql(f"SELECT Date, Close FROM {sql}", self.engine)) #you can inlcude other columns here
        return prices

    def maxdate(self):
        sql = self.index+'.'+f'`{self.gettables().TABLE_NAME[0]}`' #must account for dot inside tables names
        return pd.read_sql(f"SELECT MAX(Date) FROM {sql}", self.engine) 

    def updateDB(self):
        maxdate = self.maxdate()['MAX(Date)'][0]
        engine = sqlalchemy.create_engine('mysql://root:Shift777@localhost:3306/' +self.index)
        for symbol in self.gettables().TABLE_NAME:
            data = yf.download(symbol, start=maxdate)
            data = data[data.index > maxdate]
            data = data.reset_index()
            data.to_sql(symbol, engine, if_exists='append')
        print(f'{self.index} successfully updated')
    
    #the following are technical indicators
    def MACDdecision(self,df):
        df['MACD_diff'] = ta.trend.macd_diff(df.Close)
        df['Decision MACD'] = np.where((df.MACD_diff > 0) & (df.MACD_diff.shift(1) < 0), True, False)
        
    def Goldencrossdecision(self, df):
        df['SMA20'] = ta.trend.sma_indicator(df.Close, window=20)
        df['SMA50'] = ta.trend.sma_indicator(df.Close, window=50)
        df['Signal'] = np.where(df['SMA20'] > df["SMA50"], True, False)
        df['Decision GC'] = df.Signal.diff() 
    
    def RSI_SMAdecision(self, df):
        df['RSI'] = ta.momentum.rsi(df.Close, window=10)
        df['SMA200'] = ta.trend.sma_indicator(df.Close, window=200)
        df['Decision RSI/SMA'] = np.where((df.Close > df.SMA200) & (df.RSI < 30), True, False)

    #technical indicators are applied to these prices
    def applytechnicals(self):
        prices = self.getprices()
        for frame in prices:
            self.MACDdecision(frame)
            self.Goldencrossdecision(frame)
            self.RSI_SMAdecision(frame)
        return prices

    #recommendations when technical indicator is fulfilled
    def recommender(self):
        signals = []
        indicators = ['Decision MACD', 'Decision GC', 'Decision RSI/SMA']
        for symbol, frame in zip(self.gettables().TABLE_NAME, self.applytechnicals()):
            if frame.empty is False: #if empty space in database
                for indicator in indicators:
                    if frame[indicator].iloc[-1] == True:
                        signals.append(f"{indicator} Buying Signal for "+ symbol)
        return signals

# %%
instnifty = Recommender('Nifty50')

# %%
instbovespa = Recommender('Bovespa')

# %%
instrtsi = Recommender('RTSI')

# %%
instnifty.updateDB

# %%
instbovespa.updateDB()

# %%
instrtsi.updateDB()

# %%
import smtplib

# %%
sender = "stockrecommendationapp@gmail.com"
password = "geauxmtuecuerlor"

# message to be sent   
SUBJECT = "Recommendations"   
TEXT = f"""\
    Subject: Recommendations \
        
        Nifty
        {instnifty.recommender()},
        
        Bovespa
        {instbovespa.recommender()},
        
        RTSI
        {instrtsi.recommender()}
        
        Good Luck!"""
 

message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)

# %%
server.sendmail(sender, sender, message)


