# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class ScaleReporting(models.Model):
   _name = 'scale.reporting'
   _auto = False
   _description = 'Informe de entradas y salidas de bascula'

   order = fields.Char('Numero del pedido', readonly=True)
   folio = fields.Char('Folio', readonly=True)
   date_order = fields.Datetime('Fecha de orden', readonly=True)
   product = fields.Many2one('product.product', "Producto", readonly=True)
   license_plate = fields.Char('Matrícula', readonly=True)
   tare_weight = fields.Float('Peso tara', readonly=True)
   gross_weight = fields.Float('Peso bruto', readonly=True)
   net_weight = fields.Float('Peso neto', readonly=True)
   driver_id = fields.Many2one('scale.driver', 'Chofer', readonly=True)
   type = fields.Selection([('entrance', 'Entrada'), ('exit', 'Salida')], 'Tipo',
                           readonly=True)
   entrance_date = fields.Datetime('Fecha de entrada', readonly=True)
   exit_date = fields.Datetime('Fecha de salida', readonly=True)
   create_id = fields.Many2one('res.users', 'Creado por', readonly=True)
   note = fields.Text('Nota', readonly=True)

   def init(self):
      tools.drop_view_if_exists(self.env.cr, self._table)
      query = """
      CREATE OR REPLACE VIEW scale_reporting AS 
SELECT ROW_NUMBER() OVER(ORDER BY sp.date_order) AS id, * FROM (SELECT po.name AS "order", se.name AS folio, po.date_order AS date_order,  eo.name AS product, fv.license_plate AS license_plate,
eo.tare_weight AS tare_weight, eo.gross_weight AS gross_weight, eo.net_weight AS net_weight, se.driver_id AS driver_id, se.type AS "type",
se.entrance_date AS entrance_date, se.exit_date AS exit_date, eo.create_uid AS create_id, se.note AS note
	FROM scale_entrance_orderline eo 	
	INNER JOIN scale_entrance se ON eo.order_id = se.id
	INNER JOIN fleet_vehicle fv ON se.vehicle_id = fv.id
	INNER JOIN purchase_order po ON se.order_id = po.id WHERE se.state='sent'
UNION ALL
SELECT po.name AS "order", se.name AS folio, po.date_order AS date_order,  eo.name AS product, fv.license_plate AS license_plate,
eo.tare_weight AS tare_weight, eo.gross_weight AS gross_weight, eo.net_weight AS net_weight, se.driver_id AS driver_id, se.type AS "type",
se.entrance_date AS entrance_date, se.exit_date AS exit_date, eo.create_uid AS create_id, se.note AS note
	FROM scale_exit_orderline eo 	
	INNER JOIN scale_exit se ON eo.order_id = se.id
	INNER JOIN fleet_vehicle fv ON se.vehicle_id = fv.id
	INNER JOIN sale_order po ON se.order_id = po.id WHERE se.state='sent') AS sp;
      """
      self.env.cr.execute(query)
