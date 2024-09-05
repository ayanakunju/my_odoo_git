# -*- coding: utf-8 -*-
from asyncio import create_task

from wheel.cli.convert import parse_wininst_info

from odoo import models, fields


class SaleOrderLine(models.Model):
    """ model SaleOrderLine is used to inherit the sale order line and add the custom field Milestone """
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string='Milestone', help="Milestone")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_project(self):
        """action create project is to create project and task when clicking the create project button"""
        project = self.env['project.project']
        task = self.env['project.task']
        for order in self:
            project = project.create({'name': order.name})

            lines_by_milestone = {}
            for line in order.order_line:
                milestone = line.milestone or 0
                if milestone not in Q:
                    lines_by_milestone[milestone] = []
                    lines_by_milestone[milestone].append(line)
                    for lines in lines_by_milestone.items():
                        parent_task_name = f"Milestone {milestone}"
                        parent_task = task.create({'name': parent_task_name, 'project_id': project.id})
        return
