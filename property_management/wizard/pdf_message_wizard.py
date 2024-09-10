# -*- coding: utf-8 -*-

from odoo import models, fields


class PdfMessageWizard(models.TransientModel):
    _name = 'pdf.message.wizard'
    _description = 'Pdf Message Wizard'

    from_date = fields.Datetime(string='From Date')
    to_date = fields.Datetime(string='To Date')
    tenant_id = fields.Many2one('res.partner',string='Customer')
    owner_id = fields.Many2one('hr.employee',string='Owner')
    type = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], default='rent')
    property = fields.Many2one('property.management',string='Property')
    state = fields.Selection(selection=[('draft', 'Draft'), ('approved', 'Approved'), ('confirmed', 'Confirmed'),
                                        ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired'),
                                        ], string='Status', required=True, copy=False, tracking=True, default='draft')

