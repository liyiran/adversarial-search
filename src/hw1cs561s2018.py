from collections import Counter
from collections import namedtuple
from copy import deepcopy

infinity = float('inf')
Action = namedtuple('Action', 'action_name, new_state')


# ______________________________________________________________________________
# Minimax Search


def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minimax_decision:
    return max(game.actions(state),
               key=lambda a: min_value(game.result(state, a)))


# ______________________________________________________________________________


def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                                         game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class Configuration:
    def __init__(self, path):
        if path:
            with open(path) as f:
                file_lines = f.read().splitlines()
                self.player = file_lines[0][0].upper()
                self.algorithm = file_lines[1]
                self.depth_limit = int(file_lines[2])
                self.initial_state = Board(pieces=None, map=[line.split(',') for line in file_lines[3:11]])
                self.row_values = map(int, file_lines[11].split(','))


class Piece:
    def __init__(self, type, coor):
        self.type = type
        self.coor = coor

    def __eq__(self, other):
        return self.type == other.type and self.coor == other.coor

    def __str__(self):
        return "{}({},{})".format(self.type, self.coor[0], self.coor[1])


class Board:
    def __init__(self, pieces, map):
        self.map = map
        if pieces:
            self.pieces = pieces
        else:
            self.pieces = []
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if "S" in map[i][j] or "C" in map[i][j]:
                        number = int(map[i][j][1:])
                        for k in range(number):
                            piece = Piece(map[i][j][0], (i, j))
                            self.pieces.append(piece)

    def is_only_one_play(self):
        return len(Counter(map(lambda p: p.type, self.pieces)).keys()) == 1

    def evaluation(self, row_values, player):
        utility_value = 0
        for piece in self.pieces:
            row = piece.coor[0]
            if piece.type == "S":
                utility = row_values[7 - row]
            else:
                utility = row_values[row]
            if piece.type == player:
                utility_value += utility
            else:
                utility_value -= utility
        return utility_value

    def get_element(self, coor):
        if coor[0] < 0 or coor[1] < 0 or coor[0] >= len(self.map[0]) or coor[1] >= len(self.map[0]):
            return "-1"
        else:
            return self.map[coor[0]][coor[1]]

    def on_boarder(self, coor):
        if coor[0] == 0 and 'S' in self.get_element(coor):
            return True
        if coor[0] == 7 and 'C' in self.get_element(coor):
            return True
        return False


class Utility:

    @staticmethod
    def left_down(coor):
        return coor[0] + 1, coor[1] - 1

    @staticmethod
    def left_down_down(coor):
        return coor[0] + 2, coor[1] - 2

    @staticmethod
    def right_down(coor):
        return coor[0] + 1, coor[1] + 1

    @staticmethod
    def right_down_down(coor):
        return coor[0] + 2, coor[1] + 2

    @staticmethod
    def left_up(coor):
        return coor[0] - 1, coor[1] - 1

    @staticmethod
    def left_up_up(coor):
        return coor[0] - 2, coor[1] - 2

    @staticmethod
    def right_up(coor):
        return coor[0] - 1, coor[1] + 1

    @staticmethod
    def right_up_up(coor):
        return coor[0] - 2, coor[1] + 2


class GameState:
    def __init__(self, to_move, utility, board, row_values):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.row_values = row_values

    def move_piece(self, board, coor, old_piece):
        new_board = deepcopy(board)
        new_board.map[old_piece.coor[0]][old_piece.coor[1]] = '0'
        position = new_board.map[coor[0]][coor[1]]
        if position == '0':
            new_board.map[coor[0]][coor[1]] = old_piece.type + '1'
        else:
            new_board.map[coor[0]][coor[1]] = old_piece.type + str(int(position[1:]) + 1)
        piece = deepcopy(old_piece)
        piece.coor = coor
        new_board.pieces = filter(lambda p: p.coor != coor, board.pieces).append(piece)
        to_move = old_piece.type == 'S' and 'C' or 'S'
        new_state = GameState(to_move=to_move, utility=new_board.evaluation(self.row_values, to_move), board=new_board)
        return new_state

    def moves(self):
        player = self.to_move
        board = self.board
        pieces = filter(lambda p: p.type == player, board.pieces)
        action_list = []
        for p in pieces:
            coor = p.coor
            left_down = Utility.left_down(coor)
            right_down = Utility.right_down(coor)
            left_up = Utility.left_up(coor)
            right_up = Utility.right_up(coor)
            if player == "C":
                '''
                        C
                       0 0
                '''
                if board.get_element(left_down) == '0' or board.on_boarder(left_down):  # left down corner
                    # action should be a tuple,(action name, new board)
                    action_name = (coor, left_down)

                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, left_down, p)))

                if board.get_element(right_down) == '0' or board.on_boarder(right_down):  # right down corner
                    action_name = (coor, right_down)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, right_down, p)))

                left_down_down = Utility.left_down_down(coor)
                if "S" in board.get_element(left_down) and (board.get_element(left_down_down) == '0' or board.on_boarder(left_down_down)):  # eat and jump
                    action_name = (coor, left_down_down)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, left_down_down, p)))  # left eat down
                right_down_down = Utility.right_down_down(coor)
                if "S" in board.get_element(right_down) and (board.get_element(right_down_down) == '0' or board.on_boarder(right_down_down)):  # eat and jump
                    action_name = (coor, right_down_down)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, right_down_down, p)))  # right eat down
            if player == "S":
                '''
                       0 0
                        S
                '''
                if board.get_element(left_up) == '0' or board.on_boarder(left_up):
                    action_name = (coor, left_up)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, left_up, p)))
                if board.get_element(right_up) == '0' or board.on_boarder(right_up):
                    action_name = (coor, right_up)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, right_up, p)))
                left_up_up = Utility.left_up_up(coor)
                if "C" in board.get_element(left_up) and (board.get_element(left_up_up) == '0' or board.on_boarder(left_up_up)):
                    action_name = (coor, left_up_up)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, left_up_up, p)))
                right_up_up = Utility.right_up_up(coor)
                if "C" in board.get_element(right_up) and (board.get_element(right_up_up) == '0' or board.on_boarder(right_up_up)):
                    action_name = (coor, right_up_up)
                    action_list.append(Action(action_name=action_name, new_state=self.move_piece(board, right_up_up, p)))
        return action_list


class Chess(Game):
    def actions(self, state):
        return state.moves()

    def __init__(self, path):
        self.conf = Configuration(path=path)
        self.initial = GameState(to_move=self.conf.player, utility=self.conf.initial_state.evaluation(self.conf.row_values, self.conf.player), board=self.conf.initial_state, row_values=self.conf.row_values)

    def utility(self, state, player):
        return state.utility

    def result(self, state, move):
        return move.new_state
