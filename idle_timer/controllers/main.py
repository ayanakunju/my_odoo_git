from odoo import http
from odoo.http import request


class QuizTimeSelector(http.Controller):

    @http.route('/get_idle_time/timer', auth='public', type='json')
    def get_idle_time(self):
            idle_time = request.env['ir.config_parameter'].sudo().get_param('idle_timer.idle_time')
            idle_seconds = request.env['ir.config_parameter'].sudo().get_param('idle_timer.idle_seconds')
            data = {
                'idle_time': idle_time,
                'idle_seconds': idle_seconds,
            }
            return data

# from odoo.addons.survey.controllers.main import Survey
# from odoo import http
# from odoo.http import request
#
#
# class IdleTimer(Survey):
#     @http.route('/survey/<string:survey_token>/<string:answer_token>', type='http', auth='public', website=True)
#     def survey_display_page(self, survey_token, answer_token, **post):
#         idle_time = request.env['ir.config_parameter'].sudo().get_param('idle_timer.config_settings')
#         print(idle_time, 'qwertyui')
#
#         access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
#         if access_data['validity_code'] is not True:
#             return self._redirect_with_error(access_data, access_data['validity_code'])
#
#         answer_sudo = access_data['answer_sudo']
#         if answer_sudo.state != 'done' and answer_sudo.survey_time_limit_reached:
#             answer_sudo._mark_done()
#
#         return request.render('survey.survey_page_fill',
#                               self._prepare_survey_data(access_data['survey_sudo'], answer_sudo, **post))

