# -*- coding: utf-8 -*-

from odoo import fields, models


class Lob(models.Model):
   _name = 'lob'
   _description = 'Línea de negocio'

   name = fields.Char('Nombre', required=True)
   code = fields.Char('Código', required=True)
   logo = fields.Binary(attachment=True, copy=False)

   scale_entrance = fields.Boolean('Báscula de entrada', copy=False)
   scale_exit = fields.Boolean('Báscula de salida', copy=False)
   scale_manoeuvre = fields.Boolean('Maniobras', copy=False)

   entrance_seq_id = fields.Many2one('ir.sequence',
                                     'Secuencia de báscula de entrada', copy=False)
   exit_seq_id = fields.Many2one('ir.sequence',
                                 'Secuencia de báscula de sálida', copy=False)
   manoeuvre_seq_id = fields.Many2one('ir.sequence',
                                 'Secuencia de maniobras', copy=False)
