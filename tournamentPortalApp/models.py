from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage

from enum import Enum
import uuid

from .helpers import makeThumbnail

fs = FileSystemStorage()

# This user is meant to take ownership of some of the orphaned objects.
# We wan't to preserve for example the past tournaments history.


def getUserDeleted():
    return get_user_model().objects.get(id=2)


class PortalUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, is_active=False, is_admin=False, is_dummy=False):
        if not email or not first_name or not last_name or not password:
            raise ValueError('Some fields are empty!')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin,
            is_dummy=is_dummy
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, is_active=True, is_admin=True, is_dummy=False):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            is_dummy=is_dummy
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class PortalUser(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_dummy = models.BooleanField(default=False)

    objects = PortalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_active', 'is_admin', 'is_dummy']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Tournament(models.Model):
    class TournamentLocationChoice(models.TextChoices):
        NETWORK = 'net', _("Network")
        PHYS_LOC = 'loc', _("Physical location")

    class TournamentGameFormatChoice(models.TextChoices):
        STANDARD = 'std', _("Standard")
        WILD = 'wld', _("Wild")

    class TournamentDeckFormatChoice(models.TextChoices):
        SINGLE_DECK = 'sin', _("Single-deck")
        MULTIPLE_DECK = 'mul', _("Multiple-deck")

    name = models.CharField(max_length=100)
    entry_deadline = models.DateTimeField()
    entry_limit = models.PositiveSmallIntegerField()
    event_date = models.DateTimeField()
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.SET(getUserDeleted))
    organiser_name = models.CharField(max_length=50)
    location_type = models.CharField(
        max_length=3, choices=TournamentLocationChoice.choices)
    location = models.CharField(max_length=50)
    game_format = models.CharField(
        max_length=3, choices=TournamentGameFormatChoice.choices)
    deck_format = models.CharField(
        max_length=3, choices=TournamentDeckFormatChoice.choices)
    description = models.TextField()
    prizes = models.TextField()

    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.name)


def get_sponsor_file_path(instance, filename):
    return 'tournaments/{}/sponsors/{}.webp'.format(instance.tournament.id, instance.uuid)


class Sponsor(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=get_sponsor_file_path, storage=fs)

    def save(self, *args, **kwargs):
        self.logo = makeThumbnail(self.logo, size=(150, 150))
        super().save(*args, **kwargs)


class Participant(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.SET(getUserDeleted))
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
