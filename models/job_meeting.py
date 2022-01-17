from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta, date
from ast import literal_eval
import base64


class ActionOneMany(models.Model):
    _inherit = "action.one.many"

    job_id = fields.Many2one('hr.job', 'Job Applicant Interview')

    # @api.onchange('job_id')
    # def onchange_applicant(self):
    #     for rec in self:
    #         if rec.job_id:
    #             rec.agenda_many_id.partner_ids.id = rec.job_id.application_ids.id
