# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    concept = fields.Text('Concepto', copy=False)
    check_number = fields.Char('Numero de cheque', readonly=True, copy=False)

    def print_check(self):
        self.ensure_one()
        seq = self.env['ir.sequence']
        code = self.journal_id.check_sequence_id.code
        if code and not self.check_number:
            self.check_number = seq.next_by_code(code)
        self.write({'is_move_sent': True})
        return self.env.ref('pm_check.check_report').report_action(self)
