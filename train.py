import agent
import maze
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
import plotter
import sys

def main():
    maze_name = 'blocked_maze'
    learning_rate = 0.05
    exploration_rate = 0.5

    N = 500
    m = maze.Maze(player_type='robot', rules='relaxed', maze=maze_name)
    a = agent.Agent(learning_rate, exploration_rate, maze_shape=m.maze_shape)

    plotter.prepare_animation()

    step_evolution = np.empty(N)
    for i in tqdm(range(N)):
        m = maze.Maze(player_type='robot', rules='relaxed', maze=maze_name)
        a.store_reward(m.get_state_and_reward())
        
        while m.is_game_over() == False:
            action_list = m.get_moves()
            action = a.choose_action(action_list)
            m.move(action())
            a.store_reward(m.get_state_and_reward())

        a.learn()

        # record number of steps for plotting
        step_evolution[i] = m.get_steps()

        plotter.plot(step_evolution[:i+1], m, a)

    print('creating gif animation')
    plotter.create_animation(f'{maze_name}_lr{learning_rate}_er{exploration_rate:.2f}.gif')
        
if __name__ == '__main__': main()