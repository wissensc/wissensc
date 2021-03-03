# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

from datetime import datetime

import requests
import json
import logging

_logger = logging.getLogger(__name__)

STATES = {'draft': [('readonly', False)], 'assigned': [('readonly', True)],
          'sent': [('readonly', True)]}


class ScaleExit(models.Model):
   _name = 'scale.exit'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de salida'

   name = fields.Char('Folio', readonly=True, required=True,
                      copy=False, default='/')

   state = fields.Selection(
      [('draft', 'Borrador'), ('assigned', 'Asignado'), ('sent', 'Enviado')],
      'Estado',
      readonly=True, copy=False, required=True,
      index=True, tracking=1,
      default='draft')

   type = fields.Selection([('exit', 'Salida')], 'Tipo', default='exit',
                           required=True, readonly=True)

   lob_id = fields.Many2one('lob', 'Línea de negocio', default=None,
                            required=True,
                            domain="[('scale_exit','=',True)]",
                            states=STATES,
                            ondelete='restrict')

   @api.onchange('lob_id')
   def _resetOrder(self):
      self.order_id = None
      self.orderline_ids = None

   order_id = fields.Many2one('sale.order', 'Orden de venta',
                              states=STATES, copy=False,
                              required=True, ondelete='cascade',
                              domain="[('state', '=', 'sale'),('business_line_id','=',lob_id),('scale_id','=',False)]")

   vehicle_id = fields.Many2one('fleet.vehicle', 'Vehículo',
                                states=STATES,
                                required=True)
   rel_license_plate = fields.Char('Matrícula',
                                   related='vehicle_id.license_plate',
                                   readonly=True)

   driver_id = fields.Many2one('scale.driver', 'Chofer',
                               states=STATES,
                               domain="[('external', '=', False)]",
                               required=True, ondelete='restrict')

   rel_user = fields.Char('Comercial', related='order_id.user_id.name',
                          readonly=True)
   rel_date_order = fields.Datetime('Fecha de orden',
                                    related='order_id.date_order',
                                    readonly=True)
   rel_idpartner = fields.Integer('Cliente Id',
                                  related='order_id.partner_id.id',
                                  readonly=True)
   rel_partner = fields.Char('Cliente',
                             related='order_id.partner_id.name',
                             readonly=True)

   unit_id = fields.Many2one('uom.uom', 'Unidad de báscula',
                             states=STATES,
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True)
   rel_unit_name = fields.Char(related="unit_id.name", string='Unidad',
                               readonly=True)
   initial_weight = fields.Float('Peso Inicial', readonly=True)
   photo_url = fields.Char("URL", readonly=True, default='')
   reference = fields.Char('Referencia unica', readonly=True)

   @api.onchange('order_id')
   def _onchangelines(self):
      if self.order_id:
         self.orderline_ids = None
         picking_ids = self.order_id.picking_ids.filtered(
            lambda x: x.state == 'assigned').mapped('id')
         print(picking_ids)
         for moveline in self.env['stock.move.line'].search(
               [('picking_id', 'in', picking_ids)]):
            dic = {
               'moveline_id': moveline,
               'name': moveline.product_id.name,
               'product_id': moveline.product_id,
               'unit_id': moveline.product_uom_id,
               'weight_order': moveline.product_uom_qty
            }
            self.orderline_ids = [(0, 0, dic)]

   @api.constrains('order_id', 'unit_id')
   def _onchangeuom(self):
      for record in self:
         if record.orderline_ids:
            for moveline in record.orderline_ids:
               if moveline.unit_id != record.unit_id:
                  raise ValidationError(_(
                     'La unidad de medida "%s" %s no existe en todas las lineas del pedido %s') % (
                                           record.unit_id.name, record.unit_id,
                                           record.order_id.name))
         else:
            raise ValidationError(_(
               'No existen movimientos de stock validos para la orden %s') % (
                                     record.order_id.name))

   orderline_ids = fields.One2many('scale.exit.orderline', 'order_id',
                                   string='Lineas del pedido', states=STATES,
                                   copy=False)

   note = fields.Text('Nota')

   entrance_date = fields.Datetime('Hora y fecha de inicio',
                                   default=fields.Datetime.now,
                                   readonly=True)
   exit_date = fields.Datetime('Hora y fecha de salida', readonly=True)

   @api.depends('orderline_ids.net_weight', 'order_id')
   def _compute_lines(self):
      for record in self:
         total = 0
         for line in record.orderline_ids:
            total = total + line.net_weight
         # record.total_weight = total
         record.update({'total_weight': total})

   total_weight = fields.Float('Peso neto total', store=True,
                               compute=_compute_lines)

   def name_get(self):
      result = []
      for record in self:
         name = _(
            'Borrador (* Orden %s)' % record.order_id.name) if record.name == '/' else record.name
         result.append((record.id, name))
      return result

   @api.model
   def create(self, vals):
      res = super(ScaleExit, self).create(vals)
      if res:
         self.env['sale.order'].browse(res.order_id.id).write(
            {'scale_id': res.id})
         date = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'scale')]).write_date
         res.reference = date.strftime('M%d%m%y%H%M-') + str(res.id)
      return res

   def write(self, vals):
      for record in self:
         if record.name == '/' and vals.get('state') == 'assigned':
            seq = record.env['ir.sequence']
            lob_id = vals.get('lob_id') or record.lob_id.id
            code = record.env['lob'].browse(lob_id).exit_seq_id.code
            record.name = seq.next_by_code(code) or 'Nuevo'
      return super(ScaleExit, self).write(vals)

   def unlink(self):
      for record in self:
         if record.state == 'assigned':
            raise ValidationError(
               _('No es posible eliminar la báscula con peso inicial'))
         if record.state == 'sent':
            raise ValidationError(
               _('No se puede eliminar báscula enviada, existen movimientos'))
      return super(ScaleExit, self).unlink()

   def action_sent(self):
      self.ensure_one()

      if not 'draft' in self.orderline_ids.mapped('state'):
         stock = self.env['stock.move.line']

         for moveline in self.orderline_ids:
            id = moveline.moveline_id.id
            stock.browse(id).write({'qty_done': moveline.net_weight})
         self.exit_date = datetime.now()
         response = self._request('close')
         data = response.json()
         if response.status_code == requests.codes.ok:
            _logger.info(data)
            self.state = 'sent'
         else:
            raise UserError("%s" % json.dumps(data))
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))

   def confirmation_init(self):
      self.ensure_one()
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'exit.init.confirmation',
         'view_mode': 'form',
         'context': {'active_id': self.id},
         'target': 'new',
      }

   def _request(self, option='initial'):
      url = self.env.ref('scale.url_scale').sudo().value
      api_key = self.env.ref('scale.api_key_scale').sudo().value

      headers = {'content-type': 'application/json',
                 'x-api-key': api_key,
                 }
      lob = {
         'Planta Teotihuacán': 'Teotihuacan',
         'Planta Xalostoc': 'Teotihuacan',
         'Oficinas Xalostoc': 'Teotihuacan'
      }

      type = {'entrance': 'UNLOAD', 'exit': 'LOAD'}

      if option == 'close':
         params = {
            'key': self.reference
         }
         url = url + '/close'
         return requests.post(url, data=json.dumps(params), headers=headers)

      elif option == 'initial':
         params = {
            'key': self.reference,
            'location': lob.get(self.lob_id.name),
            'secKey': 'S-Peso Inicial',
            'type': type.get('exit')
         }
         return requests.put(url, data=json.dumps(params), headers=headers)

   def init_weight(self):
      self.ensure_one()
      response = self._request()
      data = response.json()
      _logger.info(data)

      if response.status_code == requests.codes.ok:
         self.initial_weight = data.get('grossWeight', 0.0)
         self.photo_url = data.get('photoUrl', '')
         self.state = 'assigned'
      else:
         raise UserError("%s" % json.dumps(data))
