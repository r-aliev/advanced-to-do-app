from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone

from .models import *

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # Add bootstrap class for visible fields
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Task
        fields = ['title', 'description', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        help_texts = {
            'expiration_date': 'YYYY-MM-DD HH:MM:SS',
        }

    def clean_expiration_date(self):
        picked_date = self.cleaned_data['expiration_date']
        if picked_date:
            if timezone.now() > picked_date:
                # Impossible date seleceted
                raise forms.ValidationError('Choose time in the future')

        return picked_date



class  ShareForm(forms.Form):            
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    comment = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        #super().clean() - deqiqleshdir
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError('User with such username does not exist')
        elif email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('User with such email does not exist')
        else:
            raise forms.ValidationError('Provide username or email')

        self.user = user
        return self.cleaned_data

    @property
    def user_to_share(self):
        return getattr(self, 'user')


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # Add bootstrap class for visible fields
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
	    model = User
	    fields = ['username', 'email', 'password1', 'password2']

