import pytest

from utils.api_post import post_request
import time
import datetime


class TestsTech:

    @pytest.fixture(autouse=True)
    def sleep1(self):
        time.sleep(1)

    @staticmethod
    def test_positive_payload():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": "0.001",
            "price": "60776.00",
            "side": "buy",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json['symbol'] == 'btcusd'
        assert response_json['exchange'] == 'gemini'
        assert response_json['side'] == 'buy'
        assert response_json['type'] == 'exchange limit'
        assert not response_json['is_live']
        assert response_json['is_cancelled']
        assert not response_json['is_hidden']
        assert not response_json['was_forced']
        assert response_json['executed_amount'] == '0'
        assert response_json['reason'] == 'MakerOrCancelWouldTake'
        assert response_json['options'] == ['maker-or-cancel']
        assert response_json['reason'] == 'MakerOrCancelWouldTake'
        print(response_json['order_id'])

    @staticmethod
    def test_negative_payload_same_nonce():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))

        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": "10",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response1 = post_request(payload)
        assert response1.status_code == 200
        response2 = post_request(payload)
        response_json = response2.json()

        assert response2.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidNonce'
        assert response_json['message'] == \
               f"Nonce '{payload_nonce}' has not increased since your last call to the Gemini API."

    @staticmethod
    def test_negative_payload_invalid_request():
        invalid_request = "/v1/order/new1"

        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000 + 120))
        payload = {
            "request": invalid_request,
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": "10",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'EndpointMismatch'
        assert response_json['message'] == 'EndpointMismatch'

    @staticmethod
    def test_negative_payload_empty_request():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": "10",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'EndpointMismatch'
        assert response_json['message'] == 'EndpointMismatch'

    @staticmethod
    def test_negative_payload_negative_amount():
        amount = '-2'
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": amount,
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidQuantity'
        assert response_json['message'] == f'Invalid quantity for symbol BTCUSD: {amount}'

    @staticmethod
    def test_negative_payload_negative_price():
        price_negative = "-1"
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": "10",
            "price": price_negative,
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidPrice'
        assert response_json['message'] == f'Invalid price for symbol BTCUSD: {price_negative}'

    @staticmethod
    def test_negative_payload_negative_amount():
        amount_negative = "-2"
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": "btcusd",
            "amount": amount_negative,
            "price": "50000",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidQuantity'
        assert response_json['message'] == f'Invalid quantity for symbol BTCUSD: {amount_negative}'

    @staticmethod
    def test_negative_payload_empty_nonce():
        payload = {
            "request": "/v1/order/new",
            "nonce": '',
            "symbol": "btcusd",
            "amount": "10",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidNonce'
        assert response_json['message'] == 'Nonce \'""\' was not parseable as a number.'

    @staticmethod
    def test_negative_payload_empty_symbol():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": '',
            "amount": "10",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidNonce'
        assert response_json['message'] == 'Nonce \'""\' was not parseable as a number.'

    @staticmethod
    def test_negative_payload_empty_amount():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": 'btcusd',
            "amount": "",
            "price": "50776.00",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidQuantity'
        assert response_json['message'] == 'Invalid quantity for symbol BTCUSD: '

    @staticmethod
    def test_negative_payload_empty_price():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": 'btcusd',
            "amount": "1",
            "price": "",
            "side": "sell",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidPrice'
        assert response_json['message'] == 'Invalid price for symbol BTCUSD: '

    @staticmethod
    def test_negative_payload_empty_side():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": 'btcusd',
            "amount": "1",
            "price": "2500",
            "side": "",
            "type": "exchange limit",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidSide'
        assert response_json['message'] == "Invalid side for symbol BTCUSD: ''"

    @staticmethod
    def test_negative_payload_empty_type():
        t = datetime.datetime.now()
        payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))
        payload = {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": 'btcusd',
            "amount": "1",
            "price": "2500",
            "side": "sell",
            "type": "",
            "options": ["maker-or-cancel"]
        }

        response = post_request(payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 400
        assert response_json['result'] == 'error'
        assert response_json['reason'] == 'InvalidOrderType'
        assert response_json['message'] == "Invalid order type for symbol BTCUSD: ''"
