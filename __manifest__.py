# -*- coding: utf-8 -*-
{
    'name': 'Recruitment Extension',
    'summary': """Something about recruitment Extension.""",
    'description': """ 
Recruitment Extension
=====================
Something about recruitment extension.
    """,
    'version': '13.0.1.0',
    'author': 'A.T.M Shamiul Bashir',
    'website': 'https://daffodilvarsity.edu.bd/',
    'category': 'Tools',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'contacts',
        'web',
        'hr',
        'dsl_corporate_meeting',
        'website_hr_recruitment',
        'hr_recruitment',
        'hr_recruitment_survey',
        'website_partner',
        'website_mail',
        'website_form',
        'board',
        'web_one2many_kanban',
    ],
    'data': [
        'data/ir_sequence.xml',
        'data/config_data.xml',
        'data/extension_recruitment_data.xml',
        # 'data/mail_template.xml',

        ##report
        'report/job_admit_card_report.xml',
        'report/written_exam_list_report.xml',
        'report/job_written_exam_list_report.xml',
        'report/written_exam_list_report_admit_download.xml',
        'report/position_department_wise_total_cv.xml',
        'report/job_cv_report.xml',

        ## security
        'security/recruitment_security.xml',
        'security/ir.model.access.csv',

        ## View & Wizard
        'views/assets.xml',
        'views/job_view.xml',
        # 'views/menus.xml',
        'views/website_job_view_template.xml',
        'views/website_applicant_view.xml',
        'views/job_meeting.xml',
        'views/job_portal.xml',
        'views/exam_mark.xml',
        'views/job_applicant_view.xml',
        'views/admit_form.xml',
        'views/head_dean.xml',
        'views/pay_order.xml',
        'views/dashboard.xml',
        'views/final_shortlist.xml',

        ## Wizard
        'wizards/video_show.xml',
    ],
    'qweb': [],
    'demo': [

    ],
    'external_dependencies': {
        'python': [
            'werkzeug',
        ],
    },
    # 'icon': '/extension_recruitment/static/description/icon.png',
    # 'images': [
    #     'static/description/banner.png',
    # ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
    'contributors': [
        'A.T.M Shamiul Bashir <https://github.com/01shamiul>',
    ],
}
