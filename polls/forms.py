'''
class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
'''
from polls.models import Question
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        #fields = '__all__'
        #exclude = ['title']
        fields = ('question_text',)
        #widgets = {'question_text': Input(attrs={'cols': 100, 'rows': 1}),}
        labels = {
            'question_text': _('Question'),
        }
        help_texts = {
            'question_text': _('Some useful question help text.'),
        }
        error_messages = {
            'question_text': {
                'max_length': _("This question's is too long."),
            },
        }

    