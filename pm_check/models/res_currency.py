# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, tools, _

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text2(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount

        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = parts[2] or '0'

        lang = tools.get_lang(self.env)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word=self.currency_unit_label,
        )
        if not self.is_zero(amount - integer_value):
            longitud = len(fractional_value)
            if longitud == 1:
                fractional_value = fractional_value + '0'
            if longitud > 2:
                fractional_value = fractional_value[0:2]
            amount_words += ' {0}/100'.format(fractional_value)
        else:
            amount_words += ' 00/100'

        return amount_words
