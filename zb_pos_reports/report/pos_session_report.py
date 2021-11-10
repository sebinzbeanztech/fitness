import pytz
import time
import datetime
from odoo import api, fields, models
from datetime import timedelta

class SessionReport(models.AbstractModel):
    _name = "report.zb_pos_reports.pos_session_report_template_new"
    
    def _get_utc_time_range(self, form):
        user = self.env['res.users'].browse()
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        between_dates = {}

        for date_field, delta in {'start_at': {'days': 0}, 'date_order': {'days': 1}}.items():
            timestamp = datetime.datetime.strptime(form[date_field] , "%Y-%m-%d") + timedelta(**delta)
            timestamp = user_tz.localize(timestamp).astimezone(pytz.utc)
            between_dates[date_field] = timestamp.strftime("%Y-%m-%d")
        return between_dates['start_at'], between_dates['date_order']
    
    
    def get_payments(self, form,model):
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = self.env['res.users'].company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = self.env["pos.order"].search([('session_id','=',model.id),('date_order','>',date_start),('date_order','<=',date_end),('state','in',['paid','invoiced','done']),('session_id.config_id','in',user_ids)])
            pos_id=[]
            for pos in pos_ids:
                pos_id.append(pos.id)
            data={}
            if pos_id:
                payment_ids = self.env["pos.payment"].search([('pos_order_id', 'in', pos_id)])
                if payment_ids:
                    a_l=[]
                    for r in payment_ids:
                        a_l.append(r.id)
                    
                    self._cr.execute("select pm.name,sum(amount) from pos_payment as pl,pos_payment_method as pm " \
                                    "where pm.id =pl.payment_method_id and pl.id IN %s"\
                                    "group by pm.name",(tuple(a_l),))
     
                    data = self.env.cr.dictfetchall()
                    return data
            else:
                return {}
    
    
    
    
    
    def _get_report_values(self, docids,data=None):
        doc_id = self.env['pos.session'].browse(docids)
        for i in doc_id.payment_method_ids:
            print('======',i)
        pos_orders = [order.id for order in doc_id.order_ids]
        payment_ids = self.env["pos.payment"].search([('pos_order_id', 'in', pos_orders)])
        a_l=[]
        for r in payment_ids:
            a_l.append(r.id)
        self._cr.execute("select pm.name,sum(amount) from pos_payment as pl,pos_payment_method as pm " \
                                    "where pm.id =pl.payment_method_id and pl.id IN %s"\
                                    "group by pm.name",(tuple(a_l),))
     
        datas = self.env.cr.dictfetchall()
        payment=[]
        for dict in datas:
            payment.append(dict)
        print('===============================',payment)
        docargs = {
                'docs': doc_id,
                'payment_data' : payment,
               }
        
        return docargs
        
        
        
        
        
        
        
        
        
        