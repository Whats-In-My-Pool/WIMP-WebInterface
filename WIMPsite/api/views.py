from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core import serializers
from WIMPsite.models import *

import json


from WIMPsite.models import ScheduledTest


class TestAPI(View):
    def get(self, request, action):
        get = request.GET

        if action == "current_tests":
            j = json.loads(serializers.serialize("json", ScheduledTest.objects.all()))
        else:
            j = {"error": "{} not found".format(action)}

        return JsonResponse(j, safe=False)

    def post(self, request, action):
        post = request.POST

        if action == "report_test":
            if "model" in post:
                if post["model"] == "WIMPsite.scheduledtest":
                    test = ScheduledTest.objects.get(pk=post["pj"])
                    test.last_run(post["last_run"])






class SettingsAPI(View):
    def get(self, request):
        get = request.GET

