# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    """Extends the pos session model."""
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('due_limit')
        return result
