# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from datetime import datetime

STATES = {'draft': [('readonly', False)], 'sent': [('readonly', True)]}


class ScaleEntrance(models.Model):
   _name = 'scale.entrance'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de entrada'

   name = fields.Char('Folio', readonly=True, required=True,
                      copy=False, default='Nuevo', tracking=1)

   state = fields.Selection([('draft', 'Borrador'), ('sent', 'Enviado')],
                            'Estado',
                            readonly=True, copy=False, required=True,
                            index=True, tracking=3,
                            default='draft')

   type = fields.Selection([('ent', 'Entrada')], 'Tipo', default='ent',
                           required=True, readonly=True)

   plant_id = fields.Many2one('lob', 'Línea de negocio', default=None, required=True,
                              domain="[('scale_entrance','=',True)]",
                              states=STATES,
                              ondelete='restrict', tracking=True)

   @api.onchange('plant_id')
   def _resetOrder(self):
      self.order_id = None
      self.order_line_ids = None

   order_id = fields.Many2one('purchase.order', 'Número de orden de compra',
                              states=STATES, copy=False,
                              required=True, ondelete='cascade',
                              domain="[('state', '=', 'purchase'),('business_line_id','=',plant_id)]",
                              tracking=2)

   vehicle_id = fields.Many2one('fleet.vehicle', 'Vehículo',
                                states=STATES,
                                required=True, tracking=True)
   rel_license_plate = fields.Char('Matrícula',
                                   related='vehicle_id.license_plate',
                                   readonly=True)

   driver_id = fields.Many2one('scale.driver', 'Chofer',
                               states=STATES,
                               domain="[('external', '=', True)]",
                               required=True, ondelete='restrict',
                               tracking=True)

   rel_user = fields.Char('Comercial', related='order_id.user_id.name',
                          readonly=True)
   rel_date_order = fields.Datetime('Fecha de orden',
                                    related='order_id.date_order',
                                    readonly=True)
   rel_idpartner = fields.Integer('Proveedor Id',
                                  related='order_id.partner_id.id',
                                  readonly=True)
   rel_partner = fields.Char('Proveedor',
                             related='order_id.partner_id.name',
                             readonly=True)

   unit_id = fields.Many2one('uom.uom', 'Unidad de báscula',
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True)

   @api.onchange('order_id')
   def _onchangelines(self):
      if self.order_id:
         self.order_line_ids = None
         for line in self.env['purchase.order.line'].search(
               [('order_id', '=', self.order_id.id),
                ('display_type', '=', False)]):
            dic = {'line_id': line.id, 'name': line.product_id.name,
                   'unit_id': line.product_uom,
                   'weight_order': line.product_uom_qty}
            self.order_line_ids = [(0, 0, dic)]

   @api.constrains('order_id', 'unit_id')
   def _onchangeuom(self):
      if self.order_id:
         for line in self.env['purchase.order.line'].search(
               [('order_id', '=', self.order_id.id),
                ('display_type', '=', False)]):
            if line.product_uom.id != self.unit_id.id:
               raise ValidationError(_(
                  'La unidad de medida "%s" %s no existe en todas las lineas del pedido %s') % (
                                        self.unit_id.name, self.unit_id,
                                        self.order_id.name))

   order_line_ids = fields.One2many('scale.entrance.orderline', 'order_id',
                                    string='Lineas del pedido',
                                    states=STATES, copy=False)

   note = fields.Text('Nota')

   entrance_date = fields.Datetime('Hora y fecha de inicio',
                                   default=fields.Datetime.now,
                                   readonly=True)
   exit_date = fields.Datetime('Hora y fecha de salida', readonly=True)


   @api.depends('order_line_ids', 'order_id')
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
         code = self.env['lob'].browse(vals['plant_id']).entrance_seq_id.code
         vals['name'] = seq.next_by_code(code) or 'Nuevo'
      result = super(ScaleEntrance, self).create(vals)
      return result

   def unlink(self):
      if self.state == 'sent':
         raise ValidationError(_('No se puede eliminar báscula enviada, existen movimientos'))
      return super(ScaleEntrance, self).unlink()

   def action_confirm(self):
      if not 'draft' in self.order_line_ids.mapped('state'):
         self.exit_date = datetime.now()
         self.state = 'sent'

         for line in self.env['purchase.order.line'].search(
               [('order_id', '=', self.order_id.id)]):
            line.qty_received = self.order_line_ids.filtered(
               lambda x: x.line_id.id == line.id).net_weight
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))
