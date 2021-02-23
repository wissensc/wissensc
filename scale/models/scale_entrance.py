# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from datetime import datetime

STATES = {'draft': [('readonly', False)], 'assigned': [('readonly', True)],
          'sent': [('readonly', True)]}


class ScaleEntrance(models.Model):
   _name = 'scale.entrance'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de entrada'

   name = fields.Char('Folio', readonly=True, required=True, default='/',
                      copy=False)

   state = fields.Selection(
      [('draft', 'Borrador'), ('assigned', 'Asignado'), ('sent', 'Enviado')],
      'Estado',
      readonly=True, required=True,
      index=True, tracking=1,
      default='draft')

   type = fields.Selection([('entrance', 'Entrada')], 'Tipo',
                           default='entrance',
                           required=True, readonly=True)

   lob_id = fields.Many2one('lob', 'Línea de negocio', default=None,
                            required=True,
                            domain="[('scale_entrance','=',True)]",
                            states=STATES,
                            ondelete='restrict')

   @api.onchange('lob_id')
   def _resetOrder(self):
      self.order_id = None
      self.order_line_ids = None

   order_id = fields.Many2one('purchase.order', 'Número de orden de compra',
                              states=STATES, required=True, ondelete='cascade',
                              domain="[('state', '=', 'purchase'),('business_line_id','=',lob_id),('scale_id','=',False)]")

   vehicle_id = fields.Many2one('fleet.vehicle', 'Vehículo',
                                states=STATES,
                                required=True)
   rel_license_plate = fields.Char('Matrícula',
                                   related='vehicle_id.license_plate',
                                   readonly=True)

   driver_id = fields.Many2one('scale.driver', 'Chofer',
                               states=STATES,
                               domain="[('external', '=', True)]",
                               required=True, ondelete='restrict')

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
                             states=STATES,
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True)
   rel_unit_name = fields.Char(related="unit_id.name", string='Unidad',
                               readonly=True)
   vehicle_weight = fields.Float('Peso del vehículo', readonly=True)

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

   @api.depends('order_line_ids.net_weight', 'order_id')
   def _compute_lines(self):
      for record in self:
         total = 0
         for line in record.order_line_ids:
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
      res = super(ScaleEntrance, self).create(vals)
      if res:
         self.env['purchase.order'].browse(res.order_id.id).write(
            {'scale_id': res.id})
      return res

   def write(self, vals):
      for record in self:
         if record.name == '/' and vals.get('state') == 'assigned':
            seq = record.env['ir.sequence']
            lob_id = vals.get('lob_id') or record.lob_id.id
            code = record.env['lob'].browse(lob_id).entrance_seq_id.code
            record.name = seq.next_by_code(code) or 'Nuevo'
      return super(ScaleEntrance, self).write(vals)

   def unlink(self):
      for record in self:
         if record.state == 'assigned':
            raise ValidationError(
               _('No es posible eliminar la báscula con peso inicial'))
         if record.state == 'sent':
            raise ValidationError(
               _('No se puede eliminar báscula enviada, existen movimientos'))
      return super(ScaleEntrance, self).unlink()

   def action_sent(self):
      self.ensure_one()
      if not 'draft' in self.order_line_ids.mapped('state'):
         self.exit_date = datetime.now()
         self.state = 'sent'

         # for line in self.env['purchase.order.line'].search(
         #       [('order_id', '=', self.order_id.id)]):
         #    line.qty_received = self.order_line_ids.filtered(
         #       lambda x: x.line_id.id == line.id).net_weight

         if self.order_id.picking_ids:
            print(self.order_id.picking_ids)
         # for line in self.env['purchase.order.line'].search(
         #       [('order_id', '=', self.order_id.id)]):
         #    line.qty_received = self.order_line_ids.filtered(
         #       lambda x: x.line_id.id == line.id).net_weight
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))

   def confirmation_init_weight(self):
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'scale.confirmation',
         'view_mode': 'form',
         'context': {'active_id': self.id, 'operation': 'purchase'},
         'target': 'new',
      }

   def init_weight(self):
      self.ensure_one()
      self.state = 'assigned'
      self.vehicle_weight = 2000.00
