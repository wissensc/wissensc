# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    business_line = fields.Many2one('lob', 'Linea de negocio', tracking=True)
    rel_code = fields.Char('Serie', related='business_line.code',
                           readonly=True)

