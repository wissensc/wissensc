# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DocumentWizard(models.TransientModel):
   _name = 'document.wizard'
   _description = 'Asistente de confirmación de documento'

   move_id = fields.Many2one('account.move', string="Asiento", required=True,
                             default=lambda self: self.env.context.get('active_id', None), readonly=True)
   rel_move_id = fields.Integer(related="move_id.id", string="Id movimiento")
   edi_format_id = fields.Many2one('account.edi.format', string="Formato EDI",
                                   required=True,
                                   default=lambda self: self.env.ref(
                                      'l10n_mx_edi.edi_cfdi_3_3').id)

   attachment_id = fields.Many2one('ir.attachment', string="Adjunto",
                                   domain="[('res_model', '=', 'account.move'),('res_id', '=', rel_move_id),('mimetype','like','xml')]")
   state = fields.Selection(
      [('to_send', 'Por enviar'), ('sent', 'Enviado'),
       ('to_cancel', 'Cancelar'),
       ('cancelled', 'Cancelado')], default='sent', string='Estado')
   error = fields.Text('Error')

   def yes(self):
      if self.attachment_id:
         self.attachment_id.write(
            {'index_content': 'application', 'mimetype': 'application/xml'})
      self.env['account.edi.document'].create({
         'move_id': self.move_id.id,
         'edi_format_id': self.edi_format_id.id,
         'state': self.state,
         'attachment_id': self.attachment_id.id
      })
