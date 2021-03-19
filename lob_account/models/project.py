# -*- coding: utf-8 -*-

from odoo import fields, models


class Project(models.Model):
   _name = 'account.move.project'
   _description = 'Proyecto'

   name = fields.Char("Proyecto", required=True)
