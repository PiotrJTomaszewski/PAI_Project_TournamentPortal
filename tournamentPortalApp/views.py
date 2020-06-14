from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, FormView, UpdateView, TemplateView
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q

from libgravatar import Gravatar

from .models import Tournament, Sponsor, PortalUser
from .forms import *
from .helpers import formErrorsToMessage
from .tokens import account_token
from .mail import sendRegisterConfirmationMail, sendPasswordResetMail
from .background import pair_participants_up

# def index(request):
#     context = {
#     }
#     uuid=Tournament.objects.filter(name='Lorem Ipsum')[0].uuid
#     pair_participants_up.now(uuid) #TODO: Queue this
#     return render(request, 'tournaments/index.html', context)

class PortalUserRegister(UserPassesTestMixin, FormView):
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
        messages.add_message(self.request, messages.SUCCESS,
                             "We've sent an activation link to your email.")
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'Can\'t sign up when logged in')
        return redirect(reverse('tournamentList'))


def portalUserActivate(request, uuid_base64, token):
    try:
        uuid = force_text(urlsafe_base64_decode(uuid_base64))
        user = PortalUser.objects.get(uuid=uuid)
    except:
        user = None
    if user is not None and account_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "Account activated")
    else:
        messages.add_message(request, messages.ERROR,
                             "Activation link is invalid")
    return redirect(reverse('index'))


class PortalUserLogin(UserPassesTestMixin, FormView):
    model = PortalUser
    form_class = PortalUserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('tournamentList')
    
    def form_valid(self, form):
        # Called if valid data was posted
        user = form.user
        auth.login(self.request, user)
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'Already logged in')
        return redirect(reverse('tournamentList'))

class PortalUserPasswordForgotten(FormView):
    form_class = PortalUserPasswordForgottenForm
    template_name = 'users/password_forgotten.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        try:
            user = PortalUser.objects.get(email=form.cleaned_data['email'])
            if user is not None:
                sendPasswordResetMail(self.request, user)
        except:  # Ignoring errors, we don't want to inform the user wheter he gave us a correct email anyway
            pass
        messages.add_message(self.request, messages.SUCCESS,
                             "If you gave us a correct email you'll receive password reset instructions.")
        return super().form_valid(form)


def portalUserResetPassword(request, uuid_base64, token):
    try:
        uuid = force_text(urlsafe_base64_decode(uuid_base64))
        user = PortalUser.objects.get(uuid=uuid)
    except:
        user = None
    if user is not None and account_token.check_token(user, token):
        if request.method == 'POST':
            form = auth.forms.SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                auth.update_session_auth_hash(request, form.user)
                messages.add_message(
                    request, messages.SUCCESS, "Password changed")
                return redirect(reverse('index'))
            else:
                messages.add_message(
                    request, messages.ERROR, 'Something went wrong')
                return render(request, 'users/password_reset.html', {'form': form})
        else:
            form = auth.forms.SetPasswordForm(user)
            form.fields['new_password1'].widget.attrs.update(
                {"class": "form-control"})
            form.fields['new_password2'].widget.attrs.update(
                {"class": "form-control"}
            )
            return render(request, 'users/password_reset.html', {'form': form})
    else:
        messages.add_message(request, messages.ERROR,
                             "Activation link is invalid")
        return redirect(reverse('index'))


def portalUserLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, "Logged out")
    return redirect('/')


class PortalUserDashboard(LoginRequiredMixin, DetailView):
    template_name = 'users/dashboard.html'
    model = PortalUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournaments_organised_by_me'] = Tournament.objects.filter(
            creator=self.request.user)
        context['tournaments_comming_up'] = Participant.objects.filter(user=self.request.user, tournament__event_start_date__gte=datetime.now()).select_related('tournament')
        context['tournaments_past'] = Participant.objects.filter(user=self.request.user, tournament__event_start_date__lte=datetime.now()).select_related('tournament')
        return context


class TournamentList(ListView):
    template_name = 'tournaments/list.html'
    model = Tournament
    paginate_by = 10
    context_object_name = 'tournaments'
    queryset = Tournament.objects.filter(event_start_date__gte=datetime.now()).order_by('entry_deadline')


class TournamentDetail(DetailView):
    template_name = 'tournaments/details.html'
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        participants = Participant.objects.filter(tournament=tournament.uuid).order_by('current_ranking')
        context['sponsors'] = Sponsor.objects.filter(
            tournament=tournament.uuid)
        context['can_participate'] = (tournament.entry_deadline >= datetime.now(tz=tournament.entry_deadline.tzinfo)) and\
            (tournament.entry_limit - tournament.current_participant_no > 0) and\
            not (self.request.user.is_authenticated and Participant.objects.filter(
                user=self.request.user, tournament=tournament).exists())
        context['participants'] = participants
        context['is_creator'] = self.request.user.is_authenticated and tournament.creator.uuid == self.request.user.uuid
        return context


