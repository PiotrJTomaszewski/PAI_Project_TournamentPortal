from django import forms
from django.forms.fields import SplitDateTimeField
from django.forms.widgets import DateInput, TimeInput, MultiWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
import django.contrib.auth as auth
from django.core.exceptions import ValidationError

from .models import *


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
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email.widget.attrs.update({"class": "form-control"})
    user = None

    def clean(self):
        clean_data = super(PortalUserLoginForm, self).clean()
        email = clean_data['email']
        password = clean_data['password']
        self.user = auth.authenticate(email=email, password=password)
        if self.user is None:
            self.add_error('password', _('Wrong email or password!'))
        return clean_data

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
        for field_name in self.base_fields:
            self.base_fields[field_name].widget.attrs.update(
                {"class": "form-control"})
        super(TournamentCreateForm, self).__init__(*args, **kwargs)
        self.fields['entry_limit'].widget.attrs['min'] = 3
        self.fields['description'].widget.attrs['maxlength'] = 512
        self.fields['prizes'].widget.attrs['maxlength'] = 512
        self.fields['location_lat'].help_text = 'Double click to open a map'
        self.fields['location_long'].help_text = 'Double click to open a map'

    def clean(self):
        clean_data = super(TournamentCreateForm, self).clean()
        event_start_date = clean_data.get('event_start_date')
        entry_deadline = clean_data.get('entry_deadline')
        if event_start_date is None or entry_deadline is None:
            return clean_data
        if event_start_date < entry_deadline:
            raise ValidationError(
                _("Entry deadline must be before the event start date"))
        return clean_data

    def clean_entry_deadline(self):
        entry_deadline = self.cleaned_data['entry_deadline']
        if self.initial.entry_deadline is not None and self.initial.entry_deadline != entry_deadline:
            raise ValidationError(_("Entry deadline cannot be changed"))
        if entry_deadline < datetime.now(tz=entry_deadline.tzinfo):
            raise ValidationError(_("Entry deadline cannot be in the past"))
        return entry_deadline

    def clean_event_start_date(self):
        event_start_date = self.cleaned_data['event_start_date']
        if event_start_date < datetime.now(tz=event_start_date.tzinfo):
            raise ValidationError(_("You can't add a past event"))
        return event_start_date

    def clean_entry_limit(self):
        entry_limit = self.cleaned_data['entry_limit']
        if entry_limit < 3:
            raise ValidationError(_('Entry limit should be at least 3'))
        return entry_limit

    class Meta:
        model = Tournament
        fields = ('name', 'event_start_date', 'entry_deadline', 'entry_limit',
                  'organiser_name', 'location_lat', 'location_long', 'location_details', 'game_format', 'deck_format', 'description', 'prizes')


class SponsorCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['name'].widget.attrs.update({'class': 'form-control'})
        self.base_fields['logo'].widget.attrs.update({'class': 'form-control'})
        super(SponsorCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sponsor
        fields = ('name', 'logo')


class ParticipantCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['license_number'].widget.attrs.update({'class': 'form-control'})
        self.base_fields['current_ranking'].widget.attrs.update({'class': 'form-control'})
        super(ParticipantCreateForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Participant
        fields = ('license_number', 'current_ranking')
