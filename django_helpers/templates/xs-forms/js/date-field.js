jQuery(function ($) {
    $('#' + '{{ id }}').datepicker({
        dataFormat : "{{ date_format }}",
        {% if change_month %}changeMonth : true, {% endif %}
        {% if change_year %}changeYear : true, {% endif %}
        {% if min_date %}minDate : new Date("{{ min_date.isoformat }}"), {% endif %}
        {% if max_date %}maxDate : new Date("{{ max_date.isoformat }}"), {% endif %}
    });
});