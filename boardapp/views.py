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

from .models import Notice


class IndexView(TemplateView):
    """ view for checking: if user authenticarted then redirect him to 'board' page
        else show 'index' page
    """

    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('board'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)


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
    """for add message"""

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            'content',
            FormActions(
                Submit('add_button', 'Add message', css_class="btn btn-primary btn-lg"),
            ),
        )

        # set form field properties
        self.helper.field_class = 'col-sm-12'

    content =forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your message here!",
                                     'rows': 3}),
        label=False
    )

class CorrectNoticeForm(BaseNoticeForm):
    """class for correct message"""
    def __init__(self, *args, **kwargs):
        super(CorrectNoticeForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div(HTML("""
                    <input type="hidden" value="{{ node.id }}" name="id-node">
                """)),
            'content',
            FormActions(Submit('correct_message', 'Submit'),
                        Submit('cancel_correct_message', 'Cancel', css_class="btn btn-danger"),
                       ),

        )
        # set form field properties
        self.helper.field_class = 'col-sm-12'

    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your corrected comment here!",
                                     'rows': 2, 'id': "id_content_correct",
                                     },
                              ),
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
            FieldWithButtons('content', Submit('add_comment', 'Submit')),

        )

        # set form field properties
        self.helper.field_class = 'col-sm-offset-1 col-sm-10'

    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Write your comment here!",
                                     'rows': 1, 'id': "id_content_comment",
                                     },
                              ),
        label=False
    )


def show_notices(request):
    form, form_comment, form_correct = None, None, None

    if request.method == 'POST':
        # if we pushed 'Add button' ( added new message )
        if request.POST.get('add_button'):
            form = NoticeForm(request.POST)
            form_comment = CommentForm()
            form_correct = CorrectNoticeForm()

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

        # if was pushed button 'Add comment'
        elif request.POST.get('add_comment'):
            form = NoticeForm()
            form_comment = CommentForm(request.POST)
            form_correct = CorrectNoticeForm()

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
        elif request.POST.get('correct_message'):
            form = NoticeForm()
            form_comment = CommentForm()
            form_correct = CorrectNoticeForm(request.POST)

            if form_correct.is_valid():
                try:
                    notice = Notice.objects.get(pk=request.POST.get('id-node'))
                    notice.content = request.POST.get('content')
                    notice.save()
                except Exception as e:
                    messages.error(request, 'Error during adding message!' + str(e))
                else:
                    messages.success(request, 'Message was corrected successful!')
                return HttpResponseRedirect(reverse('board'))
            else:
                messages.info(request, 'Validation errors!')
        elif request.POST.get('cancel_correct_message'):
            messages.info(request, 'Canceled correct message!')
            return HttpResponseRedirect(reverse('board'))
    else:
        form = NoticeForm()
        form_comment = CommentForm()
        form_correct = CorrectNoticeForm()

    return render(request, "board.html", {'form': form,
                                          'form_comment': form_comment,
                                          'form_correct': form_correct,
                                          'notices': Notice.objects.all()})

class NoticeList(ListView):
    model = Notice
    queryset = Notice.objects.all()
    template_name = 'board.html'
    context_object_name = 'notices'
