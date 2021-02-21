import base64
import datetime
import hashlib
import hmac
import json

import requests
from utils.util import Utils

base_url = "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"


def post_request(payload):
    url = base_url + endpoint

    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(Utils.gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': Utils.gemini_api_key,
                       'X-GEMINI-PAYLOAD': b64,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    return response



