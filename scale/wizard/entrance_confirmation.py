# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EntranceConfirmation(models.TransientModel):
   _name = 'entrance.confirmation'
   _description = 'Asistente de confirmación de entrada'

   lot_name = fields.Char("Número de lote")

   def yes(self):
      active = self._context.get('active_id', False)
      moveline = self.env['scale.entrance.orderline'].browse(active)
      if self.lot_name:
         moveline.lot_name = self.lot_name
      moveline.action_weight()
      return True
