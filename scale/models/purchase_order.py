# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
   _inherit = 'purchase.order'

   scale = fields.Boolean('Báscula', default=False)