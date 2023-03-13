import pandas as pd
from backtesting import Strategy
from backtesting import Backtest
from backtesting.lib import crossover

# read CSV file into a pandas DataFrame
df = pd.read_csv('csv\BTCUSDT-5m.csv')
#df = pd.read_csv('csv\BTCUSDT-5m-2018-08.csv')

# drop unwanted columns
# native colum are : Open time,	Open, High, Low, Close,	Volume,	Close time,	Quote asset volume,	Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore
# df = df.drop(columns=['Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
df = df.iloc[:, :6]

# rename the columns
df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

# convert the timestamp to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

# set the timestamp as the index
df = df.set_index('Timestamp')

# convert the remaining columns to float
df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

# sort the DataFrame by date
df = df.sort_index()

#full data frame
#print(df)
#few first rows
#print(df.head())
#few last rows
#print(df.tail())
#input("Press Enter to continue...")

def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 21
    n2 = 55
    n3 = 200
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
        self.sma3 = self.I(SMA, self.data.Close, self.n3)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2) and self.data.Close > self.sma3:
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1) and self.data.Close < self.sma3:
            self.position.close()
            self.sell()
            
bt = Backtest(df, SmaCross, cash=100000, commission=.004)
stats = bt.run()
#bt.plot(resample=True)
#bt.plot(resample='8H')
#bt.plot(resample='1D')
#optimized = bt.optimize(method='grid', n1=range(10, 30, 1), n2=range(30, 60, 1), n3=range(100, 300, 10), maximize='Equity Final [$]', max_tries=500, constraint=lambda p: p.n1 < p.n2)
optimized = bt.optimize(method='skopt', n1=range(10, 30, 1), n2=range(30, 60, 1), n3=range(100, 300, 10), maximize='Equity Final [$]', max_tries=500, constraint=lambda p: p.n1 < p.n2)
#bt.plot(results=optimized)
print(optimized)
print(optimized._strategy)
#print("=====================================")
#print(stats)
#print(stats._strategy)
