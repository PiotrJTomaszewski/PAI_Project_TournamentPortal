from django import forms
from django.forms.fields import SplitDateTimeField
from django.forms.widgets import DateInput, TimeInput, MultiWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
import django.contrib.auth as auth
from django.core.exceptions import ValidationError

from .models import Tournament, PortalUser, Sponsor

class PortalUserCreationForm(UserCreationForm):
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

class PortalUserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email.widget.attrs.update({"class": "form-control"})
    user = None
    def clean_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        self.user = auth.authenticate(email=email, password=password)
        if self.user is None:
            raise ValidationError(_('Wrong email or password!'))
        return password
    class Meta:
        model = PortalUser
        fields = ['email', 'password']

class PortalUserPasswordForgottenForm(forms.Form):
    email = forms.EmailField(label="Email")
    email.widget.attrs.update({"class": "form-control"})


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