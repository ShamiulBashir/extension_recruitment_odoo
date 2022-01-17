from datetime import time, date

from addons.website.tools import get_video_embed_code
from odoo import api, fields, models, tools, _, SUPERUSER_ID, http

import logging

from odoo.exceptions import UserError, ValidationError
from odoo.tools import datetime, DEFAULT_SERVER_DATETIME_FORMAT

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Good'),
    ('2', 'Very Good'),
    ('3', 'Excellent')
]

_logger = logging.getLogger(__name__)


class JobApplicant(models.Model):
    _name = "job.applicant"
    _description = "Job Applicant Info"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']

    tracking_id = fields.Char(string="Tracking No", readonly=True)
    head_approve = fields.Many2one('hr.head', string="Head Approve")
    partner_id = fields.Many2one('res.partner', "Contact", copy=False)
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    employee_id = fields.Char(string="Roll")
    active = fields.Boolean(string="Active", default="True")
    is_job = fields.Boolean('Is Already Job Applicant')
    partner_name = fields.Char(string="Name")
    transaction_no = fields.Char(string="Transaction No")
    email_from = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone")
    password = fields.Char(string="Password")
    confirm_password = fields.Char(string="Confirm Password")
    partner_mobile = fields.Char(string="Mobile")
    father = fields.Char(string="Father Name")
    mother = fields.Char(string="Mother Name")
    birthday = fields.Date(string="Birthday")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    image_id = fields.Binary("Image", attachment=True, store=True, help="Select image here")
    video_resume = fields.Binary("Video Résumé", attachment=True, store=True, help="Select video here")
    demo_video = fields.Binary("Demo Video", attachment=True, store=True, help="Select video here")
    video_resumes = fields.Char(string="Video Résumé")
    demo_videos = fields.Char(string="Demo Video")
    resume_embed_code = fields.Char(compute="_compute_embed_code")
    demo_embed_code = fields.Char(compute="_compute_embed_code")

    Resume = fields.Binary("Resume", attachment=True, store=True, help="Select resume here")
    applicant_signature = fields.Binary("Applicant Signature", attachment=True, store=True,
                                        help="Select Applicant Signature here")
    job_marriage_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('single_mother', 'Single Mother'),
        ('widowed', 'Widowed'),
        ('engaged', 'Engaged'),
        ('single_father', 'Single Father')], string="Marital Status")
    job_religion = fields.Selection([
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('christianity', 'Christianity'),
        ('sikhism', 'Sikhism')], string="Religion")
    blood_group = fields.Selection([
        ('a+', 'A+ve'),
        ('ab+', 'AB+ve'),
        ('b+', 'B+ve'),
        ('o+', 'O+ve'),
        ('a-', 'A-ve'),
        ('ab-', 'AB-ve'),
        ('b-', 'B-ve'),
        ('o-', 'O-ve')], string="Blood Group")
    national_id = fields.Char(string="National Id")
    description = fields.Text("Description")
    passport_no = fields.Char(string="Passport No")
    nationality = fields.Char(string="Nationality")
    f_phone = fields.Char(string="Father Mobile")
    m_mobile = fields.Char(string="Mother Mobile")
    present_address = fields.Text(string="Present Address")
    permanent_address = fields.Text(string="Permanent Address")
    linkedin_link = fields.Char(string="LinkedInLink")
    facebook_link = fields.Char(string="Facebook Link")
    google_site_link = fields.Char(string="Github Link")
    youtube_link = fields.Char(string="Youtube Link")
    twitter_link = fields.Char(string="Twitter Link")
    instagram_link = fields.Char(string="Instagram Link")
    website_link = fields.Char(string="Website Link")
    description = fields.Char(string="Website Link")
    transaction_date = fields.Date(string="Website Link")
    computer_skill = fields.Text(string="Computer and Other Skills")
    extra_curricula = fields.Char(string="Extra Curricular")
    salary_expected = fields.Float("Expected Salary", group_operator="avg", help="Salary Expected by Applicant")
    job_id = fields.Many2one('hr.job', string="Position")
    department_id = fields.Many2one('hr.department', string="Department")
    emp_id = fields.Many2one('hr.employee', string="Employee", help="Employee linked to the applicant.", copy=False)
    state_id = fields.Selection([
        ('draft', 'Draft'),
        ('accept', 'Accepted'),
        ('reject', 'Rejected'),
    ], string='Status', default='draft')
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'job.applicant')],
                                     string='Attachments')
    name = fields.Char(string="Applicant Name")
    color = fields.Integer("Color Index", default=0)
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        copy=False, default='normal', required=True)
    age = fields.Float(string='Age')
    legend_blocked = fields.Char(string='Kanban Blocked', readonly=False)
    legend_done = fields.Char(string='Kanban Valid', readonly=False)
    legend_normal = fields.Char(string='Kanban Ongoing', readonly=False)
    experience = fields.Char(string="Experience")
    video_info = fields.One2many(comodel_name="video", inverse_name="video_id", string="Job Applicant Video")
    job_applicant_education_info = fields.One2many(comodel_name="job.applicant.education",
                                                   inverse_name="job_application_education_id",
                                                   string="Job Applicant Education")
    job_applicant_experience_info = fields.One2many(comodel_name="job.applicant.experience",
                                                    inverse_name="job_application_experience_id",
                                                    string="Job Applicant Experience")
    job_applicant_reference_info = fields.One2many(comodel_name="job.applicant.reference",
                                                   inverse_name="job_application_reference_id",
                                                   string="Job Applicant Reference")
    job_applicant_article_info = fields.One2many(comodel_name="job.applicant.article",
                                                 inverse_name="job_application_article_id",
                                                 string="Job Applicant Article")
    job_applicant_publication_info = fields.One2many(comodel_name="job.applicant.publication",
                                                     inverse_name="job_application_publication_id",
                                                     string="Job Applicant Publication Book")
    job_applicant_conference_info = fields.One2many(comodel_name="conference",
                                                    inverse_name="job_application_conference_id",
                                                    string="Job Applicant Conference")
    job_applicant_project_info = fields.One2many(comodel_name="project", inverse_name="job_application_project_id",
                                                 string="Job Applicant Project")
    job_applicant_membership_info = fields.One2many(comodel_name="membership",
                                                    inverse_name="job_application_membership_id",
                                                    string="Job Applicant Membership")
    job_applicant_ids = fields.One2many(comodel_name="hr.applicant", inverse_name="job_applicant_id",
                                        string="Job Applicant Profile")
    job_certification_id = fields.One2many(comodel_name="professional.certificate", inverse_name="certification_id",
                                           string="Certification info")
    job_training_id = fields.One2many(comodel_name="professional.training", inverse_name="training_id",
                                      string="Training info")
    job_award_id = fields.One2many(comodel_name="professional.award", inverse_name="award_id", string="Award info")
    first_shortlist = fields.Many2one('first.shortlist', string="First Shortlist")
    second_shortlist = fields.Many2one('second.shortlist', string="Second Shortlist")
    final_shortlist = fields.Many2one('final.shortlist', string="Final Shortlist")
    written_admit_card = fields.Many2one('written.admit.card', string="Written Admit Card")
    written_entry_mark = fields.Many2one('job.applicant.written.mark.entry', string="Witten Mark entry")
    job_language_id = fields.One2many(comodel_name="language.proficiency", inverse_name="language_id",
                                      string="Language info")

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('tracking_id_unique', 'unique(tracking_id)', 'Code already exists!'),
    ]

    @api.depends('video_resumes', 'demo_videos')
    def _compute_embed_code(self):
        for rec in self:
            rec.resume_embed_code = get_video_embed_code(rec.video_resumes)
            rec.demo_embed_code = get_video_embed_code(rec.demo_videos)

    def calculate_age_birth(self, birthday):
        today = date.today()
        if birthday > today:
            return 0
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    @api.onchange('birthday')
    def _onchange_birthday(self):
        for row in self:
            if row.birthday:
                row.age = self.calculate_age_birth(row.birthday)

    def archive_applicant(self):
        self.write({'active': False})

    def reset_applicant(self):
        """ Reinsert the applicant into the recruitment pipe in the first stage"""
        self.write({'active': True})

    @api.model
    def create(self, vals):
        vals['tracking_id'] = self.env['ir.sequence'].next_by_code('job.applicant')
        res = super(JobApplicant, self).create(vals)
        return res

    def action_video_resumes_wizard(self):
        video_resumes = self.video_resumes

        view = self.env.ref('extension_recruitment.video_resume_wizard_form_view')





