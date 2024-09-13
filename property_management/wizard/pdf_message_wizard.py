# -*- coding: utf-8 -*-

import io
import xlsxwriter
from odoo import fields, models, api, _
from odoo.tools import date_utils
from odoo.exceptions import ValidationError
import json


class PdfMessageWizard(models.TransientModel):
    _name = 'pdf.message.wizard'
    _description = 'Pdf Message Wizard'

    from_date = fields.Datetime(string='From Date')
    to_date = fields.Datetime(string='To Date')
    tenant_ids = fields.Many2many('res.partner', string='Customer')
    owner_id = fields.Many2one('hr.employee', string='Owner')
    status = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], default='rent')
    property_id = fields.Many2one('property.management', string='Property')

    def print_report(self):
        data = {
            'to_date': self.to_date,
            'from_date': self.from_date,
            'tenant_ids': self.tenant_ids.ids,
            'status': self.status,
            'owner_id': self.owner_id.id,
            'property_id': self.property_id.id,
        }
        return self.env.ref('property_management.action_report_lease_management').report_action(None, data=data)

    def print_xlsx(self):

        data = {
            'to_date': self.to_date,
            'from_date': self.from_date,
            'tenant_ids': self.tenant_ids.ids,
            'status': self.status,
            'owner_id': self.owner_id.id,
            'property_id': self.property_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'pdf.message.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    @api.model
    def get_xlsx_report(self, data, response):

        query = """
                    SELECT
                        rp_tenant.name AS tenant,
                        lm.state,
        				lm.status,
                        hr_owner.name AS owner,
                        lm.date_start AS start_date,
                        lm.date AS end_date,
                        pm.property_name,
                        mp.rental_amount
                    FROM lease_management AS lm
        			INNER JOIN multiple_property mp ON lm.id = mp.id
                    LEFT JOIN property_management pm ON mp.multiple_property_id = pm.id
                    LEFT JOIN res_partner rp_tenant ON lm.tenant_id = rp_tenant.id
                    LEFT JOIN hr_employee hr_owner ON pm.owner_id = hr_owner.id
                    WHERE 1=1 		

                """

        if data.get('from_date'):
            query += " AND lm.date_start >= '%s'" % (data['from_date'])
        if data.get('to_date'):
            query += " AND lm.date <= '%s'" % (data['to_date'])
        if data.get('tenant_ids'):
            query += " AND lm.tenant_id in %s" % str(tuple(data['tenant_ids'])).replace(',)', ')')
        if data.get('status'):
            query += " AND lm.status = '%s'" % (data['status'])
        if data.get('owner_id'):
            query += " AND pm.owner_id = '%s'" % (data['owner_id'])
        if data.get('property_id'):
            query += " AND pm.id = '%s'" % (data['property_id'])
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()

        if not results:
            raise ValidationError("No records found for the given criteria.")

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        nums = workbook.add_format({'font_size': '10px', 'align': 'right'})

        sheet.merge_range('B2:O3', 'PROPERTY MANAGEMENT REPORT', head)
        sheet.merge_range('B5:C5', 'Tenant', cell_format)
        sheet.merge_range('D5:E5', 'Property', cell_format)
        sheet.merge_range('F5:G5', 'Owner', cell_format)
        sheet.merge_range('H5:I5', 'status', cell_format)
        sheet.merge_range('J5:K5', 'Start Date', cell_format)
        sheet.merge_range('L5:M5', 'End Date', cell_format)
        sheet.merge_range('N5:O5', 'Amount', cell_format)
        row = 5
        for record in results:
            row += 1
            sheet.merge_range(f'B{row}:C{row}', record['tenant'], txt)
            sheet.merge_range(f'D{row}:E{row}', record['property_name'], txt)
            sheet.merge_range(f'F{row}:G{row}', record['owner'], txt)
            sheet.merge_range(f'H{row}:I{row}', record['status'], txt)
            sheet.merge_range(f'J{row}:K{row}', record['start_date'].strftime('%Y-%m-%d'), txt)
            sheet.merge_range(f'L{row}:M{row}', record['end_date'].strftime('%Y-%m-%d'), txt)
            sheet.merge_range(f'N{row}:O{row}', record['rental_amount'], nums)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
