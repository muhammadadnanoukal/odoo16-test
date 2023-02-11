from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning


class StockValuationLayerInherit(models.AbstractModel):
    _inherit = 'stock.valuation.layer'

    reference = fields.Char(related='stock_move_id.reference', string='wh Reference')
    customerorvendor = fields.Char(string="Customer/Vendor Name",
                                   compute='_compute_costomervendor_ref', store=True)
    reference_stock = fields.Char(string='Bill/Inv Reference', compute='_compute_inv_bill_ref', store=True)
    vendor_reference_stock = fields.Char(string='Vendor Reference', compute='_compute_vendor_ref', store=True)
    price_stock = fields.Monetary(string='Avg Cost', store=True)
    num_reference = fields.Char(string='Bill/Inv Number', compute='_compute_vendor_ref', store=True)

    current_quantity = fields.Float(string='Current Quantity', store=True)

    @api.depends('stock_move_id.picking_id')
    def _compute_vendor_ref(self):
        for rec in self:
            vendor_ref = self.env['purchase.order'].search([('name', '=', rec.stock_move_id.picking_id.origin)])
            print('vendor_ref...', vendor_ref.name)
            if vendor_ref:
                rec.vendor_reference_stock = vendor_ref.partner_ref

    @api.depends('stock_move_id.picking_id')
    def _compute_costomervendor_ref(self):
        for rec in self:
            costomervendor_ref_pur = self.env['purchase.order'].search(
                [('name', '=', rec.stock_move_id.picking_id.origin)])
            costomervendor_ref_sale = self.env['sale.order'].search(
                [('name', '=', rec.stock_move_id.picking_id.origin)])

            if costomervendor_ref_pur:
                rec.customerorvendor = costomervendor_ref_pur.partner_id.name
                rec.num_reference = costomervendor_ref_pur.name
            if costomervendor_ref_sale:
                rec.customerorvendor = costomervendor_ref_sale.partner_id.name
                rec.num_reference = costomervendor_ref_sale.name




    @api.depends('account_move_id.name')
    def _compute_inv_bill_ref(self):
        for rec in self:

            purchase_ref = self.env['purchase.order'].search(
                [('name', '=', rec.stock_move_id.picking_id.origin)])
            sale_ref = self.env['sale.order'].search(
                [('name', '=', rec.stock_move_id.picking_id.origin)])

            print('hello from compute')
            print('purchase_ref..', purchase_ref)
            print('purchase_ref.name..', purchase_ref.name)

            ref_stock_pur = self.env['account.move'].search([('invoice_origin', '=', purchase_ref.name)],
                                                            limit=1)
            ref_stock_sale = self.env['account.move'].search([('invoice_origin', '=', sale_ref.name)],
                                                             limit=1)

            print('ref_stock_pur..', ref_stock_pur)
            print('ref_stock_pur.name..', ref_stock_pur.name)

            if ref_stock_pur and ref_stock_pur.name != '/':
                rec.reference_stock = ref_stock_pur.name
                print('test from if')
                print('ref_stock_pur...', ref_stock_pur)
                print('ref_stock_pur.name...', ref_stock_pur.name)

            if ref_stock_sale and ref_stock_sale.name != '/':
                rec.reference_stock = ref_stock_sale.name
                print('test from else')
                print('ref_stock_sale...', ref_stock_sale)
                print('ref_stock_sale.name...', ref_stock_sale.name)

    @api.model
    def create(self, vals):
        # mm = self.env['product.product'].search([('id', '=', vals['product_id'] )]).avg_cost
        mm = self.env['product.product'].search([('id', '=', vals['product_id'])])
        print('mm..', mm)
        print('mm..', mm.qty_available)
        vals['price_stock'] = self.env['product.product'].search([('id', '=', vals['product_id'])]).avg_cost
        vals['current_quantity'] = self.env['product.product'].search([('id', '=', vals['product_id'])]).qty_available
        res = super(StockValuationLayerInherit, self).create(vals)

        print('res..', res)
        print('vals..', vals)
        print('vals..', vals['product_id'])
        return res
