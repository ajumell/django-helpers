jQuery(function ($) {
    var elem = $('#' + '{{ id }}'),
        hidden = elem.siblings('[type=hidden][name=' + '{{ name }}]');
    elem.raty({
        number : {{ number }},
        size : {{ size }},
        score : {{ score }},
        {% if half %}half : true, {% endif %}
        {% if cancel %}cancel : true, {% endif %}
        click : function (score) {
            hidden.val(score);
        }
    });
});