# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
   _inherit = 'product.template'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)