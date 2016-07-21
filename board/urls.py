"""board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from user_auth.views import custom_login #, reset_pwd
from boardapp.views import IndexView, MessageList, show_genres, show_notices, NoticeList

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^board/$', show_notices, name='board'),
    url(r'^genres/$', NoticeList.as_view(), name='genres'),

    # User Related urls
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'index'}, name='auth_logout'),
    url(r'^users/login/$', custom_login, name='auth_login'),

    url(r'^register/complete/$', RedirectView.as_view(pattern_name='board'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # Social Auth Related urls
    url('^social/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^admin/', admin.site.urls),
]
