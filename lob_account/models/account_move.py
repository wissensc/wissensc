# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
   _inherit = 'account.move'

   project_id = fields.Many2one('account.move.project', "Proyecto", ondelete="restrict")
