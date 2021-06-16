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

        self.hand = []
        self.spell = []

    def is_alive(self):
        return not self.is_dead

    def get_id(self):
        return self.id

    def get_blood_volume(self):
        return self.blood

    def get_blood(self, amount):
        self.blood += amount

    def lost_blood(self, amount):
        self.blood = -amount

    def get_unfinished_sorcerer_coins(self):
        return self.unfinished_sorcerer_coin

    def get_damaged(self, damage):
        if sum(self.damage_delayed) < self.health:
            self.damage_delayed.append(damage)
        # todo: move below to game round rules
        # self.health -= damage
        # if self.health <= 0:
        #     self.health = 0
        #     self.is_dead = True

    def heal(self, heal):
        self.health += heal

    def create_spell(self, cards):
        if all(card in self.hand for card in cards):
            self.hand = [card for card in self.hand if card not in cards]
            self.spell = cards

    def append_to_spell(self, cards):
        if all(card in self.hand for card in cards):
            self.hand = [card for card in self.hand if card not in cards]
            self.spell.extend(cards)

    def add_treasures(self, treasures):
        self.treasures.extend(treasures)

    def remove_treasures(self, treasures):
        if all(treasure in self.treasures for treasure in treasures):
            self.treasures = [treasure for treasure in self.treasures if treasure not in treasures]
