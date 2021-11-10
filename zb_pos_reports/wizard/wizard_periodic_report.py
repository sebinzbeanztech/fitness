# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from decimal import localcontext
from datetime import timedelta,datetime



class periodicSalesReports(models.TransientModel):
    _name = 'periodic.sales.reports'
    _description = 'Periodic Sales Report'
    
    
    
    start_date = fields.Date(required=True,default=fields.Date.context_today)
    end_date = fields.Date(required=True,default=fields.Date.context_today)
    user_ids= fields.Many2many('res.users', 'pos_details_report_user_rel', 'user_id', 'wizard_id', 'Salesperson')
    
    def print_report(self):
        datas = {
            'ids': self.ids,
            'form': self.read(),
            
        }
        return self.env.ref('zb_pos_reports.report_periodicsaless').report_action(self,data=datas)
