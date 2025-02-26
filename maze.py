import numpy as np

# for colored terminal output
class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKCYAN      = '\033[96m'
    OKGREEN     = '\033[92m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    ENDC        = '\033[0m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'

class Maze():
    def __init__(self, rules='relaxed', player_type='human', maze='default'):
        """Set up the maze, and store `rules` and `player_type`"""

        # index i defines row (y-axis)
        # index j defines col (x-axis)

        self._load_maze(maze)
        self.pos = np.copy(self.start)


        # position player at start position in the maze
        self.maze[*self.pos] = 2
        self.maze[*self.end] = 3

        self._steps = 0
        self._game_over = False

        self.rules = rules
        self._player_type = player_type
        self._allowed_tries = self.shape[0]**2

    def reset(self):
        self.pos = np.copy(self.start)
        self._steps = 0
        self._game_over = False
    
    def _load_maze(self, filename):
        # load the default maze, as suggested in the tutorial
        if filename == 'default':
            self.maze = np.array([[1,0,1,1,1,1,1],
                                  [1,0,0,0,0,0,1],
                                  [1,0,0,0,0,0,1],
                                  [1,0,0,1,1,1,1],
                                  [1,0,0,1,0,0,1],
                                  [1,0,0,0,0,0,1],
                                  [1,1,1,1,1,0,1]], dtype=int)
            
            self.shape = (7,7)
            self.start = np.array([0,1], dtype=int)
            self.end = np.array([6,5], dtype=int)
        else:
            # print('loading maze')
            file = open('mazes/' + filename)
            lines = file.readlines()
            self.shape = (len(lines), len(lines))
            
            self.maze = np.zeros(shape=self.shape)

            for i, line in enumerate(lines):
                # remove every second character (' ') whis is just there
                # for better visuals of the text file
                for j, char in enumerate(line[::2]):

                    match char:
                        case 'x': self.maze[i,j] = 1
                        case ' ': self.maze[i,j] = 0
                        case '2': 
                            self.start = np.array([i,j], dtype=int)
                            self.maze[i,j] = 0
                        case '3':
                            self.end = np.array([i,j], dtype=int)
                            self.maze[i,j] = 0

    def __str__(self):
        """String representation of the maze, to enable `print(Maze)`"""
        string = ""
        for row in self.maze:
            for pos in row:
                match pos:
                    case 0:
                        string += ' '
                    case 1:
                        string += 'x'
                    case 2:
                        string += 'P'
                    case 3:
                        string += 'E'
                string += ' '
            string += '\n'
        return string

    def _check_pos(self, pos) -> bool:
        """Check if the position is an allowed position of the maze"""
        # return False if pos is a wall
        if self.maze[*pos] == 1: return False

        # move is allowed
        return True
    
    def _allowed_moves(self):
        allowed_moves = []
        if self._player_type == 'human':
            if self._check_pos(self.up()): allowed_moves.append('U')
            if self._check_pos(self.down()): allowed_moves.append('D')
            if self._check_pos(self.left()): allowed_moves.append('L')
            if self._check_pos(self.right()): allowed_moves.append('R')
        if self._player_type == 'robot':
            for action in [self.up, self.down, self.left, self.right]:
                if self._check_pos(action()): allowed_moves.append(action)
        return allowed_moves
    
    def get_moves(self):
        # strict rules: give all moves
        if self.rules == 'strict':
            if self._player_type == 'human':
                return ['U', 'D', 'L', 'R']
            if self._player_type == 'robot':
                return [self.up, self.down, self.left, self.right]
            
        # relaxe rules: just return allowed moves
        return self._allowed_moves()
    
    def move(self, new_pos):
        """Move player to the new position"""

        # handle forbidden move
        if self._check_pos(new_pos) == False:
            # if rules are relaxed player may simply try again
            if self.rules == 'relaxed': 
                print(bcolors.WARNING + 
                      "This move is not allowed!\n" + 
                      bcolors.ENDC)
                return

            # strict rules: end game
            self._steps += 1
            self._game_over = True
            self.pos = new_pos
            return
                
        # remove player from board, update position & add back to board
        self.maze[*self.pos] = 0
        self.pos = new_pos
        self.maze[*self.pos] = 2

        self._steps += 1

        # end game if player is at the end
        if self._is_won(): self._game_over = True

        # end game if player has take too many moves
        if self._steps > self._allowed_tries: self._game_over = True

    def up(self):
        """Position above player"""
        return self.pos + [0,-1]

    def down(self):
        """Position below player"""
        return self.pos + [0,+1]

    def left(self):
        """Position left of player"""
        return self.pos + [-1,0]

    def right(self):
        """Position right of player"""
        return self.pos + [+1,0]
        
    def get_state_and_reward(self):
        """Reward function to train agent"""
        # if self._is_won(): reward = self.shape[0]**2
        # else: reward = -1
        
        return self.pos, -1
    
    def is_game_over(self):
        return self._game_over
    
    def _is_won(self):
        return tuple(self.pos) == tuple(self.end)
    
    def get_steps(self):
        return self._steps
    
########################################################################
# From here there is code for direct execution of the maze as an       #
# interactive game                                                     #
########################################################################

def play(rules='relaxed'):    
    m = Maze(rules)

    while m.is_game_over() == False:
        print(m)

        move = input(f"possible moves: {m.get_moves()}: ")
        match move.upper():
            case 'U': new_pos = m.up()
            case 'D': new_pos = m.down()
            case 'L': new_pos = m.left()
            case 'R': new_pos = m.right()
            case _:
                print(bcolors.WARNING + 
                        "Cannot interpret your instruction\n" + 
                        bcolors.ENDC)
                continue
            
        m.move(new_pos)

    print(m)

    if m._is_won(): print(bcolors.OKGREEN + "You Won!\n" + bcolors.ENDC)
    else: print(bcolors.FAIL + "You Lost!\n" + bcolors.ENDC)

def main():
    print(bcolors.HEADER + "Welcome to the maze game!" + bcolors.ENDC)
    print()

    prompt_text = "What do you want to do?\n" + \
        bcolors.UNDERLINE + "P" + bcolors.ENDC + "lay/" + \
        "Play " +bcolors.UNDERLINE + "S" + bcolors.ENDC + "trict/" + \
        bcolors.UNDERLINE + "Q" + bcolors.ENDC + "uit ['P', 'S', 'Q']: "
    
    inp = input(prompt_text).upper()
    
    while True:
        print()
        match inp:
            # Play with relaxed rules
            case 'P':
                play()
            # Play with strict rules
            case 'S':
                play(rules='strict')
            # Quit game
            case 'Q':
                exit(0)
        
        inp = input(prompt_text).upper()


if __name__ == '__main__': main()