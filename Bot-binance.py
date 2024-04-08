from binance import Client
from datetime import datetime
import pandas as pd
import tti
import time
from telegram import Bot
import asyncio

def get_historic_dates(symbol, interval, fecha_inicial_str, fecha_actual_str):

    historical_klines = client.get_historical_klines(symbol, interval, fecha_inicial_str, fecha_actual_str)
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume', 'ignore']
    df = pd.DataFrame(historical_klines, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def getDataFrame():
    data =pd.DataFrame( candles, columns=['open time', 'Open price', 'High price', 'Low price', 'Close', 'Volume', 'Close time', 'Asset volume', 'Number of trades', 'Taker volume', 'Maker volume', 'nothing'] )

    data['Datetime'] = pd.DatetimeIndex(pd.to_datetime(data['Close time'], unit='ms'))
    data['Open price'] = data['Open price'].astype('float')
    data['High price'] = data['High price'].astype('float')
    data['Low price'] = data['Low price'].astype('float')
    data['Close'] = data['Close'].astype('float')
    data['Volume'] = data['Volume'].astype('float')
    data['Close time'] = pd.DatetimeIndex(pd.to_datetime(data['Close time'], unit='ms'))
    data['Asset volume'] = data['Asset volume'].astype('float')
    data['Number of trades'] = data['Number of trades'].astype('float')
    data['Taker volume'] = data['Taker volume'].astype('float')
    data['Maker volume'] = data['Maker volume'].astype('float')
    data['nothing'] = data['nothing'].astype('float')

    data = data.set_index('Datetime')

    return data

async def run(saldo, ma, bb, rsi, tiempo_inicial, tiempo_limite, df):
    sobreventa = 50
    sobrecompra = 20

    
    while True:
        time.sleep(2)
        if (time.time() - tiempo_inicial >= tiempo_limite):
            print('tiempo finalizado')
            return saldo
        else:
            if (df.iloc[-1]['close'] < bb.getTiData().iloc[-1]['lower_band']):
                print('compro')

                saldo -= df.iloc[-1]['close']
            else:
                if (df.iloc[-1]['close'] > bb.getTiData().iloc[-1]['upper_band']):
                    print('vendo')
                    saldo += df.iloc[-1]['close']
                
            if (df.iloc[-1]['close'] > ma.getTiData().iloc[-1]['ma-simple']):
                print('vendo')
                saldo += df.iloc[-1]['close']
            else:
                if (df.iloc[-1]['close'] < ma.getTiData().iloc[-1]['ma-simple']):
                    print('compro')
                    await enviar_mensaje(chat_id='6839920601', mensaje='Compro accion')
                    saldo -= df.iloc[-1]['close']
                    print(saldo)
        
async def enviar_mensaje(chat_id, mensaje):
    await bot.send_message(chat_id=chat_id, text=mensaje)

################################# CONNECT ################################################
key = 'pXybkp3SAJGjQD3IgrIF7C6QOB1IauVZB0InO2SBIczMZSyLmPqsTXp64piCgPcY'
secret = 'BAJbHHjl9tofmxyrn416RvUgbG24gnC9UHsMpFqtuHRo54KBAbSGUtG9pOTDAZgUY'

client = Client(key, secret)

TOKEN = '6404398205:AAEjHkAn6q8fOyV14LrjtmX9MI_oeGJhXVQ'

# Crear una instancia del bot
bot = Bot(token=TOKEN)

# Método para enviar
##########################################################################################

interval = Client.KLINE_INTERVAL_1DAY
symbol = 'SOLUSDT'

fecha_actual = datetime.now()
fecha_inicial = fecha_actual.replace(month=fecha_actual.month - 1)

# Convierte las fechas en formato de cadena
fecha_inicial_str = fecha_inicial.strftime('%d %b, %Y')
fecha_actual_str = fecha_actual.strftime('%d %b, %Y')

saldo = 100000.00
saldo_inicial = saldo
##hitoric_dates = get_historic_dates(symbol, interval, fecha_inicial_str, fecha_actual_str)

candles = client._historical_klines(symbol, interval)

df = getDataFrame()


ma = tti.indicators.MovingAverage(input_data=df, period=20, ma_type='simple')
bb = tti.indicators.BollingerBands(input_data=df, period=20, std_number=2, fill_missing_values=True)
rsi = tti.indicators.RelativeStrengthIndex(input_data=df, period=14, fill_missing_values=True)

tiempo_inicial = time.time()
tiempi_limite = 10

saldo = asyncio.run(run(saldo=saldo, ma=ma, bb=bb, rsi=rsi, tiempo_inicial=tiempo_inicial, tiempo_limite=tiempi_limite, df=df))

diferencia = saldo-saldo_inicial

print('el saldo es: ' + str(saldo) + ' por lo tanto la diferencia es de: ' + str(diferencia))

