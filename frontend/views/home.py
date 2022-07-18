from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string


class Home(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return HttpResponse(render_to_string("home.html"))
