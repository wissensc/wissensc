# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from datetime import datetime

STATES = {'draft': [('readonly', False)], 'sent': [('readonly', True)]}


class ScaleExit(models.Model):
   _name = 'scale.exit'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de salida'

   name = fields.Char('Folio', readonly=True, required=True,
                      copy=False, default='Nuevo', tracking=1)

   state = fields.Selection([('draft', 'Borrador'), ('sent', 'Enviado'),
                             ('cancel', 'Cancelado')], 'Estado',
                            readonly=True, copy=False, required=True,
                            index=True, tracking=3,
                            default='draft')

   type = fields.Char(default='Salida', required=True, readonly=True)

   plant_id = fields.Many2one('lob', 'Planta', default=None, required=True,
                              domain="[('scale_exit','=',True)]",
                              states=STATES,
                              ondelete='restrict', tracking=True)

   @api.onchange('plant_id')
   def _resetOrder(self):
      self.sale_order_id = None

   sale_order_id = fields.Many2one('sale.order', 'Pedido de venta',
                                   states=STATES,
                                   required=True, ondelete='cascade',
                                   domain="[('state', '=', 'sale'),('business_line','=',plant_id)]",
                                   tracking=2)

   vehicle_id = fields.Many2one('fleet.vehicle', 'Vehículo',
                                states=STATES,
                                required=True, tracking=True)
   rel_license_plate = fields.Char('Matrícula',
                                   related='vehicle_id.license_plate',
                                   readonly=True)

   driver_id = fields.Many2one('scale.driver', 'Chofer',
                               states=STATES,
                               required=True, ondelete='restrict',
                               tracking=True)

   rel_user = fields.Char('Comercial', related='sale_order_id.user_id.name',
                          readonly=True)
   rel_date_order = fields.Datetime('Fecha de pedido',
                                    related='sale_order_id.date_order',
                                    readonly=True)
   rel_customerId = fields.Integer('Cliente Id',
                                   related='sale_order_id.partner_id.id',
                                   readonly=True)
   rel_customer = fields.Char('Cliente',
                              related='sale_order_id.partner_id.name',
                              readonly=True)

   unit_id = fields.Many2one('uom.uom', 'Unidad de medida',
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True,
                             readonly=True)

   @api.onchange('sale_order_id')
   def _onchangelines(self):
      if self.sale_order_id:
         self.order_line_ids = None
         for line in self.env['sale.order.line'].search(
               [('order_id', '=', self.sale_order_id.id)]):
            dic = {'id_line': line.id, 'name': line.product_id.name,
                   'unit_id': line.product_uom,
                   'weight_order': line.product_uom_qty}
            print(dic)
            self.order_line_ids = [(0, 0, dic)]

   @api.constrains('sale_order_id', 'unit_id')
   def _onchangeuom(self):
      if self.sale_order_id:
         for line in self.env['sale.order.line'].search(
               [('order_id', '=', self.sale_order_id.id)]):
            if line.product_uom.id != self.unit_id.id:
               raise ValidationError(_(
                  'La unidad de medida "%s" %s no existe en todas las lineas del pedido %s') % (
                                        self.unit_id.name, self.unit_id,
                                        self.sale_order_id.name))

   order_line_ids = fields.One2many('scale.exit.orderline', 'order_id',
                                    string='Lineas del pedido', states=STATES)

   note = fields.Text('Nota')

   output_uid = fields.Char('Usuario', default=lambda x: x.env.user.name,
                            readonly=True)

   input_date = fields.Datetime('Hora y fecha de inicio',
                                default=fields.Datetime.now,
                                readonly=True)
   output_date = fields.Datetime('Hora y fecha de salida', readonly=True)

   @api.depends('order_line_ids', 'sale_order_id')
   def _compute_lines(self):
      total = 0
      for line in self.order_line_ids:
         total = total + line.net_weight
      self.total_weight = total

   total_weight = fields.Float('Peso neto total', compute=_compute_lines)

   @api.model
   def create(self, vals):
      if vals.get('name', 'Nuevo') == 'Nuevo':
         seq = self.env['ir.sequence']
         code = self.env['lob'].browse(vals['plant_id']).exit_seq_id.code
         vals['name'] = seq.next_by_code(code) or 'Nuevo'
      result = super(ScaleExit, self).create(vals)
      return result

   def action_confirm(self):
      if not 'draft' in self.order_line_ids.mapped('state'):
         self.output_date = datetime.now()
         self.state = 'sent'

         for line in self.env['sale.order.line'].search(
               [('order_id', '=', self.sale_order_id.id)]):
            line.qty_delivered = self.order_line_ids.filtered(
               lambda x: x.id_line == line.id).net_weight
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))
