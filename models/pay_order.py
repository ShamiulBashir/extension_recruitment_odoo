from odoo import api, fields, models, _


class PayOrder(models.Model):
    _name = "pay.order"
    _description = "Pay Order"
    _order = "id desc"

    applicant_id = fields.Many2one('job.applicant', string="Applicant")
    active = fields.Boolean(string="Active", default="True")
    payorder_rec = fields.Many2one('hr.applicant', string="Applicant")
    job_id = fields.Many2one('hr.job', string="Position")
    transaction_date = fields.Date(string="Transaction Date")
    transaction_no = fields.Char(string="Transaction No")
    account_move_id = fields.Many2one('account.move', string="Invoice")
    transaction_status = fields.Selection([
        ('not received', 'Not Received'),
        ('received', 'Received')
    ], string='Status', default='not received')
    invoice_payment_status = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Invoice Status', store=True, readonly=True, copy=False, tracking=True,
        related='account_move_id.invoice_payment_state')
    name = fields.Char(string="Transaction Serial", readonly=True)

    _sql_constraints = [
        ('id_unique', 'unique(id)', 'Name already exists!'),
        ('name_unique', 'unique(name)', 'Transaction Serial already exists!')]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('pay.order')
        res = super(PayOrder, self).create(vals)
        return res

    @api.onchange('transaction_status')
    def onchange_payorder_rec(self):
        record_ids = self.env['hr.applicant'].search([('id', '=', self.payorder_rec.id)])
        for record in record_ids:
            record.write({
                'transaction_status': self.transaction_status
            })

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_confirm_receive(self):
        """ Reinsert the applicant into the recruitment pipe in the first stage"""
        self.write({'transaction_status': 'received'})
        record_ids = self.env['hr.applicant'].search([('id', '=', self.payorder_rec.id)])
        for record in record_ids:
            record.write({
                'hr_application_state': 'pay'
            })

    def action_accounts_approve(self):
        """ Reinsert the applicant into the recruitment pipe in the first stage"""
        record_ids = self.env['hr.applicant'].search([('id', '=', self.payorder_rec.id)])
        for record in record_ids:
            record.write({
                'hr_application_state': 'applied'
            })





