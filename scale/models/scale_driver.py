# -*- coding: utf-8 -*-

from odoo import fields, models


class ScaleDriver(models.Model):
   _name = 'scale.driver'
   _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
   _description = 'Chofer de camión'

   name = fields.Char('Nombre', required=True, tracking=1)

   license = fields.Char('Licencia', copy=False)
   external = fields.Boolean('Externo')

   _sql_constraints = [
      ('license_uniq', 'unique (license)', 'Licencia usada por otro chofer')
   ]
