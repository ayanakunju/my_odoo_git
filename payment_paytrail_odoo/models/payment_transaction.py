# -*- coding: utf-8 -*-

import logging
import pprint
from werkzeug import urls
import datetime

from odoo import _, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Paytrail-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res

        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, '/payment/paytrail/return')
        print("hello", processing_values)
        print("processing values", round(processing_values['amount']))
        dt = datetime.datetime.utcnow()
        items = []
        for line in self.sale_order_ids[0].order_line :
            items.append({'unitPrice':round(line.price_total),
                          'units':line.product_uom_qty,
                          'vatPercentage': line.tax_id.amount,
                          'productCode':line.product_template_id.name,
                          'deliveryDate': str(datetime.date.today())})
            print(items)
            line.price_total = int(line.price_total)
            print(line.price_total, "sum")

        payload = {"stamp": str(dt.timestamp()),
                   "reference": processing_values['reference'],
                   "amount": round(processing_values['amount']),
                   "currency": "EUR",
                   "language": "FI",
                   "items":items,
                   "customer":{"email":"test.customer@example.com"},
                   "redirectUrls": {"success": redirect_url,
                                   "cancel": redirect_url}}
        print(payload, "payload")
        print(payload['amount'], "amount")
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._paytrail_make_request('/payments', data=payload)

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')
        print(payment_data, "hello")
        print(payment_data.get('value'), "value")

        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Paytrail and query parameters are provided.
        checkout_url = payment_data['href']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Paytrail data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            return tx
        print(notification_data, "hello")
        tx = self.search(
            [('reference', '=', notification_data.get('checkout-reference')), ('provider_code', '=', 'paytrail')]
        )
        if not tx:
            raise ValidationError("Paytrail: " + _(
                "No transaction found matching reference %s.", notification_data.get('checkout-reference')
            ))
        print("tx",tx)
        return tx
    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Paytrail data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        print("completed")
        super()._process_notification_data(notification_data)
        if self.provider_code != 'paytrail':
            return
        payment_status = notification_data.get('checkout-status')
        if payment_status in ['pending','delayed']:
            self._set_pending()

        elif payment_status == 'ok':
            self._set_done()
        elif payment_status == 'fail':
            self._set_canceled("Paytrail: " + _("Canceled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Paytrail: " + _("Received data with invalid payment status: %s", payment_status)
            )
        print('notification data',payment_status)
