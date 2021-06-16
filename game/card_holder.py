import random

from game.game import Game
from game.player import Player

# todo cardlist
CARD_DECK = []


def card_101(game: Game, player: Player):
    # todo: pick a card from deck
    pass


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
        player.lost_blood(3)
        additional_cards = random.sample(player.hand, 1)
        player.append_to_spell(cards=additional_cards)


def card_213(game: Game, player: Player):
    enemy: Player = game.get_random_player(exclusion=[player])
    if enemy:
        enemy.get_damaged(1)
    if sum(player.damage_delayed) > player.health:
        if [x for x in player.spell if x.is_beast]:
            player.damage_delayed.remove(max(player.damage_delayed))


def card_214(game: Game, player: Player):
    additional_card_amount = 1
    if game.get_castle_owner() == player.get_id():
        additional_card_amount = 2
    additional_cards = random.sample(player.hand, additional_card_amount)
    player.append_to_spell(cards=additional_cards)


def card_215(game: Game, player: Player):
    game.assign_castle(player=player)
    if player.get_blood_volume() >= 1:
        player.lost_blood(1)
        coin_amount = game.get_unfinished_sorcerer_coin_amount()
        damage = 2 * coin_amount
        alive_enemy = game.get_all_alive_players(exclusion=[player])
        for s in alive_enemy:
            s.get_damaged(damage=damage)


def card_216(game: Game, player: Player):
    game.assign_castle(player=player)
    if player.get_blood_volume() >= 1:
        player.lost_blood(1)
        coin_amount = game.get_unfinished_sorcerer_coin_amount()
        damage = 2 * coin_amount
        alive_enemy = game.get_all_alive_players(exclusion=[player])
        for s in alive_enemy:
            s.get_damaged(damage=damage)


CARD_FUNCTION_LIST = {
    101: card_101,
    211: card_211,
    212: card_212,
    213: card_213,
    214: card_214,
    215: card_215,
    216: card_216,
}
