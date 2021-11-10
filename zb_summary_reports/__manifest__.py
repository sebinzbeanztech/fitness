# -*- coding: utf-8 -*-
{
    'name': 'ZB Summary reports',
    'version': '0.05',
    'category': '',
    'sequence': 1000,
    'description': """
    ZB Sales summary reports
======================================================================================================
    """,
    'author': 'Zesty Beanz',
    'website': 'http://www.zbeanztech.com',
    'depends': ['board','point_of_sale','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_summary_reports.xml',
        'views/product_sale_summary.xml',
        'views/location_sale_summary.xml',
        'views/income_dashboard.xml',
        'views/category_sale_summary.xml'
    ],
    'demo': [],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
