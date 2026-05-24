from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    birth_date = fields.Date()

    history = fields.Html()

    cr_ratio = fields.Float()

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ])

    pcr = fields.Boolean()

    image = fields.Image()

    address = fields.Text()

    age = fields.Integer(
        compute="_compute_age",
        store=True
    )

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    department_id = fields.Many2one(
        'hms.department',
        domain="[('is_opened', '=', True)]"
    )

    department_capacity = fields.Integer(
        related='department_id.capacity'
    )

    doctor_ids = fields.Many2many(
        'hms.doctor'
    )

    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()

                rec.age = (
                    today.year
                    - rec.birth_date.year
                    - (
                        (today.month, today.day)
                        <
                        (rec.birth_date.month, rec.birth_date.day)
                    )
                )
            else:
                rec.age = 0

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError(
                    "CR Ratio is required when PCR is checked"
                )

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically because age is below 30'
                }
            }

    def write(self, vals):

        if 'state' in vals:
            for rec in self:

                self.env['hms.patient.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {vals['state']}"
                })

        return super().write(vals)