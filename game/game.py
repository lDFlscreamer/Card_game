import random

from game.card_deck import Card_deck
from game.player import Player


class Game:
    def __init__(self):
        self.castle_owner = 0  # 0 is no one

        self.card_deck = Card_deck()
        self.card_deck.shufl_all()

        self.players = []  # begin with empty
        self.already_performed_spells = []  # begin with empty

    def get_players(self):
        return self.players

    def get_already_performed_spells_players(self, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive()))]
        if not players:
            return None
        return players

    def get_left_player(self, player_id, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive() or (x.get_id() < player_id)))]
        if not players:
            players = [x for x in self.players
                       if ((x not in exclusion) or (not x.is_alive() or (x.get_id() > player_id)))]
        if not players:
            return None
        players.sort(key=lambda x: x.get_id(), reverse=True)
        return players[0]

    def get_right_player(self, player_id, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive() or (x.get_id() > player_id)))]
        if not players:
            players = [x for x in self.players
                       if ((x not in exclusion) or (not x.is_alive() or (x.get_id() < player_id)))]
        if not players:
            return None
        players.sort(key=lambda x: x.get_id())
        return players[0]

    def get_all_alive_players(self, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive()))]
        if not players:
            return None
        return players

    def get_random_player(self, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive()))]
        if not players:
            return None
        return random.choice(players)

    def get_most_tenacious(self, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive()))]
        if not players:
            return None
        players.sort(key=lambda x: x.helth, reverse=True)
        return players[0]

    def get_most_fragile(self, exclusion):
        players = [x for x in self.players
                   if ((x not in exclusion) or (not x.is_alive()))]
        if not players:
            return None
        players.sort(key=lambda x: x.helth)
        return players[0]

    def get_castle_owner(self):
        return self.castle_owner

    def assign_castle(self, player: Player):
        self.castle_owner = player.id

    def release_castle(self):
        self.castle_owner = 0

    def get_unfinished_sorcerer_coin_amount(self):
        unfinished_sorcerer_coin_amount = 0
        for s in self.players:
            unfinished_sorcerer_coin_amount += s.get_unfinished_sorcerer_coins()
        return unfinished_sorcerer_coin_amount
