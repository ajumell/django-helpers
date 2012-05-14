from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader, RequestContext as Context
from SIS.Library.helpers import can_delete
from form_addons.preview import Form

def getatt(object, name, default=None):
    val = getattr(object, name, default)
    try:
        return val()
    except Exception:
        return val


def is_multipart(Form):
    for x in Form.base_fields:
        y = Form.base_fields[x]
        if y.widget.needs_multipart_form:
            return True
    return False


def mform_view(request, Form, success_message, heading, obj=None, user_field=None, args=None):
    if args is None: args = {}
    if obj is not None: args['instance'] = obj

    if request.method == "POST":
        if is_multipart(Form):
            form = Form(request.POST, request.FILES, **args)
        else:
            form = Form(request.POST, **args)

        if form.is_valid():
            if user_field is not None:
                ret = form.save(False)
                setattr(ret, user_field, request.user)
                ret.save()
            else:
                ret = form.save()
            messages.success(request, success_message)
            return ret, True
        else:
            form.error_message = "Please correct the errors."
    else:
        if obj is not None:
            form = Form(**args)
        else:
            form = Form()

    form.heading = heading
    template = loader.get_template("generic/form.html")
    context = Context(request)
    context['form'] = form
    html = template.render(context)
    return HttpResponse(html)


def form_view(request, Form, success_message, return_url, heading, obj=None, user_field=None, args=None):
    ret = mform_view(request, Form, success_message, heading, obj, user_field, args)
    try: len(ret)
    except Exception: return ret
    return redirect(return_url)


def delete_view(request, obj, name, attr, return_url):
    if can_delete(request) is False:
        template = loader.get_template("generic/confirm.html")
        context = Context(request)
        msg = 'Do you want to delete %s "%s" ?' % (name, getatt(obj, attr))
        msg = msg + "<br />" + "Every data related to this will also be deleted."
        msg = msg + "<br />" + "Are you sure ?"
        context['message'] = msg
        context['back_url'] = return_url
        html = template.render(context)
        return HttpResponse(html)
    else:
        obj.delete()
        messages.success(request, '%s delete successfully.' % name.capitalize())
        return redirect(return_url)


def preview(request, obj, forms, title=None, buttons=None, start=None, end=None):
    if hasattr(obj, 'count'):
        preview_forms = []
        for o in obj:
            preview_form = [Form(o, form) for form in forms]
            preview_forms.extend(preview_form)
    else:
        preview_forms = [Form(obj, form) for form in forms]
    if start is not None: preview_forms.insert(0, Form(None, start))
    if end is not None: preview_forms.append(Form(None, end))
    template = loader.get_template("preview.html")
    context = Context(request)
    context['forms'] = preview_forms
    context['title'] = title
    context['buttons'] = buttons
    html = template.render(context)
    return HttpResponse(html)


def render_view(request, query, heading, actions=None, coloums=None, group_actions=None,
                title='Objects', action_buttons=None, error_message='There are no data to display.'):
    page = request.GET.get("page", '1')
    #    query = query.select_related()
    paginator = Paginator(query, 50)
    try:
        paged_data = paginator.page(page)
    except PageNotAnInteger:
        paged_data = paginator.page(1)
    except EmptyPage:
        paged_data = paginator.page(paginator.num_pages)

    template = loader.get_template("generic/table.html")
    context = Context(request)

    context["objects"] = paged_data
    context['actions'] = actions
    context['coloums'] = coloums
    context['empty_message'] = error_message
    context['group_actions'] = group_actions
    context['action_buttons'] = action_buttons
    context['heading'] = heading
    context['table_title'] = title
    html = template.render(context)
    return HttpResponse(html)