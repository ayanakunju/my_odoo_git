# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route
from odoo import fields


class WebFormController(Controller):
    @route('/rent_lease', auth='user', website=True)
    def web_form(self, **kwargs):
        properties = request.env['property.management'].sudo().search([])
        return request.render("property_management.web_form_template", {
            'properties': properties,
        })

    @route('/rent_lease/submit', type='http', auth='user', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        request.env['lease.management'].sudo().create({
            'tenant_id': request.env.user.partner_id.id,
            'status': post.get('status'),
            'date_start': post.get('date_start'),
            'date': post.get('date'),
            'order_line_ids': [fields.Command.create({
                'multiple_property_id': post.get('property_id')
            })],
        })
        return request.render("property_management.web_rent_thanks")