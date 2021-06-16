import os

from numpy import unravel_index
from tensorflow.keras.models import *

import CONSTANT
from game.agent.gameNN.agent import Game_agent
from game.enviroment.game_env import Game_environment


def get_bot():
    model_is_exist = os.path.exists(CONSTANT.AGENT_ACCURACY_MODEL_PATH)
    if not model_is_exist:
        env = Game_environment()
        agent = Game_agent()

        agent.reinforcement_learning(env=env)
        return get_bot()
    return load_model(CONSTANT.DETECTION_ACCURACY_MODEL_PATH)


def predict_action(model, state):
    q_s = model.predict(state)
    a = unravel_index(q_s.argmax(), q_s.shape)
    card_ids = [CONSTANT.DATASET_LABEL[label - 1] for label in a]
    return card_ids
