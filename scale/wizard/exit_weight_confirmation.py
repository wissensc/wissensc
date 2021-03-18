# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeightConfirmation(models.TransientModel):
   _name = 'exit.weight.confirmation'
   _description = 'Asistente de confirmación de pesada'

   text = fields.Text(
      default="Una vez confirmada la pesada no podra revertirse")

   def yes(self):
      active = self._context.get('active_id', False)
      self.text = "Una vez confirmada la pesada no podra revertirse"
      self.env['scale.exit.orderline'].browse(active).action_weight()

      return True
