import numpy as np
import maze

class Agent():
    """A robot that can be teached to solve a maze of `maze.py`"""
    
    def __init__(
            self,
            learning_rate,
            exploration_rate,
            decrease_rate=0.95,
            maze_shape=7,
        ):
        self._maze_shape = maze_shape
        self._learning_rate = learning_rate
        self._exploration_rate = exploration_rate
        self._decrease_rate = decrease_rate

        # initialize entire reward table to zero
        self._reward_table = np.zeros(shape = self._maze_shape)

        # storage for moves from one episode (game)
        self._pos_history = []
        self._rew_history = []

        # provide random number generator for random moves
        self._rng = np.random.default_rng()

    def choose_action(self, action_list):
        """Choose action from action list"""

        # choose random action
        index = self._rng.integers(low=0, high=len(action_list))

        # exploit with chance of 1 - exploration_rate
        if self._rng.random() > self._exploration_rate:
            # before this loop a random action should be chosen in case all
            # actions lead to same result
            max_reward = -np.inf
            # choose action which provides the maximum reward
            for i, action in enumerate(action_list):
                if self._reward_table[*action()] > max_reward:
                    max_reward = self._reward_table[*action()]
                    index = i
        return action_list[index]

    def choose_action_2(self, action_list):
        """Choose action from action list"""

        # choose random action
        index = self._rng.integers(low=0, high=len(action_list))

        # exploit with chance of 1 - exploration_rate
        if self._rng.random() > self._exploration_rate:
            # before this loop a random action should be chosen in case all
            # actions lead to same result
            max_reward = -np.inf
            # choose action which provides the maximum reward
            for i, action in enumerate(action_list):
                if self._reward_table[*action()] > max_reward:
                    max_reward = self._reward_table[*action()]
                    index = i
        
        # attempt to make him not reverse moves immediatly
        # if action returns to previous position choose again with
        # certain probability
        try:
            if tuple(action_list[index]()) == self._pos_history[-2]:
                if len(action_list) > 1:
                    action_list.pop(index)
                    return self.choose_action(action_list)
        # at the start he has no position history
        except IndexError: pass
        
        return action_list[index]
     
    def store_reward(self, pos, reward):
        self._pos_history.append(tuple(pos))
        self._rew_history.append(reward)
    
    def learn(self):
        "Learn form the past steps taken"
        
        # ALL REWARDS ARE NEGATIVE

        # initialize reward to zero
        cum_reward = 0

        # follow the path backwards (ie. start at last position)
        for pos, pos_reward in zip(self._pos_history[::-1], self._rew_history[::-1]):
            # add all reward of cumulatively
            # this ensures each position along the path gets smaller and
            # smaller rewards 
            cum_reward += pos_reward

            self._reward_table[*pos] += \
                self._learning_rate*(cum_reward-self._reward_table[*pos])
        
        # reduce exploration rate
        # self._exploration_rate *= 1-10**(-np.log(self._maze_shape[0]))
        self._exploration_rate *= self._decrease_rate

        # store move - only convenient for plotting
        self.last_pos_history = self._pos_history
        # empty reward and position history for next episode
        self._pos_history = []
        self._rew_history = []

    def learn_2(self):
        """Improved learning algorithm
        This algorithm only updates the reward table with the smalles
        reward from the path. Otherwise if the path ends is a dead end
        the end of path becomes a reward close to zero, which favours
        them.
        """
        cum_rewards = np.cumsum(self._rew_history[::-1])[::-1]
        for i in range(self._maze_shape[0]):
            for j in range(self._maze_shape[1]):
                try:
                    low_index = self._pos_history.index((i,j))
                    cum_reward = cum_rewards[low_index]

                    self._reward_table[i, j] += \
                        self._learning_rate*(cum_reward-self._reward_table[i, j])
                except ValueError: pass
        
        # reduce exploration rate
        # self._exploration_rate *= 1-10**(-np.log(self._maze_shape[0]))
        self._exploration_rate *= self._decrease_rate

        # store move - only convenient for plotting
        self.last_pos_history = self._pos_history
        # empty reward and position history for next episode
        self._pos_history = []
        self._rew_history = []
                