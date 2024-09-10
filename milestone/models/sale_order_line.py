# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    """ model SaleOrderLine is used to inherit the sale order line and add the custom field Milestone """
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string='Milestone', help="create project and task based on the milestone field")
    task_id = fields.Many2one('project.task', string='Related Task')

class SaleOrder(models.Model):
    """model SaleOrder is used to inherit the sale order and create task and project based on the conditions"""
    _inherit = 'sale.order'

    is_project_created = fields.Boolean(string='Project Created')

    def action_create_project(self):
        """ for create the project"""
        for order in self:
            project = self.env['project.project'].create({
                'name': order.name,
                'sale_order_id': order.id,
            })
            self._create_tasks_for_project(project)
            self.is_project_created = True

    def action_update_project(self):
        """for updating the project and task"""
        for order in self:
            existing_project = self.env['project.project'].search([('sale_order_id', '=', order.id)])
            existing_task = self.env['project.task'].search([('project_id','=',order.id)])
            if existing_project:
                existing_task.unlink()
                existing_project.unlink()
            self.action_create_project()

    def _create_tasks_for_project(self, project):
        """Function to create the project and tasks"""
        tasks = [(f"Milestone {line.milestone}", line.name) for line in self.order_line if line.milestone]
        milestones = {}
        for milestone, task in tasks:
            if milestone not in milestones:
                milestones.setdefault(milestone,tasks)

        for milestone_name, products in milestones.items():
            parent_task = self.env['project.task'].create({
                'name': milestone_name,
                'project_id': project.id,
            })
            child_tasks = [(self.env['project.task'].create({
                    'name': f"{milestone_name} - {product}",
                    'project_id': project.id,
                    'parent_id': parent_task.id,
                })) for product in products]

    def action_get_project(self):
        """ action_get_project function is for view the corresponding projects
        that are created inside the sale order """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'kanban,form,tree',
            'res_model': 'project.project',
            'context': {'create': False, 'name': self.project_id.id}
        }
