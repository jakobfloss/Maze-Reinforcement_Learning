import numpy as np
import maze

class Agent():
    """A robot that can be teached to solve a maze of `maze.py`"""
    
    def __init__(
            self,
            learning_rate,
            exploration_rate,
            maze_shape=7,
        ):
        self._maze_shape = maze_shape
        self._learning_rate = learning_rate
        self._exploration_rate = exploration_rate

        # initialize entire reward table to zero
        self._reward_table = np.zeros(shape = self._maze_shape)

        # storage for moves from one episode (game)
        self._moves = []

        # provide random number generator for random moves
        self._rng = np.random.default_rng()

    def choose_action(self, action_list):
        """Choose action from action list"""

        # choose random action
        chosen_action = action_list[self._rng.integers(low=0, high=len(action_list))]

        # explore with chance of exploration_rate
        if self._rng.random() < self._exploration_rate:
            return chosen_action

        # before this loop a random action should be chosen in case all
        # actions lead to same result
        max_reward = -np.inf
        # choose action which provides the maximum reward
        for action in action_list:
            if self._reward_table[*action()] > max_reward:
                max_reward = self._reward_table[*action()]
                chosen_action = action
        
        return chosen_action
     
    def store_reward(self, pos_and_reward):
        self._moves.append(pos_and_reward)
    
    def learn(self):
        "Learn form the past steps taken"
        
        # ALL REWARDS ARE NEGATIVE

        # initialize reward to zero
        cum_reward = 0

        # follow the path backwards (ie. start at last position)
        for pos, pos_reward in reversed(self._moves):
            # add all reward of cumulatively
            # this ensures each position along the path gets smaller and
            # smaller rewards 
            cum_reward += pos_reward

            self._reward_table[*pos] += \
                self._learning_rate*(cum_reward-self._reward_table[*pos])
        
        # reduce exploration rate
        self._exploration_rate *= 0.99

        # store move - only convenient for plotting
        self.last_moves = self._moves
        # empty 
        self._moves = []
