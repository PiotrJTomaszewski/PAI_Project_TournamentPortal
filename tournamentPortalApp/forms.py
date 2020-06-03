from django.forms import ModelForm
from django.forms.fields import SplitDateTimeField
from django.forms.widgets import SplitDateTimeWidget, DateInput, TimeInput

from .models import Tournament

class TournamentCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TournamentCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tournament
        fields = '__all__'
        widgets = {
            # 'start_date': SplitDateTimeWidget()
        }
