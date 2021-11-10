odoo.define('zb_pos_reports.pos_taxt', function (require) {
"use strict";

var models = require('point_of_sale.models');

models.Orderline = models.Orderline.extend({

	get_prd_tax_name: function(){
    	var product =  this.get_product();
    	var taxes_ids = product.taxes_id;
        var taxes =  this.pos.taxes;
        var product_taxes = [];
        var taxname = '';
        _(taxes_ids).each(function(el){
            product_taxes.push(_.detect(taxes, function(t){
            	return t.id === el;
            }));
        });
        console.log(product_taxes,'producttaxes')
        _(product_taxes).each(function(tax) {
            taxname = taxname + tax.name + ' ';
        });
        return {
            "displayTaxPdt": taxname,
        };
    },
    
});

});
