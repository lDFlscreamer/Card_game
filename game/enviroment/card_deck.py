import random

from game.enviroment.card import Card
from game.enviroment.card_holder import SPELL_CARD_DECK, TREASURE_CARD_DECK, UNFINISHED_SORCERER_CARD_DECK


class Card_deck:

    def __init__(self):
        self.card_deck = []
        self.treasure_card_deck = []
        self.unfinished_sorcerer_card_deck = []

    def get_treasure(self, amount):
        treasures = random.sample(self.treasure_card_deck, amount)
        if all(treasure in self.treasure_card_deck for treasure in treasures):
            self.treasure_card_deck = [treasure for treasure in self.treasure_card_deck if treasure not in treasures]
        return treasures

    def get_random_spell_card(self, amount, card_class=None):
        if not card_class:
            return random.sample(self.card_deck, amount)
        if card_class != 2 or card_class != 3 or card_class != 4:
            return None
        cards_in_deck = [card for card in self.card_deck if card_class or card.get_card_class() == card_class]
        return random.sample(cards_in_deck, amount)

    def get_card_by_id(self, card_id):
        card: Card
        for card in self.card_deck:
            if card.get_id() == card_id:
                return card

    def reset(self):
        self.card_deck = SPELL_CARD_DECK.copy()
        self.treasure_card_deck = TREASURE_CARD_DECK.copy()
        self.unfinished_sorcerer_card_deck = UNFINISHED_SORCERER_CARD_DECK.copy()
