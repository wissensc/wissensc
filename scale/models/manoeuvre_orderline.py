# -*- coding: utf-8 -*-

from odoo import fields, models


class ManoeuvreOrderLine(models.Model):
   _name = 'scale.manoeuvre.orderline'
   _description = 'Linea de pedido de báscula de maniobra'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], 'Estado',
      default='draft', readonly=True)

   name = fields.Char('Nombre')

   order_id = fields.Many2one('scale.manoeuvre', 'Número de orden',
                              ondelete='cascade')

   unit_id = fields.Many2one('uom.uom', 'Unidad de medida',
                             ondelete='restrict')
   weight_order = fields.Float('Peso requerido')

   tare_weight = fields.Float('Peso tara')
   gross_weight = fields.Float('Peso bruto')
   net_weight = fields.Float('Peso neto')

   def action_test(self):
      self.net_weight = 300
      self.state = 'done'
