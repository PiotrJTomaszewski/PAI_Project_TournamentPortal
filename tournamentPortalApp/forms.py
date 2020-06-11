from django import forms
from django.forms.fields import SplitDateTimeField
from django.forms.widgets import DateInput, TimeInput, MultiWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from .models import Tournament, PortalUser, Sponsor

class PortalUserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email.widget.attrs.update({"class": "form-control"})
    class Meta:
        model = PortalUser

class PortalUserCreationForm(UserCreationForm):
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     raise ValidationError(_('asd'))
    #     return data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = PortalUser
        fields = ['email', 'first_name', 'last_name']


class PortalUserChangeForm(UserChangeForm):
    class Meta:
        model = PortalUser
        fields = ['email', 'first_name', 'last_name']

class TournamentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TournamentCreateForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super().is_valid()

    class Meta:
        model = Tournament
        fields = '__all__'
        # widgets = {
        #     'event_date': CustomDateTimeWidget
        # }

class SponsorCreateForm(forms.ModelForm):
    def is_valid(self):
        return True

    class Meta:
        model = Sponsor
        fields = '__all__'