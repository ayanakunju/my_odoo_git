from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(string='Age')
    blood_group = fields.Selection(
        [('option 1', 'A+'), ('option 2', 'A-'), ('option 3', 'B+'), ('option 4', 'B-'), ('option 5', 'o+'),
         ('option 6', 'o-'), ('option 7', 'AB+'), ('option 8', 'AB-')])
    dob = fields.Date(string='DOB')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    dob = fields.Date(string='DOB')


class HrDepartment(models.Model):
    _inherit = 'hr.department'


class OpModel(models.Model):
    _name = 'op.model'
    _description = "Op Ticket"

    op_number = fields.Char(string="op", default=lambda self: _('New'),
                            copy=False, readonly=True, tracking=True)

    token_no = fields.Integer()
    age = fields.Integer()
    date = fields.Date()
    department_id = fields.Many2one('hr.department')
    patient_id = fields.Many2one('res.partner')
    doctor_id = fields.Many2one('hr.employee')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    def button_done(self):
        self.write({
            'state': "confirmed"
        })

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.age = self.patient_id.age

    @api.onchange('doctor_id')
    def onchange_doctor_id(self):
        self.department_id = self.doctor_id.department_id

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the op ticket """
        for vals in vals_list:
            if vals.get('op_number', _('New')) == _('New'):
                vals['op_number'] = self.env['ir.sequence'].next_by_code(
                    'op.ticket')
        return super().create(vals_list)


class ConsultationModel(models.Model):
    _name = 'consultation.model'
    _description = "Consultation Page"

    op_ticket = fields.Many2one(string='OP')
    date = fields.Date()
    patient_id = fields.Many2one('res.partner')
    age = fields.Integer()
    doctor_id = fields.Many2one('hr.employee')
    prescription = fields.Text()


#   # @api.depends('owned_property_ids')
#     # def _compute_owned_properties(self):
#     #     for record in self:
#     #         properties = [(rec.property_name, rec.state) for rec in record.owned_property_ids]
#     #         record.owned_property_summary = ', '.join(f'{name} ({state})' for name, state in properties)