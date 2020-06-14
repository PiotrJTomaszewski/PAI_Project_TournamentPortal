from django.core.management.base import BaseCommand
from tournamentPortalApp.models import PortalUser

import os


class Person:
    def __init__(self, line):
        self.first_name, self.last_name, self.email, self.password = line.split(',')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path+'/fakeNameGenerator_com.csv', 'r') as personal_data:
            for line in personal_data:
                person = Person(line)
                user = PortalUser(first_name=person.first_name,
                           last_name=person.last_name,
                           email=person.email,
                           is_active=True,
                           is_admin=False,
                           )
                user.set_password(person.password)
                user.save()
