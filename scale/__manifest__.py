# -*- coding: utf-8 -*-
{
    'name': "Báscula",

    'summary': """Báscula""",

    'description': """
        
    """,

    'author': "Wissen",
    'website': "http://www.yourcompany.com",


    'category': 'Báscula',
    'version': '14.0.1',

    'depends': ['sale_management', 'purchase', 'fleet', 'contacts', 'lob_extend'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'report/scale_report.xml',
        'report/scale_report_template.xml',
        'views/scale_exit_views.xml',
        'views/scale_driver_views.xml',
        'views/scale_exit_orderline_views.xml',
        #'wizard/bascule_exit_register_view.xml'
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #    'demo.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
