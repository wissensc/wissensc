# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitConfirmation(models.TransientModel):
   _name = 'entrance.init.confirmation'
   _description = 'Asistente de confirmación de entrada'

   text = fields.Text(
      default="¿Desea registrar el peso inicial?<br/>Una vez confirmada la operación no se puede revertir")

   def yes(self):
      active = self._context.get('active_id', False)
      if active:
         self.env['scale.entrance'].browse(active).init_weight()

      return True
