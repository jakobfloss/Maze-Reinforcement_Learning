import agent
import maze
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
import plotter
import sys
import dill

def main():
    maze_name = 'very_very_big_maze'
    learning_rate = 0.15
    exploration_rate = 0.3
    decrease_rate = 0.99
    do_plots = True
    load_agent = False
    store_agent = False

    N_plots = 100
    N_iters = 500
    plot_freq = N_iters//N_plots
    m = maze.Maze(player_type='robot', rules='relaxed', maze=maze_name)
    if load_agent:
        agent_file = open(f"agents/{maze_name}_lr{learning_rate}_er{exploration_rate}.agent", 'rb')
        a = dill.load(agent_file)
    else: a = agent.Agent(learning_rate, exploration_rate, decrease_rate, maze_shape=m.shape)

    if do_plots: update_frame, fig = plotter.prepare_animation(a, m)

    step_evolution = np.empty(N_iters)
    eps_evolution = np.empty(N_iters)
    for i in tqdm(range(N_iters)):
        a.store_reward(*m.get_state_and_reward())
        
        while m.is_game_over() == False:
            action_list = m.get_moves()
            action = a.choose_action(action_list)
            # action = a.choose_action_2(action_list)
            m.move(action())
            a.store_reward(*m.get_state_and_reward())

        # a.learn()
        a.learn_2()

        # record number of steps for plotting
        step_evolution[i] = m.get_steps()
        eps_evolution[i] = a._exploration_rate
        if do_plots: 
            if i%plot_freq == 0:
                update_frame(a, step_evolution[:i+1], eps_evolution[:i+1])

        m.reset()

    if do_plots:
        print('creating gif animation')
        plotter.create_animation(f'{maze_name}N{N_iters}_lr{learning_rate}_er{exploration_rate:.2f}_dr{decrease_rate:.5f}.gif', fig, N_iters-(N_iters-1)%plot_freq)
    else:
        plt.plot(step_evolution)
        plt.show()
    
    # store agent for later use
    if store_agent:
        agent_file = open(f"agent/{maze_name}N{N_iters}_lr{learning_rate}_er{exploration_rate}.agent", 'wb')
        dill.dump(a, agent_file)

    plotter.plot_solution(a, m, f"figures/{maze_name}_N{N_iters}_lr{learning_rate:.2f}_er{exploration_rate:.2f}_dr{decrease_rate:.5f}.png")

if __name__ == '__main__': main()