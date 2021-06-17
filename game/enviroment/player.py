class Player:
    player_amount = 0

    def __init__(self):
        Player.player_amount += 1
        self.id = Player.player_amount
        self.is_dead = False

        self.health = 20
        self.blood = 0

        self.unfinished_sorcerer_coin = 0

        self.damage_delayed = []

        self.beasts = []
        self.treasures = []
        self.delayed_treasure = []
        self.unfinished_sorcerer_cards = []

        self.hand = []
        self.spell = []

    def reset(self):
        self.is_dead = False

        self.health = 20
        self.blood = 0

        self.unfinished_sorcerer_coin = 0

        self.damage_delayed = []

        self.beasts = []
        self.treasures = []
        self.delayed_treasure = []
        self.unfinished_sorcerer_cards = []

        self.hand = []
        self.spell = []

    def as_array(self):
        return [self.health,self.blood,len(self.beasts),self.unfinished_sorcerer_coin]
    def get_id(self):
        return self.id

    def get_health(self):
        return self.health

    def get_beasts(self):
        return self.beasts

    def is_alive(self):
        return not self.is_dead

    def kill(self):
        self.reset()
        self.is_dead = True
        self.health = 0

    def get_blood_volume(self):
        return self.blood

    def get_blood(self, amount):
        self.blood += amount

    def lose_blood(self, amount):
        self.blood = -amount

    def get_unfinished_sorcerer_coins(self):
        return self.unfinished_sorcerer_coin

    def get_spell(self):
        return self.spell

    def get_hand(self):
        return self.hand

    def remove_card_from_hand(self, cards):
        if all(card in self.hand for card in cards):
            self.hand = [card for card in self.hand if card not in cards]

    def append_card_to_hand(self, cards):
        self.hand.extend(cards)

    def get_damaged(self, damage):
        if sum(self.damage_delayed) < self.health:
            self.damage_delayed.append(damage)

    def heal(self, heal):
        if not self.is_dead:
            self.health += heal

    def create_spell(self, cards):
        if all(card in self.hand for card in cards):
            self.hand = [card for card in self.hand if card not in cards]
            self.spell = cards
            return True
        return False

    def append_to_spell(self, cards):
        if all(card in self.hand for card in cards):
            self.hand = [card for card in self.hand if card not in cards]
            self.spell.extend(cards)

    def add_treasures(self, treasures):
        self.treasures.extend(treasures)

    def add_delayed_treasures(self, treasures):
        self.delayed_treasure.extend(treasures)

    def remove_treasures(self, treasures):
        if all(treasure in self.treasures for treasure in treasures):
            self.treasures = [treasure for treasure in self.treasures if treasure not in treasures]

    def is_surprise(self):
        return sum(self.damage_delayed) > self.health
