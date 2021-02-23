# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ScaleConfirmation(models.TransientModel):
    _name = 'scale.confirmation'
    _description = 'Asistente de confirmación'

    # scale_id = fields.Many2one('scale.entrance')
    text = fields.Text(default="¿Desea registrar el peso inicial?<br/>Una vez confirmada la operación no se puede revertir")

    def yes(self):
        active = self._context.get('active_id', False)
        operation = self._context.get('operation', False)
        if active and operation == 'purchase':
           self.env['scale.entrance'].browse(active).init_weight()
        elif active and operation == 'sale':
           self.env['scale.exit'].browse(active).init_weight()
        return True
