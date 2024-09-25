# -*- coding: utf-8 -*-

from odoo import models

class PosSession(models.Model):
    """Extends the pos session model."""
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('due_limit')
        return result

    # def _pos_ui_models_to_load(self):
    #     res = super()._pos_ui_models_to_load()
    #     res.append('res.partner')
    #     return res
    #
    # def _loader_params_res_partner(self):
    #     return {
    #         'search_params': {
    #             'domain': [('state', '=', 'draft')],
    #             'fields': ['name', 'partner_id', 'state', 'custom_field'],
    #         },
    #     }

