# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError


class LeaseManagement(models.Model):
    _name = 'lease.management'
    _description = 'Lease Management'
    _inherit = 'mail.thread'
    _rec_name = 'sequence_number'

    sequence_number = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    property_id = fields.Many2one('multiple.property', string='Property')
    status = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], default='rent')
    tenant_id = fields.Many2one('res.partner', required=True)
    legal_amount = fields.Float(string="Legal Amount")
    total_amount = fields.Float(related='property_id.total_amount')
    company_id = fields.Many2one('res.company', string='company', default=lambda self: self.env.company)
    date_start = fields.Datetime(string='Start Date', required=True)
    date = fields.Datetime(string='Expiration Date', tracking=True, required=True)
    duration = fields.Integer(compute='_compute_total_days')
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                        ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired'),
                                        ('invoice', 'Invoiced')
                                        ], string='Status', required=True, copy=False, tracking=True, default='draft')
    order_line_ids = fields.One2many('multiple.property', inverse_name='property_name', string="Order Lines", copy=True)
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice Count')
    move_ids = fields.Many2many('account.move', string='Invoices', readonly=True)
    invoice_paid = fields.Boolean(string="Invoice Paid", compute='_compute_invoice_paid', store=True)
    payment_state = fields.Selection(related='move_ids.payment_state', readonly=True, copy=False, tracking=True)
    active = fields.Boolean(default=True)
    # payment_state = fields.Selection(selection=[('paid', 'Paid'), ('partial','Partial'), ('not_paid', 'Not Paid')] , compute='_compute_payment_state')


    # @api.depends('move_ids.payment_state')
    # def _compute_payment_state(self):
    #     if self.move_ids:
    #         for record in self.move_ids:
    #             if record.payment_state != 'paid':
    #                 self.payment_state = 'partial'
    #             else:
    #                 self.payment_state = 'paid'

    @api.depends('move_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.move_ids)

    @api.depends('move_ids.state')
    def _compute_invoice_paid(self):
        for record in self:
            record.invoice_paid = all(move.state == 'posted' for move in record.move_ids)

    @api.depends('date_start', 'date', 'duration')
    def _compute_total_days(self):
        for record in self:
            if record.date_start and record.date:
                start_date = datetime.strptime(str(record.date_start), '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(str(record.date), '%Y-%m-%d %H:%M:%S')
                difference = timedelta(seconds=3600)
                new_date = (end_date - start_date - difference) * 24
                record.duration = int(new_date.days + 1) / 24
            else:
                record.duration = 0

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the property """
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code('lease.manage')
        return super().create(vals_list)

    def action_confirm(self):
        attachments = self.env['ir.attachment'].search([('res_id', '=', self.id), ('res_model', '=', self._name)])
        if attachments:
            self.write({
                'state': "confirmed"})
            template = self.env.ref('property_management.lease_management_confirm_template')
            template.send_mail(self.id, force_send=True)
        else:
            raise ValidationError(_('please attach the document'))

    def action_close(self):
        self.write({
            'state': "closed"
        })
        template = self.env.ref('property_management.lease_management_close_template')
        template.send_mail(self.id, force_send=True)

    def action_return(self):
        self.write({
            'state': "returned"
        })

    def action_expire(self):
        self.write({
            'state': "expired"
        })
        template = self.env.ref('property_management.lease_management_expire_template')
        template.send_mail(self.id, force_send=True)

    def action_reset_to_draft(self):
        self.write({
            'state': "draft"
        })

    # def action_create_invoice(self):
    #     for record in self:
    #         if record.state != 'confirmed':
    #             raise ValidationError(_('Only confirmed rent/lease can create an invoice'))
    #
    #         invoice_obj = self.env['account.move']
    #         invoice = self.env['account.move'].search([
    #             ('move_type', '=', 'out_invoice'),
    #             ('state', '=', 'draft'),
    #             ('partner_id', '=', record.tenant_id.id),
    #         ])
    #
    #         if not invoice:
    #             invoice = invoice_obj.create({
    #                 'move_type': 'out_invoice',
    #                 'partner_id': record.tenant_id.id,
    #                 'invoice_line_ids': [(fields.Command.create({
    #                     'name': rec.multiple_property_id.property_name,
    #                     'price_unit': rec.total_amount,
    #                 }) for rec in record.order_line_ids if not rec.invoice_id)],
    #             })
    #             self.order_line_ids.write({
    #                 'invoice_id': invoice.id
    #             })
    #             record.message_post(body=_('Invoice %s created') % invoice.name)
    #         else:
    #             print(record.order_line_ids)
    #             invoice.write({
    #                 'invoice_line_ids':[(fields.Command.clear())]
    #             })
    #             invoice.write({
    #                 'invoice_line_ids': [(fields.Command.create({
    #                     'name': rec.multiple_property_id.property_name,
    #                     'price_unit': rec.total_amount,
    #                 }) for rec in record.order_line_ids)]
    #             })
    #             record.message_post(body=_('Invoice %s updated') % invoice.name)
    #
    #         record.write({'state': "confirmed", 'move_ids': [(fields.Command.clear(invoice.id))]})
    #     return {
    #         'name': _('Create Invoices'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'account.move',
    #         'res_id': invoice.id,
    #         'target': 'current'
    #     }

    def action_create_invoice(self):
        for record in self:
            if record.state != 'confirmed':
                raise ValidationError(_('Only confirmed rent/lease can create an invoice'))

            invoice_obj = self.env['account.move']
            invoice = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'draft'),
                ('partner_id', '=', record.tenant_id.id),
            ])

            if not invoice:
                invoice = invoice_obj.create({
                    'move_type': 'out_invoice',
                    'partner_id': record.tenant_id.id,
                    'invoice_date': datetime.today(),
                    'invoice_line_ids': [(0, 0, {
                        'name': rec.multiple_property_id.property_name,
                        'price_subtotal': rec.total_amount,
                        'price_unit':rec.rental_amount,
                        'quantity': rec.duration,
                    }) for rec in record.order_line_ids if not rec.invoice_id],
                })
                self.order_line_ids.write({
                    'invoice_id': invoice.id
                })
                record.message_post(body=_('Invoice %s created') % invoice.name)
            else:
                print(record.order_line_ids)
                invoice.write({
                    'invoice_line_ids': [(5, 0, 0)]
                })
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'name': rec.multiple_property_id.property_name,
                        'price_subtotal': rec.total_amount,
                        'price_unit': rec.rental_amount,
                        'invoice_date': datetime.today(),
                        'quantity': rec.duration,
                    }) for rec in record.order_line_ids]
                })
                record.message_post(body=_('Invoice %s updated') % invoice.name)

            record.write({'state': "confirmed", 'move_ids': [(4, invoice.id)]})
        return {
            'name': _('Create Invoices'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current'
        }

    def action_view_invoice(self):
        return {
            'name': _('Customer Invoice'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice', 'create': True}",
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.move_ids.ids)],
        }

    def _auto_expire_leases(self):
        for record in self:
            today = date.today()
            leases = record.search([('state', '=', 'confirmed'),('date', '<', today)])
            if leases:
                record.write({
                    'state': "expired"
                })


    def _followup_payment(self):
        today= datetime.now().date()
        late_leases = self.search([
            ('state', '=', 'confirmed'),
            ('date', '<', today - timedelta(days=30)),
            ('invoice_paid', '=', 'False')
            ])

        for lease in late_leases:
            lease._send_email(lease.management.payment_followups_template)


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

    # def expire_draft_sent_orders(self):
    #     limit_date = datetime.now()
    #     for order in self.filtered(lambda rec: rec.state  in ["confirmed"] and rec.date < datetime.now()):
    #         order.action_expire()


# @api.model
    # def _auto_expire_leases(self):
    #     for rec in self.search([('state', '!=', 'expired'),('state', '=', 'confirmed')]):
    #         if rec.date_start and rec.date <= fields.Date.today():
    #             rec.write({'state': 'expired'})

