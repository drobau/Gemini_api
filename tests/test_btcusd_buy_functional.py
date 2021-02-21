import pytest

from utils.api_post import post_request
from utils.build_payload import Payload
import time


class TestsTech:
    # current_price_BTCUSD is an actual price for moment of execution. Ideally I would to use GET request and
    # pull it automatically, but requirements is: "Do not invoke any other API endpoints"
    current_price_BTCUSD = 50776.00

    @pytest.fixture(autouse=True)
    def sleep1(self):
        time.sleep(1)

    @staticmethod
    def test_maker_or_cancel_fulfill():
        amount = "0.001"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD - 10000))
        options = ["maker-or-cancel"]
        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
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
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD + 10000))
        options = ["maker-or-cancel"]
        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
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

    @staticmethod  # TODO need fix always cancel-true
    def test_immediate_or_cancel_fulfill():
        amount = "0.0001"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD + 1000))
        options = ["immediate-or-cancel"]

        payload = Payload.create_payload_buy("btcusd", amount, price, options)
        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == "buy"
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert not response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['options'] == options
        assert response_json['price'] == price
        assert response_json['original_amount'] == amount
        assert response_json['remaining_amount'] == amount

    @staticmethod
    def test_immediate_or_cancel_cancel():
        amount = "4"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD - 1000))
        options = ["immediate-or-cancel"]

        payload = Payload.create_payload_buy("btcusd", amount, price, options)
        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
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
        amount = "5"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD - 1000))
        options = ["maker-or-cancel"]

        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
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
        amount = "0.001"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD + 1000))
        options = ["maker-or-cancel"]

        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"
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
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD))
        options = ["auction-only"]
        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == "error"
        assert response_json['reason'] == 'AuctionNotOpen'
        assert response_json['message'] == "Failed to place an auction-only order because there is no current " \
                                           "auction open for BTCUSD"

    # Always shows the same error message 'Invalid quantity for symbol BTCUSD: ' with any parameters.  Can't find the
    # same functionality in the Gemini sandbox UI
    @staticmethod
    def test_indication_of_interest():
        amount = "1"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD))
        options = ["indication-of-interest"]
        payload = Payload.create_payload_buy("btcusd", amount, price, options)

        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidQuantity'
        assert response_json['message'] == f'Invalid quantity for symbol BTCUSD: {amount}'

    # TODO Need fix: always throws an error Invalid price for symbol BTCUSD:
    @staticmethod
    def test_stop_limit_orders():
        amount = "0.1"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD))
        stop_price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD - 5000))
        payload = Payload.create_stop_limit_payload_buy("btcusd", amount, price, stop_price)

        response = post_request(payload)
        response_json = response.json()

        print(response.status_code)
        print(response_json)
        assert response.status_code == 200
        assert response_json['symbol'] == "btcusd"

    @staticmethod
    def test_negative_stop_limit_orders():
        amount = "0.1"
        price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD - 1000))
        stop_price = str('{0:.2f}'.format(TestsTech.current_price_BTCUSD))
        payload = Payload.create_stop_limit_payload_buy("btcusd", amount, price, stop_price)

        response = post_request(payload)
        response_json = response.json()

        print(response.status_code)
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == "error"
        assert response_json['reason'] == "InvalidStopPriceBuy"
        assert response_json['message'] == f'Stop Price: ${"{0:,.2f}".format(float(stop_price))} must be lower ' \
                                           f'than Price: ${"{0:,.2f}".format(float(price))} for Stop Limit buy Orders'
