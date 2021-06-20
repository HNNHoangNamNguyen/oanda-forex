import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import (TrailingStopLossDetails)

account_id = "101-003-18483320-001"
access_token = "87a216bb7b0e640e4af97a43499b58b9-4803472d0b66dd35b5d7541f3105caf5"

def create_market_order(instrument, order_type, order_quantity):
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

def create_market_order_with_sl_tp(instrument, order_type, order_quantity, sl_price, tp_price):
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

def create_market_order_with_sl_only(instrument, order_type, order_quantity, sl_price):
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

def create_market_order_with_trailing_sl_tp(instrument, order_type, order_quantity, trailing_sl_pip, tp_price):
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

def create_market_order_with_trailing_sl_only(instrument, order_type, order_quantity, trailing_sl_pip):
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

def create_limit_order(instrument, order_type, order_quantity, order_price):
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

def create_limit_order_with_sl_tp(instrument, order_type, order_quantity,order_price, sl_price, tp_price):
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

