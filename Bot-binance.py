from binance import Client
from datetime import datetime
import pandas as pd
import backtrader as bt

# API Key: HIEj9iosnrLJGPCgg1NtmAaoIeA6VFBJN1ESmpnBcEBWRCjSfzj9e87k5NCfcQyq

# Secret Key: DshpXwXA1LHKgEHADj4gRDMEHd7PF8FxdzXGyz4Ic1tJQamX0hccpAgHN8bIgxfV

def get_historic_dates(symbol, interval, fecha_inicial_str, fecha_actual_str):

    historical_klines = client.get_historical_klines(symbol, interval, fecha_inicial_str, fecha_actual_str)
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume', 'ignore']
    df = pd.DataFrame(historical_klines, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# def strategyBollinger(hitoric_dates, saldo, symbol):


#     def __init__(self):
#         params = (
#             ("period", 20),
#             ("devfactor", 2),
#         )

#         self.dataclose = hitoric_dates['close'][0]
#         self.sma = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.period)
#         self.stddev = bt.indicators.StandardDeviation(self.dataclose, period=self.params.period)
#         self.bollinger_top_band = self.sma + self.params.devfactor * self.stddev
#         self.bollinger_low_band = self.sma - self.params.devfactor * self.stddev

#     global cantidad_transacciones

    
#     if self.dataclose < self.bollinger_low_band:
#         print('compro')
#         saldo =- pd.DataFrame(client.get_recent_trades(symbol = 'SOLUSDT'))['price'][0]
#         cantidad_transacciones += 1

#     elif dataclose > bollinger_top_band:
#         print('vendo')
#         saldo =+ pd.DataFrame(client.get_recent_trades(symbol = 'SOLUSDT'))['price'][0]
#         cantidad_transacciones += 1

class BollingerStrategy(bt.Strategy):

    params = (
        ("period", 20),
        ("devfactor", 2),
    )

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.period)
        self.stddev = bt.indicators.StandardDeviation(self.dataclose, period=self.params.period)
        self.bollinger_top_band = self.sma + self.params.devfactor * self.stddev
        self.bollinger_low_band = self.sma - self.params.devfactor * self.stddev

    def next(self):
        global cantidad_transacciones

        if not self.position:
            if self.dataclose < self.bollinger_low_band:
                self.buy()
                cantidad_transacciones += 1

        elif self.dataclose > self.bollinger_top_band:
            self.sell()
            cantidad_transacciones += 1



################################# CONNECT ################################################
key = 'pXybkp3SAJGjQD3IgrIF7C6QOB1IauVZB0InO2SBIczMZSyLmPqsTXp64piCgPcY'
secret = 'BAJbHHjl9tofmxyrn416RvUgbG24gnC9UHsMpFqtuHRo54KBAbSGUtG9pOTDAZgUY'

client = Client(key, secret)
##########################################################################################

interval = Client.KLINE_INTERVAL_1DAY
symbol = 'SOLUSDT'

fecha_actual = datetime.now()
fecha_inicial = fecha_actual.replace(month=fecha_actual.month - 1)

# Convierte las fechas en formato de cadena
fecha_inicial_str = fecha_inicial.strftime('%d %b, %Y')
fecha_actual_str = fecha_actual.strftime('%d %b, %Y')

saldo = 100000.00

hitoric_dates = get_historic_dates(symbol, interval, fecha_inicial_str, fecha_actual_str)



print(saldo)

# Convierte el timestamp de UNIX a formato de fecha legible

# Muestra el DataFrame con los datos históricos

# info = pd.DataFrame(client.get_historical_trades(symbol=symbol))

# print(info)
