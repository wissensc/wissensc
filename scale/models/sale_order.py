# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
   _inherit = 'sale.order'

   scale_id = fields.Many2one('scale.exit', 'Báscula', default=False, copy=False)

   valid_count = fields.Integer('Transferencias pendientes',
                                   compute='_compute_validate_count',
                                   store=True)

   @api.depends('picking_ids.state')
   def _compute_validate_count(self):
      for r in self:
         r.update({'valid_count': len(
            r.picking_ids.filtered(lambda x: x.state == 'assigned'))})
