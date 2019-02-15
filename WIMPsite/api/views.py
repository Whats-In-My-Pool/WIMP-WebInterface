from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from WIMPsite.models import *
import datetime

import json

class TestAPI(View):
    def get(self, request, action):
        get = request.GET

        if action == "scheduled_tests":
            j = json.loads(serializers.serialize("json", ScheduledTest.objects.all()))
        elif action == "test_strip":
            if "pk" in get:
                strip = TestStrip.objects.get(pk=get["pk"])

                j = json.loads(serializers.serialize("json", strip.tests.all()))
            else:
                j = []
        else:
            j = {"error": "{} not found".format(action)}

        return JsonResponse(j, safe=False)

    def post(self, request, action):
        body = request.body.decode('utf8')
        body = json.loads(body)

        if action == "report_test":
            if "scheduled_test_pk" in body:
                test_run = ScheduledTest.objects.get(pk=body["scheduled_test_pk"])
                test_run.last_run = datetime.datetime.fromtimestamp(body["time_stamp"])
                test_run.save()

                for result in body["results"]:
                    chemical_test_pk = result["pk"]
                    r = result["r"]
                    g = result["g"]
                    b = result["b"]
                    color_match = TestResult.get_color_match(chemical_test_pk, r, g, b)

                    TestResult.objects.create(chemical_test_id=chemical_test_pk, r=r, g=g, b=b, color_match=color_match,
                                              time_run=test_run.last_run)

                return HttpResponse("Success")

        return HttpResponse("Fail")

class SettingsAPI(View):
    def get(self, request):
        get = request.GET

