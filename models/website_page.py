from odoo import api, fields, models, _


class WebsitePublishedMixin(models.AbstractModel):
    _inherit = 'website.published.mixin'
    _description = 'Website Published Mixin'

    deadline = fields.Many2one('hr.job', string="Deadline", compute='_compute_unpublish')

    @api.model_create_multi
    def _compute_unpublish(self):
        for record in self:
            record.deadline = record.deadline.end_date
            print(record.deadline)
            record.website_published = record.deadline
            print(record.website_published)
            record.website_published = False
            print(record.website_published)
