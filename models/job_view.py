# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

import logging

_logger = logging.getLogger(__name__)


class Job(models.Model):
    _inherit = "hr.job"
    _description = "Hr Job"

    job_category = fields.Many2one('diu.job.category', string="Job Type")
    post_type = fields.Many2one('post.category', string="Post Type")
    subject = fields.Char(string="Subject")
    payment_allow = fields.Boolean(string="Payment", default="True")
    amount = fields.Float(string="Payment fee")
    amount_name = fields.Char(string="Name")
    start_date = fields.Date(string="Publishing Date")
    end_date = fields.Date(string="Deadline")
    required_reference = fields.Integer(string="Required References")
    experience = fields.Text(string="Experience")
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'), ('Any', 'Any')], string="Gender")
    education_requirements = fields.Text(string="Educational Requirements")
    additional_requirements = fields.Text(string="Additional Requirements")
    position_responsibilities = fields.Text(string="Position Responsibilities")
    other_benefits = fields.Text(string="Other Benefits")
    salary_range = fields.Char(string="Salary Range", help="If don't mention, will show Negotiable")
    age_range = fields.Char(string="Age Range", help="If don't mention, skip")
    product_line_id = fields.Many2one("product.product", string="Product")
    hr_applicant_exam = fields.Many2many(comodel_name="hr.applicant", string="Applicant Name")
    meeting_job_count = fields.Integer(compute='_job_meeting_count', string="Job Count")
    written_date = fields.Date(string="Written Date")
    written_time = fields.Float(string="Written Time")
    demo_date = fields.Date(string="Demo Date")
    demo_time = fields.Float(string="Demo Time")
    viva_date = fields.Date(string="Viva Date")
    viva_time = fields.Float(string="Viva Time")
    road_map_date = fields.Date(string="Road Map Date")
    road_map_time = fields.Float(string="Road Map Time")
    active = fields.Boolean(string="Active", default="True")
    hr_applicant_ids = fields.One2many(comodel_name="hr.applicant", inverse_name="job_id",
                                       string="Job Application Profile")
    draft_application_count = fields.Integer(compute='_compute_application_count_draft',
                                             string="Draft Application Count")
    bkash_application_count = fields.Integer(compute='_compute_application_count_bkash',
                                             string="bKash Application Count")
    applied_application_count = fields.Integer(compute='_compute_application_count_applied',
                                               string="Applied Application Count")
    recommendation_application_count = fields.Integer(compute='_compute_application_count_recommendation',
                                                      string="Recommendation Application Count")
    shortlist_application_count = fields.Integer(compute='_compute_application_count_shortlist',
                                                 string="Shortlist Application Count")

    def _compute_application_count_bkash(self):
        for s_id in self:
            read_group_result = self.env['hr.applicant'].search([('job_id', '=', s_id.id), ('hr_application_state', '=', 'pay')])
            s_id.bkash_application_count = len(read_group_result)

    def _compute_application_count_draft(self):
        for s_id in self:
            read_group_result = self.env['hr.applicant'].search([('job_id', '=', s_id.id), ('hr_application_state', '=', 'draft')])
            s_id.draft_application_count = len(read_group_result)

    def _compute_application_count_applied(self):
        for s_id in self:
            read_group_result = self.env['hr.applicant'].search(
                [('job_id', '=', s_id.id), ('hr_application_state', '=', 'applied')])
            s_id.applied_application_count = len(read_group_result)

    def _compute_application_count_recommendation(self):
        for s_id in self:
            read_group_result = self.env['hr.applicant'].search(
                [('job_id', '=', s_id.id), ('hr_application_state', '=', 'recommendation')])
            s_id.recommendation_application_count = len(read_group_result)

    def _compute_application_count_shortlist(self):
        for s_id in self:
            read_group_result = self.env['hr.applicant'].search(
                [('job_id', '=', s_id.id), ('hr_application_state', '=', 'shortlist')])
            s_id.shortlist_application_count = len(read_group_result)

    def _job_meeting_count(self):
        for s_id in self:
            support_ids = self.env['calendar.event'].search([("meeting_timesheet_ids.job_id", '=', self.id)])
            s_id.meeting_job_count = len(support_ids)
        return

    def job_meeting_button(self):
        self.ensure_one()
        return {
            'name': 'Meeting',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'domain': [("meeting_timesheet_ids.job_id", '=', self.id)],
        }

    def hr_state_button(self):
        self.ensure_one()
        return {
            'name': 'HR',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.applicant',
            'domain': ([('job_id', '=', self.id), ('hr_application_state', '=', 'pay')]),
        }

    @api.onchange('product_line_id')
    def onchange_amount(self):
        for rec in self:
            if rec.product_line_id:
                rec.amount = rec.product_line_id.lst_price
                rec.amount_name = rec.product_line_id.name

    @api.model
    def action_send_card(self):
        print(self.id)
        print(self.env.ref('extension_recruitment.job_position_email_template').id)
        template_id = self.env.ref('extension_recruitment.job_position_email_template').id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        print(template)
        template.send_mail(self.id, force_send=True)


class DiuJobCategory(models.Model):
    _name = "diu.job.category"
    _description = "DIU Job Category"

    name = fields.Char(string="Name", required=True)
    notes = fields.Char(string="Note")
    active = fields.Boolean(string="Active", default="True")


