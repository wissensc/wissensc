# -*- coding: utf-8 -*-
{
   'name': "Báscula maniobras",

   'summary': """Báscula maniobras""",

   'description': """
        
    """,

   'author': "Wissen",
   'website': "http://www.yourcompany.com",

   'category': 'Uncategorized',
   'version': '14.0.1',

   'depends': ['scale'],

   'data': [
      'security/groups.xml',
      'security/ir.model.access.csv',
      'views/scale_manoeuvre_views.xml',
      'wizard/manoeuvre_init_confirmation_wizard.xml',
      'wizard/manoeuvre_weight_confirmation_wizard.xml',
   ],
   'installable': True,
   'application': True,
   'auto_install': False,
}
