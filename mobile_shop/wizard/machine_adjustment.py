from odoo import models, fields, api
import datetime

import logging
_logger = logging.getLogger(__name__)

class MachineAdjust(models.TransientModel):
    _name = 'machine.adjust'
    _description = 'Machine Adjust'
    
    machine_id = fields.Many2one(
        string="الماكينة",
        comodel_name="money.machine",readonly=True,
        compute="compute_machine_id"
    )
    
    trans_date = fields.Datetime(string="التاريخ",default=fields.Datetime.now(),readonly=True)
    counted = fields.Float(string="القيمه الموجودة", )
    name = fields.Char(string="Name", )
    
    @api.depends('name')
    def compute_machine_id(self):
        machine = self.env['money.machine'].search([('name_tag', '=', self.name)]).id
        _logger.exception("==========================omar%s",machine)
        self.machine_id = machine
    
    def send_adjust(self):
        machine_id = self.machine_id
        old_balance = machine_id.curent_amount
        cash_balance = machine_id.cash_amount
        new_balance = old_balance - self.counted        
        machine_id.curent_amount = self.counted
        machine_id.cash_amount = cash_balance + new_balance    
        inventory = self.env['machine.inventory']
        inventory.create({
                        'machine_id' : machine_id.id ,
                        'trans_date' : fields.Datetime.now(),
                        'amount' : self.counted,
                        'trans_type' : 'machine' })
        
        inventory.create({
                        'machine_id' : machine_id.id ,
                        'trans_date' : fields.Datetime.now(),
                        'amount' : new_balance,
                        'trans_type' : 'machine' })
        
class Machineinventory(models.Model):
    _name = 'machine.inventory'
    _description = 'Money Inventory'

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
                ('cash', 'Cash'),
                ('machine', 'Machine'),
        ],
    )
    trans_date = fields.Datetime(string="trans date",default=fields.Datetime.now() )
    amount = fields.Float(string="Amount", )