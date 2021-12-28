odoo.define('eq_ownerp_ui.FormRenderer', function (require) {
"use strict";
var FormRenderer = require('web.FormRenderer');
FormRenderer.include({
    _renderButtonBox: function (node) {
        var self = this;
        var $result = $('<' + node.tag + '>', { 'class': 'o_not_full' });
        var buttons = _.map(node.children, function (child) {
            if (child.tag === 'button') {
                return self._renderStatButton(child);
            } else {
                return self._renderNode(child);
            }
        });
        _.each(buttons, function ($button) {
            $button.appendTo($result);
        });
        this._handleAttributes($result, node);
        this._registerModifiers(node, this.state, $result);
        return $result;
    },
});
});