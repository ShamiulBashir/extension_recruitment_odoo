from addons.website.tools import get_video_embed_code
from odoo import api, fields, models, _
from odoo.tools import datetime


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    def _default_shortlist_stage_id(self):
        if self._context.get('default_job_id'):
            return self.env['shortlist.stage'].search([
                '|',
                ('job_ids', '=', False),
                ('job_ids', '=', self._context['default_job_id']),
                ('fold', '=', False)
            ], order='sequence asc', limit=1).id
        return False

    exam_date = fields.Datetime(string="Exam Date/Time")
    admit_card_status = fields.Boolean(
        string="Admit Card Status", default=False)
    exam_venue = fields.Many2one('venue', string="Venue/Center")
    invoice_payment_status = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Invoice Status', store=True, readonly=True, copy=False, tracking=True,
        related='account_move_id.invoice_payment_state')
    hr_application_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pay', 'bKash Pay'),
        ('applied', 'Applied Job'),
        ('recommendation', 'Recommended'),
        ('shortlist', 'Shortlisted')],
        string='Application Status', default='pay')
    hr_application_stage = fields.Many2one('shortlist.stage', 'Shortlist Stage', ondelete='restrict', tracking=True,
                                           domain="['|', ('job_ids', '=', False), ('job_ids', '=', job_id)]",
                                           copy=False, index=True,
                                           group_expand='_read_group_stage_ids',
                                           default=_default_shortlist_stage_id)
    last_hr_application_stage = fields.Many2one('shortlist.stage', "Last Stage",
                                                help="Stage of the applicant before being in the current stage. Used for lost cases analysis.")
    account_move_id = fields.Many2one('account.move', string="Invoice")
    head_approve = fields.Many2one('hr.head', string="Head Approve")
    first_shortlist = fields.Many2one(
        'first.shortlist', string="First Shortlist")
    second_shortlist = fields.Many2one(
        'second.shortlist', string="Second Shortlist")
    final_shortlist = fields.Many2one(
        'final.shortlist', string="final Shortlist")
    written_entry_mark = fields.Many2one(
        'job.applicant.written.mark.entry', string="Witten Mark entry")
    written_admit_card = fields.Many2one(
        'written.admit.card', string="Written Admit Card")
    dean_approve = fields.Many2one('hr.dean', string="Dean Approve")
    message = fields.Char(string="Message")
    job_applicant_written_mark = fields.One2many(comodel_name="job.applicant.written.mark",
                                                 inverse_name="name",
                                                 string="Job Applicant Written Mark")
    job_applicant_demo_mark = fields.One2many(comodel_name="job.applicant.demo.mark",
                                              inverse_name="name", string="Job Applicant Demo Mark")
    job_applicant_viva_mark = fields.One2many(comodel_name="job.applicant.viva.mark",
                                              inverse_name="name", string="Job Applicant Viva Mark")
    job_applicant_id = fields.Many2one(
        'job.applicant', string="Applicant Profile")
    image = fields.Binary(
        related='job_applicant_id.image_id', string="Applicant Image")
    video_resume = fields.Char(
        related='job_applicant_id.video_resumes', string="Video Resume")
    demo_video = fields.Char(
        related='job_applicant_id.demo_videos', string="Demo Video")
    birthday = fields.Date(
        related='job_applicant_id.birthday', string="Birthday")
    father_name = fields.Char(
        related='job_applicant_id.father', string="Father Name")
    resume_embed_code = fields.Char(compute="_compute_embed_code")
    demo_embed_code = fields.Char(compute="_compute_embed_code")
    applicant_education = fields.One2many(
        related='job_applicant_id.job_applicant_education_info', string="Applicant Education")
    resume = fields.Binary(related='job_applicant_id.Resume', string="Resume")
    applicant_state_id = fields.Selection([
        ('draft', 'Draft'),
        ('accept', 'Accepted'),
        ('reject', 'Rejected'),
    ], string='Status', default='draft')
    exam_roll = fields.Char(string="Roll", readonly=True)

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('exam_roll_unique', 'unique(exam_roll)', 'Roll already exists!'),
    ]

    @api.depends('video_resume', 'demo_video')
    def _compute_embed_code(self):
        for rec in self:
            rec.resume_embed_code = get_video_embed_code(rec.video_resume)
            rec.demo_embed_code = get_video_embed_code(rec.demo_video)

    def _onchange_job_id_internal(self, job_id):
        department_id = False
        company_id = False
        user_id = False
        company_id = False
        stage_id = self.stage_id.id or self._context.get('default_stage_id')
        if job_id:
            job = self.env['hr.job'].browse(job_id)
            if not stage_id:
                stage_ids = self.env['hr.recruitment.stage'].search([
                    '|',
                    ('job_ids', '=', False),
                    ('job_ids', '=', job.id),
                    ('fold', '=', False)
                ], order='sequence asc', limit=1).ids
                stage_id = stage_ids[0] if stage_ids else False

        return {'value': {
            'department_id': department_id,
            'company_id': company_id,
            'user_id': user_id,
            'stage_id': stage_id
        }}

    def website_form_input_filter(self, request, values):
        if 'partner_name' in values:
            values.setdefault('name', values['partner_name'])
            return values

    def website_form_input(self, values):
        if 'partner_phone' in values:
            values.setdefault('partner_mobile', values['partner_phone'])
            return values

    @api.onchange('payorder_rec')
    def onchange_payorder_rec(self):
        for rec in self:
            if rec.payorder_rec:
                rec.transaction_status = rec.payorder_rec.transaction_status

    @api.onchange('job_id')
    def onchange_job_id_stage(self):
        vals = self._onchange_job_id_internal_stage(self.job_id.id)
        self.hr_application_stage = vals['value']['hr_application_stage']

    def _onchange_job_id_internal_stage(self, job_id):

        hr_application_stage = self.hr_application_stage.id or self._context.get(
            '_default_shortlist_stage_id')
        if job_id:
            job_id_hr = self.env['hr.job'].browse(job_id)
            if not hr_application_stage:
                hr_application_stages = self.env['shortlist.stage'].search([
                    '|',
                    ('job_ids', '=', False),
                    ('job_ids', '=', job_id_hr.id),
                    ('fold', '=', False)
                ], order='sequence asc', limit=1).ids
                hr_application_stage = hr_application_stages[0] if hr_application_stages else False

        return {'value': {
            'hr_application_stage': hr_application_stage
        }}

    @api.model
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s_%s_%s' % (self.exam_roll, self.job_id.name, self.partner_name)

    def create(self, vals):

        if vals.get('department_id') and not self._context.get('default_department_id'):
            self = self.with_context(
                default_department_id=vals.get('department_id'))
        if vals.get('user_id'):
            vals['date_open'] = fields.Datetime.now()
        if vals.get('email_from'):
            vals['email_from'] = vals['email_from'].strip()
        if vals.get('job_id') or self._context.get('default_job_id'):
            job_id = vals.get('job_id') or self._context.get('default_job_id')
            for key, value in self._onchange_job_id_internal_stage(job_id)['value'].items():
                if key not in vals:
                    vals[key] = value
        if 'hr_application_stage' in vals:
            vals.update(self._onchange_job_id_internal_stage(
                vals.get('hr_application_stage'))['value'])
        vals['exam_roll'] = self.env['ir.sequence'].next_by_code(
            'hr.applicant')
        res = super(Applicant, self).create(vals)

        self.create_invoice_hr_applicant_rent(res)
        self.create_written_mark(res)
        return res

    def create_invoice_hr_applicant_rent(self, record):
        if record:
            if not record.account_move_id:

                account_move = self.env['account.move'].sudo().create({
                    'name': "INV/JOB/E-RECRUITMENT/" + str(datetime.now().year) + "/" + str(
                        record.job_id.id) + "/" + str(
                        record.id),
                    'partner_id': record.partner_id.id,
                    'ref': record.id,
                    'type': 'out_invoice',
                    'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': record.job_id.product_line_id.id,
                        'name': record.job_id.amount_name,
                        'account_id': False,
                        'price_unit': record.job_id.amount,
                        'quantity': 1.0,
                        'discount': 0.0,
                        # 'product_uom_id': _hr_job_invoice.product_line_id.uom_id.id,
                    })],
                })
                if account_move:
                    invoice_post_status = account_move.sudo().action_post()
                    record.sudo().write({
                        'account_move_id': account_move.id,
                        'invoice_payment_status': account_move.invoice_payment_state,
                    })

    def create_written_mark(self, record):
        if record:
            if not record.job_applicant_written_mark:
                hr_rec_exam_written = self.env['job.applicant.written.mark'].sudo().create({
                    'name': record.id,
                    'job_id': record.job_id.id,
                })
            hr_rec_exam_demo = self.env['job.applicant.demo.mark'].sudo().create({
                'name': record.id,
                'job_id': record.job_id.id,
            })
            hr_rec_exam_viva = self.env['job.applicant.viva.mark'].sudo().create({
                'name': record.id,
                'job_id': record.job_id.id,
            })

    @api.onchange('hr_application_state')
    def action_hr_application_state_accounts(self):

        print(self)
        self.write({'hr_application_state': 'applied'})

    def action_hr_application_state_applied(self):

        self.write({'hr_application_state': 'recommendation'})

    def action_hr_application_state_recommendation(self):

        self.write({'hr_application_state': 'shortlist'})
