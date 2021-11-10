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

class pos_product_summary(models.Model):
    
    # Private attributes
    _name = "pos.product.summary"
    _description = "Product Summary Analysis"
    _auto = False
    
    line_id     = fields.Many2one('pos.order.line', string="Point of Sale" , readonly=True)
    qty         = fields.Float('Quantity' , readonly=True)
    product_id  = fields.Many2one('product.product', string='Product', readonly=True)
    price_unit  = fields.Float(string="Price", readonly=True, digits=dp.get_precision('Product Unit of Measure'))
    name        = fields.Char("Name", readonly=True)
    create_date = fields.Datetime("Order Date", readonly=True)
    company_id  = fields.Many2one('res.company' , string='Branch', readonly=True)
    
    
    def init(self):
        """Initialize the sql view for the product analysis """
        
        tools.drop_view_if_exists(self._cr, 'pos_product_summary')
        self._cr.execute(""" CREATE VIEW pos_product_summary AS (
            SELECT
                l.id::varchar as id,
                l.id as line_id,
                l.name as name,
                l.product_id as product_id,
                l.qty as qty,
                l.price_unit as price_unit,
                l.company_id as company_id,
                l.create_date as create_date
                
                
            FROM "pos_order_line" l
        )""")
