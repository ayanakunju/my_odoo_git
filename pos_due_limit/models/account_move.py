# -*- coding: utf-8 -*-

from odoo import models,fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    # due_limit = fields.One2many('res.partner','',string='Due Limit')

