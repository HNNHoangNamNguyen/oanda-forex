import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.requests import (TrailingStopLossDetails)
import oandapyV20.endpoints.positions as positions

import json
import pandas as pd
import ast
import glob

import datetime
from datetime import (timedelta, date)

import ta
from ta import trend
from ta import momentum
from ta import volatility



############## READ FILE ##############
def read_all_file_in_directory(directory, file_type, sep = "\t"):
    print(directory)
    file_list= [f for f in glob.glob(directory + "*." + file_type)]
    
    all_data = pd.DataFrame()
    temp = pd.DataFrame()
    for file in file_list:
            df = pd.read_csv(file, sep= sep, encoding = "utf8", engine='python')
            temp = pd.concat([temp, df])
    all_data = pd.concat([all_data, temp])
    return all_data

############## DATA CLEANING ##############
def convert_to_json(text):
    try:
        return ast.literal_eval(text)
    except:
        return {}


def clean_historical_candle_data(df, price_type = 'ask' ):
    
    df_modified = df[['complete', 'currency_pair', 'time', 'volume', price_type]]
    df_modified[price_type] = df_modified[price_type].astype(str)
    df_modified[price_type] = df_modified[price_type].apply(convert_to_json)
    
    price_df = pd.json_normalize(df_modified[price_type])
    
    df_modified = pd.merge(df_modified, price_df,
                          left_index=True, right_index=True)
    
    df_modified = df_modified[['complete','currency_pair', 'time', 'volume','o', 'h', 'l', 'c']]
    df_modified.columns = ['complete','currency_pair', 'time', 'volume','price_open','price_high', 'price_low', 'price_close']
    
    df_modified[["price_open", "price_high", "price_low", "price_close"]] = df_modified[["price_open", "price_high",
                                                                                         "price_low", "price_close"]].apply(pd.to_numeric)
    df_modified["time"] = pd.to_datetime(df_modified["time"])
    
    return df_modified


def clean_candle_data(df, price_type = 'ask' ):
    
    df_modified = df[['complete', 'currency_pair', 'time', 'volume', price_type]]

    price_df = pd.json_normalize(df_modified[price_type])
    
    df_modified = pd.merge(df_modified, price_df,
                          left_index=True, right_index=True)
    
    df_modified = df_modified[['complete','currency_pair', 'time', 'volume','o', 'h', 'l', 'c']]
    df_modified.columns = ['complete','currency_pair', 'time', 'volume','price_open','price_high', 'price_low', 'price_close']
    
    df_modified[["price_open", "price_high", "price_low", "price_close"]] = df_modified[["price_open", "price_high",
                                                                                         "price_low", "price_close"]].apply(pd.to_numeric)
    df_modified["time"] = pd.to_datetime(df_modified["time"])
    return df_modified


