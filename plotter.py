import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

# from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

def plot_maze(maze, ax):
    walls = maze.maze
    walls[*maze.start] = 0
    walls[*maze.end] = 0

    # https://www.freepik.com/search?format=search&last_filter=query&last_value=person&query=person&type=icon
    start_icon = plt.imread('images/start_blue.png')
    finish_icon = plt.imread('images/finish_blue.png')
    player_icon = plt.imread('images/player_blue.png')

    ax.imshow(start_icon, extent=[maze.start[0]-0.4, maze.start[0]+0.4, maze.start[1]+0.4, maze.start[1]-0.4], zorder=2)
    ax.imshow(finish_icon, extent=[maze.end[0]-0.4, maze.end[0]+0.4, maze.end[1]+0.4, maze.end[1]-0.4], zorder=2)
    ax.imshow(player_icon, extent=[maze.pos[0]-0.4, maze.pos[0]+0.4, maze.pos[1]+0.4, maze.pos[1]-0.4], zorder=2)
    ax.imshow(walls.T, cmap='Greys', vmin=0, vmax=1, zorder=1)

def plot_rewards(agent, fig, ax):
    """Plot reward matrix ontop of maze."""
    # create a cmap whick is transparent for values above vmax
    # stack overflow answer 
    # <https://stackoverflow.com/a/16401183/17822608>
    my_cmap = mpl.cm.get_cmap('RdYlGn')
    my_cmap.set_under((0,0,0,0)) #(0,0,0,0) is black with alpha = 0
    my_cmap.set_over((0,0,0,0)) #(0,0,0,0) is black with alpha = 0

    # plot 
    rwrds = ax.imshow(agent._reward_table.T, cmap=my_cmap, zorder=1, vmax=-1e-10)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)

    fig.colorbar(rwrds, cax=cax, orientation='vertical')

def plot_path(agent, fig, ax):
    np.array([pos for pos, rew in agent.last_moves]).T
    ax.plot(*np.array([pos for pos, rew in agent.last_moves]).T)

def plot_steps(steps, ax):
    ax.plot(steps)

    ax.set_yscale('log')

    ax.set_xlabel('attempt')
    ax.set_ylabel('number of steps')

def plot(steps, maze, agent):
    fig, axs = plt.subplots(1,2, figsize=(6.4, 2.5), layout='tight')#, title=f"learning rate: {agent._learning_rate}, exploration rate: {agent._exploration_factor}")

    plot_maze(maze, axs[1])
    plot_rewards(agent, fig, axs[1])
    plot_path(agent, fig, axs[1])
    plot_steps(steps, axs[0])

    plt.suptitle(f"learning rate: {agent._learning_rate}, exploration rate: {agent._exploration_factor:.2f}")
    # plt.savefig(f'animation/{len(steps):03d}.jpg')
    plt.savefig(f'tmp_anim_frames/{len(steps):03d}.png')
    plt.close()

def prepare_animation():
    try: os.mkdir('tmp_anim_frames/')
    except FileExistsError: pass

def create_animation(name):
    os.system(f'convert -delay 20 tmp_anim_frames/* learning_animations/{name}')
    os.system('rm -rf tmp_anim_frames/')