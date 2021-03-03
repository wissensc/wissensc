# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError

import requests
import json
import logging

_logger = logging.getLogger(__name__)


class ManoeuvreOrderLine(models.Model):
   _name = 'scale.manoeuvre.orderline'
   _description = 'Linea de pedido de báscula de maniobra'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], "Estado",
      default='draft', readonly=True)

   name = fields.Char("Nombre", required=True)
   product_id = fields.Many2one('product.product', "Producto", readonly=True)

   order_id = fields.Many2one('scale.manoeuvre', "Número de orden",
                              ondelete='cascade')
   rel_state = fields.Selection(string="Estado de orden",
                                related='order_id.state', readonly=True)
   # moveline_id = fields.Many2one('stock.move.line',
   #                               "Linea de movimiento de stock",
   #                               readonly=True)

   unit_id = fields.Many2one('uom.uom', "UdM",
                             ondelete='restrict',
                             required=True)
   weight_order = fields.Float("Peso requerido")

   tare_weight = fields.Float("Peso tara")
   gross_weight = fields.Float("Peso bruto")
   net_weight = fields.Float("Peso neto")

   photo_url = fields.Char("URL", readonly=True, default='')

   def confirmation_weight(self):
      self.ensure_one()
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'manoeuvre.weight.confirmation',
         'view_mode': 'form',
         'context': {'active_id': self.id},
         'target': 'new',
      }

   def _request(self):
      url = self.env.ref('scale.url_scale').sudo().value
      api_key = self.env.ref('scale.api_key_scale').sudo().value

      headers = {'content-type': 'application/json',
                 'x-api-key': api_key,
                 }

      type = {'entrance': 'UNLOAD', 'exit': 'LOAD'}

      params = {
         'key': self.order_id.reference,
         'location': 'Teotihuacan',
         'secKey': 'M-' + str(self.id),
         'type': type.get('entrance')
      }
      print(params)

      return requests.post(url, data=json.dumps(params), headers=headers)

   def action_weight(self):
      self.ensure_one()
      response = self._request()
      data = response.json()
      _logger.info(data)

      if response.status_code == requests.codes.ok:
         self.net_weight = data.get('netWeight', 0.0) if data.get('netWeight',
                                                                  0.0) > 0 else data.get(
            'netWeight', 0.0) * - 1
         self.gross_weight = data.get('grossWeight', 0.0)
         self.tare_weight = data.get('tareWeight', 0.0)
         self.photo_url = data.get('photoUrl', '')
         self.state = 'done'
      else:
         raise UserError("%s" % json.dumps(data))

   def action_url(self):
      self.ensure_one()
      return {
         "type": "ir.actions.act_url",
         "url": self.photo_url,
         "target": "new"
      }
