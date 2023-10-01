# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class RiskAnalysisType(models.Model):
    _name = "risk_analysis_type"
    _inherit = [
        "risk_analysis_type",
    ]

    reference_document_set_ids = fields.Many2many(
        string="Reference Document Sets",
        comodel_name="reference_document_set",
        relation="rel_risk_analysis_type_2_reference_document_set",
        column1="type_id",
        column2="set_id",
    )
