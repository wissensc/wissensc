# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
   _inherit = 'account.move'

   project_id = fields.Many2one('account.move.project', "Proyecto",
                                ondelete="restrict")
   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)

   @api.onchange('partner_id')
   def _resetOrder(self):
      self.l10n_mx_edi_payment_method_id = self.partner_id.payment_method_id.id
      self.l10n_mx_edi_usage = self.partner_id.edi_usage

   @api.model
   def create(self, vals):
      res = super(AccountMove, self).create(vals)
      if vals.get('partner_id') and vals.get('invoice_origin'):
         partner_id = self.env['res.partner'].browse(vals.get('partner_id'))
         res.l10n_mx_edi_payment_method_id = partner_id.payment_method_id.id
         res.l10n_mx_edi_usage = partner_id.edi_usage
      return res
