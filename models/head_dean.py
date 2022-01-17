from odoo import api, fields, models, _


class HrHead(models.Model):
    _name = 'hr.head'

    name = fields.Many2one('hr.job', string="Job Position")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="head_approve", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="head_approve", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string="Department")
    active = fields.Boolean(string="Active", default="True")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.application_ids
                rec.department_id = rec.name.department_id


class HrDean(models.Model):
    _name = 'hr.dean'

    name = fields.Many2one('hr.job', string="Job Position")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="dean_approve", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string="Department")
    active = fields.Boolean(string="Active", default="True")


