from odoo import models, fields, api, _


class CocBasic(models.Model):
    _name = 'coc.basic'
    _inherit = 'mrp.bom'

    state = fields.Selection(selection=[('draft', 'draft'), ('approved', 'approved')])



