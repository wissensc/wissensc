# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
   _inherit = 'product.template'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)
   weight_ok = fields.Boolean("Puede ser pesado", default=False)

   line_id = fields.Many2one('product.line', "Línea")
   classification_id = fields.Many2one('product.classification', "Clasificación")
   presentation_id = fields.Many2one('product.presentation', "Presentación")
   packing_id = fields.Many2one('product.packing', "Empaque")


class ProductLine(models.Model):
   _name = 'product.line'
   _description = 'Línea'

   active = fields.Boolean("Activo", default=True)
   name = fields.Char("Nombre", required=True)


class ProductClassification(models.Model):
   _name = 'product.classification'
   _description = 'Clasificación'

   active = fields.Boolean("Activo", default=True)
   name = fields.Char("Nombre", required=True)


class ProductPresentation(models.Model):
   _name = 'product.presentation'
   _description = 'Presentación'

   active = fields.Boolean("Activo", default=True)
   name = fields.Char("Nombre", required=True)


class ProductPacking(models.Model):
   _name = 'product.packing'
   _description = 'Empaque'

   active = fields.Boolean("Activo", default=True)
   name = fields.Char("Nombre", required=True)
