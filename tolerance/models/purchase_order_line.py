# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    tolerance_percentage = fields.Float(string='Tolerance  (%)')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                purchase_lines = self.env['purchase.order.line'].search([('sale_line_id', '=', line.id)])
                for purchase_line in purchase_lines:
                    purchase_line.tolerance_percentage = line.tolerance_percentage
        return res



# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     def action_confirm(self):
#         super(SaleOrder, self).action_confirm()
#         for order in self:
#             for line in order.order_line:
#                 purchase_lines = self.env['purchase.order.line'].search([('sale_line_id', '=', line.id)])
#                 for purchase_line in purchase_lines:
#                     purchase_line.x_custom_field = line.x_custom_field





# class PurchaseOrder(models.Model):
#    _inherit = 'purchase.order'
#
#    @api.onchange('sale_order_id')
#    def onchange_sale_order_id(self):
#       if self.sale_order_id:
#         self.tolerance_percent = self.sale_order_id.partner_id.tolerance_percent
#
#    tolerance_percent = fields.Float(string='Tolerance (%)', default=0)



#    from odoo import models, fields, api
#
# class Customer(models.Model):
#   _inherit = 'res.partner'
#
#  tolerance_percentage = fields.Float(string='Tolerance Percentage')
#
# # Update Sale Order model
# class SaleOrder(models.Model):
#   _inherit = 'sale.order'

#   tolerance_percentage = fields.Float(string='Tolerance Percentage', related='partner_id.tolerance_percentage')
#
# # Update Sale Order Line model
# class SaleOrderLine(models.Model):
#   _inherit = 'sale.order.line'

#   tolerance_percentage = fields.Float(string='Tolerance Percentage', related='order_id.tolerance_percentage')
#
# # Update Purchase Order model
# class PurchaseOrder(models.Model):
#   _inherit = 'purchase.order'
#
#   tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_id.tolerance_percentage')
#
# # Update Internal Transfer model
# class InternalTransfer(models.Model):
#   _inherit = 'stock.picking'

#   tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_id.tolerance_percentage')
#
# # Implement tolerance calculation
# def calculate_tolerance_range(ordered_qty, tolerance_percentage):
#   min_qty = ordered_qty - (ordered_qty * tolerance_percentage / 100)
#   max_qty = ordered_qty + (ordered_qty * tolerance_percentage / 100)
#   return min_qty, max_qty
#
# # Update transfer quantity
# class StockMove(models.Model):
#   _inherit = 'stock.move'


#   @api.onchange('quantity_done')
#   def onchange_quantity_done(self):
#    if self.picking_id.sale_order_id:
#  min_qty, max_qty = calculate_tolerance_range(self.product_uom_qty, self.picking_id.tolerance_percentage)
#  if self.quantity_done < min_qty or self.quantity_done > max_qty:
#   # Display warning message wizard
#   wizard = self.env['warning.message.wizard'].create({
#    'message': 'Quantity is outside acceptable range. Accept or reject?',
#    'accept_button': 'Accept',
#    'reject_button': 'Reject'
#   })
#   if wizard.accept_button:
#    self.quantity_done = min_qty
#   else:
#    self.quantity_done = 0


