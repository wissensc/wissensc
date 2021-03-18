# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitConfirmation(models.TransientModel):
   _name = 'manoeuvre.init.confirmation'
   _description = 'Asistente de confirmación de maniobra'

   text = fields.Text(
      default="¿Desea registrar el peso inicial?<br/>Una vez confirmada la operación no se puede revertir")

   def yes(self):
      active = self._context.get('active_id', False)
      operation = self._context.get('operation', False)
      if active:
         self.env['scale.manoeuvre'].browse(active).init_weight()
      return True
