import time
from openerp import api, fields, models
from datetime import datetime
from operator import itemgetter
from datetime import timedelta
import datetime
import psycopg2
import pytz
from PIL._imaging import outline

class PosDetailsReport(models.AbstractModel):
    _name = "report.zb_pos_reports.report_detailsofsales"
    
#     def convert_datetime_field(self,date):
#         user = self.env['res.users'].browse()
#         user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
#         timestamp = date.strftime("%Y-%m-%d %H:%M:%S")
#         dt = pytz.utc.localize(timestamp).astimezone(user_tz)
#         order_date = dt.strftime('%d/%m/%Y %H:%M:%S')
#         return order_date
    
    def _get_utc_time_range(self, form):
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
        data = []
        list_pos=[]
        result = {}
        tup = ()
        total=0
        qty=0
        discount=0
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            report_type = dat['report_detail']
            pos_ids = pos_obj.search([
                ('date_order', '>=', dat['start_date']),
                ('date_order', '<=', dat['end_date']),
                ('session_id.config_id', 'in', user_ids),
                ('state', 'in', ['done', 'paid', 'invoiced']),
    #             ('company_id', '=', company_id)
            ], order="id asc")
#             sql = """ select id from pos_order where order_date>'%s' and order_date<='%s'"""%(dat['start_date'],dat['end_date'])
#             self._cr.execute(sql)
#             pos_ids =  self._cr.fetchall()
            tot_qty = 0
            tot_disc = 0
            total_vat = 0
            category = {}
            users_listtt=[]
            for pos in pos_ids:
                if pos.user_id.name not in users_listtt:
                    users_listtt.append(pos.user_id.name)
                method = ''
                total_qty = 0
                total_disc = 0
                total_price = 0
                profit_without_dis_n = 0
                total_cost = 0
                total_price_unit = 0
                price_total = 0
                  
                for payment in pos.payment_ids:
                    if payment.payment_method_id:
                        method = payment.payment_method_id.name
                pos_name = pos.name
                if pos.account_move:
                    pos_name = pos.account_move.name
                              
#                 total_vat = total_vat + pos.amount_tax
                
                for pol in pos.lines:
                    price_total = pol.price_unit*pol.qty
                    category_key = pol.product_id.categ_id.name
                    
                    if category_key in category:
                        category[category_key]['qty'] += pol.qty
                        category[category_key]['price'] += price_total
                     
                    else:  
                        category[category_key] = {'qty':pol.qty,'price':price_total,'name':category_key}
                     
    #                 if pol.product_id.landed_cost == 0:
                    prdt_cost = pol.product_id.standard_price
    #                 else:
    #                     prdt_cost = pol.product_id.landed_cost
                          
                    vat = pol.price_subtotal_incl- pol.price_subtotal
                    profit_without_dis = (pol.price_unit * pol.qty) - (prdt_cost*pol.qty)
                    profit_without_dis_n = profit_without_dis_n + ((pol.price_unit * pol.qty) - (prdt_cost*pol.qty))
                    total_qty = total_qty + pol.qty
                    total_disc = total_disc + pol.discount
                    total_price = total_price + pol.price_unit
#                     total_vat = total_vat + pol.vat_amount
    #                 if pol.product_id.landed_cost == 0:
                    total_cost = total_cost + (pol.product_id.standard_price*pol.qty)
    #                 else:
    #                     total_cost = total_cost + (pol.product_id.landed_cost*pol.qty)
                              
                    total_price_unit = total_price_unit + (pol.price_unit * pol.qty)
                    tot_qty = tot_qty + pol.qty
                    tot_disc = tot_disc + pol.discount
                      