# # Create warning message wizard
# class WarningMessageWizard(models.TransientModel):
#   _name = 'warning.message.wizard'
#
#   message = fields.Char(string='Message')
#   accept_button = fields.Boolean(string='Accept')
#   reject_button = fields.Boolean(string='Reject')
#
#   def accept(self):
#    return {'type': 'ir.actions.act_window_close'}
#
#   def reject(self):
#    return {'type': 'ir.actions.act_window_close'}
#
#
# <?xml version="1.0" encoding="utf-8"?>
# <odoo>
#   <!-- Add tolerance percentage field to Customer form view -->
#   <record id="view_partner_form" model="ir.ui.view">
#    <field name="name">res.partner.form</field>
#    <field name="model">res.partner</field>
#    <field name="inherit_id" ref="base.view_partner_form"/>
#    <field name="arch" type="xml">
#  <xpath expr="//field[@name='name']" position="after">
#   <field name="tolerance_percentage"/>
#  </xpath>
#   </field>
#   </record>
#
#   <!-- Add tolerance percentage field to Sale Order form view -->
#   <record id="view_sale_order_form" model="ir.ui.view">
#    <field name="name">sale.order.form</field>
#    <field name="model">sale.order</field>
#    <field name="inherit_id" ref="sale.view_order_form"/>
#    <field name="arch" type="xml">
#  <xpath expr="//field[@name='partner_id']" position="after">
#   <field name="tolerance_percentage"/>
#  </xpath>
#    </field>
#   </record>
#
#   <!-- Add tolerance percentage field to Sale Order Line form view -->
#   <record id="view_sale_order_line_form" model="ir.ui.view">
#    <field name="name">sale.order.line.form</field>
#    <field name="model">sale.order.line</field>
#    <field name="inherit_id" ref="sale.view_order_line_form"/>
#    <field name="arch" type="xml">
#  <xpath expr="//field[@name='product_id']" position="after">
#   <field name="tolerance_percentage"/>
#  </xpath>
#    </field>
#   </record>
#
#   <!-- Add tolerance percentage field to Purchase Order form view -->
#   <record id="view_purchase_order_form" model="ir.ui.view">
#    <field name="name">purchase.order.form</field>
#   <field name="model">purchase.order</field>
#    <field name="inherit_id" ref="purchase.view_order_form"/>
#    <field name="arch" type="xml">
#  <xpath expr="//field[@name='partner_id']" position="after">
#   <field name="tolerance_percentage"/>
#  </xpath>
#    </field>
#   </record>
#
#  <!-- Add tolerance percentage field to Internal Transfer form view -->
#   <record id="view_stock_picking_form" model="ir.ui.view">
#    <field name="name">stock.picking.form</field>
#    <field name="model">stock.picking</field>
#    <field name="inherit_id" ref="stock.view_picking_form"/>
#    <field name="arch" type="xml">
#  <xpath expr="//field[@name='partner_id']" position="after">
#   <field name="tolerance_percentage"/>
#  </xpath>
#    </field>
#   </record>


#
# from odoo import models, fields, api
#
# class WarningMessageWizard(models.TransientModel):
#     _name = 'warning.message.wizard'
#     _description = 'Warning Message Wizard'
#
#     default_message = fields.Text(string='Message')
#     default_accept_button = fields.Char(string='Accept Button')
#     default_reject_button = fields.Char(string='Reject Button')
#     default_move_ids = fields.Many2many('stock.move', string='Moves')
#
#     def action_accept(self):
#         for move in self.default_move_ids:
#             move.picking_id.button_validate()
#         return {'type': 'ir.actions.act_window_close'}
#
#     def action_reject(self):
#         return {'type': 'ir.actions.act_window_close'}
# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     def button_validate(self):
#         for record in self:
#             if record.move_ids_without_package:
#                 sale_order = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
#                 if sale_order:
#                     tolerance = sale_order.order_line.tolerance_percentage
#                     out_of_range_moves = []
#                     for move in record.move_ids_without_package:
#                         min_qty = move.product_uom_qty - tolerance
#                         max_qty = move.product_uom_qty + tolerance
#                         if move.quantity < min_qty or move.quantity > max_qty:
#                             out_of_range_moves.append(move)
#
#                     if out_of_range_moves:
#                         return {
#                             'type': 'ir.actions.act_window',
#                             'res_model': 'warning.message.wizard',
#                             'view_mode': 'form',
#                             'view_id': self.env.ref('tolerance.view_warning_message_wizard_form').id,
#                             'target': 'new',
#                             'context': {
#                                 'default_message': 'Some quantities are out of the acceptable range. Do you want to accept or reject?',
#                                 'default_accept_button': 'Accept',
#                                 'default_reject_button': 'Reject',
#                                 'default_move_ids': [(6, 0, [move.id for move in out_of_range_moves])],
#                             }
#                         }
#         return super(StockPicking, self).button_validate()
# <odoo>
#     <record id="view_warning_message_wizard_form" model="ir.ui.view">
#         <field name="name">warning.message.wizard.form</field>
#         <field name="model">warning.message.wizard</field>
#         <field name="arch" type="xml">
#             <form string="Warning">
#                 <group>
#                     <field name="default_message" readonly="1"/>
#                 </group>
#                 <footer>
#                     <button name="action_accept" type="object" string="Accept" class="btn-primary"/>
#                     <button name="action_reject" type="object" string="Reject" class="btn-secondary"/>
#                 </footer>
#             </form>
#         </field>
#     </record>
# </odoo>
#
#
