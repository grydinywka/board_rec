from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from .models import Message, Genre


class IndexView(TemplateView):
    """ view for checking: if user authenticarted then redirect him to 'board' page
        else show 'index' page
    """

    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('board'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class MessageList(ListView):
    """
    class for render list or messages
    """

    model = Message
    queryset = Message.objects.filter(parent=None).order_by('-created')
    template_name = 'board.html'
    context_object_name = 'user_messages'

def show_genres(request):
    return render_to_response("genres.html",
                          {'nodes':Genre.objects.all()},
                          context_instance=RequestContext(request))
