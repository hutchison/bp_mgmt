"""bp_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login

from bp_setup.forms import BPAuthenticationForm

admin.site.site_header = 'Administration: BP Allgemeinmedizin'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^setup/', include('bp_setup.urls', namespace='bp_setup')),
    url(r'^info/', include('django.contrib.flatpages.urls')),
    url(r'^/?', include('bp_cupid.urls', namespace='bp_cupid')),
    url(r'^login/$', login,
        {'authentication_form': BPAuthenticationForm},
        name='login',
    ),
    url('^', include('django.contrib.auth.urls')),
]
