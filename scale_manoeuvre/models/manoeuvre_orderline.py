# -*- coding: utf-8 -*-

from odoo import fields, models


class ManoeuvreOrderLine(models.Model):
   _name = 'scale.manoeuvre.orderline'
   _description = 'Linea de pedido de báscula de maniobra'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], "Estado",
      default='draft', readonly=True)

   name = fields.Char("Nombre", required=True)

   order_id = fields.Many2one('scale.manoeuvre', "Número de orden", ondelete='cascade')
   rel_state = fields.Selection(string="Estado de orden",
                                related='order_id.state', readonly=True)
   # moveline_id = fields.Many2one('stock.move.line',
   #                               "Linea de movimiento de stock",
   #                               readonly=True)

   unit_id = fields.Many2one('uom.uom', "UdM",
                             ondelete='restrict', required=True)
   weight_order = fields.Float("Peso requerido")

   tare_weight = fields.Float("Peso tara")
   gross_weight = fields.Float("Peso bruto")
   net_weight = fields.Float("Peso neto")

   lot_name = fields.Char("Número de lote")

   def confirmation_weight(self):
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'manoeuvre.weight.confirmation',
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

