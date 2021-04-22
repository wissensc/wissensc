# -*- coding: utf-8 -*-
{
    'name': "Cheque",

    'summary': """Check""",

    'description': """
    """,

    'author': "Wissen",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': ['base', 'account', 'l10n_mx_edi'],

    'data': [
        'report/check_report.xml',
        'report/banamex_template.xml',
        'report/bancomer_template.xml',
        'report/check_report_template.xml',
        'views/account_journal_view.xml',
        'views/account_payment_view.xml',
        'data/data.xml',
    ],

    'installable': True,
}
