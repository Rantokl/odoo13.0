odoo.define('viseo_analytic_viseo.analytic', function (require) {
    "use strict";

    console.log("Module loaded")
    var AbstracAction = require('web.AbstractAction');
    var core = require('web.core');
    var AbstractRenderer = require('web.AbstractRenderer');
    var Analytic = AbstracAction.extend({
        template:'custom_html_template',

        init: function(){
            this._super.apply(this, arguments);
            console.log('Analytic initialized....');
        },
        _render: function () {
            this.$el.empty();
            this.show_pivottt();
            return $.when();
        },
    
        show_pivottt: function(){
            console.log("Test")
            var self = this;	
            $('.pivot_table').css("height", "100%").css("background-color", "blue");	
            $('.pivot_table').append("<div id='container' style=' width: 100%;height: 100%;margin: 0;padding: 0;'></div>");
            anychart.onDocumentReady(function () {    
                // create data
                var data = [];
                rpc.query({
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'read_group_department_ids',
                    args: [1],
                }).then(function(output) {
                    data = output;
                    console.log(output);
                });
            });

   
        }

    })


   core.action_registry.add('viseo_analytic_viseo',Analytic);
   return Analytic;
});