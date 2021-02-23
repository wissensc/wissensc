# -*- coding: utf-8 -*-

from odoo import fields, models


class ExitOrderLine(models.Model):
   _name = 'scale.exit.orderline'
   _description = 'Linea de pedido de báscula de salida'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], 'Estado',
      default='draft', readonly=True)

   name = fields.Char('Nombre', readonly=True)

   order_id = fields.Many2one('scale.exit', 'Número de orden', readonly=True,
                              ondelete='cascade')
   rel_state = fields.Selection(string='Estado de orden', related='order_id.state', readonly=True)
   line_id = fields.Many2one('sale.order.line', 'Linea de orden', readonly=True)
   rel_line_id_id = fields.Integer(string='Id', related='line_id.id', readonly=True)

   unit_id = fields.Many2one('uom.uom', 'UdM', readonly=True,
                             ondelete='restrict')
   weight_order = fields.Float('Peso requerido', readonly=True)

   tare_weight = fields.Float('Peso tara', readonly=True)
   gross_weight = fields.Float('Peso bruto', readonly=True)
   net_weight = fields.Float('Peso neto', readonly=True, default="34.12")

   def action_test(self):
      self.net_weight = 300
      self.state = 'done'
