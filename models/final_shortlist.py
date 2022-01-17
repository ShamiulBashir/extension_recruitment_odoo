from odoo import api, fields, models, _


class ShortlistStage(models.Model):
    _name = "shortlist.stage"
    _description = "Shortlist Stages"
    _order = 'sequence'

    name = fields.Char("Stage Name", required=True, translate=True)
    sequence = fields.Integer(
        "Sequence", default=10,
        help="Gives the sequence order when displaying a list of stages.")
    job_ids = fields.Many2many(
        'hr.job', string='Job Specific',
        help='Specific jobs that uses this stage. Other jobs will not use this stage.')
    shortlist_requirements = fields.Text("Shortlist Requirements")
    template_id = fields.Many2one(
        'mail.template', "Email Template",
        help="If set, a message is posted on the applicant using the template when the applicant is set to the stage.")
    fold = fields.Boolean(
        "Folded in Kanban",
        help="This stage is folded in the kanban view when there are no records in that stage to display.")
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda self: _('Blocked'), translate=True, required=True)
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda self: _('Ready for Next Stage'), translate=True, required=True)
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda self: _('In Progress'), translate=True, required=True)

    @api.model
    def default_get(self, fields):
        if self._context and self._context.get('default_job_id') and not self._context.get('shortlist_stage_mono', False):
            context = dict(self._context)
            context.pop('default_job_id')
            self = self.with_context(context)
        return super(ShortlistStage, self).default_get(fields)


class FirstShortlist(models.Model):
    _name = "first.shortlist"
    _description = "First Shortlist"

    name = fields.Many2one('hr.job', string="Job Position")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="first_shortlist", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="first_shortlist", string="Applicant")
    applicant_education = fields.One2many(comodel_name="job.applicant.education", inverse_name="first_shortlist", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string="Department")
    active = fields.Boolean(string="Active", default="True")
    code = fields.Char(string="Code")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.application_ids
                rec.department_id = rec.name.department_id


    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('first.shortlist')
        res = super(FirstShortlist, self).create(vals)
        return res


class SecondShortlist(models.Model):
    _name = "second.shortlist"
    _description = "Second Shortlist"

    name = fields.Many2one('first.shortlist', string="Job Position")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="second_shortlist", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="second_shortlist", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string="Department")
    active = fields.Boolean(string="Active", default="True")
    code = fields.Char(string="Code")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.applicant
                rec.department_id = rec.name.department_id

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('second.shortlist')
        res = super(SecondShortlist, self).create(vals)
        return res


class FinalShortlist(models.Model):
    _name = "final.shortlist"
    _description = "Final Shortlist"

    name = fields.Many2one('second.shortlist', string="Job Position")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="final_shortlist", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="final_shortlist", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string="Department")
    active = fields.Boolean(string="Active", default="True")
    code = fields.Char(string="Code")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.applicant
                rec.department_id = rec.name.department_id

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('final.shortlist')
        res = super(FinalShortlist, self).create(vals)
        return res

