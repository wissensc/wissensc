# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPayment(models.Model):
   _inherit = 'account.payment'

   #rel_check_format = fields.Selection(string='Formato de Cheque', related='journal_id.check_format', readonly=True)





