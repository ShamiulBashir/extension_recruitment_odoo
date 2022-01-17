# -*- coding: utf-8 -*-
import copy

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from odoo import api, http, SUPERUSER_ID
from odoo.exceptions import MissingError, AccessError, UserError
from odoo.http import request, content_disposition
from datetime import datetime
import calendar, math, re, io, base64, os, json, werkzeug
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

from odoo.tools import consteq


def _(param):
    pass


class View(http.Controller):

    @http.route('/web/view/edit_custom', type='json', auth="user")
    def edit_custom(self, custom_id, arch, view_id):
        """
        Edit a custom view

        :param int custom_id: the id of the edited custom view
        :param str arch: the edited arch of the custom view
        :returns: dict with acknowledged operation (result set to True)
        """
        if custom_id:
            custom_view = request.env['ir.ui.view.custom'].browse(custom_id)
        else:
            custom_view = request.env['ir.ui.view'].browse(view_id)
        custom_view.write({'arch': arch})
        return {'result': True}


class WebsiteHrRecruitmentInherit(WebsiteHrRecruitment):

    @http.route([
        '/jobs',
    ], type='http', auth="public", website=True)
    def jobs(self, **kwargs):
        res = super(WebsiteHrRecruitmentInherit, self).jobs(post_category=None, salary_expected=None, start_date=None,
                                                            end_date=None, **kwargs)

        return res

    @http.route('''/jobs/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="user", website=True)
    def jobs_apply(self, job, **kwargs):
        user = request.env.user

        job_applicant_apply = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)],
                                                                         limit=1)

        return request.render("extension_recruitment.apply_extension", {
            'job_applicant_apply': job_applicant_apply,
            'job': job,

        })

    @http.route('''/job/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_apply_extension(self, job, **kwargs):
        user = request.env.user

        job_applicant_apply = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)],
                                                                         limit=1)
        return request.render("extension_recruitment.apply_position", {
            'job': job,
            'job_applicant_apply': job_applicant_apply,
        })

    @http.route('''/jobs/apply/signup/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_apply_signup(self, job, **kwargs):

        return request.render("extension_recruitment.signup_extension", {
            'job': job,

        })

    @http.route(['/create/user/job/'], website=True, auth='public', type='http', csrf=False, methods=['POST', 'GET'])
    def create_user_job(self, **kwargs):
        email_from = kwargs['email_from']
        _applicant_user = http.request.env['res.users'].search([('login', '=', email_from)])


        # Create Invoice of Admission Application

        if _applicant_user:
            _hr_job_invoice = http.request.env['hr.job'].search([('id', '=', kwargs['job_id'])])
            _job_applicant_user = http.request.env['job.applicant'].search([('email_from', '=', email_from)])
            _job_applicant_user.write(kwargs)

            base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            _login_url = base_url + "/web/login"
            mail_server_id = http.request.env['ir.mail_server'].sudo().search([], limit=1).id
            mail_receipient_partners = list()
            mail_receipient_partners.append(_applicant_user.partner_id.id)
            mail_receipient_partners = list(set(mail_receipient_partners))
            mail_subject = "Job Application Successful"
            mail_body_job = """
                                                        <html>
                                                            <body>
                                                                <p>Dear <b>%s</b>,</p>
                                                               <p>Your application has been successfully submitted for the position <b>%s</b>. You will be notified if you are shortlisted.</p>
                                                               <p>You have successfully applied in Daffodil International University (DIU).</p>
                                                               <p>Welcome to DIU's Job Applicant Portal. If you are unable to make payment, you can pay from your Job Applicant Portal.</p>
                                                               <p>Your user access is:</p>
                                                               <ul style='list-style-type: none'>
                                                                   <li> <div style="margin: 16px 8px 16px 8px;"> <a href="%s'>%s" style="background-color: #875a7b; text-decoration: none; color: #fff; padding: 8px 16px 8px 16px; border-radius: 5px;">Login URL</a></li>  
                                                               </ul>
                                                               <p><b>Best regard,</b></p>
                                                               <p>Human Resource Division</p>
                                                               <p>DIU E-recruitment System</p>
                                                               <p>Daffodil International University</p>
                                                               <p>by <a target='_blank' href='https://daffodilvarsity.edu.bd/'>Daffodil International University (DIU)</a></p>
                                                           </body>
                                                       </html>
                                                       """ % (
                str(_job_applicant_user.partner_name),
                str(_hr_job_invoice.name),
                str(_login_url),
                str(_login_url),
            )
            if mail_receipient_partners and mail_server_id:
                mail = http.request.env['mail.mail'].sudo().create({
                    'subject': mail_subject,
                    'email_from': _job_applicant_user.email_from,
                    'email_to': _job_applicant_user.email_from,
                    'recipient_ids': [(6, 0, mail_receipient_partners)],
                    'body_html': mail_body_job,
                    'mail_server_id': mail_server_id,
                })
                mail.sudo().send()

        return _applicant_user

    @http.route(['/hr-applicant/'], website=True, auth='public', type='http', csrf=False, methods=['POST', 'GET'])
    def create_user_hr(self, id=None, **kwargs):
        partner_name = kwargs['partner_name']
        email_from = kwargs['email_from']
        partner_mobile = kwargs['partner_mobile']
        father = kwargs['father']
        mother = kwargs['mother']
        gender = kwargs['gender']
        job_id = kwargs['job_id']
        salary_expected = kwargs['salary_expected']
        job_applicant_id = kwargs['job_applicant_id']
        department_id = kwargs['department_id']
        company_id = kwargs['company_id']
        transaction_no = kwargs['transaction_no']
        description = kwargs['description']
        national_id = kwargs['national_id']
        transaction_date = kwargs['transaction_date']

        _applicant_user = http.request.env['res.users'].search([('login', '=', email_from)])

        if _applicant_user:
            _user = request.env.user

            _hr_rec = http.request.env['hr.applicant'].sudo().create({
                'name': partner_name,
                'partner_name': partner_name,
                'email_from': email_from,
                'partner_mobile': partner_mobile,
                'job_id': job_id,
                'salary_expected': salary_expected,
                'job_applicant_id': job_applicant_id,
                'transaction_no': transaction_no,
                'transaction_date': transaction_date,
                'description': description,
                'department_id': department_id,
                'company_id': company_id,
                'partner_id': _user.partner_id.id,

            })

            # if 'Resume' in kwargs:
            #     if str(kwargs['Resume']) != "<FileStorage: '' ('application/octet-stream')>":
            #         resume_ids = self.upload_attachment_job(kwargs, 'Resume', 'hr.applicant', _hr_rec.id)
            #     del kwargs['Resume']
            #     del kwargs['father']
            #     del kwargs['mother']
            #     del kwargs['gender']
            #     del kwargs['birthday']
            #     del kwargs['national_id']
            #     _image_value = _hr_rec.write(kwargs)
            #
            # else:
            #     del kwargs['father']
            #     del kwargs['mother']
            #     del kwargs['gender']
            #     del kwargs['birthday']
            #     del kwargs['national_id']
            #     _image_value = _hr_rec.write(kwargs)

            pay_order = http.request.env['pay.order'].sudo().create({
                'payorder_rec': _hr_rec.id,
                'job_id': job_id,
                'transaction_no': transaction_no,
                'transaction_date': transaction_date,
            })

            _hr_rec.sudo().write({
                'payorder_rec': pay_order.id,
                'transaction_status': pay_order.transaction_status,
            })

            hr_rec_exam_written = http.request.env['job.applicant.written.mark'].sudo().create({
                'name': _hr_rec.id,
                'job_id': job_id,
            })
            hr_rec_exam_demo = http.request.env['job.applicant.demo.mark'].sudo().create({
                'name': _hr_rec.id,
                'job_id': job_id,
            })
            hr_rec_exam_viva = http.request.env['job.applicant.viva.mark'].sudo().create({
                'name': _hr_rec.id,
                'job_id': job_id,
            })

        # Create Invoice of Admission Application
        _hr_job_invoice = http.request.env['hr.job'].search([('id', '=', kwargs['job_id'])])
        _job_applicant_user = http.request.env['job.applicant'].search([('email_from', '=', email_from)])
        del kwargs['company_id']
        del kwargs['job_applicant_id']
        _job_applicant_user.write(kwargs)
        account_move = http.request.env['account.move'].sudo().create({
            'name': "INV/JOB/E-RECRUITMENT/" + str(datetime.now().year) + "/" + str(
                _hr_job_invoice.id) + "/" + transaction_no,
            'partner_id': _hr_rec.partner_id.id,
            'ref': _hr_rec.id,
            'type': 'out_invoice',
            'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'invoice_line_ids': [(0, 0, {
                'product_id': _hr_job_invoice.product_line_id.id,
                'name': _hr_job_invoice.amount_name,
                'account_id': False,
                'price_unit': _hr_job_invoice.amount,
                'quantity': 1.0,
                'discount': 0.0,
                # 'product_uom_id': _hr_job_invoice.product_line_id.uom_id.id,
            })],
        })
        if account_move:
            invoice_post_status = account_move.sudo().action_post()
            _hr_rec.sudo().write({
                'account_move_id': account_move.id,
                'invoice_payment_status': account_move.invoice_payment_state,
            })
            pay_order.sudo().write({
                'account_move_id': account_move.id,
            })

        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _login_url = base_url + "/web/login"
        mail_server_id = http.request.env['ir.mail_server'].sudo().search([], limit=1).id
        mail_receipient_partners = list()
        mail_receipient_partners.append(_applicant_user.partner_id.id)
        mail_receipient_partners = list(set(mail_receipient_partners))
        mail_subject = "Job Application Successful"
        mail_body_job = """
                                            <html>
                                                <body>
                                                    <p>Dear <b>%s</b>,</p>
                                                   <p>Your application has been successfully submitted for the position <b>%s</b>. You will be notified if you are shortlisted.</p>
                                                   <p>You have successfully applied in Daffodil International University (DIU).</p>
                                                   <p>Welcome to DIU's Job Applicant Portal. If you are unable to make payment, you can pay from your Job Applicant Portal.</p>
                                                   <p>Your user access is:</p>
                                                   <ul style='list-style-type: none'>
                                                       <li> <div style="margin: 16px 8px 16px 8px;"> <a href="%s'>%s" style="background-color: #875a7b; text-decoration: none; color: #fff; padding: 8px 16px 8px 16px; border-radius: 5px;">Login URL</a></li>  
                                                   </ul>
                                                   <p><b>Best regard,</b></p>
                                                   <p>Human Resource Division</p>
                                                   <p>DIU E-recruitment System</p>
                                                   <p>Daffodil International University</p>
                                                   <p>by <a target='_blank' href='https://daffodilvarsity.edu.bd/'>Daffodil International University (DIU)</a></p>
                                               </body>
                                           </html>
                                           """ % (
            str(_job_applicant_user.partner_name),
            str(_hr_job_invoice.name),
            str(_login_url),
            str(_login_url),
        )
        if mail_receipient_partners and mail_server_id:
            mail = http.request.env['mail.mail'].sudo().create({
                'subject': mail_subject,
                'email_from': _job_applicant_user.email_from,
                'email_to': _job_applicant_user.email_from,
                'recipient_ids': [(6, 0, mail_receipient_partners)],
                'body_html': mail_body_job,
                'mail_server_id': mail_server_id,
            })
            mail.sudo().send()

        return request.render("extension_recruitment.successful_hr", {
            '_hr_rec': _hr_rec,
        })

    @http.route(['/create/user/job/applicant'], website=True, auth='public', type='http', csrf=False,
                methods=['POST', 'GET'])
    def successful_signup(self, **kwargs):
        partner_name = kwargs['partner_name']
        email_from = kwargs['email_from']
        partner_mobile = kwargs['partner_mobile']
        password = kwargs['password']
        confirm_password = kwargs['confirm_password']

        _applicant_user = http.request.env['res.users'].search([('login', '=', email_from)])
        _user = self.create_user(partner_name, email_from, password, partner_mobile)
        _job_rec = http.request.env['job.applicant'].sudo().create({
            'name': partner_name,
            'partner_name': partner_name,
            'email_from': email_from,
            'partner_mobile': partner_mobile,
            'password': password,
            'confirm_password': confirm_password,
            'user_id': _user.id,
            'partner_id': _user.partner_id.id,

        })

        return request.render("extension_recruitment.successful_signup", {
            '_job_rec': _job_rec,
        })

    def create_user(self, name, login, password, partner_mobile, **kwargs):

        user_group = http.request.env.ref("base.group_portal") or False
        user_timezone = http.request._context.get('tz') or False
        _applicant_user = http.request.env['res.users'].search([('login', '=', login)])
        if not _applicant_user:
            _applicant_user = http.request.env['res.users'].sudo().create({
                'name': name,
                'login': login,
                'password': password,
                'email': login,
                'phone': partner_mobile,
                'mobile': partner_mobile,
                'is_job_applicant': True,
                'groups_id': user_group,
                'tz': user_timezone,
            })

            ## Send Mail of User Access to Job Applicant

            if _applicant_user:
                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                _login_url = base_url + "/web/login"
                mail_server_id = http.request.env['ir.mail_server'].sudo().search([], limit=1).id
                mail_receipient_partners = list()
                mail_receipient_partners.append(_applicant_user.partner_id.id)
                mail_receipient_partners = list(set(mail_receipient_partners))
                mail_subject = "DIU Job Application"
                mail_body_job = """
                        <html>
                            <body>
                                <p>Dear <b>%s</b>,</p>
                               <p>You have successfully applied in Daffodil International University (DIU).</p>
                               <p>Welcome to DIU's Job Applicant Portal. If you are unable to make payment, you can pay from your Job Applicant Portal.</p>
                               <p>Your user access is:</p>
                               <ul style='list-style-type: none'>
                                   <li> <div style="margin: 16px 8px 16px 8px;"> <a href="%s'>%s" style="background-color: #875a7b; text-decoration: none; color: #fff; padding: 8px 16px 8px 16px; border-radius: 5px;">Login URL</a></li>  
                                   <li>Username: <b>%s</b></li>
                                   <li>Password: <b>%s</b></li>
                               </ul>
                               <p>by <a target='_blank' href='https://daffodilvarsity.edu.bd/'>Daffodil International University (DIU)</a></p>
                           </body>
                       </html>
                       """ % (
                    str(name),
                    str(_login_url),
                    str(_login_url),
                    str(login),
                    str(password),
                )
                if mail_receipient_partners and mail_server_id:
                    mail = http.request.env['mail.mail'].sudo().create({
                        'subject': mail_subject,
                        'email_from': login,
                        'email_to': login,
                        'recipient_ids': [(6, 0, mail_receipient_partners)],
                        'body_html': mail_body_job,
                        'mail_server_id': mail_server_id,
                    })
                    mail.sudo().send()

        return _applicant_user

    @http.route(['/create/user/payorder/'], website=True, auth='public', type='http', csrf=False,
                methods=['POST', 'GET'])
    def create_user_payorder(self, **kwargs):

        job_id = kwargs['job_id']
        job_applicant_id = kwargs['job_applicant_id']
        transaction_no = kwargs['transaction_no']
        transaction_date = kwargs['transaction_date']

        pay_order = http.request.env['pay.order'].sudo().create({
            'applicant_id': job_applicant_id,
            'job_id': job_id,
            'transaction_no': transaction_no,
            'transaction_date': transaction_date,
        })

        return pay_order

    @http.route('/my/view-table', type='http', auth="user", website=True)
    def view_table(self, **kwargs):
        user = request.env.user

        view_job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        return request.render("extension_recruitment.view_table", {
            'view_job_applicant_rec': view_job_applicant_rec,
        })

    @http.route('/job/meeting/information/', type='http', auth="user", website=True)
    def meeting_table(self, **kwargs):
        user = request.env.user

        meeting_applicant_rec = request.env['calendar.event'].sudo().search([('partner_ids', '=', user.partner_id.id)])

        return request.render("extension_recruitment.meeting_table", {
            'meeting_applicant_rec': meeting_applicant_rec,
        })

    @http.route('/job/meeting/information/<int:id>', type='http', auth="user", website=True)
    def meeting_details(self, id=None, **kwargs):
        meeting_applicant_rec = request.env['calendar.event'].sudo().search([('id', '=', id)])

        return request.render("extension_recruitment.meeting_details", {
            'meeting_applicant_rec': meeting_applicant_rec,
        })

    @http.route('/my/job/applicant/apply/list', type='http', auth="user", website=True)
    def list_table(self, **kwargs):
        user = request.env.user

        _job_applicant_rec = request.env['hr.applicant'].sudo().search([('email_from', '=', user.email)])

        return request.render("extension_recruitment.list_table", {
            '_job_applicant_rec': _job_applicant_rec,
        })

    @http.route('/my/job/applicant/result', type='http', auth="user", website=True)
    def result(self, **kwargs):
        user = request.env.user

        _job_applicant_rec = request.env['hr.applicant'].sudo().search([('email_from', '=', user.email)])

        return request.render("extension_recruitment.result", {
            '_job_applicant_rec': _job_applicant_rec,
        })

    @http.route(['/my/jobs/account/my/admit/card/<int:job_applicant_admit_id>'], type="http", auth="public",
                website=True)
    def job_admit_card_report(self, job_applicant_admit_id, access_token=None, report_type=None, download=False,
                              **kwargs):
        if job_applicant_admit_id:
            model_sudo = self._document_check_access('hr.applicant', job_applicant_admit_id, access_token)
            if report_type in ('html', 'pdf', 'text'):
                return self._show_report(model=model_sudo, report_type=report_type,
                                         report_ref='extension_recruitment.job_applicant_admit_card_id',
                                         download=download)
        else:
            return http.request.redirect('/my')

    def _document_check_access(self, model_name, document_id, access_token=None):
        document = request.env[model_name].browse([document_id])
        document_sudo = document.with_user(SUPERUSER_ID).exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        try:
            document.check_access_rights('read')
            document.check_access_rule('read')
        except AccessError:
            if not access_token or not document_sudo.access_token or not consteq(document_sudo.access_token,
                                                                                 access_token):
                raise
        return document_sudo

    def _show_report(self, model, report_type, report_ref, download=False):
        if report_type not in ('html', 'pdf', 'text'):
            raise UserError(_("Invalid report type: %s") % report_type)

        report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)

        if not isinstance(report_sudo, type(request.env['ir.actions.report'])):
            raise UserError(_("%s is not the reference of a report") % report_ref)

        method_name = 'render_qweb_%s' % (report_type)
        report = getattr(report_sudo, method_name)([model.id], data={'report_type': report_type})[0]
        reporthttpheaders = [
            ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
            ('Content-Length', len(report)),
        ]
        if report_type == 'pdf' and download:
            filename = "%s.pdf" % (re.sub('\W+', '-', model._get_report_base_filename()))
            reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
        return request.make_response(report, headers=reporthttpheaders)

    @http.route('/my/jobs/hr/applicant/<int:id>', type='http', auth="user", website=True)
    def hr_applicant_view(self, id=None, **kwargs):

        hr_applicant_rec = request.env['hr.applicant'].sudo().search([('id', '=', id)])
        # Render page
        return request.render("extension_recruitment.hr_applicant", {
            'hr_applicant_rec': hr_applicant_rec,
        })

    @http.route('/my/jobs/account/<int:id>', type='http', auth="user", website=True)
    def applicant(self, id=None, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search(
            [('partner_id', '=', user.partner_id.id), ('id', '=', id)])

        image_id = http.request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'image_id')])
        if image_id:
            image_id = image_id
        else:
            image_id = ""

        Resume = http.request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'Resume')])
        if Resume:
            Resume = Resume
        else:
            Resume = ""

        applicant_signature = http.request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'applicant_signature ')])
        if applicant_signature:
            applicant_signature = applicant_signature
        else:
            applicant_signature = ""

        # Render page
        return request.render("extension_recruitment.job_applicant", {
            'job_applicant_rec': job_applicant_rec,
            'image_id': image_id,
            'Resume': Resume,
            'applicant_signature': applicant_signature,

        })

    @http.route('/my/jobs/account/edu', type='http', auth="user", website=True)
    def applicant_edu(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        level_of_education = kwargs['level_of_education']
        exam_degree_title_name = kwargs['exam_degree_title_name']
        concentration_major_group_name = kwargs['concentration_major_group_name']
        board_name = kwargs['board_name']
        institute_name = kwargs['institute_name']
        result = kwargs['result']
        cgpa = kwargs['cgpa']
        mark = kwargs['mark']
        scale = kwargs['scale']
        passing_year = kwargs['passing_year']
        duration = kwargs['duration']
        achievement = kwargs['achievement']
        # certificate = kwargs['certificate']

        file_job_education = self.upload_job_education(kwargs, level_of_education, exam_degree_title_name,
                                                       concentration_major_group_name, board_name, institute_name,
                                                       result, cgpa, mark, scale, passing_year, duration, achievement,
                                                       'job.applicant.education', job_applicant_rec.id)
        job_education_rec = request.env['job.applicant.education'].sudo().search([('id', '=', file_job_education.id)])

        data_list = []
        if job_education_rec:
            data_list = {
                'exam': job_education_rec.exam_degree_title_name,
                'major': job_education_rec.concentration_major_group_name,
                'institute': job_education_rec.institute_name,
                'cgpa': job_education_rec.cgpa,
                'mark': job_education_rec.mark,
                'scale': job_education_rec.scale,
                'passing_year': job_education_rec.passing_year,
                'duration': job_education_rec.duration,
            }

        return str(data_list)

    @http.route('/my/jobs/account/edu/delete', type='http', auth="user", website=True)
    def applicant_edu_del(self, **kwargs):
        print(kwargs['id'])
        job_education_rec = request.env['job.applicant.education'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_education_rec)

        job_education_rec.unlink()

        return

    @http.route('/my/jobs/account/article/delete', type='http', auth="user", website=True)
    def applicant_article_del(self, **kwargs):
        print(kwargs['id'])
        job_article_rec = request.env['job.applicant.article'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_article_rec)

        job_article_rec.unlink()

        return

    @http.route('/my/jobs/account/conference/delete', type='http', auth="user", website=True)
    def applicant_conference_del(self, **kwargs):
        print(kwargs['id'])
        job_conference_rec = request.env['conference'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_conference_rec)

        job_conference_rec.unlink()

        return

    @http.route('/my/jobs/account/book/delete', type='http', auth="user", website=True)
    def applicant_book_del(self, **kwargs):
        print(kwargs['id'])
        job_book_rec = request.env['job.applicant.publication'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_book_rec)

        job_book_rec.unlink()

        return

    @http.route('/my/jobs/account/project/delete', type='http', auth="user", website=True)
    def applicant_project_del(self, **kwargs):
        print(kwargs['id'])
        job_project_rec = request.env['project'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_project_rec)

        job_project_rec.unlink()

        return

    @http.route('/my/jobs/account/member/delete', type='http', auth="user", website=True)
    def applicant_member_del(self, **kwargs):
        print(kwargs['id'])
        job_member_rec = request.env['membership'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_member_rec)

        job_member_rec.unlink()

        return

    @http.route('/my/jobs/account/experience/delete', type='http', auth="user", website=True)
    def applicant_experience_del(self, **kwargs):
        print(kwargs['id'])
        job_experience_rec = request.env['job.applicant.experience'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_experience_rec)

        job_experience_rec.unlink()

        return

    @http.route('/my/jobs/account/degree/delete', type='http', auth="user", website=True)
    def applicant_degree_del(self, **kwargs):
        print(kwargs['id'])
        job_degree_rec = request.env['professional.certificate'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_degree_rec)

        job_degree_rec.unlink()

        return

    @http.route('/my/jobs/account/training/delete', type='http', auth="user", website=True)
    def applicant_training_del(self, **kwargs):
        print(kwargs['id'])
        job_training_rec = request.env['professional.training'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_training_rec)

        job_training_rec.unlink()

        return

    @http.route('/my/jobs/account/award/delete', type='http', auth="user", website=True)
    def applicant_award_del(self, **kwargs):
        print(kwargs['id'])
        job_award_rec = request.env['professional.award'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_award_rec)

        job_award_rec.unlink()

        return

    @http.route('/my/jobs/account/language/delete', type='http', auth="user", website=True)
    def applicant_language_del(self, **kwargs):
        print(kwargs['id'])
        job_language_rec = request.env['language.proficiency'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_language_rec)

        job_language_rec.unlink()

        return

    @http.route('/my/jobs/account/reference/delete', type='http', auth="user", website=True)
    def applicant_reference_del(self, **kwargs):
        print(kwargs['id'])
        job_reference_rec = request.env['job.applicant.reference'].sudo().search([('id', '=', kwargs['id'])], limit=1)
        print(job_reference_rec)

        job_reference_rec.unlink()

        return

    @http.route('/my/jobs/account/reference', type='http', auth="user", website=True)
    def applicant_reference(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        reference_name = kwargs['reference_name']
        reference_organization = kwargs['reference_organization']
        reference_position = kwargs['reference_position']
        reference_relation = kwargs['reference_relation']
        reference_mobile = kwargs['reference_mobile']
        reference_phone = kwargs['reference_phone']
        reference_email = kwargs['reference_email']
        reference_address = kwargs['reference_address']

        job_application_reference_id = job_applicant_rec.id
        file_job_reference = self.upload_job_reference(kwargs, reference_name, reference_organization,
                                                       reference_position, reference_relation, reference_mobile,
                                                       reference_phone, reference_email, reference_address,
                                                       'job.applicant.reference', job_application_reference_id)
        job_reference_rec = request.env['job.applicant.reference'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                                 limit=1)

        job_reference_rec = request.env['job.applicant.reference'].sudo().search([('id', '=', file_job_reference.id)])

        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _reference_url = base_url + "/reference/verification/"
        mail_server_id = http.request.env['ir.mail_server'].sudo().search([], limit=1).id
        mail_receipient_partners = list()
        mail_receipient_partners.append(job_applicant_rec.partner_id.id)
        mail_receipient_partners = list(set(mail_receipient_partners))
        mail_subject = "Job Applicant Verification"
        mail_body_job = """
                                              <html>
                                                  <body>
                                                      <p>Dear <b>%s</b> Sir,</p>
                                                     <p>Your applicant <b>%s</b> has been successfully submitted.Please You will be your profile verification. Your applicant will be notified if your applicant are shortlisted.</p>
                                                     <p>Your verification access is:</p>
                                                     <ul style='list-style-type: none'>
                                                         <li> <div style="margin: 16px 8px 16px 8px;"> <a href="%s%s" style="background-color: #875a7b; text-decoration: none; color: #fff; padding: 8px 16px 8px 16px; border-radius: 5px;">Verification</a></li>
                                                     </ul>
                                                     <p><b>Best regard,</b></p>
                                                     <p>Human Resource Division</p>
                                                     <p>DIU E-recruitment System</p>
                                                     <p>Daffodil International University</p>
                                                     <p>by <a target='_blank' href='https://daffodilvarsity.edu.bd/'>Daffodil International University (DIU)</a></p>
                                                 </body>
                                             </html>
                                             """ % (
            str(reference_name),
            str(job_applicant_rec.partner_name),
            str(_reference_url),
            str(job_reference_rec.id),
        )
        if mail_receipient_partners and mail_server_id:
            mail = http.request.env['mail.mail'].sudo().create({
                'subject': mail_subject,
                'email_from': reference_email,
                'email_to': reference_email,
                'recipient_ids': [(6, 0, mail_receipient_partners)],
                'body_html': mail_body_job,
                'mail_server_id': mail_server_id,
            })
            mail.sudo().send()

        data_list = []
        if job_reference_rec:
            data_list = {
                'name': job_reference_rec.reference_name,
                'org': job_reference_rec.reference_organization,
                'position': job_reference_rec.reference_position,
                'mobile': job_reference_rec.reference_mobile,
                'phone': job_reference_rec.reference_phone,
                'email': job_reference_rec.reference_email,

            }

        return str(data_list)

    @http.route('/reference/verification/<int:id>', type='http', auth="public", website=True)
    def reference_verification(self, id=None, **kwargs):
        job_reference_rec = request.env['job.applicant.reference'].sudo().search([('id', '=', id)])

        return request.render("extension_recruitment.reference_verification", {
            'job_reference_rec': job_reference_rec,

        })

    @http.route('/verified', type='http', auth="public", website=True)
    def verified(self, **kwargs):

        xxx = kwargs['xxx']

        job_reference_rec = request.env['job.applicant.reference'].sudo().search([('id', '=', xxx)])

        job_reference_rec.sudo().write({
            'verify_status': True,
        })

        return job_reference_rec

    @http.route('/admit-card', type='http', auth="public", website=True)
    def admit_card_verified(self, **kwargs):

        xx = kwargs['xx']

        hr_reference_rec = request.env['hr.applicant'].sudo().search([('id', '=', xx)])

        print(hr_reference_rec)

        hr_reference_rec.sudo().write({
            'admit_card_status': True,
        })
        print(hr_reference_rec)

        return hr_reference_rec

    @http.route('/my/jobs/account/experience', type='http', auth="user", website=True)
    def applicant_experience(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        company_name = kwargs['company_name']
        position = kwargs['position']
        department = kwargs['department']
        area_experiences = kwargs['area_experiences']
        responsibilities = kwargs['responsibilities']
        company_location = kwargs['company_location']
        start_date = kwargs['start_date']
        to_date = kwargs['to_date']

        job_application_experience_id = job_applicant_rec.id
        file_job_experience = self.upload_job_experience(kwargs, company_name, position, department, area_experiences,
                                                         responsibilities, company_location, start_date, to_date,
                                                         'job.applicant.experience', job_application_experience_id)
        job_experience_rec = request.env['job.applicant.experience'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                                   limit=1)
        data_list = []
        if job_experience_rec:
            data_list = {
                'name': job_experience_rec.company_name,
                'position': job_experience_rec.position,
                'department': job_experience_rec.department,
                'from': job_experience_rec.start_date,
                'to': job_experience_rec.to_date,

            }

        return str(data_list)

    @http.route('/my/jobs/account/article', type='http', auth="user", website=True)
    def applicant_article(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        article_name = kwargs['article_name']
        article_author = kwargs['article_author']
        vol_no = kwargs['vol_no']
        page_no = kwargs['page_no']
        article_publication_date = kwargs['article_publication_date']
        publication_country = kwargs['publication_country']

        job_application_article_id = job_applicant_rec.id
        file_job_article = self.upload_job_article(kwargs, article_name, article_author, vol_no, page_no,
                                                   article_publication_date, publication_country,
                                                   'job.applicant.article', job_application_article_id)
        job_article_rec = request.env['job.applicant.article'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                             limit=1)
        data_list = []
        if job_article_rec:
            data_list = {
                'name': job_article_rec.article_name,
                'author': job_article_rec.article_author,
                'date': job_article_rec.article_publication_date,
                'country': job_article_rec.publication_country,

            }

        return str(data_list)

    @http.route('/my/jobs/account/conference', type='http', auth="user", website=True)
    def applicant_conference(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        proceedings_name = kwargs['proceedings_name']
        conference_author = kwargs['conference_author']
        conference_page_no = kwargs['conference_page_no']
        conference_article_publication_date = kwargs['conference_article_publication_date']
        conference_publication_country = kwargs['conference_publication_country']

        job_application_conference_id = job_applicant_rec.id
        file_job_conference = self.upload_job_conference(kwargs, proceedings_name, conference_author,
                                                         conference_page_no, conference_article_publication_date,
                                                         conference_publication_country, 'conference',
                                                         job_application_conference_id)
        job_conference_rec = request.env['conference'].sudo().search([('id', '=', job_applicant_rec.id)], limit=1)
        data_list = []
        if job_conference_rec:
            data_list = {
                'name': job_conference_rec.proceedings_name,
                'author': job_conference_rec.conference_author,
                'date': job_conference_rec.conference_article_publication_date,
                'country': job_conference_rec.conference_publication_country,

            }

        return str(data_list)

    @http.route('/my/jobs/account/training', type='http', auth="user", website=True)
    def applicant_training(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        training_title = kwargs['training_title']
        training_institute_name = kwargs['training_institute_name']
        training_company_location = kwargs['training_company_location']
        training_start_date = kwargs['training_start_date']
        training_to_date = kwargs['training_to_date']
        training_concentration_major_name = kwargs['training_concentration_major_name']

        training_id = job_applicant_rec.id
        file_job_training = self.upload_job_training(kwargs, training_title, training_institute_name,
                                                     training_company_location, training_start_date, training_to_date,
                                                     training_concentration_major_name, 'professional.training',
                                                     training_id)
        job_training_rec = request.env['professional.training'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                              limit=1)
        data_list = []
        if job_training_rec:
            data_list = {
                'title': job_training_rec.training_title,
                'institute': job_training_rec.training_institute_name,
                'start': job_training_rec.training_start_date,
                'to': job_training_rec.training_to_date,
                'major': job_training_rec.training_concentration_major_name,

            }

        return str(data_list)

    @http.route('/my/jobs/account/certification', type='http', auth="user", website=True)
    def applicant_certification(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        certification = kwargs['certification']
        degree_institute_name = kwargs['degree_institute_name']
        degree_company_location = kwargs['degree_company_location']
        degree_start_date = kwargs['degree_start_date']
        degree_to_date = kwargs['degree_to_date']
        degree_concentration_major_name = kwargs['degree_concentration_major_name']

        certification_id = job_applicant_rec.id
        file_job_certification = self.upload_job_certification(kwargs, certification, degree_institute_name,
                                                               degree_company_location, degree_start_date,
                                                               degree_to_date, degree_concentration_major_name,
                                                               'professional.certificate', certification_id)

        return request.render("extension_recruitment.job_applicant", {
            'job_applicant_rec': job_applicant_rec,

        })

    @http.route('/my/jobs/account/language', type='http', auth="user", website=True)
    def applicant_language(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        language_name = kwargs['language_name']
        reading = kwargs['reading']
        writing = kwargs['writing']
        speaking = kwargs['speaking']
        listening = kwargs['listening']

        language_id = job_applicant_rec.id
        file_job_language = self.upload_job_language(kwargs, language_name, reading, writing, speaking, listening,
                                                     'language.proficiency', language_id)
        job_language_rec = request.env['language.proficiency'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                             limit=1)
        data_list = []
        if job_language_rec:
            data_list = {
                'name': job_language_rec.language_name,
                'read': job_language_rec.reading,
                'write': job_language_rec.writing,
                'speak': job_language_rec.speaking,
                'listen': job_language_rec.listening,
            }

        return str(data_list)

    @http.route('/my/jobs/account/award', type='http', auth="user", website=True)
    def applicant_award(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        award = kwargs['award']
        award_by = kwargs['award_by']
        award_year = kwargs['award_year']

        award_id = job_applicant_rec.id
        file_job_award = self.upload_job_award(kwargs, award, award_by, award_year, 'professional.award', award_id)

        job_award_rec = request.env['professional.award'].sudo().search([('id', '=', job_applicant_rec.id)], limit=1)
        data_list = []
        if job_award_rec:
            data_list = {
                'award': job_award_rec.award,
                'by': job_award_rec.award_by,
                'year': job_award_rec.award_year,
            }

        return str(data_list)

    @http.route('/my/jobs/account/project', type='http', auth="user", website=True)
    def applicant_project(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        academic_program_name = kwargs['academic_program_name']
        title = kwargs['title']
        project_year = kwargs['project_year']

        job_application_project_id = job_applicant_rec.id
        file_job_project = self.upload_job_project(kwargs, academic_program_name, title, project_year, 'project',
                                                   job_application_project_id)

        job_project_rec = request.env['project'].sudo().search([('id', '=', job_applicant_rec.id)], limit=1)
        data_list = []
        if job_project_rec:
            data_list = {
                'name': job_project_rec.academic_program_name,
                'title': job_project_rec.title,
                'year': job_project_rec.project_year,
            }

        return str(data_list)

    @http.route('/my/jobs/account/book', type='http', auth="user", website=True)
    def applicant_book(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        publication_name = kwargs['publication_name']
        publisher = kwargs['publisher']
        year = kwargs['year']

        job_application_publication_id = job_applicant_rec.id
        file_job_publication = self.upload_job_publication(kwargs, publication_name, publisher, year,
                                                           'job.applicant.publication', job_application_publication_id)

        job_book_rec = request.env['job.applicant.publication'].sudo().search([('id', '=', job_applicant_rec.id)],
                                                                              limit=1)
        data_list = []
        if job_book_rec:
            data_list = {
                'name': job_book_rec.publication_name,
                'publisher': job_book_rec.publisher,
                'year': job_book_rec.year,
            }

        return str(data_list)

    @http.route('/my/jobs/account/member', type='http', auth="user", website=True)
    def applicant_member(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])
        job_member_rec = request.env['membership'].sudo().search([('id', '=', job_applicant_rec.id)], limit=1)

        description = kwargs['description']
        member_year = kwargs['member_year']

        job_application_membership_id = job_applicant_rec.id
        file_job_member = self.upload_job_member(kwargs, description, member_year, 'membership',
                                                 job_application_membership_id)

        data_list = []
        if job_member_rec:
            data_list = {
                'description': job_member_rec.description,
                'year': job_member_rec.member_year,
            }

        return str(data_list)

    @http.route('/my/jobs/account/video', type='http', auth="user", website=True)
    def applicant_video(self, **kwargs):
        user = request.env.user

        job_applicant_rec = request.env['job.applicant'].sudo().search([('partner_id', '=', user.partner_id.id)])

        video_resumes = kwargs['video_resumes']
        demo_videos = kwargs['demo_videos']

        file_job_video = self.upload_job_video(kwargs, video_resumes, demo_videos, 'job.applicant',
                                               job_applicant_rec.id)

        return request.render("extension_recruitment.job_applicant", {
            'job_applicant_rec': job_applicant_rec,

        })

    @http.route('/my/jobs/account/update', type='http', auth="user", website=True)
    def successful(self, **kwargs):

        job_applicant_rec = request.env['job.applicant'].sudo().search([('id', '=', kwargs['employee_id'])])
        job_attachment_rec = request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'image_id')])
        job_attachment_rec_resume = request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'Resume')])
        job_attachment_rec_signature = request.env['ir.attachment'].sudo().search(
            [('res_id', '=', job_applicant_rec.id), ('res_field', '=', 'applicant_signature')])

        kw = copy.copy(kwargs)

        if 'image' in kwargs:
            if str(kwargs['image_id']) != "<FileStorage: '' ('application/octet-stream')>":
                file = self.update_attachment_job(kwargs, 'image_id', 'job.applicant', job_applicant_rec.id,
                                                  job_attachment_rec)
            del kw['image']

        else:
            files = self.upload_attachment_job(kwargs, 'image_id', 'job.applicant', job_applicant_rec.id)

        if 'resumes' in kwargs:
            if str(kwargs['Resume']) != "<FileStorage: '' ('application/octet-stream')>":
                resume_id = self.update_attachment_job(kwargs, 'Resume', 'job.applicant', job_applicant_rec.id,
                                                       job_attachment_rec_resume)
            del kw['resumes']

        else:

            resume_ids = self.upload_attachment_job(kwargs, 'Resume', 'job.applicant', job_applicant_rec.id)

        if 'applicant' in kwargs:
            if str(kwargs['applicant_signature']) != "<FileStorage: '' ('application/octet-stream')>":
                signature = self.update_attachment_job(kwargs, 'applicant_signature', 'job.applicant',
                                                       job_applicant_rec.id, job_attachment_rec_signature)
            del kw['applicant']

        else:
            signatures = self.upload_attachment_job(kwargs, 'applicant_signature', 'job.applicant',
                                                    job_applicant_rec.id)

        del kw['image_id']
        del kw['Resume']
        del kw['applicant_signature']
        # del kw['video_resume']
        # del kw['demo_video']

        _image_value = job_applicant_rec.write(kw)

        return request.render("extension_recruitment.successful", {
            'job_applicant_rec': job_applicant_rec,
        })

    def upload_job_education(self, values, level_of_education, exam_degree_title_name, concentration_major_group_name,
                             board_name, institute_name, result, cgpa, mark, scale, passing_year, duration, achievement,
                             model_name, data):

        education_data_file = http.request.env['job.applicant.education'].sudo().create({
            'level_of_education': level_of_education,
            'exam_degree_title_name': exam_degree_title_name,
            'concentration_major_group_name': concentration_major_group_name,
            'board_name': board_name,
            'institute_name': institute_name,
            'result': result,
            'cgpa': cgpa,
            'mark': mark,
            'scale': scale,
            'passing_year': passing_year,
            'duration': duration,
            'achievement': achievement,
            'job_application_education_id': int(data),
        })
        # files_certificate = self.upload_attachment_job(values, 'certificate', 'job.applicant.education', data)

        if education_data_file:
            return education_data_file

    def upload_job_article(self, values, article_name, article_author, vol_no, page_no, article_publication_date,
                           publication_country, model_name, data):

        article_data_file = http.request.env['job.applicant.article'].sudo().create({
            'article_name': article_name,
            'article_author': article_author,
            'vol_no': vol_no,
            'page_no': page_no,
            'article_publication_date': article_publication_date,
            'publication_country': publication_country,
            'job_application_article_id': int(data),
        })

        if article_data_file:
            return article_data_file

    def upload_job_conference(self, values, proceedings_name, article_author, page_no, article_publication_date,
                              publication_country, model_name, data):

        conference_data_file = http.request.env['conference'].sudo().create({
            'proceedings_name': proceedings_name,
            'conference_author': article_author,
            'conference_page_no': page_no,
            'conference_article_publication_date': article_publication_date,
            'conference_publication_country': publication_country,
            'job_application_conference_id': int(data),
        })

        if conference_data_file:
            return conference_data_file

    def upload_job_project(self, values, academic_program_name, title, project_year, model_name, data):

        project_data_file = http.request.env['project'].sudo().create({
            'academic_program_name': academic_program_name,
            'title': title,
            'project_year': project_year,
            'job_application_project_id': int(data),
        })

        if project_data_file:
            return project_data_file

    def upload_job_publication(self, values, publication_name, publisher, year, model_name, data):

        publication_data_file = http.request.env['job.applicant.publication'].sudo().create({
            'publication_name': publication_name,
            'publisher': publisher,
            'year': year,
            'job_application_publication_id': int(data),
        })

        if publication_data_file:
            return publication_data_file

    def upload_job_member(self, values, description, year, model_name, data):

        membership_data_file = http.request.env['membership'].sudo().create({
            'description': description,
            'member_year': year,
            'job_application_membership_id': int(data),
        })

        if membership_data_file:
            return membership_data_file

    def upload_job_video(self, values, video_resumes, demo_videos, model_name, data):

        video_data_file = http.request.env['job.applicant'].sudo().create({
            'video_resumes': video_resumes,
            'demo_videos': demo_videos,
        })

        if video_data_file:
            return video_data_file

    def upload_job_certification(self, values, certification, institute_name, company_location, start_date, to_date,
                                 concentration_major_name, model_name, data):

        certification_data_file = http.request.env['professional.certificate'].sudo().create({
            'certification': certification,
            'degree_institute_name': institute_name,
            'degree_company_location': company_location,
            'degree_start_date': start_date,
            'degree_to_date': to_date,
            'degree_concentration_major_name': concentration_major_name,
            'certification_id': int(data),
        })

        if certification_data_file:
            return certification_data_file

    def upload_job_training(self, values, title, institute_name, company_location, start_date, to_date,
                            concentration_major_name, model_name, data):

        training_data_file = http.request.env['professional.training'].sudo().create({
            'training_title': title,
            'training_institute_name': institute_name,
            'training_company_location': company_location,
            'training_start_date': start_date,
            'training_to_date': to_date,
            'training_concentration_major_name': concentration_major_name,
            'training_id': int(data),
        })

        if training_data_file:
            return training_data_file

    def upload_job_language(self, values, language_name, reading, writing, speaking, listening, model_name, data):

        language_data_file = http.request.env['language.proficiency'].sudo().create({
            'language_name': language_name,
            'reading': reading,
            'writing': writing,
            'speaking': speaking,
            'listening': listening,
            'language_id': int(data),
        })

        if language_data_file:
            return language_data_file

    def upload_job_award(self, values, award, award_by, award_year, model_name, data):

        award_data_file = http.request.env['professional.award'].sudo().create({
            'award': award,
            'award_by': award_by,
            'award_year': award_year,
            'award_id': int(data),
        })

        if award_data_file:
            return award_data_file

    def upload_job_experience(self, values, company_name, position, department, area_experiences, responsibilities,
                              company_location, start_date, to_date, model_name, data):

        experience_data_file = http.request.env['job.applicant.experience'].sudo().create({
            'company_name': company_name,
            'position': position,
            'department': department,
            'area_experiences': area_experiences,
            'responsibilities': responsibilities,
            'company_location': company_location,
            'start_date': start_date,
            'to_date': to_date,
            'job_application_experience_id': int(data),
        })

        if experience_data_file:
            return experience_data_file

    def upload_job_reference(self, values, reference_name, reference_organization, reference_position,
                             reference_relation, reference_mobile, reference_phone, reference_email, reference_address,
                             model_name, data):

        reference_data_file = http.request.env['job.applicant.reference'].sudo().create({
            'reference_name': reference_name,
            'reference_organization': reference_organization,
            'reference_position': reference_position,
            'reference_relation': reference_relation,
            'reference_mobile': reference_mobile,
            'reference_phone': reference_phone,
            'reference_email': reference_email,
            'reference_address': reference_address,
            'verify_status': False,
            'job_application_reference_id': int(data),
        })

        if reference_data_file:
            return reference_data_file

    def upload_attachment_job(self, values, key, model_name, res_id):
        if not values and key and model_name and res_id:
            return False
        filename = key
        file = values.get(key)
        attachment_file = file.read()
        attachment = http.request.env['ir.attachment'].sudo().create({
            'name': filename,
            'store_fname': filename,
            'res_name': filename,
            'type': 'binary',
            'res_model': str(model_name),
            'res_field': str(key),
            'res_id': int(res_id),
            'datas': base64.encodestring(attachment_file)
        })

        if attachment:
            return attachment

    def update_attachment_job(self, values, key, model_name, res_id, attachment):
        if not values and key and model_name and res_id:
            return False
        filename = key
        file = values.get(key)
        attachment_file = file.read()
        attachment = attachment.write({
            'name': filename,
            'store_fname': filename,
            'res_name': filename,
            'type': 'binary',
            'res_model': str(model_name),
            'res_field': str(key),
            'res_id': int(res_id),
            'datas': base64.encodestring(attachment_file)
        })

        if attachment:
            return attachment

    @http.route(['/free/download/<int:attachment_id>', ], type='http', auth='public')
    def download_attachment_free_admission(self, attachment_id):
        # Restrict User Login to Download
        if not request.session.uid:
            # return web._login_redirect()
            return werkzeug.utils.redirect('/web/login')

        # Check if this is a valid attachment id
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "mimetype", "res_model", "res_id", "type", "url"]
        )

        if attachment:
            attachment = attachment[0]
        else:
            return redirect(self.orders_page)

        # The client has bought the product, otherwise it would have been blocked by now
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            filename = attachment['name']
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()
