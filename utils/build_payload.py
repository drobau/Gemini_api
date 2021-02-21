import time
import datetime


class Payload:
    @staticmethod
    def create_payload_buy(symbol, amount, price, options):
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))

        return {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": "buy",
            "type": "exchange limit",
            "options": options
        }

    @staticmethod
    def create_stop_limit_payload_buy(symbol, amount, price, stop_price):
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        return {
            "amount": amount,
            "client_order_id": "726813913",
            "price": price,
            "nonce": payload_nonce,
            "side": "buy",
            "request": "/v1/order/new",
            "stop_price": stop_price,
            "symbol": symbol,
            "type": "exchange stop limit"
        }
