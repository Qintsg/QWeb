from django.http import JsonResponse
from django.http import HttpRequest
from django.http import HttpResponse


def healthcheck(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"status": "ok", "service": "qweb-backend"})
