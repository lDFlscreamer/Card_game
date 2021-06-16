import gym
import numpy as np
from gym import spaces

from game.enviroment.game import Game


class Game_environment(gym.Env):
    def __init__(self):
        super(Game_environment, self).__init__()
        self.game = Game()
        # Actions of the format play  card with index
        self.action_space = spaces.Box(
            low=0, high=61, shape=(3,), dtype=np.int)

    def step(self, action):
        # Execute one time step within the environment
        pass

    def reset(self):
        # Reset the state of the environment to an initial state
        players = self.game.players
        self.game.already_performed_spells = []
        for s in players:
            s.reset()
            s.append_card_to_hand(self.game.card_deck.get_random_spell_card(8))

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        pass