def tournamentMatchesJson(request, pk):
    matches = Match.objects.filter(tournament=pk).order_by('-tournament_round', 'pair_no')
    data = list(matches.values(
        'tournament_round',
        'pair_no',
        'winner',
        'participant_zero__user__first_name',
        'participant_zero__user__last_name',
        'participant_zero__user__email',
        'participant_one__user__first_name',
        'participant_one__user__last_name',
        'participant_one__user__email'
        ))
    for entry in data:
        email = entry['participant_zero__user__email']
        if email is not None:
            entry['participant_zero__user__gravatar'] = Gravatar(email).get_image(size=80, default='retro')
        else:
            entry['participant_zero__user__gravatar'] = ''
        del entry['participant_zero__user__email'] # Don't send email addresses to users
        email = entry['participant_one__user__email']
        if email is not None:
            entry['participant_one__user__gravatar'] = Gravatar(email).get_image(size=80, default='retro')
        else:
            entry['participant_one__user__gravatar'] = ''
        del entry['participant_one__user__email']
    return JsonResponse(data, safe=False)


# @login_required
# def matchAddResult(request, tournament_pk):
#     participant = get_object_or_404(Participant, user=request.user, tournament__uuid=tournament_pk)
#     if request.method == 'GET':
#         matches = Match.objects.filter(Q(participant_zero=participant) | Q(participant_one=participant)).order_by('-tournament_round')
#         if matches and len(matches) > 0:
#             match = matches[0]
#             if match.winner is not None:
#                 messages.add_message(request, messages.ERROR, 'Winner of this match was already chosen')
#                 return reverse('tournamentDetail', kwargs={'pk': tournament_pk})
#             if (match.participant_zero == participant and match.winner_by_part_zero is None) or (match.participant_one == participant and match.winner_by_part_one is None):
#                     context = {}
#                     context['match_id'] = match.id
#                     lookup = ['Winner', 'Final', 'Semifinals', 'Quarterfinals', 'Eighth-finals', '16th-finals', '32nd-finals', '64th-finals']
#                     if match.tournament_round < len(lookup):
#                         round_no = lookup[match.tournament_round]
#                     else:
#                         round_no = '{} round'.format(match.tournament_round)
#                     context['round_no'] = round_no
#                     context['part_zero'] = {
#                         'id': match.participant_zero.id,
#                         'name': ' '.join([match.participant_zero.user.first_name, match.participant_zero.user.last_name]),
#                         'gravatar': Gravatar(match.participant_zero.user.email).get_image(size=80, default='retro')
#                     }
#                     context['part_one'] = {
#                         'id': match.participant_one.id,
#                         'name': ' '.join([match.participant_one.user.first_name, match.participant_one.user.last_name]),
#                         'gravatar': Gravatar(match.participant_one.user.email).get_image(size=80, default='retro')
#                     }
#                     return render(request, 'matches/add_result.html', context=context)
#     elif request.method == 'POST':
#         try:
#             chosen_winner_id = int(request.POST['winner_by_part'])
#             with transaction.atomic():
#                 match = Match.objects.select_for_update().get(id=request.POST['match_id'])
#                 chosen_winner = Participant.get(id=chosen_winner_id)
#                 if match.participant_zero == chosen_winner or match.participant_one != chosen_winner:
#                     raise Exception 
#                 if match.winner is None:
#                     if match.participant_zero.user == request.user and match.winner_by_part_zero == None:
#                         match.winner_by_part_zero = chosen_winner
#                     elif match.participant_one.user == request.user and match.winner_by_part_one == None:
#                         match.winner_by_part_one = chosen_winner
#                     if match.winner_by_part_zero is not None and match.winner_by_part_one is not None:
#                         if match.winner_by_part_zero == match.winner_by_part_one:
#                             match.winner = match.winner_by_part_zero
#                             next_part_no = match.pair_no % 2
#                             next_round_match = Match.objects.
#                         else:
#                             match.winner_by_part_zero = None
#                             match.winner_by_part_one = None
#                 else:
#                     raise Exception
#         except Exception:
#             pass
#     messages.add_message(request, messages.ERROR, 'Something went wrong')
#     return reverse('tournamentDetail', kwargs={'pk': tournament_pk})

class TournamentCreate(LoginRequiredMixin, FormView):
    template_name = 'tournaments/create_edit.html'
    form_class = TournamentCreateForm

    def form_valid(self, form):
        tournament = form.save(commit=False)
        tournament.creator = self.request.user
        tournament.current_participant_no = 0
        tournament.save()
        pair_participants_up(tournament.uuid.hex, schedule=tournament.entry_deadline)
        self.success_url = reverse_lazy(
            'tournamentDetail', kwargs={'pk': tournament.uuid})
        return super().form_valid(form)

