from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test(request):
    if request.method == 'GET':
        return HttpResponse('Sup')


def homepage(request):
    if request.method == 'GET':
        return HttpResponse('// TODO: MAKE HOMEPAGE ')