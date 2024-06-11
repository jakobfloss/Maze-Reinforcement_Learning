import agent
import maze
import numpy as np

pos   = lambda : ( 0, 0)
up    = lambda : ( 0, 1)
down  = lambda : ( 0,-1)
left  = lambda : (-1, 1)
right = lambda : ( 1, 0)

action_list = [up, down, left, right]

# agent is nut supposed to explore -> guaranteed to go to highest reward
a = agent.Agent(pos, 0, 0)

a._reward_table = {pos():   1,
                   up():    5,
                   down():  1,
                   left():  1,
                   right(): 1}

assert(a.choose_action(action_list)() == up())

a._reward_table = {pos():   1,
                   up():    1,
                   down():  12,
                   left():  1,
                   right(): 1}

assert(a.choose_action(action_list)() == down())

a._reward_table = {pos():   1,
                   up():    1,
                   down():  1,
                   left():  20,
                   right(): 1}

assert(a.choose_action(action_list)() == left())

a._reward_table = {pos():   1,
                   up():    1,
                   down():  1,
                   left():  1,
                   right(): 3}

assert(a.choose_action(action_list)() == right())

m = maze.Maze()
assert(tuple(m.start) == (1,0))
new_pos = m.start+np.array([0,-1])
assert(m.check_pos(m.start+np.array([0,-1])) == False)