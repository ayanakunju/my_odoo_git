from odoo import http
from odoo.http import request


class PropertyController(http.Controller):
    """This class is for the getting values for dynamic product snippets
         """
    @http.route(['/top_properties'],type='json', auth='public', website=True, methods=['POST'])
    def property_list(self):
        """Function for getting top properties"""
        properties = request.env['property.management'].search_read([],  order='create_date desc')
        property_values = {
            'properties': properties,
        }
        return property_values

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id):
        property_record = request.env['property.management'].browse(property_id)
        return request.render('property_management.property_land_template', {
            'property_record': property_record,
        })
