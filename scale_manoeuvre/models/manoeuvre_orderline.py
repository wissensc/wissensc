# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError

import requests
import json
import logging
import datetime as dt

_logger = logging.getLogger(__name__)


class ManoeuvreOrderLine(models.Model):
   _name = 'scale.manoeuvre.orderline'
   _description = 'Linea de pedido de báscula de maniobra'

   state = fields.Selection(
      [('draft', 'Sin pesar'), ('done', 'Pesado')], "Estado",
      default='draft', readonly=True)

   name = fields.Char("Descripción", required=True)
   product_id = fields.Many2one('product.product', "Producto", readonly=True)

   order_id = fields.Many2one('scale.manoeuvre', "Número de orden",
                              ondelete='cascade')
   rel_state = fields.Selection(string="Estado de orden",
                                related='order_id.state', readonly=True)
   unit_id = fields.Many2one('uom.uom', "UdM",
                             ondelete='restrict',
                             required=True)
   tare_weight = fields.Float("Peso tara", digits='Product Unit of Measure')
   gross_weight = fields.Float("Peso bruto", digits='Product Unit of Measure')
   net_weight = fields.Float("Peso neto", digits='Product Unit of Measure')

   photo_url = fields.Char("URL", readonly=True)
   weight_date = fields.Datetime("Fecha de pesada", readonly=True)

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
         'location': 'Matrix',
         'secKey': 'M-' + str(self.id),
         'type': type.get('entrance')
      }
      return requests.post(url, data=json.dumps(params), headers=headers)

   def action_weight(self):
      self.ensure_one()
      response = self._request()
      data = response.json()
      _logger.info(data)

      if response.status_code == requests.codes.ok:
         if data.get('date'):
            date_obj = dt.datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S.%f')
            self.weight_date = date_obj
         self.net_weight = data.get('netWeight', 0.0)
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
