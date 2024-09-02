# -*- coding: utf-8 -*-

from odoo import models, fields


class WarningMessageWizard(models.TransientModel):
    _name = 'warning.message.wizard'

    message = fields.Char(string='Message')
    accept_button = fields.Boolean(string='Accept')
    reject_button = fields.Boolean(string='Reject')

    def accept(self):
        return {'type': 'ir.actions.act_window_close'}

    def reject(self):
        return {'type': 'ir.actions.act_window_close'}

