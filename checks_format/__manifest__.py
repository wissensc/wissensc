# -*- coding: utf-8 -*-
{
    'name': "Formato de cheques",

    'summary': """Cheques format""",

    'description': """
    """,

    'author': "Wissen",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': ['base', 'payment'],

    'data': [
        'security/ir.model.access.csv',
        'report/checks_format_report.xml',
        'report/checks_format_report_template.xml',
        'views/checks_format_view.xml',
    ],

    'installable': True,
}
