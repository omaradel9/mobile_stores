from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from calendar import monthrange
from odoo.tools.safe_eval import datetime
import collections, functools, operator


import logging
_logger = logging.getLogger(__name__)



class repairReportWizard(models.TransientModel):
    _name = 'repair.vendor.report.wizard'

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
    detailed = fields.Boolean(string="مفصل", )
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
                'date_end': self.date_to,
                'detailed': self.detailed
            },
        }
        return self.env.ref('mobile_shop.repair_vendor_report_wizarda').report_action(self, data=data)






class ReportRepairReportView(models.AbstractModel):

    _name = 'report.mobile_shop.repair_vendor_report_wizard_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        detailed = data['form']['detailed']
        

        RO = self.env['repair.order']
        ET = self.env['exit.transactions']

        orders = RO.search([
            ('schedule_date', '>=', date_start),
            ('schedule_date', '<=', date_end),
            ('state', '=',  'done')
        ], order='schedule_date asc')
        delivery_trans = ET.search([
            ('trans_date', '>=', date_start),
            ('trans_date', '<=', date_end),
            ('state', '=',  'approved')
        ])
        docs = []
        sum_qty  = []
        sum_vendor_amount  = []
        sum_part_cost   = []
 
        for delv in delivery_trans:
            exit_amount = delv.amount
           
            if delv.trans_type == 'vend':
                sum_vendor_amount.append(exit_amount)
            
            
            
        vendors   = []
        
        for order in orders:
            product = order.operations
            main_product_id = order.product_id.name
            for rec in product:
                
                product_id = rec.product_id.name
                vendor_name = rec.vendor_name.name
                product_qty = rec.product_uom_qty
                part_cost = rec.part_cost
                if vendor_name:
                    vendors.append({vendor_name: part_cost,vendor_name+'qty': product_qty})
            
                sum_qty.append(product_qty)
                sum_part_cost.append(part_cost)
                
                docs.append({
                    'date': order.schedule_date,
                    'product_id': product_id,
                    'main_product_id': main_product_id,
                    'quantity': product_qty,
                    'part_cost': part_cost
                })
        _logger.exception("====================vendors%s",vendors)
        vendorss  = []
        
        result = dict(functools.reduce(operator.add,map(collections.Counter, vendors)))
        # for res ,sd in result.items():
        #     if res 
        #         vendorss.append({
        #             'date': order.schedule_date,
        #             'product_id': product_id,
        #             'main_product_id': main_product_id
        #         })
        #     _logger.exception("====================res%s",res)
        #     _logger.exception("====================sd%s",sd)
            
            
        sum_qty_balance = sum(sum_qty)
        sum_vendor_amount_balance = sum(sum_vendor_amount)
        sum_part_cost_balance = sum(sum_part_cost)
        date ={
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            # 'result': result,
            'sum_qty_balance': sum_qty_balance,
            'sum_vendor_amount_balance': sum_vendor_amount_balance,
            'sum_part_cost_balance': sum_part_cost_balance,
            'detailed': detailed,
            'vendor_name': vendor_name,
            
            
        }
        _logger.exception(date)
        
        return date
