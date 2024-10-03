# -*- coding: utf-8 -*-

import base64
import logging
import hashlib
import hmac
import json
import pprint
import datetime
import requests
from werkzeug import urls

from odoo import _, fields, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'


    code = fields.Selection(
        selection_add=[('paytrail', 'paytrail')], ondelete={'paytrail': 'set default'}
    )
    paytrail_merchant_id = fields.Char(
        string="Paytrail Merchant Id",
        help="The key solely used to identify the account with Paytrail.",
        required_if_provider='paytrail',
    )
    paytrail_secret_key = fields.Char(
        string="Secret key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="paytrail", groups="base.group_system"
    )

    def _paytrail_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at paytrail endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request
        :param dict data: The payload of the request
        :param str method: The HTTP method of the request
        :return The JSON-formatted content of the response
        :rtype: dict
        :raise: ValidationError if an HTTP error occurs
        """
        url = urls.url_join('https://services.paytrail.com', endpoint)
        headers = {
            "checkout-account": "375917",
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": "1234522224",
            "checkout-timestamp": datetime.date.today().isoformat(),
        }
        print("header", type(headers))
        print("data", type(data))

        checkout_headers = [k for k, v in headers.items() if k.startswith(
            "checkout-")]
        checkout_headers.sort()
        hmac_str = "\n".join(
            f"{key}:{headers[key]}" for key in checkout_headers)
        hmac_str += f"\n{data}"
        payload = json.dumps(data, separators=(",", ":"))
        signature = self.calculate_hmac(self, self.paytrail_secret_key, headers, payload)
        print("hhhhmanc")


        headers["signature"] = signature
        print(headers["signature"])

        try:
            response = requests.request(method, url, data=payload, headers=headers, timeout=60)
            print(response, "qqqqqqqqqqqqqqqq")
            print(response.json())
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
                )
                raise ValidationError(
                    "Paytrail: " + _(
                        "The communication with the API failed. Paytrail gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Paytrail: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    @staticmethod
    def compute_sha256_hash(message: str, secret: str) -> str:

        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

    # /
    # @param secret Merchant shared secret
    # @param headerParams Headers or query string parameters
    # @param body Request body or empty string for GET request
    # @return
    # /

    @staticmethod
    def calculate_hmac(self, secret: str, headerParams: dict, body: str = '') -> str:
        data = []
        for key, value in headerParams.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))
        data.append(body)
        print(self, "ooooooooooooooooooooo")
        return self.compute_sha256_hash('\n'.join(data), secret)

# • Merchant ID: 375917
# • Secret key: SAIPPUAKAUPPIAS

# . 4153 0139 9970 0313	 11/2026	313
