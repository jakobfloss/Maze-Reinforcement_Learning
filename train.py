import agent
import maze
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
import plotter

def main():
    N = 500
    a = agent.Agent(0.1, 0.25)

    plotter.prepare_animation()

    step_evolution = np.empty(N)
    for i in tqdm(range(N)):
        m = maze.Maze(player_type='robot', rules='relaxed')
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

    plotter.create_animation('learning.gif')

    # fig, axs = plt.subplots(1, 2)

    # axs[0].plot(step_evolution)
    # axs[0].set_yscale('log')


    # reward_matrix = np.zeros(m.maze.shape)
    # for (x,y), reward in a._reward_table.items():
    #     reward_matrix[x,y] = reward


    # divider = make_axes_locatable(axs[1])
    # cax = divider.append_axes('right', size='5%', pad=0.1)

    # rwrds = axs[1].imshow(-reward_matrix.T, norm='log')
    # # sc = axs[1].scatter(x, -y, c=-rewards, norm='log')    
    # axs[1].set_aspect('equal')
    
    # fig.colorbar(rwrds, cax=cax, orientation='vertical')

    # plt.tight_layout()
    # plt.show()
        
if __name__ == '__main__': main()