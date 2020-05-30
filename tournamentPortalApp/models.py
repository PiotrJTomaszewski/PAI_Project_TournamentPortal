from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

# This user is meant to take ownership of some of the orphaned objects.
# We wan't to preserve for example the past tournaments history.
def getUserDeleted():
    return get_user_model().objects.get(id=2)

class TournamentLocationChoice(Enum):
    net: "Network"
    loc: "Physical location"

class TournamentGameFormatChoice(Enum):
    std: "Standard format"
    wld: "Wild format"

class TournamentDeckFormatChoice(Enum):
    sin: "Single-deck format"
    mul: "Multiple-deck format"

class Tournament(models.Model):
    start_date = models.DateTimeField()
    name = models.CharField(max_length=250)
    entry_limit = models.PositiveSmallIntegerField()
    event_date = models.DateTimeField()
    creator = models.OneToOneField(get_user_model(), on_delete=models.SET(getUserDeleted))
    organiser_name = models.CharField(max_length=50) 
    location_type = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentLocationChoice])
    location = models.CharField(max_length=50)
    game_format = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentGameFormatChoice])
    deck_format = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in TournamentDeckFormatChoice])

    def __str__(self):
        pass
