from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.utils.simplejson import dumps
from django.views.decorators.csrf import csrf_exempt


def redirect(to, args=None, kwargs=None):
    return HttpResponseRedirect(reverse(to, args=args, kwargs=kwargs))


def render_to_response(template, request, data=None):
    """
    Renders the given template with given data and returns the HttpResponse

    @type request: django.http.HttpRequest
    @param request: The request object

    @type data: dict
    @param data: The extra variables that has to be passed to the context

    @type template: string
    @param template: The name of the template to be rendered

    @rtype: HttpResponse
    """
    context = RequestContext(request, data)
    template = loader.get_template(template)
    html = template.render(context)
    return HttpResponse(html)


def render_template(request, template, data=None, url_params=None, **kwargs):
    if url_params is not None:
        if data is None:
            data = dict()

        for url_param in url_params:
            param_value = kwargs.get(url_param, '')
            if param_value != "":
                data[url_param] = param_value
    return render_to_response(template, request, data)


def render_json(dictionary):
    string = dumps(dictionary)
    mimetype = 'application/javascript'
    return HttpResponse(string, mimetype=mimetype)


def render_to_string(template, values=None, request=None):
    template = loader.get_template(template)
    if request is None:
        context = Context(values)
    else:
        context = RequestContext(request, values)
    html = template.render(context)
    return html


def message(request, heading, message):
    return render_to_response('generic/message.html', request, {
        'heading': heading,
        'msg': message
    })


def render_error(request, message):
    return render_to_response('generic/error.html', request, {
        'heading': "Error Occured",
        'msg': message
    })


def render_form(request, form, extra=None):
    if extra is None:
        extra = {}
    extra["form"] = form
    return render_to_response('generic/form.html', request, extra)


def render_confirm(request, message, heading=None):
    return render_to_response('generic/confirm.html', request, {
        'heading': heading,
        'msg': message
    })


def is_multipart(Form):
    """
    Returns true if the given form require multipart attributr

    @param Form: A form class

    @rtype Boolean
    """
    for x in Form.base_fields:
        y = Form.base_fields[x]
        if y.widget.needs_multipart_form:
            return True
    return False


def form_view(request,
              Form,
              success_view,
              form_heading,
              success_view_args=None,
              success_message=None,
              current_user_field=None,
              submit_button="Submit",
              error_message="Please correct the errors.",
              template="generic/form.html",
              ajax_template="partials/form.html",
              obj_instance=None,
              custom_form_arguments=None,
              template_dict=None,
              obj_url_params=None,
              has_many_to_many=False,
              url_params=None,
              **kwargs
):
    """
    Returns a HttpResponse by rendering a form with given parameters

    @param Form: The form to be rendered

    @param string success_view: The name of the view to be rendered when the
    form has successfully saved.

    @rtype: HttpResponse
    """

    if custom_form_arguments is None:
        custom_form_arguments = {}

    if obj_instance is not None:
        custom_form_arguments['instance'] = obj_instance

    if template_dict is None:
        template_dict = {}

    if request.method == "POST":
        if is_multipart(Form):
            form = Form(request.POST, request.FILES, **custom_form_arguments)
        else:
            form = Form(request.POST, **custom_form_arguments)

        if form.is_valid():
            obj = form.save(has_many_to_many)

            if current_user_field is not None:
                setattr(obj, current_user_field, request.user)

            if obj_url_params is not None:
                for param in obj_url_params:
                    if type(param) == tuple:
                        val = kwargs.get(param[1])
                        param = param[0]
                    else:
                        val = kwargs.get(param)
                    setattr(obj, param, val)

            obj.save()
            if request.is_ajax():
                response_dict = {
                    "success": True,
                    "message": success_message
                }
                return render_json(response_dict)
            else:
                if success_message is not None:
                    messages.success(request, success_message)

                if success_view_args is not None:
                    args = list()
                    for argument in success_view_args:
                        args.append(kwargs.get(argument))
                    return redirect(success_view, tuple(args))
                else:
                    return redirect(success_view)
        else:
            if request.is_ajax():
                rdict = {'error': True}
                d = {}
                for e in form.errors:
                    d.update({e: form.errors[e]})
                rdict.update({'errors': d})
                return render_json(rdict)
            template_dict['form_error_message'] = error_message
    else:
        form = Form(**custom_form_arguments)

    if url_params is not None:
        for url_param in url_params:
            param_value = kwargs.get(url_param, '')
            if param_value != "":
                template_dict[url_param] = param_value

    template_dict['form'] = form
    template_dict['form_submit'] = submit_button
    template_dict['form_heading'] = form_heading

    if request.is_ajax():
        template = ajax_template

    return render_to_response(template, request, template_dict)


@csrf_exempt
def delete_items_ajax(request, Model):
    """
    A generic view to delete items from a model using ajax.
    @param request:
    @type request: django.http.HttpRequest
    @return:
    """
    if request.is_ajax():
        values = request.POST.getlist('values[]')
        query = Model.objects.filter(pk__in=values)
        query.delete()
        return HttpResponse('true')
    return HttpResponse('false')
