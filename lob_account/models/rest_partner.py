# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
   _inherit = 'res.partner'

   edi_usage = fields.Selection(
      selection=[
         ('G01', 'Acquisition of merchandise'),
         ('G02', 'Returns, discounts or bonuses'),
         ('G03', 'General expenses'),
         ('I01', 'Constructions'),
         ('I02', 'Office furniture and equipment investment'),
         ('I03', 'Transportation equipment'),
         ('I04', 'Computer equipment and accessories'),
         ('I05', 'Dices, dies, molds, matrices and tooling'),
         ('I06', 'Telephone communications'),
         ('I07', 'Satellite communications'),
         ('I08', 'Other machinery and equipment'),
         ('D01', 'Medical, dental and hospital expenses.'),
         ('D02', 'Medical expenses for disability'),
         ('D03', 'Funeral expenses'),
         ('D04', 'Donations'),
         ('D05',
          'Real interest effectively paid for mortgage loans (room house)'),
         ('D06', 'Voluntary contributions to SAR'),
         ('D07', 'Medical insurance premiums'),
         ('D08', 'Mandatory School Transportation Expenses'),
         ('D09',
          'Deposits in savings accounts, premiums based on pension plans.'),
         ('D10', 'Payments for educational services (Colegiatura)'),
         ('P01', 'To define'),
      ],
      string="Usage",
      default='P01',
      help="Used in CFDI 3.3 to express the key to the usage that will gives the receiver to this invoice. This "
           "value is defined by the customer.\nNote: It is not cause for cancellation if the key set is not the usage "
           "that will give the receiver of the document.")

   payment_method_id = fields.Many2one(
      'l10n_mx_edi.payment.method',
      string="Payment Way",
      help="Indicates the way the invoice was/will be paid, where the options could be: "
           "Cash, Nominal Check, Credit Card, etc. Leave empty if unkown and the XML will show 'Unidentified'.",
      default=lambda self: self.env.ref('l10n_mx_edi.payment_method_otros',
                                        raise_if_not_found=False))