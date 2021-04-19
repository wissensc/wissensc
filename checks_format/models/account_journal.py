# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountJournal(models.Model):
   _inherit = 'account.journal'

   check_payment_method_selected = fields.Boolean(compute='_compute_check_payment_method_selected',string="Pago en Cheque")
   check_format = fields.Selection([('cb','Citybanamex')], 'Formato de cheque', default=None)

   @api.depends('outbound_payment_method_ids')
   def _compute_check_payment_method_selected(self):
      for journal in self:
         journal.check_payment_method_selected = any(
            pm.code == 'check_format'
            for pm in journal.outbound_payment_method_ids
         )


