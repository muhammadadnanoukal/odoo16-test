from odoo import api, fields, models, tools, _


class AccountMovInh(models.AbstractModel):
    _inherit = 'account.move'
    move_type = fields.Selection(
        selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        string='Type',
        required=True,
        readonly=True,
        tracking=True,
        change_default=True,
        index=True,
        default="entry",
    )

    def action_post(self):

        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments
        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        if other_moves:
            other_moves._post(soft=False)

        if self.move_type == 'in_invoice':
            print('hellllllllllll...')
            self.env['stock.valuation.layer'].search([('num_reference', '=', self.invoice_origin)])._compute_inv_bill_ref()
            print(self.env['stock.valuation.layer'].search([('num_reference', '=', self.invoice_origin)]))
        if self.move_type == 'out_invoice':
            print('hellllllllllll2222...')
            self.env['stock.valuation.layer'].search([('num_reference', '=', self.invoice_origin)])._compute_inv_bill_ref()
            print(self.env['stock.valuation.layer'].search([('num_reference', '=', self.invoice_origin)]))
        return False
