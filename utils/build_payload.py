import time
import datetime


class Payload:
    @staticmethod
    def _generate_payload_nonce():
        t = datetime.datetime.now()
        return str(int(time.mktime(t.timetuple()) * 1000))

    @staticmethod
    def create_limit_payload_buy(symbol, amount, price, options):
        return {
            "request": "/v1/order/new",
            "nonce": Payload._generate_payload_nonce(),
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": "buy",
            "type": "exchange limit",
            "options": options
        }

    @staticmethod
    def create_stop_limit_payload_buy(symbol, amount, price, stop_price):
        return {
            "amount": amount,
            "price": price,
            "nonce": Payload._generate_payload_nonce(),
            "side": "buy",
            "request": "/v1/order/new",
            "stop_price": stop_price,
            "symbol": symbol,
            "type": "exchange stop limit"
        }

    @staticmethod
    def create_limit_payload_sell(symbol, amount, price, options):
        return {
            "request": "/v1/order/new",
            "nonce": Payload._generate_payload_nonce(),
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": "sell",
            "type": "exchange limit",
            "options": options
        }

    @staticmethod
    def create_stop_limit_payload_sell(symbol, amount, price, stop_price):
        return {
            "amount": amount,
            "price": price,
            "nonce": Payload._generate_payload_nonce(),
            "side": "sell",
            "request": "/v1/order/new",
            "stop_price": stop_price,
            "symbol": symbol,
            "type": "exchange stop limit"
        }
