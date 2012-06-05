from django_helpers.views.helpers import render_template

__author__ = 'ajumell'

class CheckJsMiddleware:
    def process_request(self, request):
        """
        Checks for cookie has js cookie
        @param request:
        @type request:django.http.HttpRequest
        @return:
        """
        cookie = request.COOKIES.get('has_js', None)
        if cookie is None:
            data = {
                'location': request.get_full_path()
            }
            return render_template(request, 'check_js.html',data)