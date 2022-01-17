# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class Portal(models.Model):
    _inherit = "res.partner"
    _description = "Partners"

    is_job_applicant = fields.Boolean(string="Is Job Applicant", default=False)
