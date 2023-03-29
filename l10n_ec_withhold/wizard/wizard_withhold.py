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
    )

    issue_date = fields.Date(string="Fecha de retencion", readonly=False, required=True, tracking=True)

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        readonly=False,
        string="Diario",
    )

    document_number = fields.Char(
        string="Numero de Retencion",
        required=True,
        readonly=False,
        tracking=True,
        size=17,
    )

    electronic_authorization = fields.Char(
        string="Electronic authorization",
        size=49,
        required=True,
        tracking=True,
        readonly=False,
    )
    
    withhold_totals = fields.Float(
        string= "Total retenido",
        store= True,
        compute= "_compute_total_withhold"
    )

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Related Document",
        readonly=True,
        required=False,
        tracking=True,
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

    def action_create_withhold(self):
        retention = self.env['l10n_ec.withhold'].create({
            'partner_id': self.partner_id.id,
            'invoice_id': self.invoice_id.id,
            'issue_date': self.issue_date,
            'document_number': self.document_number,
            'electronic_authorization': self.electronic_authorization,
            'state' : 'done',
        })

        withhold_lines = []
        for line in self.withhold_line_ids:
            withhold_lines.append((0, 0, {
                'tax_withhold_ids': line.tax_withhold_ids.id,
                'base_amount': line.base_amount,
                'withhold_amount': line.withhold_amount,
            }))

        retention.write({
            'line_ids': withhold_lines,
        })

        self.invoice_id.l10n_ec_withhold_ids = retention.id



    def action_cancel(self):
        return {"type": "ir.actions.act_window_close"}
    

    @api.depends('withhold_totals', "withhold_line_ids.withhold_amount", 'withhold_line_ids', 'document_number' , 'partner_id')      
    def create_move(self):
        """
        Generacion de asiento contable para aplicar como
        pago a factura relacionada
        """
        for ret in self:
            inv = ret.invoice_id
            move_data = {
                'journal_id': ret.journal_id.id,
                'ref': "RET" + ret.document_number,
                'date': ret.issue_date
            }
            total_counter = 0
            lines = []
            for line in ret.withhold_line_ids:
                
                lines.append((0, 0, {
                'partner_id': ret.partner_id.id,
                'account_id': line.account_tax_withhold,
                'name': "RET " + ret.document_number,
                'debit': abs(line.withhold_amount),
                'credit': 0.00,
                'tax_ids': [(4, line.tax_withhold_ids.id)],
                'tax_tag_ids': [(4, line.tax_withhold_ids.id)],
                }))
                total_counter += abs(line.withhold_amount)


            lines.append((0, 0, {
            'partner_id': ret.partner_id.id,
            'account_id': inv.partner_id.property_account_receivable_id.id,
            'name': "RET " + ret.document_number,
            'debit': 0.00,
            'credit': total_counter
            }))

            move_data.update({'line_ids': lines})
            move = self.env['account.move'].create(move_data)
            acctype = 'receivable'
            inv_lines = inv.line_ids
            acc2rec = inv_lines.filtered(lambda l: l.account_id.internal_type == acctype)  # noqa
            acc2rec += move.line_ids.filtered(lambda l: l.account_id.internal_type == acctype)  # noqa
            #ret.write({'move_ret_id': move.id})
            move.post()
            acc2rec.reconcile()
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
            if ret.invoice_id.move_type == 'out_invoice':
                    self.create_move()
                    self.action_create_withhold()
                    
        return True