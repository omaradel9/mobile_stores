# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import datetime
from random import choice
from string import digits
from collections import defaultdict

import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class MoneyMachine(models.Model):
    _name = 'money.machine'
    _description = 'Money Machine'

    name = fields.Char(string=" اسم مكاينة ",)
    machine_code = fields.Char(string="كود المكاينة ",)
    curent_amount = fields.Float(string="الرصيد", )
    cash_amount = fields.Float(string="النقدى", )
    
    name_tag = fields.Char(string="tag",)
    
    
    

    @api.model
    def get_machine_amount(self):
        machine  = self.env['money.machine'].search([('name_tag', '!=', 'net')])
        machine_cash  = self.env['money.machine'].search([('name_tag', '=', 'net')])
        transactions = self.env['representative.transactions'].search([('state', '=', 'approved')])
        total_representative = []
        for rep in transactions:
            if rep.trans_type == 'in' :
                amount = rep.amount
                total_representative.append(amount)
            else:
                amount = -(rep.amount)
                total_representative.append(amount)        
                
        values = {}
        total = []
        for rec in machine :
            total.append(rec.curent_amount)
            values[rec.name_tag+'2'] = rec.curent_amount
        
        values['total2'] = sum(total)
        values['repre2'] = sum(total_representative)
        values['net'] = sum(total)-sum(total_representative)
        machine_cash.curent_amount = sum(total)-sum(total_representative)
        
        
        
        return values
    
    def transfer_net_amount(self):
        pos_order  = self.env['pos.order']
        pos_order.create({
            'company_id': self.env.company.id,
            'session_id': self.main_pos_config.current_session_id.id,
            'partner_id': self.new_partner.id,
            'access_token': '1234567890',
            'lines': [(0, 0, {
                'name': "OL/0001",
                'product_id': self.product1.id,
                'price_unit': 10,
                'discount': 0.0,
                'qty': 1.0,
                'tax_ids': False,
                'price_subtotal': 10,
                'price_subtotal_incl': 10,
            })],
            'amount_tax': 10,
            'amount_total': 10,
            'amount_paid': 10.0,
            'amount_return': 10.0,
        })
        


class MachineTransactions(models.Model):
    _name = 'machine.transactions'
    _description = 'Money Machine'

    machine_id = fields.Many2one(
        string="Machine",
        comodel_name="money.machine",
    )
    name = fields.Char(
    related='machine_id.name',
    readonly=True,
    store=True
    )
    
    trans_type = fields.Selection(
        string="Transaction Type",
        selection=[
                ('in', 'IN'),
                ('out', 'OUT'),
        ],
    )
    trans_date = fields.Datetime(string="trans date",default=fields.Datetime.now() )
    amount = fields.Float(string="Amount", )
    
class MachineRepresentative(models.Model):
    _name = 'machine.representative'
    _description = 'Machine Representative'

    machine_id = fields.Many2one(
        string="مكاينة الدفع",
        comodel_name="money.machine",
    )
    name = fields.Char('اسم المندوب')
    
    
