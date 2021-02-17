# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
   _inherit = 'res.users'

   business_line_ids = fields.Many2many('lob',
                                        string='Líneas de negocio permitidas')
   business_line_id = fields.Many2one('lob', 'Línea de negocio predeterminada')

   @api.constrains('business_line_id', 'business_line_ids')
   def _onchange_lob(self):
      group_lob = self.env.ref('lob.group_lob', False)
      flag_lob = group_lob in self.groups_id
      for user in self:
         if user.business_line_id and user.business_line_ids:
            if not (user.business_line_id in user.business_line_ids):
               raise ValidationError(
                  "La línea de negocio predeterminada no se encuentra dentro de las permitidas")
            else:
               if flag_lob:
                  user.write({'groups_id': [(3, group_lob.id)]})
                  user.write({'groups_id': [(4, group_lob.id)]})
               else:
                  user.write({'groups_id': [(4, group_lob.id)]})
         else:
            user.write({'groups_id': [(3, group_lob.id)]})