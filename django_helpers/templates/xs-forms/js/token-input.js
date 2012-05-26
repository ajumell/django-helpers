jQuery(function ($) {
    var obj = $('#' + '{{ id }}');
    obj.tokenInput("{{ source }}", {
        {% if hint_text %}hintText : "{{ hint_text }}", {% endif %}
        {% if no_result_text %}noResultsText : "{{ no_result_text }}", {% endif %}
        {% if searching_text %}searchingText : "{{ searching_text }}", {% endif %}
        {% if delay %}searchDelay : {{ delay }}, {% endif %}
        {% if min_chars %}minChars : {{ min_chars }}, {% endif %}
        {% if limit %}tokenLimit : {{ limit }}, {% endif %}
        {% if prevent_duplicates %}preventDuplicates : {{ prevent_duplicates }}, {% endif %}
        {% if values|length %}
        prePopulate : [
            {% for value in values %}
            {id : {{ value.id }}, name : "{{ value.name }}"}{% if not forloop.last %},
            {% endif %}
            {% endfor %}
        ],
        {% endif %}
        queryParam : "term"
    });
});