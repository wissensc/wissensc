# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournal(models.Model):
   _inherit = 'account.journal'

   check_select = fields.Selection([('cb','Citybanamex')], 'Cheque', default=None)


