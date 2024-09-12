# -*- coding: utf-8 -*-

from odoo import models, fields


class PdfMessageWizard(models.TransientModel):
    _name = 'pdf.message.wizard'
    _description = 'Pdf Message Wizard'

    from_date = fields.Datetime(string='From Date')
    to_date = fields.Datetime(string='To Date')
    tenant_ids = fields.Many2many('res.partner', string='Customer')
    owner_id = fields.Many2one('hr.employee', string='Owner')
    status = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], default='rent')
    property_id = fields.Many2one('property.management', string='Property')
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('confirmed', 'Confirmed'),
                              ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired'),
                              ], string='Status', required=True, copy=False, tracking=True, default='draft')

    def print_report(self):
        data = {
            'to_date': self.to_date,
            'from_date': self.from_date,
            'tenant_ids': self.tenant_ids.ids,
            'status': self.status,
            'owner_id': self.owner_id.id,
            'property_id': self.property_id.id,
            'state': self.state
        }
        print(data)
        return self.env.ref('property_management.action_report_lease_management').report_action(None, data=data)
