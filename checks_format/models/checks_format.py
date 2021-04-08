# -*- coding: utf-8 -*-

from odoo import fields, models


class ChecksFormat(models.Model):
   _name = 'checks.format'
   _description = 'Formato de cheque'

   name = fields.Char('Nombre')

   date = fields.Date('Fecha')
   date_mtop = fields.Integer('Margen Top')
   date_mleft = fields.Integer('Margen left')
   date_lspaccing = fields.Integer('Espaciado')


