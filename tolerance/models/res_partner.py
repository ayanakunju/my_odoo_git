# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    """ model ResPartner is used to inherit the res partner and add tolerance_percentage field in it."""
    _inherit = 'res.partner'

    tolerance_percent = fields.Float(string="Tolerance (%)", help="tolerance percentage")
