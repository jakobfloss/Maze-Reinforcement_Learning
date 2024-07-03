def train():
    maze_name = 'big_maze'
    learning_rate = 0.15
    exploration_rate = 0.3
    decrease_rate = 0.99

    N_iters = 100
    m = maze.Maze(maze=maze_name)
    a = agent.Agent(learning_rate, exploration_rate, decrease_rate, maze_shape=m.shape)

    for i in range(N_iters):
        a.store_reward(*m.get_state_and_reward())
        
        while m.is_game_over() == False:
            action_list = m.get_moves()
            action = a.choose_action(action_list)
            m.move(action())
            a.store_reward(*m.get_state_and_reward())

        a.learn()
        m.reset()