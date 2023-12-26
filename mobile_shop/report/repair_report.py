from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from calendar import monthrange
from odoo.tools.safe_eval import datetime

import logging
_logger = logging.getLogger(__name__)



class repairReportWizard(models.TransientModel):
    _name = 'repair.report.wizard'

    date_from = fields.Date(string='من تاريخ')
    date_to = fields.Date(string='الى تاريخ')
    select_method = fields.Selection([('month', 'تحديد الشهر'),('date', 'تحديد التاريخ')], default="month", string="اختيار المدة")
    month       = fields.Selection([('jan', 'يناير'),
                                    ('feb', 'فبراير'),
                                    ('mar', 'مارس'),
                                    ('apr', 'أبريل'),
                                    ('may', 'مايو'),
                                    ('jun', 'يونيو'),
                                    ('jul', 'يوليو'),
                                    ('aug', 'أغسطس'),
                                    ('sep', 'سبتمبر'),
                                    ('oct', 'أكتوبر'),
                                    ('nov', 'نوفمبر'),
                                    ('dec', 'ديسمبر')], default="jan", string="شهر")
    year = fields.Selection([(str(num), str(num)) for num in range(2000, (datetime.datetime.now().year) + 1)],
                            'سنة',required=True, default=str(datetime.datetime.now().year))
    
    @api.onchange('month','year')
    def onchange_month(self):
        if not self.month:
            self.date_from = False
            self.date_to = False
            return
        if self.year:
            year = self.year
        else:
            year = datetime.datetime.now().year
        datetime_object = datetime.datetime.strptime(self.month, "%b")
        month_number = datetime_object.month
        num_days = monthrange(int(year), month_number)[1]
        self.date_from = datetime.datetime(int(year), month_number, 1)
        self.date_to = datetime.datetime(int(year), month_number, num_days)
        
    def get_report(self):
        pass
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to
                
            },
        }
        return self.env.ref('mobile_shop.repair_report_wizarda').report_action(self, data=data)






class ReportRepairReportView(models.AbstractModel):

    _name = 'report.mobile_shop.repair_report_wizard_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        

        RO = self.env['repair.order']
        ET = self.env['exit.transactions']
        # start_date = datetime.strptime(date_start, DATE_FORMAT)
        # end_date = datetime.strptime(date_end, DATE_FORMAT)

        orders = RO.search([
            ('schedule_date', '>=', date_start),
            ('schedule_date', '<=', date_end),
            ('state', '=',  'done')
        ], order='name asc')
        delivery_trans = ET.search([
            ('trans_date', '>=', date_start),
            ('trans_date', '<=', date_end),
            ('state', '=',  'approved')
        ])
        docs = []
        sum_net_amount  = []
        sum_exit_amount  = []
        sum_vendor_amount  = []
        sum_delivery    = []
        sum_part_cost   = []
        sum_unit_price  = []
        for delv in delivery_trans:
            exit_amount = delv.amount
            if delv.trans_type == 'out':
                sum_delivery.append(exit_amount)
            elif delv.trans_type == 'vend':
                sum_vendor_amount.append(exit_amount)
            else:
                sum_exit_amount.append(exit_amount)
            
            
            
        
        for order in orders:
            product = order.operations
            main_product_id = order.product_id.name
            for rec in product:
                
                product_id = rec.product_id.name
                product_qty = rec.product_uom_qty
                unit_price = rec.price_unit
                supplier = rec.supplier
                part_cost = rec.part_cost
                net_amount = rec.net_amount
                
                sum_net_amount.append(net_amount)
                sum_part_cost.append(part_cost)
                sum_unit_price.append(unit_price)
                
                docs.append({
                    'date': order.schedule_date,
                    'product_id': product_id,
                    'main_product_id': main_product_id,
                    'quantity': product_qty,
                    'unit_price': unit_price,
                    'supplier': supplier,
                    'part_cost': part_cost,
                    'net_amount': net_amount,
                })
        sum_net_amount_balance = sum(sum_net_amount)
        sum_exit_amount_balance = sum(sum_exit_amount)
        sum_delivery_balance = sum(sum_delivery)
        sum_part_cost_balance = sum(sum_part_cost)
        sum_unit_price_balance = sum(sum_unit_price)
        sum_vendor_amount_balance = sum(sum_vendor_amount)
        profit = (sum_net_amount_balance-sum_delivery_balance)/2
        date ={
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'sum_net_amount_balance': sum_net_amount_balance,
            'sum_exit_amount_balance': sum_exit_amount_balance,
            'sum_delivery_balance': sum_delivery_balance,
            'sum_part_cost_balance': sum_part_cost_balance,
            'sum_unit_price_balance': sum_unit_price_balance,
            'sum_vendor_amount_balance': sum_vendor_amount_balance,
            'sum_store_balance': profit,
            'sum_worker_balance': profit-sum_exit_amount_balance,
        }
        _logger.exception(date)
        
        return date
