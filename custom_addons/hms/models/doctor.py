from odoo import models, fields


class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'HMS Doctor'

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    image = fields.Image()

    department_id = fields.Many2one(
        'hms.department',
        string="Department"
    )

    patient_ids = fields.Many2many(
        'hms.patient',
        string="Patients"
    )

    display_name = fields.Char(
        compute="_compute_display_name"
    )

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.first_name} {rec.last_name}"