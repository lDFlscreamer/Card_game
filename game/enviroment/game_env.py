import random

import gym
import numpy as np
from gym import spaces

from game.agent.gameNN.agent_handler import get_bot, predict_action
from game.enviroment.card import Card
from game.enviroment.game import Game
from game.enviroment.player import Player

DEATH_PENALTY = 20
BEAST_COST = 5
HEALTH_POINT_COST = 4
UNFINISHED_COIN_COST = 10


class Game_environment(gym.Env):
    def __init__(self):
        super(Game_environment, self).__init__()
        self.game = Game()
        self.agent_player: Player = random.choice(self.game.players)
        # Actions of the format play  card with index
        self.action_space = spaces.Box(
            low=0, high=61, shape=(3,), dtype=np.int)

    def step(self, action):
        # Execute one time step within the environment
        obs = self.get_state()
        done = False
        before = self.get_cost()

        players = self.game.get_all_alive_players(exclusion=[])
        model = get_bot()
        for s in players:
            if s != self.agent_player:
                action = predict_action(model=model, state=obs)

            spell = [self.game.card_deck.get_card_by_id(card_id=(card_id + 1)) for card_id in action if
                     card_id != 0]
            if not s.create_spell(cards=spell):
                s.kill()

        if self.perform_cast_spell():
            done = True
        after = self.get_cost()

        reward = self.calculate_reward(before, after)
        done = self.agent_player.is_dead or done
        obs = self.get_state()
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        players = self.game.players
        self.game.already_performed_spells = []
        for s in players:
            s.reset()
            s.append_card_to_hand(self.game.card_deck.get_random_spell_card(8))

        return self.get_state()

    def get_state(self):
        state = []
        return state

    def get_cost(self):
        is_alive = self.agent_player.is_alive()
        enemies_summary_health = 0
        dead_enemies_amount = 0
        enemies_beasts_amount = 0
        agent_beast_amount = 0
        agent_health = 0
        agent_unfinished_coin = 0
        enemies_unfinished_coin = 0
        if not is_alive:
            return (is_alive, agent_beast_amount, agent_health, agent_unfinished_coin, enemies_summary_health,
                    enemies_beasts_amount, enemies_unfinished_coin,
                    dead_enemies_amount)

        enemy = self.game.get_all_player(exclusion=[self.agent_player])
        s: Player
        for s in enemy:
            if not s.is_alive():
                dead_enemies_amount += 1
            else:
                enemies_summary_health += s.get_health()
                enemies_beasts_amount += len(s.get_beasts())
            enemies_unfinished_coin += s.get_unfinished_sorcerer_coins()

        agent_beast_amount = len(self.agent_player.get_beasts())
        agent_health = self.agent_player.health
        agent_unfinished_coin = self.agent_player.get_unfinished_sorcerer_coins()
        return (
            is_alive, agent_beast_amount, agent_health, agent_unfinished_coin, enemies_summary_health,
            enemies_beasts_amount, enemies_unfinished_coin,
            dead_enemies_amount)

    def perform_cast_spell(self):
        players = self.game.get_all_alive_players(exclusion=[]).copy()
        players.sort(key=lambda x: len(x.get_spell()))
        s: Player
        for s in players:
            spell = s.get_spell()
            c: Card
            for c in spell:
                c.function(self.game, s)
        for s in players:
            s.health -= s.damage_delayed
            if s.health <= 0:
                s.kill()
        alive_players = self.game.get_all_alive_players(exclusion=[])
        if len(alive_players) == 1:
            winner = alive_players[0]
            winner: Player
            winner.unfinished_sorcerer_coin += 1
            if winner.unfinished_sorcerer_coin >= 2:
                return True
        return False

    @staticmethod
    def calculate_reward(before, after):
        reward = 0
        if before[0] or after[0]:
            return DEATH_PENALTY

        reward += (after[1] - before[1]) * BEAST_COST
        reward += (after[2] - before[2]) * HEALTH_POINT_COST
        reward += (after[3] - before[3]) * UNFINISHED_COIN_COST
        reward -= (after[4] - before[4]) * HEALTH_POINT_COST
        reward -= (after[5] - before[5]) * BEAST_COST
        reward -= (after[6] - before[6]) * BEAST_COST
        reward -= (after[7] - before[7]) * UNFINISHED_COIN_COST
        reward -= (after[8] - before[8]) * DEATH_PENALTY
        return reward
