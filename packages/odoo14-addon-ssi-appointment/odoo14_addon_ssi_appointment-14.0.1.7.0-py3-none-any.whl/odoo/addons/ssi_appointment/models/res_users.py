# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = [
        "res.users",
    ]

    allowed_appointment_type_ids = fields.Many2many(
        string="Allowed Appointment Type",
        comodel_name="appointment_type",
        relation="rel_appointment_type_2_user",
        column1="user_id",
        column2="type_id",
    )
