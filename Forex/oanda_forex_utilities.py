import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.requests import (TrailingStopLossDetails)
import oandapyV20.endpoints.positions as positions

import json
import pandas as pd

from ta import trend
from ta import momentum

############## DATA CLEANING ##############
def convert_to_json(text):
    try:
        return ast.literal_eval(text)
    except:
        return {}

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
def get_oanda_account_credentials(oanda_account_credentials_path, account_name):
    oanda_account_credentials = json.load(open(oanda_account_credentials_path + '/oanda_account_credentials.json'))
    account_details = oanda_account_credentials[account_name]
    return account_details


############## STREAM REAL TIME DATA ##############
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


############## TECHNICCAL INDICATOR ##############
    
def get_macd_indicator(df, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9, fillna: bool = False):
    indicator_macd = trend.MACD(close = df["price_close"])
    df['macd'] = indicator_macd.macd()
    df['macd_signal'] = indicator_macd.macd_signal()
    df['macd_signal_diff'] = indicator_macd.macd_diff()
    return df

def get_sma_indicator(df, price_type = 'price_close', window = 200):
    indicator_sma = trend.SMAIndicator(close = df[price_type], window=200)
    df['sma_' + str(window)] = indicator_sma.sma_indicator()
    return df

def get_rsi_indicator(df, price_type = 'price_close', window = 14):
    indicator_rsi = momentum.RSIIndicator(close = df[price_type], window=14)
    df['rsi_' + str(window)] = indicator_rsi.rsi()
    return df




