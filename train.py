import agent
import maze
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import sleep

def main():
    N = 5000
    a = agent.Agent(0.1, 0.25)

    step_evolution = np.empty(N)
    for i in tqdm(range(N)):
        m = maze.Maze(player_type='robot', rules='relaxed')
        
        while m.is_game_over() == False:
            action_list = m.get_moves()
            action = a.choose_action(action_list)
            m.move(action())
            a.store_move(m.get_state_and_reward())

        a.learn()

        # record number of steps for plotting
        step_evolution[i] = m.get_steps()

    plt.plot(step_evolution)
    plt.show()

    x = [x for (x,y), reward in a._reward_table.items()]
    y = np.array([y for (x,y), reward in a._reward_table.items()])
    rewards = np.array([reward for (x,y), reward in a._reward_table.items()])

    plt.scatter(x, -y, c=-rewards, norm='log')
    plt.colorbar()
    plt.show()
        
if __name__ == '__main__': main()