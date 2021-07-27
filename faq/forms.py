from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from faq.models import Komen, Pertanyaan,ImageUpload
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

class DocumentForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ('img',)
        labels = {
            'img': _('Images'),
        }

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name" , "email", "password1", "password2",  )

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PertanyaanForm(ModelForm):
    class Meta:
        model = Pertanyaan
        #fields = '__all__'
        #exclude = ['title']
        fields = ('pertanyaan_text',)
        #widgets = {'pertanyaan_text': Input(attrs={'cols': 100, 'rows': 1}),}
        labels = {
            'pertanyaan_text': _('Pertanyaan'),
        }
        help_texts = {
            'pertanyaan_text': _('Some useful pertanyaan help text.'),
        }
        error_messages = {
            'pertanyaan_text': {
                'max_length': _("This pertanyaan's is too long."),
            },
        }


class KomenForm(ModelForm):

    class Meta:
        model = Komen
        #fields = '__all__'
        #exclude = ['title']
        fields = ('komen_text',)
        #widgets = {'pertanyaan_text': Input(attrs={'cols': 100, 'rows': 1}),}
        labels = {
            'komen_text': _('Komen'),
        }
        help_texts = {
            'komen_text': _('Some useful komen help text.'),
        }
        error_messages = {
            'komen_text': {
                'max_length': _("This komen's is too long."),
            },
        }
