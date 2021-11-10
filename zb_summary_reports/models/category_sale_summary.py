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
from datetime import datetime


class POSCategorySummary(models.Model):
    
    # Private attributes
    _name = "pos.category.analysis"
    _description = "Category Summary Analysis"
    _auto = False
    
    pos_id = fields.Many2one('pos.order.line', string="Point of Sale" , readonly=True)
    qty = fields.Float('Quantity' , readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    categ_id = fields.Many2one('product.category', string='Category', readonly=True)
    
#     pos_categ_id = fields.Many2one('pos.category', string='Category', readonly=True)
    create_date  = fields.Datetime("Order Date", readonly=True)
    
    
    def init(self):
        """Initialize the sql view for the Category analysis """
         
        tools.drop_view_if_exists(self._cr, 'pos_category_analysis')
        self._cr.execute(""" CREATE VIEW pos_category_analysis AS (
            SELECT
                l.id::varchar as id,
                l.id as pos_id,
                l.product_id as product_id,
                l.qty as qty,
                l.create_date as create_date,
                p.product_tmpl_id,
                pt.categ_id as categ_id
                

            FROM
                    "pos_order_line" l
                LEFT JOIN product_product p ON (l.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
            GROUP BY pt.categ_id,p.product_tmpl_id, l.id
        )""")

