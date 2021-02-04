# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExitOrderLine(models.Model):
   _name = 'scale.exit.orderline'
   _description = 'Linea de pedido de báscula de salida'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], 'Estado',
      default='draft', readonly=True)

   name = fields.Char('Nombre', readonly=True)

   order_id = fields.Many2one('scale.exit', 'Número de orden', readonly=True, ondelete='cascade')
   id_line = fields.Integer('Id', readonly=True)
   unit_id = fields.Many2one('uom.uom', 'Unidad de medida', readonly=True, ondelete='restrict')
   weight_order = fields.Float('Peso requerido', readonly=True)

   tare_weight = fields.Float('Peso tara', readonly=True)
   gross_weight = fields.Float('Peso bruto', readonly=True)
   net_weight = fields.Float('Peso neto', readonly=True)

   def action_test(self):
      self.net_weight = 300
      self.state = 'done'
