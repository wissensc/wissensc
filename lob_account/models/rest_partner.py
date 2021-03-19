# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
   _inherit = 'res.partner'

   edi_usage = fields.Selection(
      selection=[
         ('G01', 'Adquisición de mercancías'),
         ('G02', 'Devoluciones, descuentos o bonificaciones'),
         ('G03', 'Gastos en general'),
         ('I01', 'Construcciones'),
         ('I02', 'Mobilario y equipo de oficina por inversiones'),
         ('I03', 'Equipo de transporte'),
         ('I04', 'Equipo de cómputo y accesorios'),
         ('I05', 'Dados, troqueles, moldes, matrices y herramental'),
         ('I06', 'Comunicaciones telefónicas'),
         ('I07', 'Comunicaciones satelitales'),
         ('I08', 'Otra maquinaria y equipo'),
         ('D01', 'Honorarios médicos, dentales y gastos hospitalarios'),
         ('D02', 'Gastos médicos por incapacidad o discapacidad'),
         ('D03', 'Gastos funerales'),
         ('D04', 'Donativos'),
         ('D05',
          'Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
         ('D06', 'Aportaciones voluntarias al SAR'),
         ('D07', 'Primas por seguros de gastos médicos'),
         ('D08', 'Gastos de transportación escolar obligatoria.'),
         ('D09',
          'Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
         ('D10', 'Pagos por servicios educativos (colegiaturas)'),
         ('P01', 'Por definir'),
      ],
      string="Uso",
      default='P01',
      help="Utilizado en CFDI 3.3 para indicar la clave del uso que le dará el receptor a esta factura. Este "
           "valor es definido por el cliente.\nNota: No es motivo de cancelación si la clave configurada no corresponde con el uso "
           "que le dará el receptor del documento.")

   payment_method_id = fields.Many2one(
      'l10n_mx_edi.payment.method',
      string="Forma de pago",
      help='Indica la forma en que se pagó o se pagará la factura, donde las opciones podrían ser: '
           'Tarjeta de Crédito, etc. Deje vacía si no conoce la forma de pago y el XML mostrará "No Identificado".',
      default=lambda self: self.env.ref('l10n_mx_edi.payment_method_otros',
                                        raise_if_not_found=False))