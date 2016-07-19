from django.shortcuts import render
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('board'))
    else:
        return login(request)