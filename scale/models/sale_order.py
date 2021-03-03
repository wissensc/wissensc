# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
   _inherit = 'sale.order'

   scale_id = fields.Many2one('scale.exit', 'Báscula', default=False, copy=False)
