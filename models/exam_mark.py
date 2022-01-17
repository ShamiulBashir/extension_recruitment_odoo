from odoo import api, fields, models, _


class JobApplicantWritten(models.Model):
    _name = "job.applicant.written"
    _description = "Job Applicant Written"

    written_date = fields.Date(string="Date")
    written_time = fields.Float(string="Time")
    active = fields.Boolean(string="Active", default="True")
    name = fields.Many2one('hr.job', string="Position")
    job_applicant_written_ids = fields.Many2many("job.applicant.written.mark", string="Job Applicant Written Id")


class JobApplicantWrittenMark(models.Model):
    _name = "job.applicant.written.mark"
    _description = "Job Applicant Written Mark"

    code = fields.Char(string="Code", readonly=True)
    english = fields.Float(string="English Marks")
    computer_literacy = fields.Float(string="Computer Literacy")
    subjective = fields.Float(string="Relevant Subject for Teaching Position")
    demo_marks = fields.Float(string="Demo Marks")
    general_knowledge = fields.Float(string="General Knowledge")
    total_written_mark = fields.Float(string="Total Written Marks")
    comments = fields.Text(string="Comments")
    active = fields.Boolean(string="Active", default="True")
    job_id = fields.Many2one('hr.job', string="Position")
    state_id = fields.Selection([
        ('not published', 'Not Published'),
        ('selected', 'Selected'),
        ('reject', 'Rejected'),
    ], string='Status', default='not published')

    name = fields.Many2one(comodel_name="hr.applicant", string="Applicant Name")
    written_mark = fields.Many2one(comodel_name="job.applicant.written.mark.entry", string="Written Mark")
    written_mark_id = fields.Many2one(comodel_name="written.admit.card", string="Written Mark")

    _sql_constraints = [
        ('id', 'unique(id)', 'Written already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.job_id = rec.name.job_id

    @api.onchange('english', 'computer_literacy', 'subjective', 'demo_marks', 'general_knowledge')
    def total_calculate_onchange(self):
        for rec in self:
            rec.total_written_mark = rec.english + rec.computer_literacy + rec.subjective + rec.demo_marks + rec.general_knowledge

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('job.applicant.written.mark')
        res = super(JobApplicantWrittenMark, self).create(vals)
        return res


class JobApplicantWrittenMarkEntry(models.Model):
    _name = "job.applicant.written.mark.entry"
    _description = "Job Applicant Written Mark Entry"

    name = fields.Many2one('written.admit.card', string="Job Position")
    active = fields.Boolean(string="Active", default="True")
    department_id = fields.Many2one('hr.department', string="Department")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="written_entry_mark", string="Applicant")
    applicant_exam_mark = fields.One2many(comodel_name="job.applicant.written.mark", inverse_name="written_mark", string="Applicant Mark")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="written_entry_mark", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    code = fields.Char(string="Code", readonly=True)

    _sql_constraints = [
        ('id', 'unique(id)', 'Written already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.onchange('name')
    def onchange_name(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.applicant
                rec.department_id = rec.name.department_id

    @api.onchange('applicant')
    def onchange_applicant(self):
        for rec in self:
            if rec.applicant:
                rec.applicant_exam_mark = rec.name.applicant.job_applicant_written_mark
                # rec.applicant_exam_mark.name.job_id = rec.name
                # rec.applicant_exam_mark = rec.name.applicant

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('job.applicant.written.mark.entry')
        res = super(JobApplicantWrittenMarkEntry, self).create(vals)
        return res


class JobApplicantDemoMark(models.Model):
    _name = "job.applicant.demo.mark"
    _description = "Job Applicant Demo Mark"

    code = fields.Char(string="Code", readonly=True)
    english = fields.Float(string="English Marks")
    computer_literacy = fields.Float(string="Computer Literacy")
    subjective = fields.Float(string="Relevant Subject for Teaching Position")
    demo_marks = fields.Float(string="Demo Marks")
    general_knowledge = fields.Float(string="General Knowledge")
    total_demo_mark = fields.Float(string="Total Demo Marks")
    comments = fields.Text(string="Comments")
    active = fields.Boolean(string="Active", default="True")
    job_id = fields.Many2one('hr.job', string="Position")
    state_id = fields.Selection([
        ('not published', 'Not Published'),
        ('selected', 'Selected'),
        ('reject', 'Rejected'),
    ], string='Status', default='not published')

    name = fields.Many2one(comodel_name="hr.applicant", string="Applicant Name")

    _sql_constraints = [
        ('id', 'unique(id)', 'Demo already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.job_id = rec.name.job_id

    @api.onchange('english', 'computer_literacy', 'subjective', 'demo_marks', 'general_knowledge')
    def total_calculate_onchange(self):
        for rec in self:
            rec.total_demo_mark = rec.english + rec.computer_literacy + rec.subjective + rec.demo_marks + rec.general_knowledge

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('job.applicant.demo.mark')
        res = super(JobApplicantDemoMark, self).create(vals)
        return res


class JobApplicantVivaMark(models.Model):
    _name = "job.applicant.viva.mark"
    _description = "Job Applicant Viva Mark"

    code = fields.Char(string="Code", readonly=True)
    english = fields.Float(string="English Marks")
    computer_literacy = fields.Float(string="Computer Literacy")
    subjective = fields.Float(string="Relevant Subject for Teaching Position")
    demo_marks = fields.Float(string="Demo Marks")
    general_knowledge = fields.Float(string="General Knowledge")
    total_viva_mark = fields.Float(string="Total Viva Marks")
    job_id = fields.Many2one('hr.job', string="Position")
    comments = fields.Text(string="Comments")
    active = fields.Boolean(string="Active", default="True")
    state_id = fields.Selection([
        ('not published', 'Not Published'),
        ('selected', 'Selected'),
        ('reject', 'Rejected'),
    ], string='Status', default='not published')

    name = fields.Many2one(comodel_name="hr.applicant", string="Applicant Name")

    _sql_constraints = [
        ('id', 'unique(id)', 'Viva already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.onchange('english', 'computer_literacy', 'subjective', 'demo_marks', 'general_knowledge')
    def total_calculate_onchange(self):
        for rec in self:
            rec.total_viva_mark = rec.english + rec.computer_literacy + rec.subjective + rec.demo_marks + rec.general_knowledge

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.job_id = rec.name.job_id

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('job.applicant.viva.mark')
        res = super(JobApplicantVivaMark, self).create(vals)
        return res


class RoadMap(models.Model):
    _name = "road.map"
    _description = "Road Map"

    code = fields.Char(string="Code", readonly=True)
    total_road_map_mark = fields.Float(string="Total Road Map Marks")
    job_id = fields.Many2one('hr.job', string="Position")
    comments = fields.Text(string="Comments")
    road_map_date = fields.Date(string="Date")
    road_map_time = fields.Float(string="Time")
    active = fields.Boolean(string="Active", default="True")
    state_id = fields.Selection([
        ('draft', 'Draft'),
        ('accept', 'Accepted'),
        ('selected', 'Selected'),
        ('reject', 'Rejected'),
    ], string='Status', default='draft')

    name = fields.Many2one(comodel_name="hr.applicant", string="Applicant Name")

    _sql_constraints = [
        ('id', 'unique(id)', 'Viva already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.job_id = rec.name.job_id

    # @api.onchange('english', 'computer_literacy', 'subjective', 'demo_marks', 'general_knowledge')
    # def total_calculate_onchange(self):
    #     for rec in self:
    #         rec.total_viva_mark = rec.english + rec.computer_literacy + rec.subjective + rec.demo_marks + rec.general_knowledge

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('road.map')
        res = super(RoadMap, self).create(vals)
        return res
