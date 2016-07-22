from django.shortcuts import render
from django import forms
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Fieldset, HTML, ButtonHolder, MultiField, Hidden
from crispy_forms.bootstrap import FormActions, PrependedText, AppendedText, FieldWithButtons, StrictButton

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


class BaseNoticeForm(forms.ModelForm):
    """base class for add/edit form"""
    class Meta:
        model = Notice
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(BaseNoticeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('board')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True


class NoticeForm(BaseNoticeForm):
    """for add/edit message"""

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            'content',
            FormActions(
                Submit('add_button', u'add message', css_class="btn btn-primary "),
            ),
        )

        # set form field properties
        self.helper.field_class = 'col-sm-12'

    content =forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your message here!",
                                     'rows': 3}),
        label=False
    )

class CommentForm(BaseNoticeForm):
    """ form for comment messages """

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div(HTML("""
                    <input type="hidden" value="{{ node.id }}" name="id-node">
                """)),
            FieldWithButtons('content', Submit('add_comment', u'Submit', css_class="btn btn-info ")),

        )

        # set form field properties
        self.helper.field_class = 'col-sm-8'

    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your comment here!",
                                     'rows': 1},
                              ),
        label=False
    )


def show_notices(request):
    form, form_comment = None,None

    if request.method == 'POST':

        if request.POST.get('add_button'):
            form = NoticeForm(request.POST)
            form_comment = CommentForm()

            if form.is_valid():
                try:
                    notice = form.save(commit=False)
                    notice.user = request.user
                    notice.save()
                except Exception as e:
                    messages.error(request, 'Error during adding message!' + str(e))
                else:
                    messages.success(request, 'Message was added successful!')
                return HttpResponseRedirect(reverse('board'))
            else:
                messages.info(request, 'Validation errors!')
            # return render(request, 'board.html', {'form': form, 'form_comment': form_comment, 'notices': Notice.objects.all()})

        # if was pushed button 'Add comment'
        elif request.POST.get('add_comment'):
            form = NoticeForm()
            form_comment = CommentForm(request.POST)

            if form_comment.is_valid():
                try:
                    notice = form_comment.save(commit=False)
                    notice.user = request.user
                    notice.parent = Notice.objects.get(pk=request.POST.get('id-node'))
                    notice.save()
                except Exception as e:
                    messages.error(request, 'Error during adding message!' + str(e))
                else:
                    messages.success(request, 'Comment was added successful!')
                return HttpResponseRedirect(reverse('board'))
            else:
                messages.info(request, 'Validation errors!')
    else:
        form = NoticeForm()
        form_comment = CommentForm()

    return render(request, "board.html", {'form': form, 'form_comment': form_comment, 'notices': Notice.objects.all()})

class NoticeList(ListView):
    model = Notice
    queryset = Notice.objects.all()
    template_name = 'board.html'
    context_object_name = 'notices'
