# -*- coding: utf-8 -*-
# from odoo import http


# class MobileShop(http.Controller):
#     @http.route('/mobile_shop/mobile_shop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile_shop/mobile_shop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile_shop.listing', {
#             'root': '/mobile_shop/mobile_shop',
#             'objects': http.request.env['mobile_shop.mobile_shop'].search([]),
#         })

#     @http.route('/mobile_shop/mobile_shop/objects/<model("mobile_shop.mobile_shop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile_shop.object', {
#             'object': obj
#         })
