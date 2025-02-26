#%%
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

norm='linear'
# norm='symlog'

cmap_maze = mpl.colormaps['Greys']
cmap_maze.set_under((0,0,0,0)) # black with alpha = 0 -> transparent

cmap_rewards = mpl.colormaps['GnBu_r']
cmap_rewards.set_over((1,1,1,0)) # black with alpha = 0 -> transparent

#%%
def prepare_animation(agent, maze):
    # remove frames from previous unfinished runs
    os.system('rm -rf tmp_anim_frames/')
    os.mkdir('tmp_anim_frames/')

    # set up figure
    fig, axs = plt.subplots(1,2, figsize=(12, 5), layout='tight')
    plt.suptitle(rf"$\alpha = {agent._learning_rate}$; " + \
                 rf"$\epsilon_0 = {agent._exploration_rate}$; " + \
                 rf"$\gamma = {agent._decrease_rate}$")
    axs_eps = axs[0].twinx()

    # set up steps on left panel
    axs[0].set_xlim((0, 1))
    axs[0].set_ylim((1, 1.1*maze._allowed_tries))
    axs[0].set_xlabel('attempts')
    axs[0].set_ylabel('steps')
    axs[0].set_yscale('log')
    line_steps = axs[0].plot([], label='steps', c='blue')[0]

    # set up exploration rate on left panel
    axs_eps.set_ylim((0, 1.1*agent._exploration_rate))
    axs_eps.set_ylabel(r'$\epsilon$')
    line_eps = axs_eps.plot([], label=r'$\epsilon$', c='red')[0]

    # axs[0].legend(labelcolor="linecolor")

    axs[0].yaxis.get_label().set_color(line_steps.get_color())
    axs_eps.yaxis.get_label().set_color(line_eps.get_color())

    # draw maze, path, rewards on right panel
    # remove ticks and labels
    axs[1].set_xticks([])
    axs[1].set_yticks([])

    # https://www.freepik.com/search?format=search&last_filter=query&last_value=person&query=person&type=icon
    start_icon = plt.imread('images/start_blue.png')
    finish_icon = plt.imread('images/finish_blue.png')
    axs[1].imshow(start_icon, extent=[maze.start[1]-0.4, maze.start[1]+0.4, maze.start[0]+0.4, maze.start[0]-0.4], zorder=3)
    axs[1].imshow(finish_icon, extent=[maze.end[1]-0.4, maze.end[1]+0.4, maze.end[0]+0.4, maze.end[0]-0.4], zorder=3)

    # create cmap for maze which is transparent for values below vmin
    cmap_maze = mpl.cm.get_cmap('Greys')
    cmap_maze.set_under((0,0,0,0)) #(0,0,0,0) is black with alpha = 0
    # draw maze with vmin = 0.5 -> entries within (0) are transparent
    axs[1].imshow(maze.maze==1, cmap=cmap_maze, vmin=0.5, vmax=1, zorder=1)

    # plot rewards with zorder 1 (below maze)
    im_rewards = axs[1].imshow(agent._reward_table, cmap=cmap_rewards, zorder=2, vmin=-maze._allowed_tries, vmax=-1, norm=norm)
    # create colorbar
    divider = make_axes_locatable(axs[1])
    cax = divider.append_axes('right', size='5%', pad=0.1)

    fig.colorbar(im_rewards, cax=cax, orientation='vertical')

    # plot path
    line_path = axs[1].plot([])[0]

    def update_frame(agent, steps, eps):
        # plt.suptitle(f"Learning Rate: {agent._learning_rate}    Exploration Rate: {agent._exploration_rate:.2f}")
        # update steps
        line_steps.set_xdata(np.arange(len(steps)))
        line_steps.set_ydata(steps)
        axs[0].set_xlim((0, len(steps)))

        line_eps.set_xdata(np.arange(len(eps)))
        line_eps.set_ydata(eps)

        # update path
        i, j = np.array([agent.last_pos_history]).T
        line_path.set_xdata(j)
        line_path.set_ydata(i)

        # update rewards
        # how to update data <https://stackoverflow.com/a/40301148>
        im_rewards.set_data(agent._reward_table)

        plt.savefig(f'tmp_anim_frames/{len(steps):05d}.png', dpi=100)

    return update_frame, fig

def plot_solution(agent, maze, name):
    # set up figure
    fig, axs = plt.subplots(1,1, figsize=(6, 5), layout='tight')

    axs = [axs]

    # remove ticks and labels
    axs[0].set_xticks([])
    axs[0].set_yticks([])

    # https://www.freepik.com/search?format=search&last_filter=query&last_value=person&query=person&type=icon
    start_icon = plt.imread('images/start_blue.png')
    finish_icon = plt.imread('images/finish_blue.png')
    axs[0].imshow(start_icon, extent=[maze.start[1]-0.4, maze.start[1]+0.4, maze.start[0]+0.4, maze.start[0]-0.4], zorder=3)
    axs[0].imshow(finish_icon, extent=[maze.end[1]-0.4, maze.end[1]+0.4, maze.end[0]+0.4, maze.end[0]-0.4], zorder=3)

    # create cmap for maze which is transparent for values below vmin
    cmap_maze = mpl.cm.get_cmap('Greys')
    cmap_maze.set_under((0,0,0,0)) #(0,0,0,0) is black with alpha = 0
    # draw maze with vmin = 0.5 -> entries within (0) are transparent
    axs[0].imshow(maze.maze==1, cmap=cmap_maze, vmin=0.5, vmax=1, zorder=1)

    # plot rewards with zorder 1 (below maze)
    im_rewards = axs[0].imshow(agent._reward_table, cmap=cmap_rewards, zorder=2, vmin=-maze._allowed_tries, vmax=-1, norm=norm)
    # create colorbar
    divider = make_axes_locatable(axs[0])
    cax = divider.append_axes('right', size='5%', pad=0.1)

    fig.colorbar(im_rewards, cax=cax, orientation='vertical')

    # plot path
    line_path = axs[0].plot([])[0]
    # update path
    i, j = np.array([agent.last_pos_history]).T
    line_path.set_xdata(j)
    line_path.set_ydata(i)
    plt.savefig(name)
    # plt.show()

#%%
def create_animation(name, fig, len_steps):
    # use ImageMagick to reate animation
    # stackoverflow: <https://askubuntu.com/a/648245>
    # reduce file size
    # stackoverflow: <https://askubuntu.com/a/757963>
    # os.system(f'convert -delay 20 -resize 20% tmp_anim_frames/* learning_animations/{name}')
    os.system(f"cp tmp_anim_frames/{len_steps:05d}.png figures/{name.split('.gif ')[0]}.png")
    os.system(f'convert -delay 30 -loop 3 tmp_anim_frames/* learning_animations/{name}')
    os.system('rm -rf tmp_anim_frames/')

    plt.close(fig)
