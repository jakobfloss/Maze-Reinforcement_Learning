import numpy as np
import maze

class Agent():
    """A robot that can be teached to solve a maze of `maze.py`"""
    
    def __init__(
            self,
            # init_pos,
            learning_rate,
            exploration_factor,
            maze_size=7,
        ):


        self._maze_size = maze_size
        # self._pos = init_pos

        self._learning_rate = learning_rate
        self._exploration_factor = exploration_factor

        self._rng = np.random.default_rng()

        self._reward_table = {}
        self._moves = []

    def _get_reward(self, pos):
        try:
            return self._reward_table[tuple(pos)] 
        except KeyError:
            reward = 0.1 + 0.9*self._rng.uniform()
            self._set_reward(pos, reward)
            return reward
    
    def _set_reward(self, pos, reward):
        self._reward_table.update({tuple(pos): reward})

    def create_reward_table(self):
        reward_table = {}
        rewards = 0.1 + 0.9*self._rng.uniform(size=(self._maze_size, self._maze_size))

        for i, col in enumerate(rewards):
            for j, reward in enumerate(col):
                reward_table.update({(i, j): reward})
        return reward_table


    def choose_action(self, action_list):
        # explore with chance of exploration_rate
        if self._rng.random() < self._exploration_factor:
            return action_list[self._rng.integers(low=0, high=len(action_list))]

        max_reward = -np.inf
        # choose action which provides the maximum reward
        for action in action_list:
            if self._get_reward(action()) > max_reward:
                max_reward = self._get_reward(action())
                max_reward_action = action

        return max_reward_action
     
    def store_move(self, pos_and_reward):
        self._moves.append(pos_and_reward)
    
    def learn(self):
        cum_reward = 0
        for pos, reward in reversed(self._moves):
            cum_reward += reward

            old_reward = self._get_reward(pos)

            reward = old_reward + self._learning_rate*(cum_reward-old_reward)
            self._set_reward(pos, reward)
        self._exploration_factor *= 0.99

        self._moves = []        
