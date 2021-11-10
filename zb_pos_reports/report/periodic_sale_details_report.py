# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import pytz
import time
import datetime
from odoo import api, fields, models
from datetime import timedelta

class PeriodicReport(models.AbstractModel):
    _name = "report.zb_pos_reports.report_periodic_saless"
    
    
    def _get_report_values(self, docids,data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id', []))
        data = dict(data or {})
        config_list = []
        results = self._pos_sales_details(data['form'])
        statements=[]                
        lists=[]
        lists1=[]
        out = []
        dic = {}
        result = results
        sum = 0
        user_listt=[]
        for res in result:
            for key,value in res.items():
                    for k, val in value.items():
                        lists.append(val)
                        lists1.append(k)
                        if k=='user_list':
                            for user in val:
                               if user not in user_listt:
                                   user_listt.append(user) 
                    dic=dict(zip(lists1,lists))
            statements.append(dic)
            print('=========user_listtuser_listt======',user_listt)
            docargs = {
                   'doc_ids':docs,
                   'doc_model': model,
                   'docs': docs,
                   'user_listt':user_listt,
                   'statement_data' : statements,
                    'get_user_names' : self._get_user_names,
                   'data': data['form'],
                   }
        return docargs


    def _get_all_users(self):
        user=[]
        user_obj = self.env['res.users']
        for user_obj in user_obj.search([]):
            user.append(user_obj.id)
        return user
            

    def _get_utc_time_range(self,form):
        user = self.env['res.users'].browse()
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        between_dates = {}
         
        for date_field, delta in {'start_date': {'days': 0}, 'end_date': {'days': 1}}.items():
            timestamp = datetime.datetime.strptime(form[date_field] , "%Y-%m-%d") + timedelta(**delta)
            timestamp = user_tz.localize(timestamp).astimezone(pytz.utc)
            between_dates[date_field] = timestamp.strftime("%Y-%m-%d")
        return between_dates['start_date'], between_dates['end_date']
   
    def _pos_sales_details(self, form):
        pos_obj = self.env['pos.order']
        user_obj = self.env['res.users']
        data1 = []
        result = {}
        for data in form:
            user_ids = data['user_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            date_start, date_end = self._get_utc_time_range(data)
            
            date_list = []
            if date_start.split(' ')[0] != data['start_date']:
                date_start = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d")
            
            delta = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d") - datetime.datetime.strptime(data['start_date'], "%Y-%m-%d")        
            
            d1 = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d")
            
            for i in range(delta.days + 1):
                date_list.append(d1 + timedelta(i))
                       
            result = {}
            user_list=[]
            for d in date_list:
                tot_qty = 0
                vat=0
                total_taxed = 0
                total_price = 0
                total_cost = 0
                total_no_trans = 0
                orginal_date = str(d)
                
                start_date = orginal_date.split(' ')[0] + ' 00:00:00' 
                end_date = orginal_date.split(' ')[0] + ' 23:59:59' 
                       
                pos_ids = pos_obj.search([
                    ('date_order', '>=', start_date),
                    ('date_order', '<=', end_date),
                    ('user_id', '=', user_ids),
                    ('state', 'in', ['done', 'paid', 'invoiced']),
#                     ('company_id', '=', company_id),
                ])
               
                for pos in pos_ids:
                    if pos.user_id.name not in user_list:
                        user_list.append(pos.user_id.name)
                    for pol in pos.lines:
                        vat = vat+(pol.price_subtotal_incl- pol.price_subtotal)
                        tot_qty = tot_qty + pol.qty
                        total_taxed = total_taxed + pol.price_subtotal_incl
                        total_price = total_price + pol.price_subtotal
#                         if pol.product_id.landed_cost == 0:
                        total_cost = total_cost + (pol.product_id.standard_price * pol.qty)
#                         else:
#                             total_cost = total_cost + (pol.product_id.landed_cost * pol.qty)
                            
                    #total_price = total_price + pos.amount_total
                    
                    total_no_trans = total_no_trans + 1
                
                o_date = orginal_date.split(' ')[0]
                if result.get(o_date):
                    if result[o_date].get(date_order) == result.get(o_date):
                        result.update({
                            o_date: {
                                    'trans_no': total_no_trans,
                                    'date_order': o_date,
                                    'qty': tot_qty, 
                                    'cost': total_cost, 
                                    'total': total_price, 
                                    'profit': total_price - total_cost, 
                                    'vat':vat,
                                    'total_taxed':total_taxed,
                                    'user_list':user_list,
                                    }
                                })
                        data1.append(result)
                else:
                    result = {
                        o_date: {
                                'trans_no': total_no_trans,
                                'date_order': o_date,
                                'qty': tot_qty, 
                                'cost': total_cost, 
                                'total': total_price, 
                                'profit': total_price - total_cost, 
                                'vat':vat,
                                'user_list':user_list,
                                'total_taxed':total_taxed,
                                }
                            }
                    data1.append(result)
        if data1:
#             data = sorted(data, key=lambda k: k['pos_name'])
            return data1
        else:
            return {}

    def _get_user_names(self, user_ids):
        user_obj = self.env['res.users']
        return ', '.join(map(lambda x: x.name, user_obj.browse(user_ids)))

    
  
