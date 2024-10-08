# -*- coding: utf-8 -*-

from odoo import api, fields, models


class IdleSurvey(models.TransientModel):
    _inherit = 'res.config.settings'

    redirect_time = fields.Float(string='Redirect time (minutes)', config_parameter='idle_timer.config_settings')


class SurveyQuiz(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def get_values(self):
        redirect_time = self.env['res.config.settings'].search_read([], ['redirect_time'])
        return redirect_time
