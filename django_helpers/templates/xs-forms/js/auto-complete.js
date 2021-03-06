jQuery(function ($) {


    var obj = $('#' + '{{ id }}'),
        hidden = $('input[type=hidden][name=' + '{{ name }}]'),
        current_value = "{{ value }}",
        current_label = "{{ label }}";


    obj.autocomplete({
        minLength : {{ min_length }},
        source : "{{ source }}",
        delay : {{ delay }},

        /**
         @author Muhammed K K
         @date-created 23/5/12, 10:25 PM
         Sets the value to textbox and id to hidden input
         manually for getting primary key value for a model
         instance.
         */
        select : function (ui, item) {
            item = item.item;

            obj.val(item.label);
            hidden.val(item.id);

            current_label = item.label;
            current_value = item.id;

            return false;
        }
    });

    /**
     @author Muhammed K K
     @date-created 23/5/12, 10:24 PM
     This function will remove the current selected value
     from the hidden field  if the value in the text box is
     changed by the user.
     */
    obj.blur(function () {
        if (current_value) {
            if (obj.val() !== current_label) {
                hidden.val('');
            } else {
                hidden.val(current_value);
            }
        }
    });
});