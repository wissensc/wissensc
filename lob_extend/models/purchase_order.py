# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
   _inherit = 'purchase.order'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', tracking=True)
