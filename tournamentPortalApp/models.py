from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxLengthValidator

from enum import Enum
import uuid

from .helpers import makeThumbnail

fs = FileSystemStorage()

# This user is meant to take ownership of some of the orphaned objects.
# We wan't to preserve for example the past tournaments history.


def getUserDeleted():
    return get_user_model().objects.get(id=2)


class PortalUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, is_active=False, is_admin=False):
        if not email or not first_name or not last_name or not password:
            raise ValueError('Some fields are empty!')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, is_active=True, is_admin=True):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class PortalUser(AbstractBaseUser):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = PortalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'is_active', 'is_admin']

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Tournament(models.Model):
    class TournamentGameFormatChoice(models.TextChoices):
        STANDARD = 'std', _("Standard")
        WILD = 'wld', _("Wild")

    class TournamentDeckFormatChoice(models.TextChoices):
        SINGLE_DECK = 'sin', _("Single-deck")
        MULTIPLE_DECK = 'mul', _("Multiple-deck")

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Event name", max_length=100)
    entry_deadline = models.DateTimeField()
    entry_limit = models.PositiveSmallIntegerField()
    current_participant_no = models.PositiveSmallIntegerField()
    event_start_date = models.DateTimeField()
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.SET(getUserDeleted))
    organiser_name = models.CharField(max_length=50)
    location_lat = models.DecimalField(
        'Location Latitude', max_digits=9, decimal_places=5)
    location_long = models.DecimalField(
        'Location Longitude', max_digits=9, decimal_places=5)
    location_details = models.CharField(max_length=100)
    game_format = models.CharField(
        max_length=3, choices=TournamentGameFormatChoice.choices)
    deck_format = models.CharField(
        max_length=3, choices=TournamentDeckFormatChoice.choices)
    description = models.TextField(validators=[MaxLengthValidator(512)])
    prizes = models.TextField(validators=[MaxLengthValidator(512)])

    def __str__(self):
        return self.name


def get_sponsor_file_path(instance, filename):
    return 'tournaments/{}/sponsors/{}.webp'.format(instance.tournament.uuid, instance.uuid)


class Sponsor(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=get_sponsor_file_path, storage=fs)

    def save(self, *args, **kwargs):
        self.logo = makeThumbnail(self.logo, size=(100, 100))
        super().save(*args, **kwargs)


class Participant(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET(getUserDeleted))
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    license_number = models.CharField("License number", max_length=100)
    current_ranking = models.PositiveSmallIntegerField("Current ranking")

    class Meta:
        unique_together = (('user', 'tournament'), ('tournament', 'license_number'), ('tournament', 'current_ranking'))


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant_zero = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant_zero', null=True, blank=True)
    participant_one = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant_one', null=True, blank=True)
    tournament_round = models.PositiveSmallIntegerField() # ceil(log2(current_number_of_players))
    pair_no = models.PositiveSmallIntegerField()
    winner_by_part_zero = models.BooleanField(null=True, blank=True)
    winner_by_part_one = models.BooleanField(null=True, blank=True)
    winner = models.BooleanField(null=True, blank=True)