class PostCategory(models.Model):
    _name = "post.category"
    _description = "Post Category"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default="True")


class AdmitCard(models.Model):
    _name = "admit.card"
    _description = "Admit Card"

    active = fields.Boolean(string="Active", default="True")
    hr_applicant = fields.Many2many('hr.applicant', string="Applicant Id")
    job_applicant = fields.Many2one('job.applicant', string="Applicant")
    name = fields.Many2one('hr.job', string="Position")
    written = fields.Many2one('job.applicant.written.mark', string="Writen")
    demo = fields.Many2one('job.applicant.demo.mark', string="Demo")
    viva = fields.Many2one('job.applicant.viva.mark', string="Viva")
    road_map = fields.Many2one('job.applicant.road.mark', string="Road Map")
    exam_date = fields.Datetime(string="Exam Date/Time")
    exam_venue = fields.Many2one('venue', string="Venue/Center")

    @api.onchange('name')
    def onchange_applicant_id(self):
        for rec in self:
            if rec.name:
                rec.hr_applicant = rec.name.application_ids


class WrittenAdmitCard(models.Model):
    _name = "written.admit.card"
    _description = "Written Admit Card"

    def _default_company_id(self):
        company_id = False
        if self._context.get('default_department_id'):
            department = self.env['hr.department'].browse(self._context['default_department_id'])
            company_id = department.company_id.id
        if not company_id:
            company_id = self.env.company
        return company_id

    active = fields.Boolean(string="Active", default="True")
    company_id = fields.Many2one('res.company', "Company", default=_default_company_id)
    written_exam_date = fields.Date(string="Exam Date")
    written_exam_time = fields.Float(string="Exam Time")
    exam_venue = fields.Many2one('venue', string="Venue/Center")
    name = fields.Many2one('hr.job', string="Job Position")
    department_id = fields.Many2one('hr.department', string="Department")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="written_admit_card", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="written_admit_card", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    code = fields.Char(string="Code")
    message_body = fields.Text(string="Message Body")
    applicant_exam_mark = fields.One2many(comodel_name="job.applicant.written.mark", inverse_name="written_mark_id",
                                          string="Applicant Mark")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                application_id = self.env['hr.applicant'].search([('job_id', '=', rec.name.id), ('hr_application_state', '=', 'shortlist')])
                rec.applicant = application_id
                rec.written = application_id
                rec.department_id = rec.name.department_id
                rec.applicant.admit_card_status = False

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):

        # hr_rec_exam_written = self.env['job.applicant.written.mark'].sudo().create({
        #     'name': self.applicant,
        #     'job_id': self.name.id,
        # })
        # print(hr_rec_exam_written)
        # hr_rec_exam_demo = self.env['job.applicant.demo.mark'].sudo().create({
        #     'name': self.applicant,
        #     'job_id': self.name.id,
        # })
        # print(hr_rec_exam_demo)
        # hr_rec_exam_viva = self.env['job.applicant.viva.mark'].sudo().create({
        #     'name': self.applicant,
        #     'job_id': self.name.id,
        # })
        # print(hr_rec_exam_viva)

        vals['code'] = self.env['ir.sequence'].next_by_code('written.admit.card')
        res = super(WrittenAdmitCard, self).create(vals)
        return res


class DemoAdmitCard(models.Model):
    _name = "demo.admit.card"
    _description = "demo Admit Card"

    active = fields.Boolean(string="Active", default="True")
    demo_exam_date = fields.Datetime(string="Exam Date/Time")
    exam_venue = fields.Many2one('venue', string="Venue/Center")
    name = fields.Many2one('final.shortlist', string="Job Position")
    department_id = fields.Many2one('hr.department', string="Department")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="written_admit_card", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="written_admit_card", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    code = fields.Char(string="Code")
    message_body = fields.Text(string="Message Body")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.applicant
                rec.written = rec.name.applicant
                rec.department_id = rec.name.department_id

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('demo.admit.card')
        res = super(DemoAdmitCard, self).create(vals)
        return res


class VivaAdmitCard(models.Model):
    _name = "viva.admit.card"
    _description = "Viva Admit Card"

    active = fields.Boolean(string="Active", default="True")
    viva_exam_date = fields.Datetime(string="Exam Date/Time")
    exam_venue = fields.Many2one('venue', string="Venue/Center")
    name = fields.Many2one('final.shortlist', string="Job Position")
    department_id = fields.Many2one('hr.department', string="Department")
    applicant = fields.One2many(comodel_name="hr.applicant", inverse_name="written_admit_card", string="Applicant")
    applicant_id = fields.One2many(comodel_name="job.applicant", inverse_name="written_admit_card", string="Applicant")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    code = fields.Char(string="Code")
    message_body = fields.Text(string="Message Body")

    @api.onchange('name')
    def onchange_applicant(self):
        for rec in self:
            if rec.name:
                rec.applicant = rec.name.applicant
                rec.written = rec.name.applicant
                rec.department_id = rec.name.department_id

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!')]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('viva.admit.card')
        res = super(VivaAdmitCard, self).create(vals)
        return res


class Venue(models.Model):
    _name = "venue"
    _description = "Exam Venue"

    code = fields.Char(string="Code", readonly=True)
    name = fields.Char(string="Name", required=True)
    address = fields.Char(string="Address")
    active = fields.Boolean(string="Active", default="True")

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('venue')
        res = super(Venue, self).create(vals)
        return res
