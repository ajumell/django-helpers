jQuery(function ($) {

    var obj = $('#{{ id }}'),
        hidden = $('input[type=hidden][name={{ name }}]');


    obj.autocomplete({
        minLength : {{ min_length }},
        source : "{{ source }}",
        delay : {{ delay }},
        select : function (ui, item) {
            item = item.item;
            obj.val(item.value);
            hidden.val(item.id);
            return false;
        }

    });
});