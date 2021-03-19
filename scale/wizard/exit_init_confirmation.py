# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitConfirmation(models.TransientModel):
   _name = 'exit.init.confirmation'
   _description = 'Asistente de confirmación de salida'

   text = fields.Text(
      default="¿Desea registrar el peso inicial?<br/>Una vez confirmada la operación no se puede revertir")

   def yes(self):
      active = self._context.get('active_id', False)
      if active:
         self.env['scale.exit'].browse(active).init_weight()

      return True
