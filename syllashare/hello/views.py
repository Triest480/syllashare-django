from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1> Hello World <h1>")


def homepage(request):
    return HttpResponse("<h1> Home Page <h1> <a href=http://127.0.0.1:8000/hello>Button<a/>")