from background_task import background
import math
from django.db import transaction
from uuid import UUID

from tournamentPortalApp.models import Participant, Match, Tournament

class Bracket:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def __init__(self, players):
        self.starting_pairs = []
        self.players = players
        self.player_no = len(players)
        self.round_no = math.ceil(math.log2(self.player_no))

    def map_indexes_to_players(self, pair):
        mapped = [None, None]
        if pair[0] < self.player_no:
            mapped[0] =  self.players[pair[0]]
        if pair[1] < self.player_no:
            mapped[1] = self.players[pair[1]]
        return mapped

    def generate_starting_pairs(self):
        self.fill_level(0, 1)
        return list(map(self.map_indexes_to_players, self.starting_pairs))

    def fill_level(self, index, current_level):
        player_no_on_level = 2**current_level
        opponend_index = player_no_on_level - index-1
        if current_level == self.round_no:
            self.starting_pairs.append((index, opponend_index))
        else:
            self.fill_level(index, current_level+1)
            self.fill_level(opponend_index, current_level+1)

@background
def pair_participants_up(tournament_uuid):
    tournament = UUID(tournament_uuid) # Passed as hex
    participants = Participant.objects.filter(tournament=tournament_uuid).order_by('current_ranking')
    bracket = Bracket(participants)
    paired_players = bracket.generate_starting_pairs()
    tournament = Tournament.objects.get(uuid=tournament_uuid)
    with transaction.atomic():
        for i, pair in enumerate(paired_players):
            Match(
                tournament=tournament,
                participant_zero=pair[0],
                participant_one=pair[1],
                tournament_round=bracket.round_no,
                pair_no=i
            ).save()
