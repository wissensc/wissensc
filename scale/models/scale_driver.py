# -*- coding: utf-8 -*-

from odoo import fields, models


class ScaleDriver(models.Model):
   _name = 'scale.driver'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Chofer de camión'

   name = fields.Char('Nombre', required=True, tracking=1)
   photo = fields.Binary(attachment=True, copy=False)
   license = fields.Char('Licencia', copy=False, tracking=2)
   external = fields.Boolean('Externo', tracking=3)

   _sql_constraints = [
      ('license_uniq', 'unique (license)', 'Licencia usada por otro chofer')
   ]
