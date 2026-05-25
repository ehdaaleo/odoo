from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import email_normalize


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        ondelete='restrict',
    )

    @api.constrains('related_patient_id', 'email')
    def _check_related_patient_email(self):
        for rec in self:
            normalized_email = email_normalize(rec.email) if rec.email else False
            if not rec.related_patient_id or not normalized_email:
                continue

            patient = self.env['hms.patient'].search([
                ('email_normalized', '=', normalized_email),
            ], limit=1)

            if patient:
                raise ValidationError(
                    "You cannot link a customer whose email already exists "
                    "on a patient."
                )

    @api.constrains('vat')
    def _check_vat_required(self):
        for rec in self:
            if not rec.vat:
                raise ValidationError("Tax ID is mandatory for customers.")

    def unlink(self):
        linked_customers = self.filtered('related_patient_id')
        if linked_customers:
            raise ValidationError(
                "You cannot delete a customer linked to a patient."
            )

        return super().unlink()
