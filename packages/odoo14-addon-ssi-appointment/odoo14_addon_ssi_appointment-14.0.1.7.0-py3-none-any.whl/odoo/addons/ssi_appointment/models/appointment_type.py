# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AppointmentType(models.Model):
    _name = "appointment_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Appointment Type"

    allowed_appointee_ids = fields.Many2many(
        string="Allowed Appointee",
        comodel_name="res.users",
        relation="rel_appointment_type_2_user",
        column1="type_id",
        column2="user_id",
    )
