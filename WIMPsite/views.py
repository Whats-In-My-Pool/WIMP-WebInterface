from django.shortcuts import render, reverse, redirect, HttpResponse
from WIMPsite.models import *
from django.views.generic import View
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
import pytz

from WIMPsite.forms import TestStripForm, ColorForm
from WIMPsite.plot import plot_graph


# Create your views here.
class Home(View):

    def get(self, request):
        context = {"active": "Home"}
        try:
            latest_test = ScheduledTest.objects.filter(current_test=True).latest('last_run')

            results = []

            for test in latest_test.test_strip.tests.all():
                result = test.results.latest('time_run')

                results.append(result)

            context["results"] = results
            time = latest_test.last_run
            local_tz = pytz.timezone(getattr(settings, "TIMEZONE", "America/Chicago"))
            time = time.astimezone(local_tz)
            context["test_run"] = time.strftime("%A %B %d at %_I:%M %p")
            context["DEBUG"] = getattr(settings, "DEBUG", False)
        except (AttributeError, TestResult.DoesNotExist):
            context["results_not_found"] = True

        return render(request, 'WIMPsite/home.html', context=context)


class TestStripList(generic.ListView):
    model = TestStrip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "Testing Strips"
        return context


class SceduledTestList(generic.ListView):
    model = ScheduledTest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "Scheduled Tests"
        return context


class AddTestStripForm(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        get = request.GET

        form = TestStripForm()

        context = {
            "form": form
        }

        return render(request, 'WIMPsite/teststrip_form.html', context=context)

    def post(self, request):
        post = request.POST
        form = TestStripForm(post)

        if form.is_valid():
            strip = form.save()
            return redirect(reverse('Test Strip Info', kwargs={"id": strip.pk}))
        else:
            return HttpResponse("error")


class TestInfo(View):
    @method_decorator(csrf_protect)
    def get(self, request, id):
        get = request.GET

        test = ChemicalTest.objects.get(pk=id)

        colors = Color.objects.filter(test_id=id).all()

        form = ColorForm(initial={"test": test})

        context = {
            "form": form,
            "test": test,
            "colors": colors
        }

        return render(request, 'WIMPsite/test_info.html', context=context)

    def post(self, request, id):
        post = request.POST
        form = ColorForm(post)

        if form.is_valid():
            color = form.save()
            return redirect(reverse('Test Info', kwargs={"id": id}))
        else:
            return HttpResponse("error")


class TestStripInfo(View):

    def get(self, request, id):
        strip = TestStrip.objects.get(pk=id)

        tests = strip.tests.all()

        context = {"tests": tests,
                   "strip": strip}

        return render(request, "WIMPsite/teststrip_info.html", context=context)

    def post(self, request, id):
        post = request.POST

        current_test = ScheduledTest.objects.filter(current_test=True).all()

        for test in current_test:
            test.current_test = False
            test.save()

        if not ScheduledTest.objects.filter(test_strip_id=id).exists():
            ScheduledTest.objects.create(test_strip_id=id, frequency=7, scale="d", current_test=True)
        else:
            test = ScheduledTest.objects.get(test_strip_id=id)
            test.current_test = True
            test.save()

        return redirect(reverse('Test Strip Info', kwargs={"id": id}))



class GraphResultView(View):
    def get(self, request):

        strip_results = []

        for test_strip in TestStrip.objects.all():
            plots = []
            tests = test_strip.tests.all()

            for test in tests:
                x = []
                y = []
                for result in test.results.all():
                    local_tz = pytz.timezone(getattr(settings, "TIMEZONE", "America/Chicago"))

                    time = result.time_run.astimezone(local_tz)
                    x.append(time.strftime("%y-%m-%d %T"))
                    y.append(result.color_match.unit_value)

                plot = plot_graph(x, y, test.name)

                plots.append(plot)

            strip_ctx = {
                "strip": test_strip,
                "plots": plots
            }

            strip_results.append(strip_ctx)

        context = {
            "strips": strip_results,
            "active": "Test Results"
        }

        return render(request, "WIMPsite/results.html", context=context)
