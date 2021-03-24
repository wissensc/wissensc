# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
   _inherit = 'sale.order'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self:self.env.user.business_line_id.id, tracking=True)
