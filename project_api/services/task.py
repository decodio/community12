# Copyright 2016 Akretion (http://www.akretion.com)
# Benoit Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=W8106
# pylint: disable=consider-merging-classes-inherited

import json
import logging

from odoo import fields as odoo_fields
from odoo.exceptions import AccessError
from odoo.tools.translate import _

from odoo.addons.base_rest.components.service import to_bool
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class ExternalTaskService(Component):
    _inherit = "base.rest.service"
    _name = "external.task.service"
    _collection = "project.project"
    _usage = "task"

    @property
    def partner(self):
        return self.work.partner

    def _map_partner_read_to_data(self, partner_read):
        if not partner_read or not partner_read[0]:
            # partner_read[0] can have the value 0 when their is not
            # partner linked to the message
            return False
        else:
            partner = self.env["res.partner"].browse(partner_read[0])
            if partner.customer_uid:
                return {
                    "type": "customer",
                    "vals": (partner.customer_uid, partner.name),
                }
            elif partner.user_ids:
                update_date = partner.write_date or partner.create_date
                return {
                    "type": "support",
                    "uid": partner.id,
                    "update_date": odoo_fields.Datetime.to_string(update_date),
                }
            else:
                return {"type": "anonymous", "vals": (0, partner.name)}

    def search(self, domain, offset, limit, order, count):
        domain = [("project_id.partner_id", "=", self.partner.id)] + domain
        tasks = self.env["project.task"].search(
            domain, offset=offset, limit=limit, order=order, count=count
        )
        if tasks:
            if count:
                # count will return the number of task in the tasks variable
                return tasks
            return tasks.ids
        return []

    def read(self, ids, fields, load):
        tasks = self.env["project.task"].search(
            [("id", "in", ids), ("project_id.partner_id", "=", self.partner.id)]
        )
        tasks = tasks.read(fields=fields, load=load)
        if tasks:
            for task in tasks:
                if "create_date" in task:
                    task["create_date"] = odoo_fields.Datetime.to_string(
                        task["create_date"]
                    )
                if "message_ids" in task:
                    messages = self.env["mail.message"].search(
                        [
                            ("id", "in", task["message_ids"]),
                            "|",
                            ("subtype_id.internal", "=", False),
                            ("subtype_id", "=", False),
                        ]
                    )
                    task["message_ids"] = ["external/%s" % mid for mid in messages.ids]
                for key in [
                    "author_id",
                    "assignee_customer_id",
                    "assignee_supplier_id",
                ]:

                    if key in task:
                        task[key] = self._map_partner_read_to_data(task[key])
                if "tag_ids" in task:
                    task["tag_ids"] = task["tag_ids"] and task["tag_ids"][0] or False
                    if "color" in task:
                        if task["tag_ids"]:
                            task["color"] = (
                                self.env["project.tags"]
                                .search([("id", "=", task["tag_ids"])])
                                .color
                            )
                        else:
                            task["color"] = 0
            return tasks
        return []

    def _get_all_project_ids_from_domain(self, domain):
        # Note we apply a filter on a project we will always
        # show all stage of this project
        # this is not a perfect solution aand will not work with
        # advanced filtering on client side
        all_project_ids = (
            self.env["project.project"]
            .search([("partner_id", "=", self.partner.id)])
            .ids
        )
        project_ids = []
        for elem in domain:
            if len(elem) == 3 and elem[0] == "project_id" and elem[1] == "=":
                if elem[2] in all_project_ids:
                    project_ids.append(elem[2])
        return project_ids

    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        domain = [("project_id.partner_id", "=", self.partner.id)] + domain
        task_obj = self.env["project.task"]
        if "stage_name" in groupby[0]:
            groupby[0] = "stage_id"
            fields[fields.index("stage_name")] = "stage_id"
            project_ids = self._get_all_project_ids_from_domain(domain)
            task_obj = task_obj.with_context(stage_from_project_ids=project_ids)
        groups = task_obj.read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
        if groupby[0] == "stage_id":
            for group in groups:
                group["stage_name"] = group.pop("stage_id")[1]._value
                group["stage_name_count"] = group.pop("stage_id_count")
        return groups

    def create(self, assignee_customer=None, **params):
        if assignee_customer:
            params["assignee_customer_id"] = self._get_partner(assignee_customer).id
        partner = self._get_partner(params.pop("author"))
        if not params.get("project_id"):
            params["project_id"] = self.partner.help_desk_project_id.id
        params["author_id"] = partner.id
        if params.get("tag_ids"):
            params["tag_ids"] = [(6, 0, [params["tag_ids"]])]
        task = (
            self.env["project.task"]
            .with_context(force_message_author_id=partner.id)
            .create(params)
        )
        return task.id

    def write(self, ids, vals, author, assignee_customer=None):
        author = self._get_partner(author)
        tasks = self.env["project.task"].search(
            [("id", "in", ids), ("project_id.partner_id", "=", self.partner.id)]
        )
        if len(tasks) < len(ids):
            raise AccessError(_("You do not have the right to modify this records"))
        if assignee_customer:
            vals["assignee_customer_id"] = self._get_partner(assignee_customer).id
        if "tag_ids" in vals:
            vals["tag_ids"] = [(6, 0, [vals["tag_ids"]])]
        # Replace field name for write because attachment_ids already exists natively
        if "attachment_ids" in vals:
            vals["support_attachment_ids"] = vals["attachment_ids"]
        return tasks.with_context(force_message_author_id=author.id).write(vals)

    def message_format(self, ids):
        allowed_task_ids = (
            self.env["project.task"]
            .search([("project_id.partner_id", "=", self.partner.id)])
            .ids
        )
        messages = self.env["mail.message"].browse(ids).message_format()
        if messages:
            for message in messages:
                if (
                    message["model"] != "project.task"
                    or message["res_id"] not in allowed_task_ids
                ):
                    raise AccessError(_("You can not read this message"))
                else:
                    message.update(
                        {"model": "external.task", "id": "external/%s" % message["id"]}
                    )
                    message["author_id"] = self._map_partner_read_to_data(
                        message["author_id"]
                    )
                if "date" in message:
                    message["date"] = odoo_fields.Datetime.to_string(message["date"])
            return messages
        return []

    def get_message(self, params):
        messages = self.env["mail.message"].message_read(
            ids=json.loads(params["ids"]),
            domain=json.loads(params["domain"]),
            message_unload_ids=json.loads(params["message_unload_ids"]),
            thread_level=params["thread_level"],
            parent_id=params["parent_id"],
            limit=params["limit"],
        )
        if messages:
            return messages
        return []

    def _get_partner(self, data):
        domain = [("parent_id", "=", self.partner.id)]
        if data.get("email"):
            domain += [
                "|",
                ("customer_uid", "=", data["uid"]),
                ("email", "=", data["email"]),
            ]
        else:
            domain += [("customer_uid", "=", data["uid"])]
        partner = self.env["res.partner"].search(domain)
        if not partner:
            partner = self.env["res.partner"].create(
                {
                    "parent_id": self.partner.id,
                    "image": data["image"],
                    "name": data["name"],
                    "customer_uid": data["uid"],
                    "email": data["email"],
                    "mobile": data["mobile"],
                    "phone": data["phone"],
                }
            )
        elif (
            partner.name != data["name"]
            or partner.image != data["image"]
            or partner.email != data["email"]
            or partner.mobile != data["mobile"]
        ):
            _logger.debug("Update partner information")
            partner.write(
                {
                    "name": data["name"],
                    "image": data["image"],
                    "email": data["email"],
                    "mobile": data["mobile"],
                    "phone": data["phone"],
                    "customer_uid": data["uid"],
                }
            )
        return partner

    def message_post(self, _id, body, author):
        partner = self._get_partner(author)
        domain = [("res_id", "=", _id), ("model", "=", "project.task")]
        parent = self.env["mail.message"].search(
            domain + [("message_type", "=", "email")], order="id ASC", limit=1
        )
        if not parent:
            parent = self.env["mail.message"].search(domain, order="id ASC", limit=1)
        task = self.env["project.task"].browse(_id)
        message = task.message_post(
            body=body,
            attachment_ids=[],
            parent_id=parent.id,
            subtype="mail.mt_comment",
            author_id=partner.id,
            message_type="comment",
            partner_ids=[],
            subject=_(""),
        )
        return message.id

    def project_list(self):
        result = []
        helpdesk = self.partner.help_desk_project_id
        if helpdesk:
            result.append((helpdesk.id, helpdesk._get_customer_project_name()))
        projects = self.env["project.project"].search(
            [("partner_id", "=", self.partner.id), ("id", "!=", helpdesk.id)]
        )
        result += [(p.id, p._get_customer_project_name()) for p in projects]
        return result

    def type_list(self):
        projects = self.partner.help_desk_project_id
        projects |= self.env["project.project"].search(
            [("partner_id", "=", self.partner.id), ("id", "!=", projects.id)]
        )
        tags = self.env["project.tags"]
        for project in projects:
            tags |= project.tag_ids
        return [(tag.id, tag.name) for tag in tags]

    # Validator
    def _validator_read(self):
        return {
            "ids": {"type": "list"},
            "fields": {"type": "list"},
            "load": {"type": "string"},
            "context": {"type": "dict"},
        }

    def _validator_search(self):
        return {
            "domain": {"type": "list"},
            "offset": {"coerce": int},
            "limit": {"coerce": int, "nullable": True, "default": 0},
            "order": {"type": "string"},
            "context": {"type": "dict"},
            "count": {"coerce": to_bool, "nullable": True},
        }

    def _validator_read_group(self):
        return {
            "domain": {"type": "list"},
            "offset": {"coerce": int},
            "limit": {"coerce": int, "nullable": True, "default": 0},
            "orderby": {"type": "string"},
            "groupby": {"type": "list"},
            "fields": {"type": "list"},
            "context": {"type": "dict"},
            "lazy": {"coerce": to_bool, "nullable": True},
        }

    def _validator_create(self):
        return {
            "name": {"type": "string", "required": True},
            "description": {"type": "string", "required": True},
            "origin_model": {"type": "string"},
            "origin_url": {"type": "string"},
            "origin_db": {"type": "string"},
            "origin_name": {"type": "string"},
            "action_id": {"type": "integer"},
            "project_id": {"type": "integer"},
            "tag_ids": {"type": "integer"},
            "priority": {"type": "string"},
            "author": self._partner_validator(),
            "attachment_ids": {"type": "list"},
            "functional_area": {"type": "string"},
            "assignee_customer": self._partner_validator(),
        }

    def _validator_write(self):
        return {
            "ids": {"type": "list"},
            "vals": {
                "type": "dict",
                "schema": {
                    "name": {"type": "string"},
                    "stage_name": {"type": "string"},
                    "description": {"type": "string"},
                    "project_id": {"type": "integer"},
                    "tag_ids": {"type": "integer"},
                    "priority": {"type": "string"},
                    "attachment_ids": {"type": "list"},
                    "functional_area": {"type": "string"},
                },
            },
            "author": self._partner_validator(),
            "assignee_customer": self._partner_validator(),
        }

    def _attachment_validator(self):
        return {
            "type": "dict",
            "schema": {"res_id": {"type": "integer"}, "db_datas": {"type": "string"}},
        }

    def _validator_message_format(self):
        return {"ids": {"type": "list"}}

    def _validator_get_message(self):
        return {
            "ids": {"type": "string"},
            "domain": {"type": "string"},
            "message_unload_ids": {"type": "string"},
            "thread_level": {"coerce": int, "nullable": True, "default": 0},
            "context": {"type": "string"},
            "parent_id": {"coerce": int, "nullable": True, "default": 0},
            "limit": {"coerce": int, "nullable": True, "default": 0},
        }

    def _validator_message_post(self):
        return {
            "_id": {"type": "integer"},
            "body": {"type": "string"},
            "author": self._partner_validator(),
        }

    def _partner_validator(self):
        return {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "uid": {"type": "integer"},
                "image": {"type": "string", "nullable": True},
                "email": {"type": "string"},
                "mobile": {"type": "string"},
                "phone": {"type": "string"},
            },
        }

    def _validator_read_support_author(self):
        return {"uid": {"type": "integer"}}

    def _validator_project_list(self):
        return {}

    def _validator_type_list(self):
        return {}
