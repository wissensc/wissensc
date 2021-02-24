# -*- coding: utf-8 -*-

from odoo import fields, models


class ExitOrderLine(models.Model):
   _name = 'scale.exit.orderline'
   _description = 'Linea de pedido de báscula de salida'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], 'Estado',
      default='draft', readonly=True)

   name = fields.Many2one('product.product', "Nombre", readonly=True)

   order_id = fields.Many2one('scale.exit', 'Número de orden', readonly=True,
                              ondelete='cascade')
   rel_state = fields.Selection(string='Estado de orden',
                                related='order_id.state', readonly=True)
   moveline_id = fields.Many2one('stock.move.line',
                                 "Linea de movimiento de stock",
                                 readonly=True)
   unit_id = fields.Many2one('uom.uom', 'UdM', readonly=True,
                             ondelete='restrict')
   weight_order = fields.Float('Peso requerido', readonly=True)

   tare_weight = fields.Float('Peso tara', readonly=True)
   gross_weight = fields.Float('Peso bruto', readonly=True)
   net_weight = fields.Float('Peso neto', readonly=True, default="34.12")

   def confirmation_weight(self):
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'exit.confirmation',
         'view_mode': 'form',
         'context': {'active_id': self.id},
         'target': 'new',
      }

   def action_weight(self):
      self.ensure_one()
      self.net_weight = 100.00;
      self.tare_weight = 200.00;
      self.gross_weight = 300.00;
      self.state = 'done'
