"""syllashare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from syllatokens.views import exchange_google_code, reassign_google_token
from user_data.views import modify_user, get_user, get_schools
from django.urls import path, re_path
from django.views.generic import TemplateView

from default_views.views import homepage
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/exchangegoogle', exchange_google_code),
    path(r'api/reassigngoogle', reassign_google_token),
    path(r'api/modifyuser', modify_user),
    path(r'api/getuser', get_user),
    path(r'api/getschools', get_schools),
    path(r'.well-known/pki-validation/873AA6D2DC9DCEC192C6E5458A29C688.txt', TemplateView.as_view(template_name='.well-known/pki-validation/873AA6D2DC9DCEC192C6E5458A29C688.txt')),
    path(r'css/react-big-calendar.css', TemplateView.as_view(template_name='css/react-big-calendar.css')),
    path(r'favicon.ico', TemplateView.as_view(template_name='favicon.ico')),
    path(r'serviceworker.js', TemplateView.as_view(template_name='serviceworker.js')),
    re_path('.*', TemplateView.as_view(template_name='index.html'))
]
