jQuery(function ($) {

    var obj = $('#{{ id }}'),
        hidden = $('input[type=hidden][name={{ name }}]'),
        current_value=null;


    obj.autocomplete({
        minLength : {{ min_length }},
        source : "{{ source }}",
        delay : {{ delay }},
        select : function (ui, item) {
            item = item.item;
            obj.val(item.value);
            current_value = item.value;
            hidden.val(item.id);
            return false;
        }
    });

    obj.blur(function(){
        if(obj.val() !== current_value){
            hidden.val('');
        }
    });
});