# -*- coding: utf-8 -*-
from odoo import models, fields


class WarningMessageWizard(models.TransientModel):
    _name = 'warning.message.wizard'
    _description = 'Warning Message Wizard'

    message = fields.Text(string="Quantity is out of the acceptable range. Do you want to accept or reject?")
    default_accept_button = fields.Char(string='Accept Button')
    default_reject_button = fields.Char(string='Reject Button')
    default_move_id = fields.Many2one('stock.move', string='Moves')

    def action_accept(self):
        """accept button function for the wizard """
        picking_id = self.env.context.get('active_id')
        if picking_id:
            picking = self.env['stock.picking'].browse(picking_id)
            if picking:
                picking.with_context(validate_from_wizard=True).button_validate()
        return {'type': 'ir.actions.act_window_close'}

    def action_reject(self):
        """action_reject function for the don't accept button"""
        return {'type': 'ir.actions.act_window_close'}