import numpy as np
import maze

class Agent():
    """A robot that can be teached to solve a maze of `maze.py`"""
    
    def __init__(
            self,
            learning_rate,
            exploration_factor,
            maze_size=7,
        ):


        self._maze_size = maze_size

        self._learning_rate = learning_rate
        self._exploration_factor = exploration_factor

        self._rng = np.random.default_rng()

        self._reward_table = np.zeros(shape=(maze_size, maze_size))
        # self._reward_table = 0.1 + 0.9*self._rng.uniform(size=(maze_size, maze_size))
        # self._reward_table = {}
        self._moves = []

    def _get_reward(self, pos):
        try:
            return self._reward_table[*pos] 
        except KeyError:
            pass
            # reward = 0.1 + 0.9*self._rng.uniform()
            # self._set_reward(pos, reward)
            # return reward
    
    def _set_reward(self, pos, reward):
        self._reward_table[*pos] = reward

# this function is deprecated
    # def create_reward_table(self):
    #     reward_table = {}
    #     rewards = 0.1 + 0.9*self._rng.uniform(size=(self._maze_size, self._maze_size))

    #     for i, col in enumerate(rewards):
    #         for j, reward in enumerate(col):
    #             reward_table.update({(i, j): reward})
    #     return reward_table


    def choose_action(self, action_list):
        """Choose action from action list"""

        # choose random action
        chosen_action = action_list[self._rng.integers(low=0, high=len(action_list))]

        # explore with chance of exploration_rate
        if self._rng.random() < self._exploration_factor:
            return chosen_action

        # before this loop a random action should be chosen in case all
        # actions lead to same result
        max_reward = -np.inf
        # choose action which provides the maximum reward
        for action in action_list:
            if self._get_reward(action()) > max_reward:
                max_reward = self._get_reward(action())
                chosen_action = action
        
        return chosen_action
     
    def store_reward(self, pos_and_reward):
        self._moves.append(pos_and_reward)
    
    def learn(self):
        cum_reward = 0
        for pos, reward in reversed(self._moves):
            cum_reward += reward

            old_reward = self._get_reward(pos)

            reward = old_reward + self._learning_rate*(cum_reward-old_reward)
            self._set_reward(pos, reward)
        self._exploration_factor *= 0.99

        self.last_moves = self._moves     
        self._moves = []
