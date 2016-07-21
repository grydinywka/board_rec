from django.shortcuts import render
from django import forms
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Message, Genre, Notice


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
    return render(request, "genres.html", {'nodes': Genre.objects.all()})

class NoticeForm(forms.ModelForm):
    """form for add/edit form"""
    class Meta:
        model = Notice
        fields = ['content']

    content =forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your message here!",
                                     'cols': 100,})
    )

def show_notices(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)

        if request.POST.get('add_message'):
            data = {}

            if form.is_valid():
                data['content'] = form.cleaned_data['content']
                # data['']
                try:
                    notice = Notice(**data)
                    notice.save()
                except Exception as e:
                    messages.error(request, 'Error during adding message!' + str(e))
                else:
                    messages.success(request, 'Message was added successful!')
                return HttpResponseRedirect(reverse('board'))
            else:
                messages.info(request, 'Validation errors!')
            return render(request, 'board.html', {'form': form, 'notices': Notice.objects.all()})
    else:
        form = NoticeForm()

    return render(request, "board.html", {'form': form, 'notices': Notice.objects.all()})

class NoticeList(ListView):
    model = Notice
    queryset = Notice.objects.all()
    template_name = 'board.html'
    context_object_name = 'notices'
