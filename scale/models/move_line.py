# -*- coding: utf-8 -*-

from odoo import fields, models


class MoveLine(models.Model):
   _inherit = 'stock.move.line'

   rel_weight_ok = fields.Boolean(
      related='product_id.product_tmpl_id.weight_ok', string="Es pesado", copy="False",
      readonly=True)

class StockMove(models.Model):
   _inherit = 'stock.move'

   rel_weight_ok = fields.Boolean(
      related='product_id.product_tmpl_id.weight_ok', string="Es pesado", copy="False",
      readonly=True)