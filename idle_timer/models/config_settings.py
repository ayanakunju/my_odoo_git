# -*- coding: utf-8 -*-

from odoo import  fields, models


class IdleSurvey(models.TransientModel):
    _inherit = 'res.config.settings'

    idle_time = fields.Float(string='Idle Time (minutes)', config_parameter='idle_timer.idle_time')
    idle_seconds = fields.Integer(string="Idle Time", store=True, config_parameter='quiz_idle_timer.idle_seconds')
