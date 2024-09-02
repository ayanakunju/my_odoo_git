# -*- coding: utf-8 -*-

# from odoo import models, fields, api
#
#
#
#
# class PurchaseOrder(models.Model):
#   _inherit = 'purchase.order'
#
#   tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_id.tolerance_percentage')





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