#                     att_date = pos.date_order
#                     from_zone = pytz.timezone(user_obj.browse().tz or 'UTC')
#                     to_zone = pytz.timezone('UTC')
#                     timein =att_date.replace(tzinfo=to_zone)
#                     date = timein.astimezone(from_zone)
#                     if str(date).find('+') != -1:
#                         date = str(date).split('+')[0]
                    order_date = pos.date_order
                      
                    if report_type == 'detail':
    #                     if pol.product_id.landed_cost == 0:
                        cost = pol.product_id.standard_price*pol.qty
    #                     else:
    #                         cost = pol.product_id.landed_cost*pol.qty
                        result = {
                            'code': pol.product_id.default_code,
                            'session':pos.session_id.config_id.name,
                            'ref':pos.pos_reference,
                            'name': pol.product_id.name,
                           'users_listtt':users_listtt,
                            'invoice_id': pos.account_move.id, 
                            'price_unit': pol.price_unit, 
                            'qty': pol.qty, 
                            'total_taxed':pol.price_subtotal_incl,
                            'vat':pol.tax_ids_after_fiscal_position.name,
                            'vat_amount':vat,
                            'discount': pol.discount, 
                            #'total': (pol.price_unit * pol.qty * (1 - (pol.discount) / 100.0)), 
                            'total':pol.price_subtotal,
                            'date_order': order_date, 
                            'pos_name': pos_name, 
                            'uom': pol.product_id.uom_id.name,
                            'brand': '',
                            #'profit': profit_without_dis - pol.discount,
                            #'total': pol.price_unit * pol.qty,
                            'cost': cost,
                            'profit': pol.price_subtotal - cost, 
                            'customer': pos.partner_id and pos.partner_id.name or '',
                            'user'   : pos.user_id and pos.user_id.name or '',
                            'method' : method,
                            'barcode': pol.product_id.barcode,
                            'category': category
                        }
                        total_vat = total_vat+pos.amount_tax
                        data.append(result)
                    if result.get('qty'):
                        qty += result.get('qty')
                    if result.get('discount'):
                        discount += result.get('discount')
                total += pos.amount_total
                if report_type == 'normal':
                    cashier = ''
                    if method.find('Credit') != -1:
                        cashier = pos.user_id.name
                      
