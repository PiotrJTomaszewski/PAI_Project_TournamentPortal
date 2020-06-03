from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from enum import Enum

# This user is meant to take ownership of some of the orphaned objects.
# We wan't to preserve for example the past tournaments history.
def getUserDeleted():
    return get_user_model().objects.get(id=2)

class TournamentLocationChoice(Enum):
    net = "Network"
    loc = "Physical location"

class TournamentGameFormatChoice(Enum):
    std = "Standard"
    wld = "Wild"

class TournamentDeckFormatChoice(Enum):
    sin = "Single-deck"
    mul = "Multiple-deck"

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    entry_limit = models.PositiveSmallIntegerField()
    event_date = models.DateTimeField()
    creator = models.OneToOneField(get_user_model(), on_delete=models.SET(getUserDeleted))
    organiser_name = models.CharField(max_length=50)
    location_type = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentLocationChoice])
    location = models.CharField(max_length=50)
    game_format = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentGameFormatChoice])
    deck_format = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentDeckFormatChoice])
    description = models.TextField()
    prizes = models.TextField()

    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.name)


class Participant(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET(getUserDeleted))
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)