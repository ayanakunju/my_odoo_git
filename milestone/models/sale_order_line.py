# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """ model SaleOrderLine is used to inherit the sale order line and add the custom field Milestone """
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string='Milestone', help="Milestone")


class SaleOrder(models.Model):
    """model SaleOrder is used to inherit the sale order and create task and project based on the conditions"""
    _inherit = 'sale.order'

    project_created = fields.Boolean(string='Project Created')


    def action_create_project(self):
        for order in self:
            project = self.env['project.project'].create({
                'name': order.name,
                'sale_order_id': order.id,
            })
            self._create_tasks_for_project(project)
            self.project_created = True


    def action_update_project(self):
        for order in self:
            existing_project = self.env['project.project'].search([('name', '=', order.name)])
            existing_task = self.env['project.task'].search([('project_id','=',order.name)])
            if existing_project:
                existing_task.unlink()
                existing_project.unlink()
            self.action_create_project()

    def _create_tasks_for_project(self, project):
        milestones = {}
        for line in self.order_line:
            if line.milestone:
                milestone_name = f"Milestone {line.milestone}"
                if milestone_name not in milestones:
                    milestones[milestone_name] = []
                milestones[milestone_name].append(line.name)

        for milestone_name, products in milestones.items():
            print(milestones.items,"ss")
            parent_task = self.env['project.task'].create({
                'name': milestone_name,
                'project_id': project.id,
            })
            for product in products:
                self.env['project.task'].create({
                    'name': f"{milestone_name} - {product}",
                    'project_id': project.id,
                    'parent_id': parent_task.id,
                })

    def action_get_project(self):
        """ action_get_project function is for view the corresponding projects
        that are created inside the sale order """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'kanban,form,tree',
            'res_model': 'project.project',
            'context': "{'create': False}"
        }