from django.conf.urls import url
from . import views, forms

urlpatterns = [
    url('home', views.Home.as_view(), name="Home"),
    url(r'^testingstrips/$', views.TestStripList.as_view(), name="Testing Strips"),
    url('scheduledtests', views.SceduledTestList.as_view(), name="Scheduled Tests"),
    url(r'^testingstrips/form/$', views.AddTestStripForm.as_view(), name="Test Strip Form"),
    url(r'^testingstrips/(?P<id>[0-9]{1,9})/$', views.TestStripInfo.as_view(), name="Test Strip Info"),
    url(r'^test/(?P<id>[0-9]{1,9})/$', views.TestInfo.as_view(), name="Test Info"),
    url(r'^results/$', views.GraphResultView.as_view(), name="Graph Results")
]