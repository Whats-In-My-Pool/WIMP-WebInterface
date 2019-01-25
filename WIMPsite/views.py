from django.shortcuts import render, reverse, redirect, HttpResponse
from WIMPsite.models import *
from django.views.generic import View
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from WIMPsite.forms import TestStripForm, ChemicalTestForm, ColorForm


# Create your views here.
class Home(View):

    def get(self, request):

        test_profile_count = TestStrip.objects.count()

        context = {
            "test_profile_count": test_profile_count,
            "active": "Home"
        }

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

        form = ChemicalTestForm(initial={"test": strip})

        context = {"tests": tests,
                   "strip": strip,
                   "form": form}

        return render(request, "WIMPsite/teststrip_info.html", context=context)

    def post(self, request, id):
        post = request.POST
        form = ChemicalTestForm(post)
        if form.is_valid():
            form.save()
            return redirect(reverse('Test Strip Info', kwargs={"id": id}))
        else:
            return HttpResponse("error")
