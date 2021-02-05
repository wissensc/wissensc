# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
   _inherit = 'sale.order'

   business_line = fields.Many2one('lob', 'Línea de negocio', tracking=True)
