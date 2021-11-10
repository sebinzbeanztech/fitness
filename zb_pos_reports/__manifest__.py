# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Reports',
    'author': "Zesty Beanz Technologies Pvt LTD",
    'website': "http://www.zbeanztech.com",
    'summary': 'POS Reports',
    'description': """
    	POS Reports 

	""",
    'version': '13.0.1.26',
    'depends': ['base','point_of_sale'],
    'data' : [
              
        'report/salesdetails_report.xml',
        'report/pos_receipt_report.xml',
        'report/pos_session_report.xml',
       # 'report/pos_invoice.xml',
        'report/periodic_sales_details_report.xml',
        'report/layouts.xml',
        'wizard/pos_details.xml',
        'wizard/wizard_periodic_report.xml',
        'views/report_details_view.xml',
        'views/res_company_view.xml',
        #'views/assets.xml',
        
     ],
    'test': [
    ],
    'demo': [
    ],
   
    'installable': True,
    'auto_install': False,
    'application': True,

}
