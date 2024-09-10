# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PropertyManagement(models.Model):
    _name = 'property.management'
    _description = 'Property Management'
    _inherit = 'mail.thread'
    _rec_name = 'property_name'

    property_name = fields.Text(required=True)
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    zip = fields.Char(string='zip')
    date = fields.Date('Date', copy=False)
    image = fields.Binary("Image", help="Select image here")
    can_be_sold = fields.Boolean()
    legal_amount = fields.Float(required=True)
    rent = fields.Float(required=True)
    owner_id = fields.Many2one('hr.employee',string='Owner')
    description = fields.Text(string='Description')
    management_id = fields.Many2one('lease.management', )
    state = fields.Selection(selection=[('draft', 'Draft'), ('rented', 'Rented'),
                                        ('leased', 'Leased'), ('sold', 'Sold')
                                        ], string='Status', required=True, copy=False, tracking=True, default='draft')
    property_count = fields.Integer(compute='_compute_count')
    user_id = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user.id)
    group_id = fields.Many2one('res.groups', string='Group')
    is_readonly = fields.Boolean(compute='_compute_is_readonly')

    @api.depends('group_id')
    def _compute_is_readonly(self):
        self.is_readonly = True
        for record in self:
            if self.env.user.has_group('property_management.property_manager_access'):
                record.is_readonly = False

    def _compute_count(self):
        for record in self:
            record.property_count = (self.env['multiple.property'].search_count(
                [('multiple_property_id', '=', self.id)]))

    def get_property(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent/Lease',
            'view_mode': 'tree',
            'res_model': 'multiple.property',
            'domain': [('multiple_property_id', '=', self.id)]
        }


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    owned_property_ids = fields.One2many('property.management', 'owner_id', string='Owned Properties')
