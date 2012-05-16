from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'(?P<name>.*)/', views.lookup, name='auto-complete-lookup')
)