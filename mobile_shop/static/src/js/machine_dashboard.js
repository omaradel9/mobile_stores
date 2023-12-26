odoo.define('mobile_shop.MachineDashboard', function (require) {
    "use strict";
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const rpc = require("web.rpc");
    var ajax = require("web.ajax");
    const _t = core._t;
    const QWeb = core.qweb;
    const SalonDashboard = AbstractAction.extend({
        template: 'MachineDashboardMain',
        events: {
            'click #momken': 'momken',
            'click #fawry': 'fawry',
            'click #aman': 'aman',
            'click #amwal': 'amwal',
            'click #bee': 'bee',
            'click #vc': 'vc',
            'click #ipx': 'ipx',
            'click #mach': 'mach',
            'click #hold': 'hold',
            'click #cash': 'cash',
            'click #exit': 'exit',
            'click #transfer': 'transfer'

        },
        init: function (parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['MachineDashBoard'];

        },

        start: function () {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function () {
                self.render_dashboards();
                self.$el.parent().addClass('oe_backgrou nd_grey');
            });

        },
        render_dashboards: function () {
            var self = this;
            var templates = ['MachineDashBoard'];
            _.each(templates, function (template) {
                self.$('.spa_salon_dashboard').append(QWeb.render(template, {widget: self}));
            });
            rpc.query({
                model: "money.machine",
                method: "get_machine_amount",
                args: [],
            })
                .then(function (result) {
                    for (const [key, value] of Object.entries(result)) {
                        console.log("=============result key : "+key+" value :"+value)
                        $("#"+key).append("<span>" + value + "</span>");


                    }
                    
                    console.log("=============result",result)

                    // console.log("pass to controller");
                    ajax.jsonRpc("/salon/chairs", "call", {}).then(function (values) {
                        $('#chairs_dashboard_view').append(values);
                    });
                });
        },
        on_reverse_breadcrumb: function () {
            var self = this;
            self.$('.spa_salon_dashboard').empty();
            self.render_dashboards();
        },

        //events
        fawry : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },

        momken : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        aman : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        amwal : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        bee : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        vc : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        ipx : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        cash : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        exit : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t('جرد الماكينة'),
                type: 'ir.actions.act_window',
                res_model: 'machine.adjust',
                view_mode: 'form',
                views: [[false, 'form']],
                context: {default_name: active_id},
                target: 'new',
            }, options);
        },
        transfer : function (ev) {
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var active_id = event.target.id
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            rpc.query({
                model: "money.machine",
                method: "transfer_net_amount",
                args: [],
            });
        },

    });
        core.action_registry.add('machine_dashboard', SalonDashboard);
    return SalonDashboard;
});
