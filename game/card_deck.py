import random


class Card_deck:

    def __init__(self):
        self.card_deck = []
        self.treasure_card_deck = []

    def get_treasure(self, amount):
        treasures = random.sample(self.treasure_card_deck, amount)
        if all(treasure in self.treasure_card_deck for treasure in treasures):
            self.treasure_card_deck = [treasure for treasure in self.treasure_card_deck if treasure not in treasures]
        return treasures

    def get_random_spell_card(self, card_class, amount):
        if card_class != 2 or card_class != 3 or card_class != 4:
            return None
        cards_in_deck = [card for card in self.card_deck if card.get_card_class() == card_class]
        return random.sample(cards_in_deck, amount)
