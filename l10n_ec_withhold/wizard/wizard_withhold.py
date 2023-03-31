from odoo import models, fields, api
from odoo.exceptions import UserError

class WizarWithhold(models.TransientModel):
    _name = 'l10n_ec.wizard.create.sale.withhold'


    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        readonly=True,
        index=True,
        auto_join=True,
        tracking=True,
        store=True
    )

    issue_date = fields.Date(string="Fecha de retencion", readonly=False, required=True, tracking=True, store=True)

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        readonly=False,
        string="Diario",
        store=True
    )

    document_number = fields.Char(
        string="Numero de Retencion",
        required=True,
        readonly=False,
        tracking=True,
        size=17,
        store=True
    )

    electronic_authorization = fields.Char(
        string="Electronic authorization",
        size=49,
        required=True,
        tracking=True,
        readonly=False,
        store=True
    )

    withhold_totals = fields.Float(
        string= "Total retenido",
        compute= "_compute_total_withhold",
        store=True
    )

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Related Document",
        readonly=True,
        required=False,
        tracking=True,
        store=True
    )

    withhold_line_ids = fields.One2many(
        comodel_name="l10n_ec.wizard.create.sale.withhold.line",
        inverse_name="withhold_id",
        string="Lines",
        readonly=False,
        required=True,
    )


    @api.depends('withhold_line_ids.withhold_amount')
    def _compute_total_withhold(self):
        for record in self:
            record.withhold_totals = sum(record.withhold_line_ids.mapped('withhold_amount'))

    def action_cancel(self):
        return {"type": "ir.actions.act_window_close"}
    
    @api.model
    @api.depends('withhold_totals', "withhold_line_ids.withhold_amount", 'withhold_line_ids', 'document_number' , 'partner_id')      
    def create_move(self):
        """
        Generacion de asiento contable para aplicar como
        pago a factura relacionada
        """

        inv = self.invoice_id
        move_data = {
            'journal_id': self.journal_id.id,
            'ref': "RET " + str(self.document_number),
            'date': self.issue_date,
            'l10n_ec_electronic_authorization': self.electronic_authorization,
            'move_type': 'entry',
            'invoice_origin': inv.id,
            'l10n_latam_document_type_id': 7 ,
            'partner_id': self.partner_id.id
        }
        total_counter = 0
        lines = []
        for line in self.withhold_line_ids:
            
            lines.append((0, 0, {
            'partner_id': self.partner_id.id,
            'quantity': 1.0,
            'price_unit': abs(line.withhold_amount),
            'account_id': line.account_tax_withhold,
            'name': "RET " + self.document_number,
            'debit': abs(line.withhold_amount),
            'credit': 0.00,
            'tax_ids': [(4, line.tax_withhold_ids.id)],
            'tax_tag_ids': [(4, line.tax_withhold_ids.id)],
            'tax_base_amount': line.base_amount,
            }))
            total_counter += abs(line.withhold_amount)


        lines.append((0, 0, {
        'partner_id': self.partner_id.id,
        'account_id': inv.partner_id.property_account_receivable_id.id,
        'name': "RET " + str(self.document_number),
        'debit': 0.00,
        'credit': total_counter
        }))

        move_data.update({'line_ids': lines})
        move = self.env['account.move'].create(move_data)
        acctype = 'receivable'
        inv_lines = inv.line_ids
        acc2rec = inv_lines.filtered(lambda l: l.account_id.internal_type == acctype)  # noqa
        acc2rec += move.line_ids.filtered(lambda l: l.account_id.internal_type == acctype)  # noqa
        #self.write({'move_ret_id': move.id})
        move.post()
        acc2rec.reconcile()

        withholding_lines = move.line_ids.filtered(lambda l: l.tax_ids)
        for line in withholding_lines:
            line.l10n_ec_withhold_id = move.id

        return True    
    

    def button_validate(self):
        """
        Botón de validación de Retención que se usa cuando
        se creó una retención manual, esta se relacionará
        con la factura seleccionada.
        """
        for ret in self:
            if not ret.withhold_line_ids:
                raise UserError('No ha aplicado impuestos.')
            #self.action_validate(self.document_number)
            if self.invoice_id.move_type == 'out_invoice':
                    self.create_move()
                    
        return True
