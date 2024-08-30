# -*- coding: utf-8 -*-

from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    rental_lease_id = fields.Many2one('lease.management' ,string='Rental Id')



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    line_id = fields.Many2one('multiple.property',string='Line Id')
