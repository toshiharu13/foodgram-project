from django.shortcuts import render
from django.views.generic import TemplateView


def page_not_found(request, exception=None):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


class AboutAuthor(TemplateView):
    template_name = "flatpages/about-author.html"


class AboutTech(TemplateView):
    template_name = "flatpages/about-tech.html"
