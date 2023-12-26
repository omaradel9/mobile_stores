from odoo import api, fields, models, _
class Repair(models.Model):
    _inherit = 'repair.order'
    
    phone = fields.Char(string="Phone",
    related='partner_id.phone',
    readonly=False,
    store=True
     )
    partner_id = fields.Many2one(domain="[('customer_rank', '=', 1)]",context="{'default_customer_rank':1}")  
    
    product_id = fields.Many2one(
        domain="[('type', '=', 'consu')]")
    schedule_date = fields.Date(default=fields.Datetime.now())
class Repair(models.Model):
    _inherit = 'repair.line'
    
    part_cost = fields.Float(string="التكلفة", )
    net_amount = fields.Float(string="الصافى", readonly=True )
    delivery = fields.Float(string="التوصيل", )
    supplier = fields.Char(string="المورد", )
    vendor_name = fields.Many2one(string="المورد",comodel_name="res.partner",domain="[('supplier_rank', '=', 1),('repair_vendor', '=', True)]"
                                  ,context="{'default_repair_vendor':'True','default_supplier_rank':1}")      
    
    
    product_id = fields.Many2one(
        domain="[('type', '=', 'rapair')]")
    
    
    
    @api.onchange('part_cost','price_unit','delivery')
    def _onchange_price(self):
        for rec in self:
            cost = rec.part_cost
            net = rec.price_unit - cost
            rec.net_amount = net
            
class ExitsTransactions(models.Model):
    _name = 'exit.transactions'
    _description = 'Exits Transactions'

    employee_id = fields.Many2one("hr.employee", string="Employee", ondelete='cascade')
    vendor_name = fields.Many2one(string="المورد",comodel_name="res.partner",domain="[('supplier_rank', '=', 1),('repair_vendor', '=', True)]")      
    trans_date = fields.Datetime(string="تاريخ العملية", default=fields.Datetime.now(), readonly=True)
    amount = fields.Float(string="القيمة", )
    trans_type = fields.Selection(
        string="نوع العملية",
        selection=[
                ('out', 'توصيل'),
                ('in', 'خوارج'),
                ('vend', 'دفع للمورد'),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
                ('draft', 'Draft'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
        ],default='draft'
    ) 
    def apply_transaction(self):
        
        self.state = 'approved'
                 
    def reject_transaction(self):
        self.state = 'rejected'

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    repair_vendor = fields.Boolean(string="مورد صيانة", )