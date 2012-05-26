jQuery(function ($) {
    $.render = function (template, arguments) {
        var arg, find, replace;
        for (arg in arguments) {
            if (arguments.hasOwnProperty(arg)) {
                find = "{{" + arg + "}}";
                replace = arguments[arg];
                while (template.indexOf(find) >= 0) {
                    template = template.replace(find, replace);
                }
            }
        }
        return template;
    }
});
