# -*- coding: utf-8 -*-
{
   'name': "Báscula Informes",

   'summary': """Informes de báscula""",

   'description': """
        
    """,

   'author': "Wissen",
   'website': "http://www.yourcompany.com",

   'category': 'Báscula',
   'version': '14.0.1',

   'depends': ['scale'],

   'data': [
      'security/ir.model.access.csv',
      'report/scale_reporting_views.xml',
   ],
   'installable': True,
   'application': False,
   'auto_install': False,
}
