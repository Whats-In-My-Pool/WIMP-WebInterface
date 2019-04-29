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
            j = json.loads(serializers.serialize("json", ScheduledTest.objects.filter(current_test=True).all()))
        elif action == "test_strip":
            if "pk" in get:
                strip = TestStrip.objects.get(pk=get["pk"])

                j = json.loads(serializers.serialize("json", strip.tests.all()))
            else:
                j = json.loads(serializers.serialize("json", TestStrip.objects.all()))
        elif action == "get_colors":
            strip = TestStrip.objects.get(pk=get["pk"])

            j = {"tests": []}
            for test in strip.tests.all():
                test_json = {}
                test_json["name"] = test.name
                test_json["colors"] = json.loads(serializers.serialize("json", test.colors.all()))

                j["tests"].append(test_json)
        else:
            j = {"error": "{} not found".format(action)}

        return JsonResponse(j, safe=False)

    def post(self, request, action):
        body = request.body.decode('utf8')
        body = json.loads(body)

        if action == "report_test":
            if "scheduled_test_pk" in body:
                test_run = ScheduledTest.objects.get(pk=body["scheduled_test_pk"])
                date = datetime.datetime.now()
                test_run.last_run = date
                test_run.save()

                for result in body["results"]:
                    chemical_test_pk = result["pk"]
                    r = result["r"]
                    g = result["g"]
                    b = result["b"]

                    TestResult.objects.create(chemical_test_id=chemical_test_pk, r=r, g=g, b=b,
                                              time_run=test_run.last_run)

                return HttpResponse("Success")
        elif action == "report_temp":
            if "temp" in body:
                TempResult.objects.create(temp=body["temp"])

                return HttpResponse("Success")
        elif action == "add_test":
            if "strip_id" in body:
                strip = TestStrip.objects.get(pk=body["strip_id"])

                chemical_test = ChemicalTest.objects.create(unit=body["unit"], name=body["strip_name"], test=strip,
                                                            region_y2=0, region_y1=0, region_x2=0, region_x1=0)

                for color in body["colors"]:
                    Color.objects.create(unit_value=color["unit_value"], text=color["text"], r=color["r"], g=color["g"],
                                         b=color["b"], test=chemical_test)

                return HttpResponse("Success")
        elif action == "add_strip":
            if "strip_name" in body:
                strip = TestStrip.objects.create(name=body["strip_name"])

                return JsonResponse({"id": strip.id})

        return HttpResponse("Fail")


class SettingsAPI(View):
    def get(self, request, action):
        get = request.GET

