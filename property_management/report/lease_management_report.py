# -*- coding: utf-8 -*-


from odoo import models, api
from odoo.exceptions import ValidationError


class AbstractLeaseModel(models.AbstractModel):

    _name = 'report.property_management.lease_management_report'
    _description = 'Abstract Report Model'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            raise ValidationError("No data provided for the report.")
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

        return {
            'data': results,
        }
