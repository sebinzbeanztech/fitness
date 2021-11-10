odoo.define('zb_pos_reports.models', function (require) {
"use strict";
var pos_model = require('point_of_sale.models');
// var field_utils = require('web.field_utils');

 // pos_model.load_fields("product.product", "name");
pos_model.Order = pos_model.Order.extend({
    // initialize: function() {
    //     _super_order.initialize.apply(this,arguments);
    //     this.disc_txt= this.disc_txt || false;
    //     this.save_to_db();
    // },
    // export_as_JSON: function() {
    //     var json = _super_order.export_as_JSON.apply(this,arguments);
    //     json.disc_txt = this.disc_txt;
    //     return json;
    // },
    // init_from_JSON: function(json){
    // 	_super_order.init_from_JSON.apply(this,arguments);
    //     this.disc_txt = json.disc_txt;
    // },
    get_total_in_words:function(total)
    {
        // return $('body').numbersinwords('123456','UK');
        return $('#amount_in_words').moneyinwords(total,'US','BD');
    },
 
  // function get_quantity_str_with_unit(){
  //       var unit = this.get_unit();
  //       var qty = field_utils.format.float(this.quantity, {digits: [69, 1]});
  //       if(unit && !unit.is_pos_groupable){
  //           return qty + ' ' + unit.name;
  //       }else{
  //           return this.quantity;
  //       }
  //  }
        
 });
 
        
 });
 