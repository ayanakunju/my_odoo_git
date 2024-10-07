# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ast import literal_eval


class IdleSurvey(models.TransientModel):
    _inherit = 'res.config.settings'

    timer = fields.Float(string='Time', config_parameter='idle_timer.config_settings')
    redirect_time = fields.Float(string='Redirect time', config_parameter='idle_timer.config_settings')


class SurveyQuiz(models.Model):
    _inherit = 'survey.survey'

    def action_test_survey(self):
        """ Open the website page with the survey form into test mode """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Test Survey",
            'target': 'new',
            'url': '/survey/test/%s' % self.access_token,
        }


