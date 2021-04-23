# -*- coding: utf-8 -*-

from odoo import fields, models


class StockMove(models.Model):
   _inherit = 'stock.move'

   percentage_error = fields.Float('Error en %', digits='Product Unit of Measure')
   weight_error = fields.Float('Error en peso', digits='Product Unit of Measure')

