from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView

from .models import Tournament, TournamentDeckFormatChoice, TournamentGameFormatChoice, TournamentLocationChoice
from .forms import TournamentCreateForm


def index(request):
    context = {
    }
    return render(request, 'tournaments/index.html', context)


class TournamentList(ListView):
    template_name = 'tournaments/list.html'
    model = Tournament
    paginate_by = 10
    context_object_name = 'tournaments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TournamentDetail(DetailView):
    template_name = 'tournaments/details.html'
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_type_text'] = TournamentLocationChoice[context['object'].location_type].value
        context['game_format_text'] = TournamentGameFormatChoice[context['object'].game_format].value
        context['deck_format_text'] = TournamentDeckFormatChoice[context['object'].deck_format].value
        return context

def tournamentCreate(request):
    if request.method == 'POST':
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            return render(request, 'tournaments/tmp.html', {'tmp_value': 'Post form ok'})
    elif request.method == 'GET':
        form = TournamentCreateForm()
        return render(request, 'tournaments/create.html', {'form': form})
    return render(request, 'tournaments/index.html', {'tmp_value': 'Nope'})
