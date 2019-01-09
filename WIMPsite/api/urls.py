from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
import WIMPsite.api.views as api

urlpatterns = [
    url(r'^test/(?P<action>\w{1,20})/$', csrf_exempt(api.TestAPI.as_view()), name="api-test"),
    url(r'^settings/$', csrf_exempt(api.SettingsAPI.as_view()), name="api-settings"),
]