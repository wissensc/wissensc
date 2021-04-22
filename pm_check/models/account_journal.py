# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    check_payment_method_selected = fields.Boolean(
        compute='_compute_check_payment_method_selected',
        string="Pago en Cheque")
    check_type = fields.Selection([('bm', 'Banamex'), ('bc', 'Bancomer')],
                                  'Diseño de cheque', default=None)
    check_sequence_id = fields.Many2one('ir.sequence', 'Secuencia de cheque',
                                        copy=False)
    bank_reference = fields.Char('Referencia de banco', copy=False)

    @api.depends('outbound_payment_method_ids')
    def _compute_check_payment_method_selected(self):
        for journal in self:
            journal.check_payment_method_selected = any(
                pm.code == 'check'
                for pm in journal.outbound_payment_method_ids
            )
