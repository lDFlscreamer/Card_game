import random

from game.game import Game
from game.player import Player

# todo cardlist
CARD_DECK = []


def card_101(game: Game, player: Player):
    all_class = [2, 3, 4]

    spell = [c.get_card_class() for c in player.get_spell()]
    all_class = [card for card in all_class if card not in spell]

    random_card = game.card_deck.get_random_spell_card(all_class[0], 1)
    player.append_to_spell(random_card)


def card_211(game: Game, player: Player):
    castle_owner = game.castle_owner
    if castle_owner != 0:
        enemy: Player = game.get_random_player(exclusion=[player])
        if player:
            enemy.get_damaged(3)
    game.assign_castle(player=player)


def card_212(game: Game, player: Player):
    enemy: Player = game.get_most_tenacious(exclusion=[player])
    if player:
        enemy.get_damaged(2)
    if player.get_blood_volume() >= 3:
        player.lose_blood(3)
        additional_cards = random.sample(player.hand, 1)
        player.append_to_spell(cards=additional_cards)


def card_213(game: Game, player: Player):
    enemy: Player = game.get_random_player(exclusion=[player])
    if enemy:
        enemy.get_damaged(1)
    if player.is_surprise():
        if [x for x in player.spell if x.is_beast()]:
            player.damage_delayed.remove(max(player.damage_delayed))


def card_214(game: Game, player: Player):
    additional_card_amount = 1
    if game.get_castle_owner() == player.get_id():
        additional_card_amount = 2
    additional_cards = random.sample(player.hand, additional_card_amount)
    player.append_to_spell(cards=additional_cards)


def card_221(game: Game, player: Player):
    game.assign_castle(player=player)
    if player.get_blood_volume() >= 1:
        player.lose_blood(1)
        coin_amount = game.get_unfinished_sorcerer_coin_amount()
        damage = 2 * coin_amount
        alive_enemy = game.get_all_alive_players(exclusion=[player])
        for s in alive_enemy:
            s.get_damaged(damage=damage)


def card_222(game: Game, player: Player):
    enemy: Player = game.get_left_player(player_id=player.get_id(), exclusion=[player])
    if enemy.get_blood_volume() >= 2:
        enemy.lose_blood(2)
        player.get_blood(2)
    else:
        enemy.get_damaged(3)


def card_223(game: Game, player: Player):
    enemies = game.already_performed_spells(exclusion=[player])
    for s in enemies:
        s.get_damaged(2)
    if player.is_surprise():
        # todo: get a 2 unfinished_sorcerer_cards
        pass


def card_224(game: Game, player: Player):
    enemy_damage = random.randint(0, 5) + 1
    self_damage = random.randint(0, 5) + 1

    enemy: Player = game.get_left_player(player_id=player.get_id(), exclusion=[player])
    if enemy:
        enemy.get_damaged(enemy_damage)
    if not (game.get_castle_owner() == player.get_id()):
        if player.get_blood_volume() >= 1:
            player.lose_blood(1)
        else:
            player.get_damaged(self_damage)


def card_231(game: Game, player: Player):
    dice_value = random.randint(0, 5) + 1
    if dice_value <= 2:
        game.assign_castle(player.get_id())
    elif dice_value <= 4:
        treasure = game.card_deck.get_treasure(1)
        player.add_treasures(treasures=treasure)
    else:
        game.assign_castle(player.get_id())
        treasure = game.card_deck.get_treasure(1)
        player.add_treasures(treasures=treasure)
    if player.is_surprise():
        treasure = game.card_deck.get_treasure(1)
        player.add_delayed_treasures(treasures=treasure)


def card_232(game: Game, player: Player):
    players = game.get_all_alive_players(exclusion=[])
    card_class = random.randint(0, 2) + 2
    k = 1
    if player.get_blood_volume() >= 4:
        player.lose_blood(4)
        k = 2
    for s in players:
        left_player: Player = game.get_left_player(player_id=s.get_id(), exclusion=[s])
        damage = 0
        for card in s.left_player.get_hand():
            if card.get_card_class() == card_class:
                damage += 1
        left_player.get_damaged(k * damage)


def card_233(game: Game, player: Player):
    players = game.get_already_performed_spells_players(exclusion=[player])
    for s in players:
        if s.get_blood_volume() >= 1:
            s.lose_blood(amount=1)
            player.get_blood(amount=1)
    not_already_performed_spells_players = game.get_all_alive_players(exclusion=[players])
    not_already_performed_spells_players = [p for p in not_already_performed_spells_players if
                                            p not in players]
    for s in not_already_performed_spells_players:
        s.get_damaged(2)


def card_234(game: Game, player: Player):
    if player.get_blood_volume() >= 2:
        player.lose_blood(2)
        enemies = game.get_all_alive_players(exclusion=[player])
        for s in enemies:
            s.get_damaged(3)
    else:
        enemy = game.get_left_player(player_id=player.get_id(), exclusion=[player])
        if enemy:
            enemy.get_demaged(3)


def card_241(game: Game, player: Player):
    enemies = game.get_all_alive_players(exclusion=[player])
    enemy = None
    if enemies:
        enemy = random.choice(enemies)
    if enemy:
        enemy_beasts = [card for card in enemy.left_player.get_hand() if card.is_beast()]
        if enemy_beasts:
            card = random.choice(enemy_beasts)
            player.remove_card_from_hand(card)
            player.append_card_to_hand(card)
        else:
            enemy.get_damaged(damage=random.randint(0, 5) + 1)


def card_242(game: Game, player: Player):
    player.heal(heal=random.randint(0, 5) + 1)
    if player.is_surprise():
        player.damage_delayed = []
        player.health = 1


def card_243(game: Game, player: Player):
    players = game.get_all_alive_players(exclusion=[])
    heal = 0
    for s in players:
        heal += len(s.get_beasts())
    player.heal(heal=heal)

    if player.get_blood_volume() > 0 and player.health < 20:
        blood = player.get_blood_volume() / 2 + 1
        player.lose_blood(blood)
        player.heal(blood)


def card_244(game: Game, player: Player):
    enemy = game.get_most_tenacious(exclusion=[player])
    if enemy:
        enemy.get_damaged(3)
    if player.get_blood_volume() >= 4:
        players = game.get_all_alive_players(exclusion=[player])
        players = [s for s in players if s.get_unfinished_sorcerer_coins() > 0]
        for s in players:
            s.get_damaged(7)


def card_251(game: Game, player: Player):
    tenacious = game.get_most_tenacious(exclusion=[player])
    if tenacious:
        if player.get_blood_volume() >= 1:
            player.get_blood(1)
            tenacious.get_blood(1)
        tenacious.get_damaged(damage=random.randint(0, 5) + 1)
    if game.get_castle_owner() == player.get_id():
        enemies = game.get_all_alive_players(exclusion=player)
        if enemies:
            enemy = random.choice(enemies)
            enemy.get_damaged(damage=random.randint(0, 5) + 1)


def card_252(game: Game, player: Player):
    pass


CARD_FUNCTION_LIST = {
    101: card_101,
    211: card_211,
    212: card_212,
    213: card_213,
    214: card_214,
    221: card_221,
    222: card_222,
    223: card_223,
    224: card_224,
    231: card_231,
    232: card_232,
    233: card_233,
    234: card_234,
    241: card_241,
    242: card_242,
    243: card_243,
    244: card_244,
    251: card_251,
    252: card_251,
}
