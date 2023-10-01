# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class RiskAnalysis(models.Model):
    _name = "risk_analysis"
    _inherit = [
        "risk_analysis",
        "mixin.reference_document",
    ]
    _reference_document_create_page = True

    reference_document_set_ids = fields.Many2many(
        relation="rel_risk_analysis_2_reference_document_set",
        column1="risk_analysis_id",
        column2="set_id",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_reference_document_set_ids(self):
        self.reference_document_set_ids = False

        if self.type_id:
            self.reference_document_set_ids = self.type_id.reference_document_set_ids
