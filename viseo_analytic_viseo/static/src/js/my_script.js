<!-- my_module/static/src/js/my_script.js -->
odoo.define('viseo_analytic_viseo.my_script', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');

    var _t = core._t;

    var MyFormView = Widget.extend({
        events: {
            'click button[name=action_afficher_template]': 'onAfficherTemplateClick',
        },

        onAfficherTemplateClick: function () {
            var self = this;
            this._rpc({
                model: 'viseo_analytic.viseo_analytic',
                method: 'action_afficher_template',
                args: [this.res_id],
            }).then(function (result) {
                // Do something with the result if needed
            });
        },
    });

    core.action_registry.add('mon_modele_form_view', MyFormView);

    return {
        MyFormView: MyFormView,
    };
});
