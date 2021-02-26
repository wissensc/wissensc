# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from datetime import datetime

STATES = {'draft': [('readonly', False)], 'assigned': [('readonly', True)],
          'sent': [('readonly', True)]}

class ScaleManoeuvre(models.Model):
   _name = 'scale.manoeuvre'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Folio de pesada de maniobra'

   name = fields.Char('Folio', readonly=True, required=True, default='/',
                      copy=False)

   state = fields.Selection(
      [('draft', 'Borrador'), ('assigned', 'Asignado'), ('sent', 'Confirmado')],
      'Estado',
      readonly=True, required=True,
      index=True, tracking=1,
      default='draft')

   type = fields.Selection([('manoeuvre', 'Maniobra')], 'Tipo',
                           default='manoeuvre',
                           required=True, readonly=True)

   lob_id = fields.Many2one('lob', 'Línea de negocio', default=None,
                            required=True,
                            domain="[('scale_manoeuvre','=',True)]",
                            states=STATES,
                            ondelete='restrict')

   @api.onchange('lob_id')
   def _resetOrder(self):
      self.orderline_ids = None



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



   unit_id = fields.Many2one('uom.uom', 'Unidad de báscula',
                             states=STATES,
                             default=lambda x: x.env.ref(
                                'uom.product_uom_kgm').id, ondelete='restrict',
                             required=True)
   rel_unit_name = fields.Char(related="unit_id.name", string='Unidad',
                               readonly=True)
   vehicle_weight = fields.Float('Peso del vehículo', readonly=True)



   @api.constrains('unit_id')
   def _onchangeuom(self):
      for record in self:
         if record.orderline_ids:
            for moveline in record.orderline_ids:
               if moveline.unit_id != record.unit_id:
                  raise ValidationError(_(
                     'La unidad de medida "%s" %s no existe en todas las lineas de la báscula') % (
                                           record.unit_id.name, record.unit_id,))

   orderline_ids = fields.One2many('scale.manoeuvre.orderline', 'order_id',
                                   string='Lineas de la báscula',
                                   states=STATES, copy=False)

   note = fields.Text('Nota')

   entrance_date = fields.Datetime('Hora y fecha de inicio',
                                   default=fields.Datetime.now,
                                   readonly=True)
   exit_date = fields.Datetime('Hora y fecha de salida', readonly=True)

   @api.depends('orderline_ids.net_weight')
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
            'Borrador (* %s)' % record.id) if record.name == '/' else record.name
         result.append((record.id, name))
      return result

   def write(self, vals):
      for record in self:
         if record.name == '/' and vals.get('state') == 'assigned':
            seq = record.env['ir.sequence']
            lob_id = vals.get('lob_id') or record.lob_id.id
            code = record.env['lob'].browse(lob_id).manoeuvre_seq_id.code
            record.name = seq.next_by_code(code) or 'Nuevo'
      return super(ScaleManoeuvre, self).write(vals)

   def unlink(self):
      for record in self:
         if record.state == 'assigned':
            raise ValidationError(
               _('No es posible eliminar la báscula con peso inicial'))
         if record.state == 'sent':
            raise ValidationError(
               _('No se puede eliminar báscula confirmada, existen movimientos'))
      return super(ScaleManoeuvre, self).unlink()

   def action_confirm(self):
      self.ensure_one()
      if not 'draft' in self.orderline_ids.mapped('state'):
         self.state = 'sent'
      else:
         raise ValidationError(_('Faltan pesadas de realizar'))

   def confirmation_init(self):
      return {
         'name': 'Confirmación',
         'type': 'ir.actions.act_window',
         'res_model': 'manoeuvre.init.confirmation',
         'view_mode': 'form',
         'context': {'active_id': self.id},
         'target': 'new',
      }

   def init_weight(self):
      self.ensure_one()
      self.state = 'assigned'
      self.vehicle_weight = 2000.00

