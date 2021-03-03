# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
   _inherit = 'purchase.order'

   scale_id = fields.Many2one('scale.entrance', 'Báscula', default=False, copy=False)
