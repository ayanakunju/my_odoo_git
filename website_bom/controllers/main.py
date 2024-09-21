from odoo import http
from odoo.http import request

class BomController(http.Controller):

    @http.route('/shop/bom/<int:product_id>', type='http', auth='public', website=True)
    def view_bom(self, product_id, **kwargs):
        product = request.env['product.product'].sudo().browse(product_id)
        if not product.exists():
            return request.not_found()

        bom_lines = product.bom_ids.bom_line_ids
        return request.render('website_bom.bom_template', {
            'product': product,
            'bom_lines': bom_lines,
        })
