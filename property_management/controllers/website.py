from odoo.http import request, Controller, route

class WebFormController(Controller):
    @route('/rent_lease', auth='public', website=True)
    def web_form(self, **kwargs):
        properties = request.env['property.management'].sudo().search([])
        return request.render("property_management.web_form_template",{
            'properties':properties,
        })

    @route('/rent_lease/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print(post)
        request.env['lease.management'].sudo().create({
                    'tenant_id': request.env.user.id,
                    'status': post.get('status'),
                    'date_start': post.get('date_start'),
                    'date': post.get('date'),
                })
        return request.redirect('/thank-you-page')

