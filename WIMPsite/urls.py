from django.conf.urls import url
from . import views

urlpatterns = [
    url('home', views.Home.as_view(), name="Home"),
    url('testingstrips', views.TestStripList.as_view(), name="Testing Strips"),
    url('scheduledtests', views.SceduledTestList.as_view(), name="Scheduled Tests")
]