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

    'depends': ['base', 'account'],

    'data': [
        #'security/ir.model.access.csv',
        'report/checks_format_report.xml',
        'report/checks_format_report_template.xml',
        'views/account_journal_view.xml',
        'views/account_payment_view.xml',
    ],

    'installable': True,
}
