jQuery(function ($) {
    $('#' + '{{ id }}').spinner({
        {% if min %}min : {{ min }}, {% endif %}
        {% if max %}min : {{ max }}, {% endif %}
        {% if places %}places : {{ places }}, {% endif %}
        step : {{ step|default:1 }},
        largeStep : {{ largeStep|default:10 }},
        prefix : ''
    });
});