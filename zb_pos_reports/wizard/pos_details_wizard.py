from odoo import api, fields, models, _
from odoo.exceptions import UserError
from decimal import localcontext
from datetime import timedelta

import psycopg2
import pytz

class PosDetailsReport(models.TransientModel):
    _name = 'wizard.pos.details'
    _description = 'Open Sales Details Report'

    start_date = fields.Date(required=True,default=fields.Date.context_today)
    end_date = fields.Date(required=True,default=fields.Date.context_today)
    pos_config_ids = fields.Many2many('pos.config', 'pos_detail_config',
        default=lambda s: s.env['pos.config'].search([]))
    report_detail = fields.Selection([('normal', 'Normal'),
                                ('detail', 'Detailed'),], 
                               'Report Type', default='normal')
 
#     def get_user_names(self):
#         list=[]
#         for record in self:
#             for rec in record.pos_config_ids:
#                 dict = {
#                     'names':rec.name,
#                     }
#                 list.append(dict)
#             return list
#      

    
    def print_customer_statement(self):
        
        datas = {
            'ids': self.ids,
            'form': self.read(),
            
        }
        return self.env.ref('zb_pos_reports.action_report_sales').report_action(self,data=datas)
    
    
    