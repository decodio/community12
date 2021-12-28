odoo.define('web.eq_widget_color', function(require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

    var EQColor = basic_fields.FieldChar.extend({
        _renderEdit: function() {
            this._prepareInput(this.$el);
            this.$input = this.$el.find('input');
            this.$input.context.type = 'color';
        },
        _setValue: function (value, options) {
             value = this.$input.context.value;
            return this._super(value, options);
        },
    });
    field_registry.add('eq_color', EQColor);
});
