import pytest
from utils.api_post import post_request
from utils.build_payload import Payload
from utils.actual_prices import Prices
import time


class TestsEthUsdBuy:

    @pytest.fixture(autouse=True)
    def sleep1(self):
        time.sleep(1)

    @staticmethod
    def test_maker_or_cancel_fulfill():
        amount = "0.001"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD - 100))
        options = ["maker-or-cancel"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert response_json['is_live']
        assert not response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_maker_or_cancel_cancel():
        amount = "0.001"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 1000))
        options = ["maker-or-cancel"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['reason'] == 'MakerOrCancelWouldTake'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_immediate_or_cancel_fulfill():
        amount = "0.001"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 1000))
        options = ["immediate-or-cancel"]

        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)
        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert not response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == amount
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == '0'

    @staticmethod
    def test_immediate_or_cancel_cancel():
        amount = "4"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD - 1000))
        options = ["immediate-or-cancel"]

        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)
        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_fill_or_kill_fulfill():
        amount = "0.001"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD - 100))
        options = ["maker-or-cancel"]

        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)
        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert response_json['is_live']
        assert not response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_fill_or_kill_cancel():
        amount = "2"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 100))
        options = ["maker-or-cancel"]

        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['reason'] == 'MakerOrCancelWouldTake'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    # UI of the Gemini sandbox provides an error message "The auction is not accepting orders yet. Please check the
    # activity feed panel on the right for updates." with any parameters.
    @staticmethod
    def test_auction_only():
        amount = "1"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD))
        options = ["auction-only"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == "error"
        assert response_json['reason'] == 'AuctionNotOpen'
        assert response_json['message'] == "Failed to place an auction-only order because there is no current " \
                                           "auction open for ETHUSD"

    @staticmethod
    def test_indication_of_interest_fulfill():
        amount = "100"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 50))
        options = ["indication-of-interest"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'indication-of-interest limit'
        assert response_json['is_live']
        assert not response_json['is_cancelled']
        assert response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_indication_of_interest_invalid_quantity():
        amount = "4"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 250))
        options = ["indication-of-interest"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidQuantity'
        assert response_json['message'] == f'Invalid quantity for symbol ETHUSD: {amount}'

    @staticmethod
    def test_indication_of_invalid_price():
        amount = "50"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD - 2500))
        options = ["indication-of-interest"]
        payload = Payload.create_limit_payload_buy("ethusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidPrice'
        assert response_json['message'] == f'Invalid price for symbol ETHUSD: {price}'

    @staticmethod
    def test_stop_limit_order():
        amount = "0.1"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 30))
        stop_price = str('{0:.2f}'.format(Prices.current_price_ETHUSD + 27))
        payload = Payload.create_stop_limit_payload_buy("ethusd", amount, price, stop_price)

        response = post_request(payload)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['symbol'] == "ethusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'stop-limit'
        assert response_json['is_live']
        assert not response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == []
        assert response_json['price'] == price
        assert response_json['stop_price'] == stop_price
        assert response_json['original_amount'] == amount

    @staticmethod
    def test_negative_stop_limit_order():
        amount = "0.1"
        price = str('{0:.2f}'.format(Prices.current_price_ETHUSD - 100))
        stop_price = str('{0:.2f}'.format(Prices.current_price_ETHUSD))
        payload = Payload.create_stop_limit_payload_buy("ethusd", amount, price, stop_price)

        response = post_request(payload)
        response_json = response.json()

        print(response.status_code)
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == "error"
        assert response_json['reason'] == "InvalidStopPriceBuy"
        assert response_json['message'] == f'Stop Price: ${"{0:,.2f}".format(float(stop_price))} must be lower ' \
                                           f'than Price: ${"{0:,.2f}".format(float(price))} for Stop Limit buy Orders'
