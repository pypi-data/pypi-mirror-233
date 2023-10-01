# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "appointment_schedule_count" in counters:
            values["appointment_schedule_count"] = (
                request.env["appointment_schedule"].search_count([])
                if request.env["appointment_schedule"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
        return values

    def _appointment_schedule_get_page_view_values(
        self, appointment_schedule, access_token, **kwargs
    ):
        values = {
            "page_name": "appointment-schedules",
            "appointment_schedule": appointment_schedule,
        }
        return self._get_page_view_values(
            appointment_schedule,
            access_token,
            values,
            "my_appointment_schedules_history",
            False,
            **kwargs
        )

    @http.route(
        ["/my/appointment-schedules", "/my/appointment-schedules/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_appointment_schedules(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        Schedule = request.env["appointment_schedule"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("# Schedule"), "order": "name"},
        }
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # projects count
        appointment_schedule_count = Schedule.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/appointment-schedules",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=appointment_schedule_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        appointment_schedules = Schedule.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_appointment_schedules_history"] = appointment_schedules.ids[
            :100
        ]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "appointment_schedules": appointment_schedules,
                "page_name": "appointment-schedules",
                "default_url": "/my/appointment-schedules",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("ssi_appointment.portal_my_appointment_schedules", values)

    @http.route(
        ["/my/appointment-schedule/<int:schedule_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_appointment_schedule(self, schedule_id=None, access_token=None, **kw):
        try:
            appointment_schedule_sudo = self._document_check_access(
                "appointment_schedule", schedule_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._appointment_schedule_get_page_view_values(
            appointment_schedule_sudo, access_token, **kw
        )
        return request.render("ssi_appointment.portal_my_appointment_schedule", values)