class RepresentativeTransactions(models.Model):
    _name = 'representative.transactions'
    _description = 'Representative Transactions'

    represent_id = fields.Many2one(
        string="المندوب",
        comodel_name="machine.representative",
    )
    trans_type = fields.Selection(
        string="نوع العملية",
        selection=[
                ('out', 'دفع للمندوب'),
                ('in', 'دفع للمحل'),
        ],
    )
    trans_date = fields.Datetime(string="تاريخ العملية",default=fields.Datetime.now() )
    amount = fields.Float(string="القيمة", )
    state = fields.Selection(
        string="State",
        selection=[
                ('draft', 'Draft'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
        ],default='draft'
    ) 
    @api.constrains('amount')
    def create_transaction(self):
        _logger.exception("==================================create_transaction")
        pass
    
    def apply_transaction(self):
        machine_id = self.represent_id.machine_id
        old_balance = machine_id.curent_amount
        new_balance = old_balance + self.amount        
        machine  = self.env['money.machine'].search([('name_tag', '=', 'cash')])
        machine_cash_amount = machine.curent_amount
        if self.trans_type == 'in':
            machine_id.curent_amount = new_balance
        else:
            machine.curent_amount= machine_cash_amount -self.amount
        self.state = 'approved'
        
            
            
            
    def reject_transaction(self):
        machine_id = self.represent_id.machine_id
        old_balance = machine_id.curent_amount
        new_balance = old_balance - self.amount        
        machine  = self.env['money.machine'].search([('name_tag', '=', 'cash')])
        machine_cash_amount = machine.curent_amount
        if self.trans_type == 'in':
            machine_id.curent_amount = new_balance
        else:
            machine.curent_amount= machine_cash_amount + self.amount
        self.state = 'rejected'
        
        
    def print_receipt(self):
        
        _logger.exception("==================================print_receipt")
        
        pass


    

class productTemplate(models.Model):
    _inherit = 'product.template'
    
    
    available_in_pos = fields.Boolean(default = True )  
    standard_price =  fields.Float(copy= True )  
    type = fields.Selection(selection_add=[('rapair', 'Repaired Device')],ondelete={'rapair': 'cascade'},)
    detailed_type = fields.Selection(selection_add=[('rapair', 'Repaired Device')],ondelete={'rapair': 'cascade'})
    vendor_name = fields.Many2one(
        string="المورد",
        comodel_name="res.partner",domain="[('supplier_rank', '=', 1),('repair_vendor', '=', False)]",
        context="{'default_repair_vendor':'False','default_supplier_rank':1}")  
    
    def change_categ(self):
        product = self.env['product.template'].search([])
        for rec in product:
            rec.pos_categ_id = 2    
    def _prepare_report_data(self):
        
        if self.qty_available <= 0:
            raise UserError(_('You need to set a positive quantity.'))
        
        xml_id = 'product.report_product_template_label_dymo'
    

        active_model = ''
      
        products = self.id
        active_model = 'product.template'
      
        # Build data to pass to the report
        custom_quantity = 1
        data = {
            'active_model': active_model,
            'quantity_by_product':products,
            'layout_wizard': 104,
            'quantity_by_products':  self.qty_available,
        }
        return xml_id, data

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        report_action = self.env.ref(xml_id).report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action
    
    def generate_random_barcode(self):
        
        for employee in self:
            employee.barcode = '231'+"".join(choice(digits) for i in range(9))  
            
def _prepare_data2(env, data):
    Product = env['product.template'].with_context(display_default_code=False)
    
    total = 0
    qty_by_product_in = data.get('quantity_by_product')
    qty_by_products = data.get('quantity_by_products')
    products = Product.search([('id', '=', qty_by_product_in)], order='name desc')
    quantity_by_product = defaultdict(list)
    # _logger.exception("==================================print_receipt %s",quantity_by_product)
    
    for product in products:
        q = 1
        quantity_by_product[product].append((product.barcode, qty_by_products))
        total += q

    _logger.exception("==================================quantity_by_product %s",quantity_by_product)
    _logger.exception("==================================(total - 1) // 1 + 1 %s",(total - 1) // 1 + 1)

    return {
        'quantity': quantity_by_product,
        'rows': 1,
        'columns': 1,
        'page_numbers': (total - 1) // 1 + 1,
        'extra_html': '',
    }
# class ProductLabelLayout(models.TransientModel):
#     _inherit = 'product.label.layout'
    
#     def process(self):
#         self.ensure_one()
#         xml_id, data = self._prepare_report_data()
#         if not xml_id:
#             raise UserError(_('Unable to find report template for %s format', self.print_format))
#         layout_wizard = self.env['product.label.layout'].browse(data.get('layout_wizard'))
       
#         _logger.exception("==================================print_receipt %s",layout_wizard.extra_html)
        
        
#         report_action = self.env.ref(xml_id).report_action(None, data=data)
#         report_action.update({'close_on_report_download': True})
#         return report_action
  
        
class ReportProductTemplateLabelDymo(models.AbstractModel):
    _inherit = 'report.product.report_producttemplatelabel_dymo'

    def _get_report_values(self, docids, data):
        return _prepare_data2(self.env, data)