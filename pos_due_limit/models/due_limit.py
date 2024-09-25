# -*- coding: utf-8 -*-

from odoo import models, fields


class DueLimit(models.Model):
    _inherit = 'res.partner'

    due_limit = fields.Float(string="Due Limit", help="Customer Due Limit")
