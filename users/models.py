from django.db import models
from django.contrib.auth.models import AbstractUser

class PortalUser(AbstractUser):
    battle_tag = models.CharField(max_length=50)

    def __str__(self):
        return self.username