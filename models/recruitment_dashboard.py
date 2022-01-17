# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from odoo.tools import float_utils


class HallDashboard(models.Model):
    _name = "recruitment.dashboard"
    _description = "Recruitment Dashboard"

    total_invoice_payment_status = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Invoice Status')
    total_hr_application_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pay', 'bKash Pay'),
        ('applied', 'Applied Job'),
        ('recommendation', 'Recommended'),
        ('shortlist', 'Shortlisted')],
        string='Application Status')
    total_state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], string='Status', readonly=True, required=True, tracking=True, copy=False, default='recruit',
        help="Set whether the recruitment process is open or closed for this job position.")

    count_total_current_job = fields.Integer(string='Total Current Job', compute='_compute_count_total_current_job')
    count_total_application_ids = fields.Integer(string='Total Application', compute='_compute_count_total_application')
    count_total_applicant = fields.Integer(string='Total Applicant', compute='_compute_count_total_applicant')

    count_total_paid = fields.Integer(string='Total Paid', compute='_compute_count_total_paid')
    count_total_not_paid = fields.Integer(string='Total Not Paid', compute='_compute_count_total_not_paid')

    count_total_job_recruit = fields.Integer(string='Total Job Recruit', compute='_compute_count_total_rectuit')
    count_total_job_not_recruit = fields.Integer(string='Total Not Recruit Job', compute='_compute_count_total_not_rectuit')

    count_total_application_draft = fields.Integer(string='Total Application Draft State', compute='_compute_count_total_draft')
    count_total_pay = fields.Integer(string='Total Application Payment State', compute='_compute_count_total_pay')
    count_total_applied = fields.Integer(string='Total Application Applied', compute='_compute_count_total_applied')
    count_total_recommendation = fields.Integer(string='Total Application Recommendation', compute='_compute_count_total_recommendation')
    count_total_shortlist = fields.Integer(string='Total Application Shortlist', compute='_compute_count_total_shortlist')

    @api.model
    def get_paid_details(self):
        total_invoice_payment_status = self.env['recruitment.dashboard'].sudo().search([('total_invoice_payment_status', '=', 'paid')])
        if total_invoice_payment_status:
            return total_invoice_payment_status.count_total_paid
        else:
            return False

    @api.model
    def get_not_paid_details(self):
        total_invoice_payment_status = self.env['recruitment.dashboard'].sudo().search(
            [('total_invoice_payment_status', '=', 'not_paid')])
        if total_invoice_payment_status:
            return total_invoice_payment_status.count_total_not_paid
        else:
            return False

    @api.model
    def get_draft_details(self):
        total_hr_application_state = self.env['recruitment.dashboard'].sudo().search([('total_hr_application_state', '=', 'draft')])
        if total_hr_application_state:
            return total_hr_application_state.count_total_application_draft
        else:
            return False

    @api.model
    def get_pay_details(self):
        total_hr_application_state = self.env['recruitment.dashboard'].sudo().search(
            [('total_hr_application_state', '=', 'pay')])
        if total_hr_application_state:
            return total_hr_application_state.count_total_pay
        else:
            return False

    @api.model
    def get_applied(self):
        total_hr_application_state = self.env['recruitment.dashboard'].sudo().search(
            [('total_hr_application_state', '=', 'applied')])
        if total_hr_application_state:
            return total_hr_application_state.count_total_applied
        else:
            return False

    @api.model
    def get_recommendation(self):
        total_hr_application_state = self.env['recruitment.dashboard'].sudo().search(
            [('total_hr_application_state', '=', 'recommendation')])
        if total_hr_application_state:
            return total_hr_application_state.count_total_recommendation
        else:
            return False


    @api.model
    def get_shortlist(self):
        total_hr_application_state = self.env['recruitment.dashboard'].sudo().search(
            [('total_hr_application_state', '=', 'shortlist')])
        if total_hr_application_state:
            return total_hr_application_state.count_total_shortlist
        else:
            return False

    @api.model
    def get_open(self):
        total_state = self.env['recruitment.dashboard'].sudo().search([('total_state', '=', 'open')])
        if total_state:
            return total_state.count_total_job_not_recruit
        else:
            return False

    @api.model
    def get_recruit(self):
        total_state = self.env['recruitment.dashboard'].sudo().search([('total_state', '=', 'recruit')])
        if total_state:
            return total_state.count_total_job_recruit
        else:
            return False

    @api.model
    def get_allocation_request_rejected(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_allocation_reject_request
        else:
            return False

    @api.model
    def get_allocation_request_cancelled(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_allocation_cancel_request
        else:
            return False

    @api.model
    def get_renew_request(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_renew_request
        else:
            return False

    @api.model
    def get_renew_request_pending(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_renew_pending_request
        else:
            return False

    @api.model
    def get_renew_request_accepted(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_renew_accepted_request
        else:
            return False

    @api.model
    def get_renew_request_rejected(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_renew_reject_request
        else:
            return False

    @api.model
    def get_renew_request_cancelled(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_cancel_request
        else:
            return False

    @api.model
    def get_cancel_request(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_request
        else:
            return False

    @api.model
    def get_cancel_request_pending(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_pending_request
        else:
            return False

    @api.model
    def get_cancel_request_accepted(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_accepted_request
        else:
            return False

    @api.model
    def get_cancel_request_rejected(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_reject_request
        else:
            return False

    @api.model
    def get_cancel_request_cancelled(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_cancel_cancel_request
        else:
            return False


    @api.model
    def get_count_total_suggestions(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_suggestions
        else:
            return False

    @api.model
    def get_count_total_pending_suggestions(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_pending_suggestions
        else:
            return False

    @api.model
    def get_count_total_responded_suggestions(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_responded_suggestions
        else:
            return False


    @api.model
    def get_count_total_requisition(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_requisition
        else:
            return False

    @api.model
    def get_count_total_pending_requisition(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_pending_requisition
        else:
            return False

    @api.model
    def get_count_total_responded_requisition(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_responded_requisition
        else:
            return False

    @api.model
    def get_count_total_male_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_male_seat
        else:
            return False

    @api.model
    def get_count_total_booked_male_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_booked_male_seat
        else:
            return False

    @api.model
    def get_count_total_available_male_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_available_male_seat
        else:
            return False

    @api.model
    def get_count_total_female_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_female_seat
        else:
            return False

    @api.model
    def get_count_total_booked_female_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_booked_female_seat
        else:
            return False

    @api.model
    def get_count_total_available_female_seat(self):
        total_facility = self.env['op.campus.facility.dashboard'].sudo().search([('facility_category', '=', 'hall')])
        if total_facility:
            return total_facility.count_total_available_female_seat
        else:
            return False

    def _compute_count_total_hall(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'hall')])
            line.count_total_hall = len(total_facility)

    def _compute_count_total_level(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'level')])
            line.count_total_level = len(total_facility)

    def _compute_count_total_room(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'room')])
            line.count_total_room = len(total_facility)

    def _compute_count_total_seat(self):
        for line in self:
            total_room = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'room')])
            total_capacity = 0
            for room in total_room:
                total_capacity = total_capacity + int(room.capacity)

            line.count_total_seat = total_capacity

    def _compute_count_total_booked_seat(self):
        for line in self:
            total_room = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'room')])
            allocated_seat = 0
            for room in total_room:

                # Check in Allocation Table
                allocations = room.facility_allocation_lines
                for allocation in allocations:
                    if allocation.is_hall_cancel == False:
                        allocated_seat = allocated_seat + 1

                # Check in Allocation Request table
                total_pending_request = self.env['opd.facility.allocation.request'].sudo().search([('room_id', '=', room.id)])
                if total_pending_request:
                    for request in total_pending_request:
                        if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                            allocated_seat = allocated_seat + 1

            line.count_total_booked_seat = allocated_seat

    def _compute_total_available_seat(self):
        for line in self:
            total_room = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'room')])
            total_capacity = 0
            allocated_seat = 0
            for room in total_room:

                # Check in Allocation Table
                allocations = room.facility_allocation_lines
                for allocation in allocations:
                    if allocation.is_hall_cancel == False:
                        allocated_seat = allocated_seat + 1

                # Check in Allocation Request table
                total_pending_request = self.env['opd.facility.allocation.request'].sudo().search([('room_id', '=', room.id)])
                if total_pending_request:
                    for request in total_pending_request:
                        if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                            allocated_seat = allocated_seat + 1

                total_capacity = total_capacity + int(room.capacity)

            line.count_total_available_seat = total_capacity - allocated_seat


    def _compute_count_total_allocation_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.request'].sudo().search([])
            line.count_total_allocation_request = len(total_request)

    def _compute_count_total_allocation_pending_request(self):
        for line in self:
            total_pending_request = self.env['opd.facility.allocation.request'].sudo().search(['|', '|', ('state', '=', 'draft'), ('state', '=', 'hall_recommend'), ('state', '=', 'accounts_recommend')])
            line.count_total_allocation_pending_request = len(total_pending_request)

    def _compute_count_total_allocation_accepted_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.request'].sudo().search([('state', '=', 'provost_recommend')])
            line.count_total_allocation_accepted_request = len(total_request)

    def _compute_count_total_allocation_cancel_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.request'].sudo().search([('state', '=', 'cancel')])
            line.count_total_allocation_cancel_request = len(total_request)

    def _compute_count_total_allocation_reject_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.request'].sudo().search([('state', '=', 'reject')])
            line.count_total_allocation_reject_request = len(total_request)


    def _compute_count_total_renew_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.renew'].sudo().search([])
            line.count_total_renew_request = len(total_request)

    def _compute_count_total_renew_pending_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.renew'].sudo().search(['|', ('state', '=', 'draft'), ('state', '=', 'hall_recommend')])
            line.count_total_renew_pending_request = len(total_request)

    def _compute_count_total_renew_accepted_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.renew'].sudo().search([('state', '=', 'accounts_recommend')])
            line.count_total_renew_accepted_request = len(total_request)

    def _compute_count_total_renew_cancel_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.renew'].sudo().search([('state', '=', 'cancel')])
            line.count_total_renew_cancel_request = len(total_request)

    def _compute_count_total_renew_reject_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.renew'].sudo().search([('state', '=', 'reject')])
            line.count_total_renew_reject_request = len(total_request)


    def _compute_count_total_cancel_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.cancel'].sudo().search([])
            line.count_total_cancel_request = len(total_request)

    def _compute_count_total_cancel_pending_request(self):
        for line in self:
            total_pending_request = self.env['opd.facility.allocation.cancel'].sudo().search(['|', '|','|', '|', ('state', '=', 'draft'), ('state', '=', 'hall_recommend'),('state', '=', 'accounts_recommend'),('state', '=', 'library_recommend'),('state', '=', 'it_recommend')])
            line.count_total_cancel_pending_request = len(total_pending_request)

    def _compute_count_total_cancel_accepted_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.cancel'].sudo().search([('state', '=', 'provost_recommend')])
            line.count_total_cancel_accepted_request = len(total_request)

    def _compute_count_total_cancel_cancel_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.cancel'].sudo().search([('state', '=', 'cancel')])
            line.count_total_cancel_cancel_request = len(total_request)

    def _compute_count_total_cancel_reject_request(self):
        for line in self:
            total_request = self.env['opd.facility.allocation.cancel'].sudo().search([('state', '=', 'reject')])
            line.count_total_cancel_reject_request = len(total_request)





    def _compute_total_suggestions(self):
        for line in self:
            total_pending_request = self.env['opd.hall.complain'].sudo().search([])
            line.count_total_suggestions = len(total_pending_request)

    def _compute_total_pending_suggestions(self):
        for line in self:
            total_pending_request = self.env['opd.hall.complain'].sudo().search([('state', '=', 'submit')])
            line.count_total_pending_suggestions = len(total_pending_request)

    def _compute_total_responded_suggestions(self):
        for line in self:
            total_pending_request = self.env['opd.hall.complain'].sudo().search([('state', '=', 'response')])
            line.count_total_responded_suggestions = len(total_pending_request)



    def _compute_total_requisition(self):
        for line in self:
            total_pending_request = self.env['opd.hall.requisition'].sudo().search([])
            line.count_total_requisition = len(total_pending_request)

    def _compute_total_pending_requisition(self):
        for line in self:
            total_pending_request = self.env['opd.hall.requisition'].sudo().search([('state', '=', 'submit')])
            line.count_total_pending_requisition = len(total_pending_request)

    def _compute_total_responded_requisition(self):
        for line in self:
            total_pending_request = self.env['opd.hall.requisition'].sudo().search([('state', '=', 'response')])
            line.count_total_responded_requisition = len(total_pending_request)



    def _compute_total_male_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'hall'), ('facility_type_hall_type', '=', 'boys')])
            allocation = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:
                        allocation = allocation + int(room.capacity)

            line.count_total_male_seat = allocation

    def _compute_total_male_booked_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True),('facility_category', '=', 'hall'),('facility_type_hall_type', '=', 'boys')])
            allocated_seat = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:

                        # Check in Allocation Table
                        allocations = room.facility_allocation_lines
                        for allocation in allocations:
                            if allocation.is_hall_cancel == False:
                                allocated_seat = allocated_seat + 1

                        # Check in Allocation Request table
                        total_pending_request = self.env['opd.facility.allocation.request'].sudo().search([('room_id', '=', room.id)])
                        if total_pending_request:
                            for request in total_pending_request:
                                if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                                    allocated_seat = allocated_seat + 1

            line.count_total_booked_male_seat = allocated_seat

    def _compute_total_male_available_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search([('is_hall_management', '=', True), ('facility_category', '=', 'hall'),('facility_type_hall_type', '=', 'boys')])
            allocated_seat = 0
            total_capacity = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:

                        # Check in Allocation Table
                        allocations = room.facility_allocation_lines
                        for allocation in allocations:
                            if allocation.is_hall_cancel == False:
                                allocated_seat = allocated_seat + 1

                        # Check in Allocation Request table
                        total_pending_request = self.env['opd.facility.allocation.request'].sudo().search([('room_id', '=', room.id)])
                        if total_pending_request:
                            for request in total_pending_request:
                                if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                                    allocated_seat = allocated_seat + 1

                        total_capacity = total_capacity + int(room.capacity)

            line.count_total_available_male_seat = total_capacity - allocated_seat

    def _compute_total_female_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search(
                [('is_hall_management', '=', True), ('facility_category', '=', 'hall'),
                 ('facility_type_hall_type', '=', 'girls')])
            allocation = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:
                        allocation = allocation + int(room.capacity)

            line.count_total_female_seat = allocation

    def _compute_total_female_booked_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search(
                [('is_hall_management', '=', True), ('facility_category', '=', 'hall'),
                 ('facility_type_hall_type', '=', 'girls')])
            allocated_seat = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:

                        # Check in Allocation Table
                        allocations = room.facility_allocation_lines
                        for allocation in allocations:
                            if allocation.is_hall_cancel == False:
                                allocated_seat = allocated_seat + 1

                        # Check in Allocation Request table
                        total_pending_request = self.env['opd.facility.allocation.request'].sudo().search(
                            [('room_id', '=', room.id)])
                        if total_pending_request:
                            for request in total_pending_request:
                                if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                                    allocated_seat = allocated_seat + 1

            line.count_total_booked_female_seat = allocated_seat

    def _compute_total_female_available_seat(self):
        for line in self:
            total_facility = self.env['op.campus.facility'].sudo().search(
                [('is_hall_management', '=', True), ('facility_category', '=', 'hall'),
                 ('facility_type_hall_type', '=', 'girls')])
            allocated_seat = 0
            total_capacity = 0
            for hall in total_facility:
                for level in hall.child_ids:
                    for room in level.child_ids:

                        # Check in Allocation Table
                        allocations = room.facility_allocation_lines
                        for allocation in allocations:
                            if allocation.is_hall_cancel == False:
                                allocated_seat = allocated_seat + 1

                        # Check in Allocation Request table
                        total_pending_request = self.env['opd.facility.allocation.request'].sudo().search(
                            [('room_id', '=', room.id)])
                        if total_pending_request:
                            for request in total_pending_request:
                                if request.state == 'draft' or request.state == 'hall_recommend' or request.state == 'accounts_recommend':
                                    allocated_seat = allocated_seat + 1

                        total_capacity = total_capacity + int(room.capacity)

            line.count_total_available_female_seat = total_capacity - allocated_seat