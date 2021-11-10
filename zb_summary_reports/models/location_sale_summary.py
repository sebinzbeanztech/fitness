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

class POSCompanySummary(models.Model):
    
    # Private attributes
    _name = "pos.company.analysis"
    _description = "Company Summary Analysis"
    _auto = False
    
    order_id    = fields.Many2one('pos.order', string="Point of Sale" , readonly=True)
    qty         = fields.Float('Quantity' , readonly=True)
    company_id  = fields.Many2one('res.company', string='Location', readonly=True)
    order_date  = fields.Datetime("Order Date", readonly=True)
    order       = fields.Char("Order")
    
    
    def init(self):
        """Initialize the sql view for the Category analysis """
         
        tools.drop_view_if_exists(self._cr, 'pos_company_analysis')
        self._cr.execute(""" CREATE VIEW pos_company_analysis AS (
            SELECT
                o.id::varchar as id,
                o.id as order_id,
                o.company_id as company_id,
                o.date_order as order_date,
                o.name as order,
                l.qty as qty

            FROM
                    "pos_order" o
                join
                    "pos_order_line" l
                on
                    (l.order_id = o.id)
        )""")





class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    
    stock_location_id = fields.Many2one('stock.location', string='Warehouse', readonly=True)
    