# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AppointmentSchedule(models.Model):
    _name = "appointment_schedule"
    _inherit = [
        "portal.mixin",
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
    ]
    _description = "Appointment Schedule"
    _order = "date, time_slot_id"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "ready"
    _approval_state = "confirm"
    _after_approved_method = "action_ready"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_ready_policy_fields = False
    _automatically_insert_ready_button = False

    _statusbar_visible_label = "draft,confirm,ready,open,done"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_ready",
        "dom_open",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    _create_sequence_state = "ready"

    title = fields.Char(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default="-",
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", False),
            ("parent_id", "!=", False),
        ],
        ondelete="restrict",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    commercial_partner_id = fields.Many2one(
        string="Commercial Contact",
        comodel_name="res.partner",
        related="partner_id.commercial_partner_id",
        store=True,
    )
    appointee_id = fields.Many2one(
        string="Appointee",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_type_ids = fields.Many2many(
        string="Allowed Type User",
        comodel_name="appointment_type",
        related="appointee_id.allowed_appointment_type_ids",
        store=False,
    )
    type_ids = fields.Many2many(
        string="Allowed Types",
        comodel_name="appointment_type",
        relation="rel_appointment_schedule_2_type",
        column1="schedule_id",
        column2="type_id",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="appointment_type",
        ondelete="restrict",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
                ("required", False),
            ],
        },
    )
    time_slot_id = fields.Many2one(
        string="Time Slot",
        comodel_name="appointment_time_slot",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    appointment_method = fields.Selection(
        string="Method",
        selection=[
            ("online", "Online"),
            ("offline", "Offline"),
        ],
        copy=False,
        default="online",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    appointment_invitation_link = fields.Char(
        string="Invitation Link",
    )
    appointment_video_link = fields.Char(
        string="Video Link",
    )
    host_id = fields.Many2one(
        comodel_name="res.users",
        string="Host",
        required=False,
    )
    co_appointee_ids = fields.Many2many(
        comodel_name="res.users",
        string="Co-Appointees",
        relation="rel_appointment_schedule_2_users",
        column1="schedule_id",
        column2="type_id",
        required=False,
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self._default_date(),
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("ready", "Ready to Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("terminate", "Terminate"),
            ("reject", "Reject"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    @api.model
    def _get_policy_field(self):
        res = super(AppointmentSchedule, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "terminate_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.constrains("time_slot_id", "appointee_id", "date")
    def _check_timeslot(self):
        error_msg = _("Time slot already schedulled")
        Schedule = self.env["appointment_schedule"]
        for document in self:
            criteria = [
                ("date", "=", document.date),
                ("appointee_id", "=", document.appointee_id.id),
                ("time_slot_id", "=", document.time_slot_id.id),
                ("id", "!=", document.id),
            ]
            appointment_count = Schedule.search_count(criteria)
            if appointment_count > 0:
                raise ValidationError(error_msg)

    @api.onchange(
        "appointee_id",
    )
    def onchange_types_ids(self):
        self.type_ids = False

    @api.onchange(
        "appointee_id",
        "type_ids",
    )
    def onchange_types_id(self):
        self.type_id = False
