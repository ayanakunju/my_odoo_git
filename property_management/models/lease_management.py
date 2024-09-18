# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
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
    date_start = fields.Date(string='Start Date', required=True)
    date = fields.Date(string='Expiration Date', tracking=True, required=True)
    duration = fields.Integer(compute='_compute_total_days', store=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('approved', 'Approved'),('confirmed', 'Confirmed'),
                                        ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired'),
                                        ], string='Status', required=True, copy=False, tracking=True, default='draft')
    order_line_ids = fields.One2many('multiple.property', inverse_name='property_name', string="Order Lines", copy=True)
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice Count')
    invoice_paid = fields.Boolean(string="Invoice Paid", compute='_compute_invoice_paid', store=True)
    active = fields.Boolean(default=True)
    move_ids = fields.One2many('account.move', 'rental_lease_id', string='Invoices')
    payment_state = fields.Selection(related='move_ids.payment_state', readonly=True, copy=False, tracking=True)


    @api.depends('move_ids')
    def _compute_invoice_count(self):
        """ To compute the invoice count"""
        for record in self:
            record.invoice_count = len(record.move_ids)

    @api.depends('move_ids.state')
    def _compute_invoice_paid(self):
        """ To compute the posted invoice"""
        for record in self:
            record.invoice_paid = all(move.state == 'posted' for move in record.move_ids)

    @api.depends('date_start', 'date', 'duration')
    def _compute_total_days(self):
        """" Calculate the total  duration"""
        for record in self:
            if record.date_start and record.date:
                start_date = datetime.strptime(str(record.date_start), '%Y-%m-%d')
                end_date = datetime.strptime(str(record.date), '%Y-%m-%d')
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

    def action_approve(self):
        self.write({
            'state': "approved"
        })

    def action_reset_to_draft(self):
        self.write({
            'state': "draft"
        })

    def action_create_invoice(self):
        """" Create invoice for the property """
        if self.move_ids:
            posted_invoice = self.move_ids.filtered(lambda inv: inv.state == 'posted')
            draft_invoice = self.move_ids.filtered(lambda inv: inv.state == 'draft')
            if draft_invoice:
                lines = []
                for rec in self.order_line_ids:
                    if ((rec.id not in posted_invoice.invoice_line_ids.line_id.ids) and
                            (rec.id in posted_invoice.invoice_line_ids.line_id.ids)):
                        invoice_line_values = {
                            'name': rec.multiple_property_id.property_name,
                            'price_unit': rec.rental_amount,
                            'price_subtotal': rec.total_amount,
                            'quantity': rec.duration,
                            'line_id': rec.id
                        }
                        lines.append(Command.create(invoice_line_values))
                for record in draft_invoice:
                    record.write({'invoice_line_ids': lines})
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'account.move',
                        'view_type': 'tree,form',
                        'view_mode': 'form',
                        'res_id': record.id
                    }

            else:
                # posted invoice
                lines = []
                for rec in self.order_line_ids:
                    for line in posted_invoice.invoice_line_ids:
                        difference_qty = rec.duration - line.quantity
                        difference_amount = line.price_unit * line.quantity
                        if rec.id in line.line_id.ids:
                            if rec.duration > line.quantity:
                                invoice_line_values = {
                                    'name': rec.multiple_property_id.property_name,
                                    'price_unit': rec.rental_amount,
                                    'price_subtotal': difference_amount,
                                    'quantity': difference_qty,
                                    'line_id': rec.id
                                }
                                lines.clear()
                                lines.append(Command.create(invoice_line_values))
                    if rec.id not in posted_invoice.invoice_line_ids.line_id.ids:
                        invoice_line_values = {
                            'name': rec.multiple_property_id.property_name,
                            'price_unit': rec.rental_amount,
                            'price_subtotal': rec.total_amount,
                            'quantity': rec.duration,
                            'line_id': rec.id
                        }
                        lines.append(Command.create(invoice_line_values))
            if lines:
                invoice_vals = {
                    'partner_id': self.tenant_id.id,
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': lines,
                    'rental_lease_id': self.id
                }
                invoice_new = self.env['account.move'].create(invoice_vals)
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'view_type': 'tree,form',
                    'view_mode': 'form',
                    'res_id': invoice_new.id,
                }
        else:
            # new invoice
            lines = []
            for rec in self.order_line_ids:
                invoice_line_values = {
                    'name': rec.multiple_property_id.property_name,
                    'price_unit': rec.rental_amount,
                    'price_subtotal': rec.total_amount,
                    'quantity': rec.duration,
                    'line_id': rec.id
                }
                lines.append(Command.create(invoice_line_values))
            invoice_vals = {
                'partner_id': self.tenant_id.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': lines,
                'rental_lease_id': self.id,
            }
            invoice_new = self.env['account.move'].create(invoice_vals)

            self.message_post_with_source(
                'mail.message_origin_link',
                render_values={'self': self, 'origin': invoice_new},
                subtype_xmlid='mail.mt_note',
            )
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_type': 'tree,form',
                'view_mode': 'form',
                'res_id': invoice_new.id,
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
        today = date.today()
        leases = self.search([('state', '=', 'confirmed'), ('date', '<', today), ('state', '!=', 'expired')])
        for lease in leases:
            lease.write({'state': "expired"
                         })
        template = self.env.ref('property_management.lease_management_expire_template')
        template.send_mail(self.id, force_send=True)

    def _auto_followup_payment(self):
        today = date.today()
        late_payments = self.search([('state', '=', 'confirmed'), ('date', '<', today), ('invoice_paid', '=', False)])

        for lease in late_payments:
            template = self.env.ref('property_management.payment_followups_template')
            template.sudo().send_mail(lease.id, force_send=True)
            lease.message_post(body=_('Payment Reminder sent to %s') % lease.sequence_number)

