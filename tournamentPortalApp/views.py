from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, FormView
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login

from .models import Tournament, Sponsor, PortalUser
from .forms import TournamentCreateForm, PortalUserCreationForm, PortalUserChangeForm, PortalUserLoginForm, SponsorCreateForm
from .helpers import formErrorsToMessage
from .tokens import account_activation_token
from .mail import sendRegisterConfirmationMail

def index(request):
    context = {
    }
    return render(request, 'tournaments/index.html', context)

class portalUserRegister(FormView):
    model = PortalUser
    form_class = PortalUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('tournamentList')

    def form_valid(self, form):
        # Called if valid data was posted
        user = form.save(commit=False)
        user.is_active = False
        user.is_admin = False
        user.is_dummy = False
        user.save()
        sendRegisterConfirmationMail(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, "Successfully registered. We've sent an activation link to your email")
        return super().form_valid(form)

def portalUserActivate(request, uuid_base64, token):
    try:
        uuid = force_text(urlsafe_base64_decode(uuid_base64))
        user = PortalUser.objects.get(uuid=uuid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "Account activated")
    else:
        messages.add_message(request, messages.ERROR, "Activation link is invalid")
    return redirect(reverse('index'))




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
        tournament = self.object
        context['sponsors'] = Sponsor.objects.filter(tournament=tournament.id)
        if self.request.user.is_authenticated and tournament.creator.id == self.request.user.id:
            context['is_creator'] = True
        else:
            context['is_creator'] = False
        return context

@login_required
def tournamentCreate(request):
    form = TournamentCreateForm()
    return render(request, 'tournaments/create.html', {'form': form})

@login_required
def tournamentCreateRequest(request):
    if request.method == 'POST':
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            formErrorsToMessage(form, request)
    return redirect('/tournaments')

def sponsorCreate(request, tournament_id):
    form = SponsorCreateForm
    return render(request, 'tournaments/sponsors/create.html', {'form': form, 'tournament_id': tournament_id})

def sponsorCreateRequest(request, tournament_id):
    form = SponsorCreateForm(request.POST, request.FILES)
    print(request.FILES['logo'])
    if form.is_valid():
        instance = form.save()
        messages.add_message(request, messages.SUCCESS, 'Sponsor sucessfully added')
        return redirect('/tournaments/{}'.format(tournament_id))
    messages.add_message(request, messages.ERROR, 'Something went wrong')
    return redirect('/')

def userLogin(request):
    if not request.user.is_authenticated:
        form = PortalUserLoginForm()
        return render(request, 'users/login.html', {'form': form})
    messages.add_message(request, messages.INFO, 'You are already signed in')
    return redirect('/')

def userLoginRequest(request):
    if request.method == 'POST':
        form = PortalUserLoginForm(request.POST)
        if form.is_valid():
            email = form.data.get('email')
            password = form.data.get('password')
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return redirect('/')
            messages.add_message(request, messages.ERROR, 'Failed to authenticate')
            return redirect('/users/login')
        else:
            formErrorsToMessage(form, request)
            return redirect('/users/login')
    messages.add_message(request, messages.ERROR, 'Something went wrong')
    return redirect('/users/login')

def userLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, "Successfully logged out")
    return redirect('/')

