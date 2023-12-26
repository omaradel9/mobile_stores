from odoo import api, fields, models, _

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    product_cost = fields.Float(string="Cost",
    related='product_id.standard_price',
    readonly=True,
    store=True
     )
    pos_categ_id = fields.Many2one(
        string="POS Category",
        comodel_name="pos.category",
        related='product_id.pos_categ_id',
        readonly=True,
        store=True
    )
    order_name = fields.Char(string="name", 
        related='order_id.name',
        readonly=True,
        store=True)
    date_orders = fields.Datetime(string="Field name", related='order_id.date_order',
        readonly=True,
        store=True )
    partner_ids = fields.Many2one(
        string="partner_id",
        comodel_name="res.partner",
        related='order_id.partner_id',
        readonly=True,
        store=True
    )
    user_ids = fields.Many2one(
        string="partner_id",
        comodel_name="res.users",
        related='order_id.user_id',
        readonly=True,
        store=True
    )
    session_ids = fields.Many2one(
        string="partner_id",
        comodel_name="pos.session",
        related='order_id.session_id',
        readonly=True,
        store=True
    )