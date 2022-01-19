from odoo import api, fields, models, _


class JobApplicantEducation(models.Model):
    _name = "job.applicant.education"
    _description = "Job Applicant Education"

    level_of_education = fields.Selection([
        ('psc', 'PSC/5'),
        ('jsc', 'JSC/JDC/8 pass'),
        ('secondary', 'Secondary'),
        ('higher_secondary', 'Higher Secondary'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor/Honors'),
        ('masters', 'Masters'),
        ('phd', 'PhD (Doctor of Philosophy)'),
    ], string='Level of Education')
    exam_degree_title_name = fields.Char(string="Exam/Degree Title")
    concentration_major_group_name = fields.Char(string="Concentration/Major/Group")
    board_name = fields.Char(string="Board")
    institute_name = fields.Char(string="Institute Name")

    result = fields.Selection([
        ('first_division', 'First Division/Class'),
        ('second_division', 'Second Division/Class'),
        ('third_division', 'Third Division/Class'),
        ('grade', 'Grade'),
        ('enrolled', 'Enrolled'),
        ('appeared', 'Appeared'),
        ('awarded', 'Awarded'),
    ], string='Result')
    cgpa = fields.Char(string="CGPA")
    mark = fields.Char(string="Marks")
    scale = fields.Char(string="Scale")
    passing_year = fields.Char(string="Year of Passing")
    duration = fields.Char(string="Duration (Years)")
    achievement = fields.Char(string="Achievement")
    certificate = fields.Binary("Certificate", attachment=True, store=True, help="Select Certificate here")

    job_application_education_id = fields.Many2one(comodel_name="job.applicant", string="Education Info")
    first_shortlist = fields.Many2one(comodel_name="first.shortlist", string="Shortlist Select")


class JobApplicantExperience(models.Model):
    _name = "job.applicant.experience"
    _description = "Job Applicant Experience"

    company_name = fields.Char(string="Company Name")
    position = fields.Char(string="Designation")
    department = fields.Char(string="Department")
    area_experiences = fields.Char(string="Area of Experiences")
    responsibilities = fields.Char(string="Responsibilities")
    company_location = fields.Char(string="Company Location")
    start_date = fields.Char(string="From Date")
    to_date = fields.Char(string="To Date")

    job_application_experience_id = fields.Many2one(comodel_name="job.applicant", string="Job Experience")


class JobApplicantReference(models.Model):
    _name = "job.applicant.reference"
    _description = "Job Applicant Reference"

    reference_name = fields.Char(string="Name")
    reference_organization = fields.Char(string="Organization")
    reference_position = fields.Char(string="Designation")
    reference_relation = fields.Char(string="Relation")
    reference_mobile = fields.Char(string="Mobile")
    reference_phone = fields.Char(string="Phone")
    reference_email = fields.Char(string="Email")
    reference_address = fields.Char(string="Address")
    verify_status = fields.Boolean(string="Status", default="False")

    job_application_reference_id = fields.Many2one(comodel_name="job.applicant", string="Job Reference")


class JobApplicantArticle(models.Model):
    _name = "job.applicant.article"
    _description = "Job Applicant Article"

    article_name = fields.Char(string="Publication/Research/Journal")
    article_author = fields.Char(string="Title with Author(s)")
    vol_no = fields.Char(string="Vol. Number")
    page_no = fields.Char(string="Number of Page")
    article_publication_date = fields.Char(string="Publication Year")
    publication_country = fields.Char(string="Country")
    article_file = fields.Char(string="Publication File")

    job_application_article_id = fields.Many2one(comodel_name="job.applicant", string="Job Article")


class Conference(models.Model):
    _name = "conference"
    _description = "Conference"

    proceedings_name = fields.Char(string="Proceedings Name")
    conference_author = fields.Char(string="Title with Author(s)")
    conference_page_no = fields.Char(string="Number of Page")
    conference_article_publication_date = fields.Char(string="Publication Year")
    conference_publication_country = fields.Char(string="Country")
    conference_article_file = fields.Char(string="Publication File")

    job_application_conference_id = fields.Many2one(comodel_name="job.applicant", string="Job Conference")


class Project(models.Model):
    _name = "project"
    _description = "Job Applicant Project"

    academic_program_name = fields.Char(string="Academic Program")
    title = fields.Char(string="Title")
    project_year = fields.Char(string="Year")

    job_application_project_id = fields.Many2one(comodel_name="job.applicant", string="Job Project")


class JobApplicantPublication(models.Model):
    _name = "job.applicant.publication"
    _description = "Job Applicant Publication Book"

    publication_name = fields.Char(string="Title of the Book")
    publisher = fields.Char(string="Publisher")
    year = fields.Char(string="Year")

    job_application_publication_id = fields.Many2one(comodel_name="job.applicant", string="Job Publication")


class Membership(models.Model):
    _name = "membership"
    _description = "Job Applicant Membership"

    description = fields.Char(string="Description")
    member_year = fields.Char(string="Year")

    job_application_membership_id = fields.Many2one(comodel_name="job.applicant", string="Job Membership")


class ProfessionalCertificate(models.Model):
    _name = "professional.certificate"
    _description = "Professional Certificate"

    certification = fields.Char(string="Certification/Degree")
    degree_institute_name = fields.Char(string="Institute Name")
    degree_company_location = fields.Char(string="Company Location")
    degree_start_date = fields.Char(string="From")
    degree_to_date = fields.Char(string="To")
    degree_concentration_major_name = fields.Char(string="Concentration/Major")

    certification_id = fields.Many2one(comodel_name="job.applicant", string="Certification")


class ProfessionalTraining(models.Model):
    _name = "professional.training"
    _description = "Professional Training"

    training_title = fields.Char(string="Title/Topic")
    training_institute_name = fields.Char(string="Institute Name")
    training_company_location = fields.Char(string="Company Location")
    training_start_date = fields.Char(string="From")
    training_to_date = fields.Char(string="To")
    training_concentration_major_name = fields.Char(string="Concentration/Major")

    training_id = fields.Many2one(comodel_name="job.applicant", string="Training")


class ProfessionalAward(models.Model):
    _name = "professional.award"
    _description = "Professional Award"

    award = fields.Char(string="Award/Recognition/Honor")
    award_by = fields.Char(string="Award By")
    award_year = fields.Char(string="Year")

    award_id = fields.Many2one(comodel_name="job.applicant", string="Award")


class LanguageProficiency(models.Model):
    _name = "language.proficiency"
    _description = "Language Proficiency"

    language_name = fields.Char(String="Language")
    reading = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Reading')
    writing = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Writing')
    speaking = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Speaking')
    listening = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Listening')

    language_id = fields.Many2one(comodel_name="job.applicant", string="Language Info")


class Video(models.Model):
    _name = "video"
    _description = "Video"

    code = fields.Char(string="Code", readonly=True)
    video_resumes = fields.Char(string="Video Résumé")
    demo_videos = fields.Char(string="Demo Video")
    active = fields.Boolean(string="Active", default="True")
    video_id = fields.Many2one(comodel_name="job.applicant", string="Profile")

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('video')
        res = super(Video, self).create(vals)
        return res