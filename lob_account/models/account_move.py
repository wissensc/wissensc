# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
   _inherit = 'account.move'

   project_id = fields.Many2one('account.move.project', "Proyecto", ondelete="restrict")

   @api.onchange('partner_id')
   def _resetOrder(self):
      self.l10n_mx_edi_payment_method_id = self.partner_id.payment_method_id.id
      self.l10n_mx_edi_usage = self.partner_id.edi_usage