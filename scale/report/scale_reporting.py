# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class ScaleReporting(models.Model):
   _name = 'scale.reporting'
   _auto = False
   _description = 'Informe de entradas y salidas de bascula'

   line_id = fields.Integer('Id de linea', readonly=True)
   order = fields.Char('Numero del pedido', readonly=True)
   folio = fields.Char('Folio', readonly=True)
   date_order = fields.Datetime('Fecha de orden', readonly=True)
   product = fields.Char('Producto', readonly=True)
   license_plate = fields.Char('Matrícula', readonly=True)
   tare_weight = fields.Float('Peso tara', readonly=True)
   gross_weight = fields.Float('Peso bruto', readonly=True)
   net_weight = fields.Float('Peso neto', readonly=True)
   driver = fields.Char('Chofer', readonly=True)
   type = fields.Selection([('ent', 'Entrada'), ('exit', 'Salida')], 'Tipo',
                           readonly=True)
   entrance_date = fields.Datetime('Fecha de entrada', readonly=True)
   exit_date = fields.Datetime('Fecha de salida', readonly=True)
   note = fields.Text('Nota', readonly=True)

   def init(self):
      tools.drop_view_if_exists(self.env.cr, self._table)
      query = """
CREATE OR REPLACE VIEW scale_reporting AS 
SELECT ROW_NUMBER() OVER(ORDER BY sp.date_order) AS id, * FROM (SELECT se.id AS line_id, po.name AS "order", se.name AS folio, po.date_order AS date_order,  eo.name AS product, fv.license_plate AS license_plate,
eo.tare_weight AS tare_weight, eo.gross_weight AS gross_weight, eo.net_weight AS net_weight, sd.name AS driver, se.type AS "type",
se.entrance_date AS entrance_date, se.exit_date AS exit_date, se.note AS note
	FROM scale_entrance_orderline eo 	
	INNER JOIN scale_entrance se ON eo.order_id = se.id
	INNER JOIN fleet_vehicle fv ON se.vehicle_id = fv.id
	INNER JOIN purchase_order po ON se.order_id = po.id
	INNER JOIN scale_driver sd ON se.driver_id = sd.id WHERE se.state='sent'
UNION ALL
SELECT se.id AS line_id, po.name AS "order", se.name AS folio, po.date_order AS date_order,  eo.name AS product, fv.license_plate AS license_plate,
eo.tare_weight AS tare_weight, eo.gross_weight AS gross_weight, eo.net_weight AS net_weight, sd.name AS driver, se.type AS "type",
se.entrance_date AS entrance_date, se.exit_date AS exit_date, se.note AS note
	FROM scale_exit_orderline eo 	
	INNER JOIN scale_exit se ON eo.order_id = se.id
	INNER JOIN fleet_vehicle fv ON se.vehicle_id = fv.id
	INNER JOIN sale_order po ON se.order_id = po.id
	INNER JOIN scale_driver sd ON se.driver_id = sd.id WHERE se.state='sent') AS sp;
      """
      self.env.cr.execute(query)
