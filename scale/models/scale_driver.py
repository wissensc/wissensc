# -*- coding: utf-8 -*-

from odoo import fields, models


class ScaleDriver(models.Model):
   _name = 'scale.driver'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Chofer de camión'

   name = fields.Char('Nombre', required=True, tracking=1)
   license = fields.Char('Licencia', tracking=2)
   external = fields.Boolean('Externo', tracking=3)