#                     att_date = datetime.datetime.strptime(pos.date_order, '%Y-%m-%d %H:%M:%S')
#                     from_zone = pytz.timezone(user_obj.browse().tz or 'UTC')
#                     to_zone = pytz.timezone('UTC')
#                     timein =att_date.replace(tzinfo=to_zone)
#                     date = timein.astimezone(from_zone)
#                     if str(date).find('+') != -1:
#                         date = str(date).split('+')[0]
                        
                    order_date = pos.date_order    
                    
                    result = {
                        'code': pos.pos_reference,
                        'name': pos.name,
                        'session':pos.session_id.config_id.name,
                        'ref':pos.pos_reference,
                        'invoice_id': pos.account_move.id, 
                        'price_unit': pos.amount_total, 
                        'qty': total_qty, 
                        'vat_amount':pos.amount_tax,
                        'discount': total_disc, 
                        #'total': (pos.amount_total * total_qty * (1 - (total_disc) / 100.0)), 
                        'total':pos.amount_total - pos.amount_tax,
                        'total_taxed':pos.amount_total,
                        'date_order': order_date, 
                        'pos_name': pos_name, 
                        'uom': '',
                        'brand': '',
                        #'profit': profit_without_dis_n - total_disc,
                        #'total': total_price_unit,
                        'users_listtt':users_listtt,
                        'cost':  total_cost ,
                        'profit': pos.amount_total - pos.amount_tax - total_cost, 
                        'customer': pos.partner_id and pos.partner_id.name or '',
                        'user'   : pos.user_id and pos.user_id.name or '',
                        'method' : method,
                        'cashier' : cashier,
                        'category': category
                       
                    }
                    
                    data.append(result)
                if result.get('qty'):
                    qty = tot_qty
                if result.get('discount'):
                    discount = tot_disc
            
        if data:
            data = sorted(data, key=lambda k: str(k['pos_name']))
            return data
        else:
            return {}

         
    def _get_all_users(self):
        user=[]
        user_obj = self.env['pos.config']
        for user_obj in user_obj.search([]):
            user.append(user_obj.id)
        return user
  

    def get_total_discount(self, form): 
        total_discount=0.000
        pos_obj = self.env['pos.order']
        user_obj = self.env['res.users']
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = pos_obj.search([('date_order','>', date_start),('date_order','<=',date_end),('session_id.config_id','in',user_ids)])
            for pos in pos_ids:
                for pol in pos.lines:
                    if pol.discount:
                        total_discount += (pol.price_unit * pol.qty * (pol.discount) / 100.0)
                    if pol.product_id.name == 'Discount':
                       total_discount = total_discount + (pol.price_unit * -1) 
        return total_discount         
    
    
    def _get_sum_invoice_2(self, form):
        total_invoiced=0.000
        pos_obj = self.env['pos.order']
        user_obj = self.env['res.users']
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = pos_obj.search([('date_order','>', date_start),('date_order','<=',date_end),('session_id.config_id','in',user_ids)])
            for pos in pos_ids:
                if pos.account_move:
                    for pol in pos.account_move.invoice_line_ids:
                        total_invoiced += (pol.price_subtotal * pol.quantity * (1 - (pol.discount) / 100.0))
        return total_invoiced

   
    def _get_user_names(self, user_ids):
        user_obj = self.env['res.users'].search([])
        names=', '.join(map(lambda x: x.name, user_obj))
        return ', '.join(map(lambda x: x.name, user_obj))
    
   
    def get_payments(self, form):
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = self.env['res.users'].company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = self.env["pos.order"].search([('date_order','>',date_start),('date_order','<=',date_end),('state','in',['paid','invoiced','done']),('session_id.config_id','in',user_ids)])
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
     
   
    def _get_reurn_total(self, form):
        total_refund=0.00
        pos_obj = self.env['pos.order']
        user_obj = self.env['res.users']
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = pos_obj.search([('date_order','>', date_start),('date_order','<=',date_end),('session_id.config_id','in',user_ids)])
            for pos in pos_ids:
                for pol in pos.lines:
                    if pol.qty < 0:
                        total_refund += abs(pol.price_subtotal)
        return total_refund  
      
    
    def get_untax_payment(self, form):
        total_pay=0.00
        pos_obj = self.env['pos.order']
        user_obj = self.env['res.users']
        for dat in form:
            user_ids = dat['pos_config_ids'] or self._get_all_users()
            company_id = user_obj.company_id.id
            date_start, date_end = self._get_utc_time_range(dat)
            pos_ids = pos_obj.search([('date_order','>', date_start),('date_order','<=',date_end),('session_id.config_id','in',user_ids)])
            for pos in pos_ids:
                if pos.amount_total:
                    total_pay += abs(pos.amount_total-pos.amount_tax)
        return total_pay 

   
    def _get_user_names(self, user_ids):
        user_obj = self.env['res.users']
        return ', '.join(map(lambda x: x.name, user_obj.browse(user_ids)))

    def _get_report_values(self, docids,data=None):
        
        result =[]
        result2 =[]
        payment=[]
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id', []))
        data = dict(data or {})
        config_list = []
        results = self._pos_sales_details(data['form'])
        payment= self.get_payments(data['form'])
        invoice=self._get_sum_invoice_2(data['form'])
        refund=self._get_reurn_total(data['form'])
        disc = self.get_total_discount(data['form'])
        untax_payment = self.get_untax_payment(data['form'])
        
        lists=[]
        lists1=[]
        statements=[]
        out = []
        dic = {}
        result = results
        sum = 0
        user_all=[]
        for res in result:
            for key,value in res.items():
                lists.append(value)
                lists1.append(key)
                if key=='users_listtt':
                        for vals in value:
                            if not vals in user_all:
                                user_all.append(vals)
                dic=dict(zip(lists1,lists))
            statements.append(dic)
       
        name_list = []
        for statement in statements:
            if statement['customer']:
                name_list.append(statement['customer'])
        dup_list = []
#         for order in name_list:
#             if order not in dup_list:
#                 dup_list.append(order)
        
        user_obj = self.env['res.users'].search([])
        names=', '.join(map(lambda x: x.name, user_obj))
        
        
        docargs = {
               'doc_ids':self._ids,
               'doc_model': model,
               'docs': docs,
                'statement_data' :statements,
                'get_user_names' : self._get_user_names,
                'payment_data' : payment,
                'getsuminvoice2':invoice,
                'get_discount':disc,
                'refund_total':refund,
                'user_all':user_all,
                'total_payment_untaxed':untax_payment,
                'data': data['form'],
                'user_names':names if names else ' '
               }
        
        return docargs