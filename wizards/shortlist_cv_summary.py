import time
from odoo import models, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request


class ShortlistCvReport(models.TransientModel):
    _name = "shortlist.cv.report"
    _description = "Shortlist Cv Report Wizard"

    application = fields.Many2one('hr.applicant', 'Application')
    applicant = fields.Many2one('job.applicant', string="Applicant")
    job_id = fields.Many2one('hr.job', string="Applied Job")

    def check_report(self):
        application = self.application
        applicant = self.applicant

        filter_report = [('application', '=', application.id)]

        # if self.state != 'done':
        #     filter_report.append(
        #         ('done', '=', self.state)
        #     )

        all_program_cv = request.env['hr.applicant'].sudo().search(filter_report)

        all_report = []
        for program in all_program_cv:
            report = {
                'applicant_name': program.name,
                'applicant_mobile': program.partner_mobile,
                'email': program.email_from,
                'father': program.job_applicant_id.father,
                'mother': program.job_applicant_id.mother,
                'birthday': program.job_applicant_id.birthday,
                'o_level_board_name': program.education_board_o_level_id.name,
                'gender': program.job_applicant_id.gender,
                'image_id': program.job_applicant_id.image_id,
                'video_resume': program.job_applicant_id.video_resume,
                'nationality': program.job_applicant_id.nationality,
            }
            all_report.append(report)

        return self.env.ref('extension_recruitment.report_opd_program_campus_wise_list') \
            .report_action(self, {'program': all_report,
                                  }, config=False)

