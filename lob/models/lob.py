# -*- coding: utf-8 -*-

from odoo import fields, models


class Lob(models.Model):
    _name = 'lob'
    _description = 'Línea de negocio'


    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    image = fields.Binary(attachment=True)

    scale_entrance = fields.Boolean('Báscula de entrada')
    scale_exit = fields.Boolean('Báscula de salida')
    entrance_seq_id = fields.Many2one('ir.sequence', 'Secuencia de báscula de entrada')
    exit_seq_id = fields.Many2one('ir.sequence', 'Secuencia de báscula de sálida')
