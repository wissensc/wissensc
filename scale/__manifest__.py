# -*- coding: utf-8 -*-
{
   'name': "Báscula",

   'summary': """Báscula""",

   'description': """
        
    """,

   'author': "Wissen",
   'website': "http://www.yourcompany.com",

   'category': 'Scale',
   'version': '14.0.1',

   'depends': ['sale_management', 'purchase', 'fleet', 'stock', 'contacts',
               'lob_extend'],

   'data': [
      'security/groups.xml',
      'security/ir.model.access.csv',
      'report/scale_report.xml',
      'report/scale_entrance_report_template.xml',
      'report/scale_exit_report_template.xml',
      'views/scale_entrance_views.xml',
      'views/scale_exit_views.xml',
      'views/scale_driver_views.xml',
      'views/move_line_view.xml',
      'wizard/scale_confirmation_wizard.xml',
      'wizard/entrance_confirmation_wizard.xml',
      'wizard/exit_confirmation_wizard.xml',
   ],
   'installable': True,
   'application': True,
   'auto_install': False,
}
