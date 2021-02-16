# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
   _inherit = 'sale.order'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', tracking=True)
