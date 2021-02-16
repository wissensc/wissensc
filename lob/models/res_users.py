# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
   _inherit = 'res.users'

   business_line_ids = fields.Many2many('lob', string='Líneas de negocio permitidas')
   business_line_id = fields.Many2one('lob', 'Línea de negocio predeterminada')


   @api.constrains('business_line_id', 'business_line_ids')
   def _onchange_lob(self):
      if not any(line.id == self.business_line_id.id for line in self.business_line_ids):
         raise ValidationError("La línea de negocio predeterminada no se encuentra dentro de las permitidas")