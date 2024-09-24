# -*- coding: utf-8 -*-

from odoo import models, fields,api

class ManufacturingCost(models.Model):
    _inherit = ('stock.move')

    component_cost = fields.Float(string='Component Cost', related='product_id.standard_price')

    @api.depends('product_id','product_uom_quantity')
    def _compute_total_amount(self):
        for record in self:
            record.total_cost = record.product_uom_quantity * record.product_id.lst_price

