# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    """Extends the pos session model."""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('product_discount')
        return result
