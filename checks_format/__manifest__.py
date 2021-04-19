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

    'depends': ['base', 'account', 'l10n_mx_edi'],

    'data': [
        #'security/ir.model.access.csv',
        'report/checks_format_report.xml',
        'report/citibanamex_template.xml',
        'report/checks_format_report_template.xml',
        'views/account_journal_view.xml',
        'views/account_payment_view.xml',
        'data/data.xml',
    ],

    'installable': True,
}
