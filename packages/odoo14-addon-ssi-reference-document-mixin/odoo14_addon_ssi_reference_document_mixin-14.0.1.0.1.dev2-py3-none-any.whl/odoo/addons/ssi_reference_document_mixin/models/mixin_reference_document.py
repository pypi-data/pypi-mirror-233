# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models


class MixinReferenceDocument(models.AbstractModel):
    _name = "mixin.reference_document"
    _description = "Reference Document Mixin"
    _reference_document_create_page = False
    _reference_document_page_xpath = "//page[last()]"
    _configurator_field_name = "type_id"
    _reference_document_set_field_name = "reference_document_set_ids"

    reference_document_set_ids = fields.Many2many(
        string="Reference Document Sets",
        comodel_name="reference_document_set",
    )
    reference_document_ids = fields.Many2many(
        string="Reference Document",
        comodel_name="reference_document",
        compute="_compute_reference_document_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "reference_document_set_ids",
    )
    def _compute_reference_document_ids(self):
        for record in self.sudo():
            result = self.env["reference_document"]
            for document_set in record.reference_document_set_ids:
                result += document_set.reference_document_ids
            record.reference_document_ids = result

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._reference_document_create_page:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._reference_document_page_xpath)
            if node_xpath:
                str_element = self.env["ir.qweb"]._render(
                    "ssi_reference_document_mixin.reference_document"
                )
                for node in node_xpath:
                    new_node = etree.fromstring(str_element)
                    node.addnext(new_node)

            View = self.env["ir.ui.view"]

            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res
