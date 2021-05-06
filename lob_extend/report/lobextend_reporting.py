# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class LobextendReporting(models.Model):
   _name = 'lobextend.reporting'
   _auto = False
   _description = 'Informe pendiente de pago'

   currency_id = fields.Many2one('res.currency', readonly=True)
   business_line_id = fields.Many2one('lob', 'Línea de negocio', readonly=True)

   invoide_date = fields.Datetime('Fecha del CFDI', readonly=True)
   categ_id = fields.Many2one('product.category', "Referencia", readonly=True)
   serie = fields.Char('Serie', readonly=True)
   folio = fields.Char('Folio', readonly=True)
   partner_id = fields.Many2one('res.partner', 'Razón social', readonly=True)

   amount_untaxed = fields.Monetary("Neto", readonly=True)
   amount_tax = fields.Monetary("Impuesto", readonly=True)
   amount_total = fields.Monetary("Total", readonly=True)
   amount_residual = fields.Monetary("Adeudo", readonly=True)

   def init(self):
      tools.drop_view_if_exists(self.env.cr, self._table)
      query = """
CREATE OR REPLACE VIEW lobextend_reporting AS
SELECT ROW_NUMBER() OVER(ORDER BY t.move_id) AS id, * FROM (SELECT am.business_line_id AS business_line_id, am.id AS move_id, am.currency_id AS currency_id, am.invoice_date AS invoide_date, 
pt.categ_id AS categ_id, 
am.serie AS serie, am.folio AS folio, 
am.partner_id AS partner_id, am.amount_untaxed AS amount_untaxed, am.amount_tax AS amount_tax, am.amount_total AS amount_total, am.amount_residual AS amount_residual 
FROM account_move am
INNER JOIN account_move_line ml ON am.id = ml.move_id AND ml.exclude_from_invoice_tab = FALSE
INNER JOIN product_product pp ON ml.product_id = pp.id  
INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id  
WHERE am.move_type = 'in_invoice') AS t
      """
      self.env.cr.execute(query)
