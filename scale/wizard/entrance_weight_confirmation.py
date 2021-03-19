# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeightConfirmation(models.TransientModel):
   _name = 'entrance.weight.confirmation'
   _description = 'Asistente de confirmación de pesada'

   lot_name = fields.Char("Número de lote")
   text = fields.Text(
      default="Una vez confirmada la pesada no podra revertirse")

   def yes(self):
      active = self._context.get('active_id', False)
      moveline = self.env['scale.entrance.orderline'].browse(active)
      if self.lot_name:
         moveline.lot_name = self.lot_name
      moveline.action_weight()
      return True
