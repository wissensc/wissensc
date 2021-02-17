# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from datetime import datetime

STATES = {'draft': [('readonly', False)], 'sent': [('readonly', True)]}


class ScaleManoeuvre(models.Model):
   _name = 'scale.manoeuvre'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de maniobra'

   name = fields.Char('Folio', readonly=True, required=True,
                      copy=False, default='Nuevo', tracking=1)

   state = fields.Selection([('draft', 'Borrador'), ('sent', 'Enviado')],
                            'Estado',
                            readonly=True, copy=False, required=True,
                            index=True, tracking=3,
                            default='draft')

   type = fields.Selection([('exit', 'Salida')], 'Tipo', default='exit',
                           required=True, readonly=True)

   plant_id = fields.Many2one('lob', 'Línea de negocio', default=None, required=True,
                              domain="[('scale_exit','=',True)]",
                              states=STATES,
                              ondelete='restrict', tracking=True)

   vehicle_id = fields.Many2one('fleet.vehicle', 'Vehículo',
                                states=STATES,
                                required=True, tracking=True)
   rel_license_plate = fields.Char('Matrícula',
                                   related='vehicle_id.license_plate',
                                   readonly=True)

   driver_id = fields.Many2one('scale.driver', 'Chofer',
                               states=STATES,
                               domain="[('external', '=', False)]",
                               required=True, ondelete='restrict',
                               tracking=True)


   unit_id = fields.Many2one('uom.uom', 'Unidad de báscula',
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True)

   order_line_ids = fields.One2many('scale.manoeuvre.orderline', 'order_id',
                                    string='Lineas del pedido', states=STATES,
                                    copy=False)

   note = fields.Text('Nota')


   entrance_date = fields.Datetime('Hora y fecha de inicio',
                                   default=fields.Datetime.now,
                                   readonly=True)
   exit_date = fields.Datetime('Hora y fecha de salida', readonly=True)

   @api.depends('order_line_ids')
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
      result = super(ScaleManoeuvre, self).create(vals)
      return result

   def unlink(self):
      if self.state == 'sent':
         raise ValidationError(_('No se puede eliminar báscula enviada, existen movimientos'))
      return super(ScaleManoeuvre, self).unlink()

   def action_confirm(self):
      if not 'draft' in self.order_line_ids.mapped('state'):
         self.exit_date = datetime.now()
         self.state = 'sent'
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))
