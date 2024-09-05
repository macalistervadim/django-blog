from django.http import HttpRequest, HttpResponse
import django.shortcuts


def homepage(request: HttpRequest) -> HttpResponse:
    return django.shortcuts.render(
        request=request,
        template_name="homepage/homepage.html",
    )
