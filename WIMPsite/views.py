from django.shortcuts import render
from WIMPsite.models import *
from django.views.generic import View
from django.views import generic


# Create your views here.
class Home(View):

    def get(self, request):

        test_profile_count = TestStrip.objects.count()

        context = {
            "test_profile_count": test_profile_count
        }

        return render(request, 'WIMPsite/home.html', context=context)


class TestStripList(generic.ListView):
    model = TestStrip

class SceduledTestList(generic.ListView):
    model = ScheduledTest

