# -*- coding: utf-8 -*-

from odoo import models,fields,api

class OwlModel(models.Model):
    _name = 'owl.model'

    @api.model
    def owl_model_search(self):
        return self.env['sale.order'].search([],limit=10)
