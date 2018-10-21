from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# Create your views here.
def test403(request):
    if request.method == 'GET':
        return HttpResponse('Nothing Here', status=403)


def homepage(request):
    if request.method == 'GET':
        return HttpResponse('// TODO: MAKE HOMEPAGE ')