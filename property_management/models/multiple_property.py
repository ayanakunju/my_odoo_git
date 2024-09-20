# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MultipleProperty(models.Model):
    _name = 'multiple.property'
    _description = 'Multiple Property'

    property_name = fields.Many2one('lease.management', string='Property Name')
    multiple_property_id = fields.Many2one('property.management', required=True, ondelete='cascade')
    type = fields.Selection(related='property_name.status')
    total_amount = fields.Float(compute='_compute_duration')
    legal_amount = fields.Float(string="Legal Amount")
    duration = fields.Integer(related='property_name.duration')
    rental_amount = fields.Float(string='Rent amount')
    legal = fields.Many2one('property.management', string='legal')
    invoice_id = fields.Many2one('account.move', string='invoice_line')

    @api.depends('duration', 'rental_amount')
    def _compute_duration(self):
        for record in self:
            record.total_amount = record.duration * record.rental_amount

    @api.onchange('multiple_property_id', 'type')
    def _onchange_property_id(self):
        if self.type == 'lease':
            self.rental_amount = self.multiple_property_id.legal_amount
        else:
            self.rental_amount = self.multiple_property_id.rent

    @api.onchange('rental_amount')
    def _onchange_rental_amount(self):
        if self.type == 'lease':
            self.multiple_property_id.legal_amount = self.rental_amount
        else:
            self.multiple_property_id.rent = self.rental_amount

