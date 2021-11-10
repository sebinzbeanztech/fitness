# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 ZestyBeanz Technologies Pvt Ltd(<http://www.zbeanztech.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from odoo import tools
from odoo.addons import decimal_precision as dp
from datetime import datetime

class pos_order(models.Model):
    
    _inherit = "pos.order"
    
    @api.depends('date_order')
    def _get_order_date(self):
        date = ''
        for order in self:
            if order.date_order:
                date = datetime.strptime(str(order.date_order), "%Y-%m-%d %H:%M:%S")
                order.order_date = date
    
    order_date = fields.Date(string="Order Date", compute=_get_order_date, store=True)




class customer_sale_summary(models.Model):
    
    # Private attributes
    _name = "customer.sale.summary"
    _description = "Customer Sale Summary"
    _auto = False
    
    pos_id = fields.Many2one('pos.order', string="Point of Sale" , readonly=True)
    name = fields.Char('Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    
    
    def init(self):
        """Initialize the sql view for the Cashier analysis """
         
        tools.drop_view_if_exists(self._cr, 'customer_sale_summary')
        self._cr.execute(""" CREATE or REPLACE VIEW customer_sale_summary AS (
            SELECT
                o.id::varchar as id,
                o.id as pos_id,
                o.partner_id as partner_id,
                o.name as name

            FROM
                    "pos_order" o
        )""")


class user_sale_summary(models.Model):
    
    # Private attributes
    _name = "user.sale.summary"
    _description = "User Sale Summary"
    _auto = False
    
    pos_id = fields.Many2one('pos.order', string="Point of Sale" , readonly=True)
    name = fields.Char('Order', readonly=True)
    user_id = fields.Many2one('res.users', string='Cashier', readonly=True)
    
    
    def init(self):
        """Initialize the sql view for the Cashier analysis """
         
        tools.drop_view_if_exists(self._cr, 'user_sale_summary')
        self._cr.execute(""" CREATE or REPLACE VIEW user_sale_summary AS (
            SELECT
                o.id::varchar as id,
                o.id as pos_id,
                o.user_id as user_id,
                o.name as name

            FROM
                    "pos_order" o
        )""")


# class cashier_sale_summary(models.Model):
    
#     # Private attributes
#     _name = "cashier.sale.summary"
#     _description = "Cashier Sale Summary"
#     _auto = False
    
#     pos_id = fields.Many2one('pos.order', string="Point of Sale" , readonly=True)
#     name = fields.Char('Order', readonly=True)
#     user_id = fields.Many2one('res.users', string='Cashier', readonly=True)
    
    
#     def init(self):
#         """Initialize the sql view for the Cashier analysis """
         
#         tools.drop_view_if_exists(self._cr, 'cashier_sale_summary')
#         self._cr.execute(""" CREATE or REPLACE VIEW cashier_sale_summary AS (
#             SELECT
#                 o.id::varchar as id,
#                 o.id as pos_id,
#                 o.user_id as user_id,
#                 o.name as name

#             FROM
#                     "pos_order" o
#             WHERE o.user_type='cashier'
#         )""")


class pos_payment_analysis(models.Model):
    
    # Private attributes
    _name = "pos.payment.analysis"
    _description = "Payment Summary Analysis"
    _auto = False
    
    line_id    = fields.Many2one('account.bank.statement.line', string="Statement" , readonly=True)
#     journal_id = fields.Many2one('account.journal', string='Payment', readonly=True)

    company_id  = fields.Many2one('res.company' , string="Branch", readonly=True)
    amount     = fields.Float(string="Price", readonly=True,digits='Product Price')
#     order           = fields.Char("Order")
    date = fields.Date(string="Date",readonly=True)
    payment_method_id = fields.Many2one('pos.payment.method', string='Payment')
    
    def init(self):
        """Initialize the sql view for the modifier analysis """
        tools.drop_view_if_exists(self._cr, 'pos_payment_analysis')
        self._cr.execute(""" CREATE or REPLACE VIEW pos_payment_analysis AS (
            SELECT
                s.id::varchar as id,
                s.id as line_id,
                s.payment_method_id as payment_method_id,
                l.company_id as company_id,
                s.amount as amount  
                 
            FROM "pos_payment" s  INNER JOIN "pos_order" l ON s.pos_order_id = l.id
            
            WHERE pos_order_id IS NOT NULL
             
        )""")
         

