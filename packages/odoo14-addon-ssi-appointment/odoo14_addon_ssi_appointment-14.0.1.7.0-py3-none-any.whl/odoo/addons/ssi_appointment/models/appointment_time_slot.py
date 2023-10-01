# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AppointmentTimeSlot(models.Model):
    _name = "appointment_time_slot"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Appointment Time Slot"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    time_start = fields.Float(
        string="Start",
        required=True,
    )
    time_end = fields.Float(
        string="End",
        required=True,
    )