class TournamentEdit(UserPassesTestMixin, FormView):
    template_name = 'tournaments/create_edit.html'
    form_class = TournamentCreateForm

    def get_form(self):
        tournament = get_object_or_404(Tournament, uuid=self.kwargs['pk'])
        return self.form_class(instance=tournament, **self.get_form_kwargs())

    def test_func(self):
        try:
            tournament = Tournament.objects.get(uuid=self.kwargs['pk'])
            test_result = (self.request.user is not None and tournament.creator == self.request.user)
        except:
            test_result = False
        return test_result

    def form_valid(self, form):
        tournament = form.save()
        self.success_url = reverse('tournamentDetail', kwargs={
                            'pk': tournament.uuid})
        return super().form_valid(form)


class SponsorCreate(UserPassesTestMixin, FormView):
    template_name = 'tournaments/sponsors/create.html'
    form_class = SponsorCreateForm

    def test_func(self):
        try:
            tournament = Tournament.objects.get(uuid=self.kwargs['pk'])
            test_result = (self.request.user is not None and tournament.creator == self.request.user)
        except:
            test_result = False
        return test_result

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR,
                             'Permission denied!')
        return redirect(reverse('tournamentDetail', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        sponsor = form.save(commit=False)
        sponsor.tournament = get_object_or_404(
            Tournament, pk=self.kwargs['pk'])
        sponsor.save()
        messages.add_message(self.request, messages.SUCCESS, 'Sponsor added')
        self.success_url = reverse('tournamentDetail', kwargs={
                                   'pk': self.kwargs['pk']})
        return super().form_valid(form)


class ParticipantCreate(LoginRequiredMixin, FormView):
    template_name = 'tournaments/participate.html'
    form_class = ParticipantCreateForm

    class AlreadyParticipantError(Exception):
        pass

    class FullParticipantsError(Exception):
        pass

    class NoTournamentError(Exception):
        pass

    class TooLateError(Exception):
        pass

    class LicenseNoDuplicateError(Exception):
        pass

    class RankingDuplicateError(Exception):
        pass

    def get_context_data(self, **kwargs):
        tournament = get_object_or_404(Tournament, uuid=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['tournament'] = tournament
        return context

    def form_valid(self, form):
        self.success_url = reverse('tournamentDetail', kwargs={
                                   'pk': self.kwargs['pk']})
        try:
            with transaction.atomic():  # Disable autocommit
                # Acquire lock
                tournaments = Tournament.objects.select_for_update().filter(
                    uuid=self.kwargs['pk'])
                if tournaments is None or len(tournaments) != 1:
                    raise self.NoTournamentError
                tournament = tournaments[0]
                # Check if user wasn't a participant already (to show him a proper message)
                if Participant.objects.filter(
                    user=self.request.user, tournament=tournament).exists():
                    raise self.AlreadyParticipantError
                if Participant.objects.filter(
                    tournament=tournament,
                    license_number=form.cleaned_data['license_number']
                ).exists():
                    raise self.LicenseNoDuplicateError
                if Participant.objects.filter(
                    tournament=tournament,
                    current_ranking=form.cleaned_data['current_ranking']
                ).exists():
                    raise self.RankingDuplicateError
                if tournament.entry_deadline < datetime.now(tz=tournament.entry_deadline.tzinfo):
                    raise self.TooLateError
                if tournament.entry_limit - tournament.current_participant_no > 0:
                    participant = form.save(commit=False)
                    participant.user = self.request.user
                    participant.tournament = tournament
                    participant.save()
                    tournament.current_participant_no = tournament.current_participant_no + 1
                    tournament.save()
                    messages.add_message(self.request, messages.SUCCESS, "You're a participant now")
                else:
                    raise self.FullParticipantsError
        except self.NoTournamentError:
            messages.add_message(self.request, messages.ERROR,
                                 "This tournament doesn't exist")
        except self.AlreadyParticipantError:
            messages.add_message(self.request, messages.ERROR,
                                 "You're already a participant")
        except self.TooLateError:
            messages.add_message(
                self.request, messages.ERROR, "Entry deadline expired")
        except self.LicenseNoDuplicateError:
            messages.add_message(
                self.request, messages.ERROR, "Participant with this license number already exists"
            )
        except self.RankingDuplicateError:
            messages.add_message(
                self.request, messages.ERROR, "Participant with this ranking already exists"
            )
        except self.FullParticipantsError:
            messages.add_message(
                self.request, messages.ERROR, "Maximum number of participants reached"
            )
        except:
            messages.add_message(
                self.request, messages.ERROR, "Something went wrong")
        return super().form_valid(form)

def debugForcePairUp(request, uuid):
    pair_participants_up.now(uuid.hex)
