# -*- coding: utf-8 -*-

from odoo import models,api
from odoo.exceptions import ValidationError


class AbstractLeaseModel(models.AbstractModel):
    _name = 'report.lease_management.lease_management_report'
    _description = 'Abstract Report Model'


    @api.model
    def _get_report_values(self, docids, data=None):
        print("data",data)

        query = f""" SELECT rp_tenant.name AS tenant,lm.state,lm.type,hr_owner.name AS owner,
                                lm.due_date,pm.property_name,mp.rental_amount FROM lease_management lm
                                INNER JOIN multiple_property mp ON lm.id=mp.multiple_property_id
                                LEFT JOIN property_management pm ON mp.property_id=pm.id
                                LEFT JOIN res_partner rp_tenant ON lm.tenant_id=rp.tenant_id.id
                                LEFT JOIN hr_employee hr_owner ON mp.owner_id=hr.owner_id.id
                                %s  """


        params = []
        where_clause = 'WHERE'
        if data['from_date'] and data['to_date']:
            where_clause += "lm.due_date BETWEEN %s AND %s"
            params = [data['from_date'], data['to_date']]
        elif data['from_date']:
            where_clause += "lm.due_date>=%s"
            params = [data['from_date']]
        elif data['to_date']:
            where_clause += "lm.due_date<=%s"
            params = [data['to_date']]
        else:
            where_clause += " true "
        if data['tenant_id']:
            where_clause += " AND lm.tenant_id=%s "
            params.append(data['tenant_id'])
        if data['state']:
            where_clause += " AND lm.state=%s "
            params.append(data['state'])
        if data['type']:
            where_clause += " AND lm.type=%s "
            params.append(data['type'])
        if data['owner_id']:
            where_clause += " AND lm.owner_id=%s "
            params.append(data['owner_id'])
        if data['property_id']:
            where_clause += " AND lm.property_id=%s "
            params.append(data['property_id'])
            print('params',params)

        self.env.cr.execute(query,params)
        return {
            'data': data,
        }


    # @api.constrains('from_date', 'to_date')
    # def _check_dates(self):
    #     for record in self:
    #         if record.from_date > record.to_date:
    #             raise ValidationError('The "From Date" cannot be later than the "To Date".')



    # def _fetch_report_data(self):
    #     """ Fetch report data using SQL query """
    #     self.env.cr.execute("""
    #         SELECT lm.sequence_number, lm.tenant_id, lm.date_start, lm.date, lm.status, mp.property_name,
    #                lm.legal_amount, lm.total_amount, lm.state
    #         FROM lease_management lm
    #         JOIN multiple_property mp ON lm.property_id = mp.id
    #         WHERE lm.date_start >= %s AND lm.date <= %s
    #           AND (%s IS NULL OR lm.state = %s)
    #           AND (%s IS NULL OR lm.tenant_id = %s)
    #           AND (%s IS NULL OR mp.owner_id = %s)
    #           AND (%s IS NULL OR lm.status = %s)
    #         """, (self.from_date, self.to_date, self.state, self.state, self.tenant_id.id, self.tenant_id.id,
    #               self.owner_id.id, self.owner_id.id, self.lease_type, self.lease_type))
    #
    #     data = self.env.cr.fetchall()
#
#         if not data:
#             raise ValidationError('No data found for the given criteria.')
#
#         return data
