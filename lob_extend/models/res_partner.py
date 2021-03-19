# -*- coding: utf-8 -*-

from odoo import fields, models, api


class RestPartner(models.Model):
   _inherit = 'res.partner'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)

   code = fields.Char('Código')
   legal_representative = fields.Char('Representante legal')