############## ORDER CREATION ##############
def create_market_order(account_id, access_token, instrument, order_type, order_quantity):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    data = {
      "order": {
        "units": str(order_quantity),
        "instrument": instrument,
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT"
      }
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_market_order_with_sl_tp(account_id, access_token, instrument, order_type, order_quantity, sl_price, tp_price):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    data = {
        "order": {
            "units": str(order_quantity),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "price": str(sl_price)
            },
            "takeProfitOnFill": {
                "price": str(tp_price)
            }
        },
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_market_order_with_sl_only(account_id, access_token, instrument, order_type, order_quantity, sl_price):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    data = {
        "order": {
            "units": str(order_quantity),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "price": str(sl_price)
            },

        },
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_market_order_with_trailing_sl_tp(account_id, access_token, instrument, order_type, order_quantity, trailing_sl_pip, tp_price):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    trailingStopLossOnFill = TrailingStopLossDetails(distance=trailing_sl_pip/10000)
    data = {
        "order": {
            "units": str(order_quantity),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "trailingStopLossOnFill": trailingStopLossOnFill.data,
            "takeProfitOnFill": {
                "price": str(tp_price)
            }
        },
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_market_order_with_trailing_sl_only(account_id, access_token, instrument, order_type, order_quantity, trailing_sl_pip):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    trailingStopLossOnFill = TrailingStopLossDetails(distance=trailing_sl_pip/10000)
    data = {
        "order": {
            "units": str(order_quantity),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "trailingStopLossOnFill": trailingStopLossOnFill.data,
        },
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_limit_order(account_id, access_token, instrument, order_type, order_quantity, order_price):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    data = {
      "order": {
        "price" : str(order_price),
        "units": str(order_quantity),
        "instrument": instrument,
        "timeInForce": "GTC",
        "type": "LIMIT",
        "positionFill": "DEFAULT"
      }
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)

def create_limit_order_with_sl_tp(account_id, access_token, instrument, order_type, order_quantity,order_price, sl_price, tp_price):
    order_quantity = order_quantity  if order_type == "BUY" else -abs(order_quantity)
    data = {
        "order": {
            "price" : str(order_price),
            "units": str(order_quantity),
            "instrument": instrument,
            "timeInForce": "GTC",
            "type": "LIMIT",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "price": str(sl_price)
            },
            "takeProfitOnFill": {
                "price": str(tp_price)
            }
        },
    }
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    r = orders.OrderCreate(accountID = account_id, data=data)

    client.request(r)


############## GET POSITION DETAILS ##############
def get_position_details(account_id, access_token, instrument):
    client = oandapyV20.API(access_token=access_token)
    r = positions.PositionDetails(accountID=account_id, instrument = instrument)
    response = client.request(r)["position"]
    long_position_units = response["long"]["units"]
    short_position_units = response["short"]["units"]
    return {'long':long_position_units,
            'short':short_position_units,}


############## GET ACCCOUNT ID AND ACCCESS TOKEN ##############
def get_oanda_account_credentials( account_name, oanda_account_credentials_path = ''):
    oanda_account_credentials = json.load(open(oanda_account_credentials_path + 'oanda_account_credentials.json'))
    account_details = oanda_account_credentials[account_name]
    return account_details


############## STREAM REAL TIME DATA ##############

def get_extraction_time(granularity):
    extraction = False
    while extraction == False:
        time_now = datetime.datetime.utcnow()
        if granularity == "M1":
            if (time_now.minute % 1 == 0) & (time_now.second == 0):
                return True
        elif granularity == "M5":
            if (time_now.minute % 5 == 0) & (time_now.second == 0):
                return True
        elif granularity == "M15":
            if (time_now.minute % 15 == 0) & (time_now.second == 0):
                return True
        elif granularity == "M30":
            if (time_now.minute % 30 == 0) & (time_now.second == 0):
                return True
        elif granularity == "H1":
            if (time_now.hour % 1 == 0) & (time_now.minute == 0) & (time_now.second == 0):
                return True
        elif granularity == "H4":
            if (time_now.minute % 4 == 0) & (time_now.minute == 0) & (time_now.second == 0):
                return True



def get_candle_data(account_id, access_token, instrument, granularity, number_of_candles=200):
    client = oandapyV20.API(access_token=access_token, environment = "practice" or "live")
    params = {
      "count": number_of_candles,
      "granularity": granularity
    }
    r = instruments.InstrumentsCandles(instrument=instrument,
                                   params=params)
    response = client.request(r)
    df = pd.DataFrame(response["candles"])
    df["currency_pair"] = instrument
    return clean_candle_data(df, "mid")
    return df


############## TECHNICAL INDICATOR ##############
    
def get_macd_indicator(df, price_type = 'price_close', window_slow: int = 26, window_fast: int = 12, window_sign: int = 9, fillna: bool = False):
    indicator_macd = trend.MACD(close = df[price_type], window_slow = window_slow, window_fast = window_fast, window_sign= window_sign, fillna = fillna)
    df['macd'] = indicator_macd.macd()
    df['macd_signal'] = indicator_macd.macd_signal()
    df['macd_signal_diff'] = indicator_macd.macd_diff()
    return df

def get_sma_indicator(df, price_type = 'price_close', window = 200):
    indicator_sma = trend.SMAIndicator(close = df[price_type], window=window)
    df['sma_' + str(window)] = indicator_sma.sma_indicator()
    return df

def get_rsi_indicator(df, price_type = 'price_close', window = 14):
    indicator_rsi = momentum.RSIIndicator(close = df[price_type], window=window)
    df['rsi_' + str(window)] = indicator_rsi.rsi()
    return df

def get_adx_indicator(df, high = "price_high", low = "price_low", close = 'price_close', window = 14):
    indicator_adx = trend.ADXIndicator(high = df[high], low = df[low], close = df[close], window = window)
    df['adx'] = indicator_adx.adx()
    df['adx_neg'] = indicator_adx.adx_neg()
    df['adx_pos'] = indicator_adx.adx_pos()
    return df

def get_atr_indicator(df, high = "price_high", low = "price_low", close = 'price_close', window = 14):
    indicator_atr = volatility.AverageTrueRange(high = df[high], low = df[low], close = df[close], window = window)
    df['atr'] = indicator_atr.average_true_range()
    return df

def get_aroon_indicator(df,close = 'price_close', window = 25):
    indicator_aroon = trend.AroonIndicator(close = df[close], window = window)
    df['aroon'] = indicator_aroon.aroon_indicator()
    df['aroon_down'] = indicator_aroon.aroon_down()
    df['aroon_up'] = indicator_aroon.aroon_up()
    return df


def get_cmf_indicator(df, high = "price_high", low = "price_low", close = 'price_close', volume = "volume", window = 20, fillna = False):
    indicator_cmf = ta.volume.ChaikinMoneyFlowIndicator(df[high],df[low], df[close], df[volume], 20, False)
    df['cmf'] = indicator_cmf.chaikin_money_flow()
    return df


def get_cci_indicator(df, high = "price_high", low = "price_low", close = 'price_close', window = 20):
    indicator_cci = trend.CCIIndicator(high = df[high], low = df[low], close = df[close], window = window)
    df['cci'] = indicator_cci.cci()
    return df

def get_ichimoku_indicator(df, high = "price_high", low = "price_low",
                           window1 = 9, window2=26, window3 = 52, visual = False, fillna = False):
    indicator_ichimoku = trend.IchimokuIndicator(high = df[high], low = df[low],
                                                 window1 = window1, window2 = window2, window3 = window3, visual = visual, fillna = fillna)
    df['ichimoku_a'] = indicator_ichimoku.ichimoku_a()
    df['ichimoku_b'] = indicator_ichimoku.ichimoku_b()
    df['ichimoku_base_line'] = indicator_ichimoku.ichimoku_base_line()
    df['ichimoku_conversion_line'] = indicator_ichimoku.ichimoku_conversion_line()
    return df

def get_dpo_indicator(df, close = 'price_close', window = 20):
    indicator_dpo = trend.DPOIndicator(close = df[close], window = window)
    df['dpo'] = indicator_dpo.dpo()
    return df



