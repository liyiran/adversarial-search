from collections import namedtuple

# ______________________________________________________________________________
# Minimax Search
infinity = float('inf')
NOOP = 'Noop'
node_counter = 1


def minimax_decision(state, game, depth_limit=infinity):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
    global node_counter
    node_counter = 1
    player = game.to_move(state)

    def max_value(state, depth):
        if game.terminal_test(state) or depth >= depth_limit:
            # print "max"
            # print state.pieces
            # print game.utility(state, player)
            # print state.to_move
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            temp = v
            v = max(v, min_value(game.result(state, a), depth + 1))
            # if temp < v:
            #     print a
        return v

    def min_value(state, depth):
        if game.terminal_test(state) or depth >= depth_limit:
            # print "min"
            # print state.pieces
            # print state.to_move
            # print game.utility(state, player)
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            temp = v
            v = min(v, max_value(game.result(state, a), depth + 1))
            # if temp < v:
            #     print a
        return v

    # Body of minimax_decision:
    if game.terminal_test(state):
        min_action = None
        farsighted = state.utility
        myopic = state.utility
        return (min_action, myopic, farsighted, node_counter)
    actions = game.actions(state)
    # print max(map(lambda a: min_value(game.result(state, a)), actions))
    if len(actions) > 0:
        # return max(map(lambda a: min_value(game.result(state, a), 0), actions))
        # return max(actions,
        #            key=lambda a: min_value(game.result(state, a)))
        myopic = - infinity
        farsighted = - infinity
        min_action = None
        for a in actions:
            result_state = game.result(state, a)
            result = min_value(result_state, 1)  # min is the first layer
            if result > farsighted:
                farsighted = result
                min_action = a
                myopic = result_state.utility
    return (min_action, myopic, farsighted, node_counter)


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


# ______________________________________________________________________________

# Some Sample Games


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
        my_action = state.moves(state.to_move)
        other_action = state.moves(state.to_move == 'S' and 'C' or 'S')
        return state.is_only_one_play() or (my_action == [NOOP] and other_action == [NOOP])

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


class Chess(Game):

    def actions(self, state):
        return state.moves(state.to_move)

    def result(self, state, move_action):
        global node_counter
        node_counter = node_counter + 1
        new_pieces = []
        '''
          if move_action == NOOP:
            for p in state.pieces:
                new_piece = Piece(type=p.type, coor=p.coor)
                new_pieces.append(new_piece)
            return GameState(to_move=state.to_move == 'S' and 'C' or 'S', utility=state.utility, pieces=new_pieces, row_values=self.config.row_values)
        '''
        if move_action == NOOP:
            new_state = state
            new_state.to_move = state.to_move == 'S' and 'C' or 'S'
            return new_state
        move = None
        original = move_action[0]
        destination = move_action[1]
        eaten = None
        if original[0] - destination[0] == 2 and original[1] - destination[1] == 2:
            eaten = (original[0] - 1, original[1] - 1)
        if original[0] - destination[0] == -2 and original[1] - destination[1] == 2:
            eaten = (original[0] + 1, original[1] - 1)
        if original[0] - destination[0] == 2 and original[1] - destination[1] == -2:
            eaten = (original[0] - 1, original[1] + 1)
        if original[0] - destination[0] == -2 and original[1] - destination[1] == -2:
            eaten = (original[0] + 1, original[1] + 1)
        for p in state.pieces:
            if p.coor == original:
                new_piece = Piece(type=p.type, coor=destination)
                move = p.type
                new_pieces.append(new_piece)
            elif p.coor == eaten:
                pass
            else:
                new_piece = Piece(type=p.type, coor=p.coor)
                new_pieces.append(new_piece)
        to_move = move == 'S' and 'C' or 'S'
        utility = Chess.evaluation(new_pieces, self.config.player, self.config.row_values)
        return GameState(to_move=to_move, utility=utility, pieces=new_pieces, row_values=self.config.row_values)

    def utility(self, state, player):
        return state.utility

    def __init__(self, path, configuration):
        if configuration:
            self.config = configuration
        else:
            self.config = Configuration(path)
        to_move = self.config.player
        pieces = []
        map = self.config.initial_map
        for i in range(len(map)):
            for j in range(len(map[i])):
                if "S" in map[i][j] or "C" in map[i][j]:
                    number = int(map[i][j][1:])
                    for k in range(number):
                        piece = Piece(map[i][j][0], (i, j))
                        pieces.append(piece)
        utility = Chess.evaluation(pieces, self.config.player, self.config.row_values)
        game_state = GameState(to_move=to_move, utility=utility, pieces=pieces, row_values=self.config.row_values)
        self.initial_state = game_state

    @staticmethod
    def evaluation(pieces, player, row_values):
        utility_value = 0
        for piece in pieces:
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

    def coor_to_letter(self, coor):
        x = coor[0]
        y = coor[1] + 1
        return chr((ord('H') - x)) + str(y)

    def translate(self, utility):
        op = utility[0]
        myopic = utility[1]
        farsighted = utility[2]
        node = utility[3]
        result = ''
        if op is (None):
            result += 'pass\n'
        else:
            result += self.coor_to_letter(op[0]) + '-' + self.coor_to_letter(op[1]) + '\n'
        result += str(myopic) + '\n'
        result += str(farsighted) + '\n'
        result += str(node) + '\n'
        return result

    def write_to_file(self, string, path='output.txt'):
        with open(path, 'a') as the_file:
            the_file.write(string)


class GameState:
    def __init__(self, to_move, utility, pieces, row_values):
        self.to_move = to_move
        self.utility = utility
        self.pieces = pieces
        self.row_values = row_values

    def is_only_one_play(self):
        type = None
        for p in self.pieces:
            if not type:
                type = p.type
            elif type != p.type:
                return False
        return True

    def moves(self, player):
        pieces = filter(lambda p: p.type == player, self.pieces)
        action_list = []
        pieces_map = dict()
        for p in self.pieces:
            coor = p.coor
            piece_list = pieces_map.get(coor)
            if piece_list is None:
                pieces_map[coor] = [p]
            else:
                piece_list.append(p)
        for p in pieces:
            coor = p.coor
            left_down = Utility.left_down(coor)
            left_down_down = Utility.left_down_down(coor)
            right_down = Utility.right_down(coor)
            right_down_down = Utility.right_down_down(coor)
            left_up = Utility.left_up(coor)
            left_up_up = Utility.left_up_up(coor)
            right_up = Utility.right_up(coor)
            right_up_up = Utility.right_up_up(coor)
            if p.type == 'S':
                '''
                     0 0
                      S
                '''
                if left_up[0] >= 0 and left_up[1] >= 0 and (pieces_map.get(left_up) is None or (left_up[0] == 0 and pieces_map.get(left_up)[0].type == 'S')):
                    action_name = (coor, left_up)
                    action_list.append(action_name)
                if right_up[0] >= 0 and right_up[1] < 8 and (pieces_map.get(right_up) is None or right_up[0] == 0 and pieces_map.get(right_up)[0].type == 'S'):
                    action_name = (coor, right_up)
                    action_list.append(action_name)
                if left_up[0] >= 0 and left_up[0] >= 0 and left_up_up[0] >= 0 and left_up_up[1] >= 0 and \
                        pieces_map.get(left_up) is not None and pieces_map.get(left_up)[0].type == 'C' \
                        and (pieces_map.get(left_up_up) is None or left_up_up[0] == 0 and pieces_map.get(left_up_up)[0].type == 'S'):
                    action_name = (coor, left_up_up)
                    action_list.append(action_name)
                if right_up[0] >= 0 and right_up[1] < 8 and right_up_up[0] >= 0 and right_up_up[1] < 8 and \
                        pieces_map.get(right_up) is not None and pieces_map.get(right_up)[0].type == 'C' \
                        and (pieces_map.get(right_up_up) is None or right_up_up[0] == 0 and pieces_map.get(right_up_up)[0].type == 'S'):
                    action_name = (coor, right_up_up)
                    action_list.append(action_name)
            if p.type == 'C':
                '''
                    C
                   0 0
                '''
                if left_down[0] < 8 and left_down[1] >= 0 and (pieces_map.get(left_down) is None or left_down[0] == 7 and pieces_map.get(left_down)[0].type == 'C'):
                    action_name = (coor, left_down)
                    action_list.append(action_name)
                if right_down[0] < 8 and right_down[1] < 8 and (pieces_map.get(right_down) is None or right_down[0] == 7 and pieces_map.get(right_down)[0].type == 'C'):
                    action_name = (coor, right_down)
                    action_list.append(action_name)
                if left_down[0] < 8 and left_down[1] >= 0 and left_down_down[0] < 8 and left_down_down[1] >= 0 and \
                        pieces_map.get(left_down) is not None and pieces_map.get(left_down)[0].type == 'S' and \
                        (pieces_map.get(left_down_down) is None or left_down_down[0] == 7 and pieces_map.get(left_down_down)[0].type == 'C'):
                    action_name = (coor, left_down_down)
                    action_list.append(action_name)
                if right_down[0] < 8 and right_down[1] < 8 and right_down_down[0] < 8 and right_down_down[1] < 8 and \
                        pieces_map.get(right_down) is not None and pieces_map.get(right_down)[0].type == 'S' \
                        and (pieces_map.get(right_down_down) is None or right_down_down[0] == 7 and pieces_map.get(right_down_down)[0].type == 'C'):
                    action_name = (coor, right_down_down)
                    action_list.append(action_name)
        if len(action_list) == 0:
            action_list.append(NOOP)
        # print self.pieces
        # print player
        # print action_list
        # print '--------'
        return action_list


class Piece(namedtuple('piece', ['type', 'coor'])):
    def __eq__(self, other):
        return self.type == other.type and self.coor == other.coor

    def __str__(self):
        return "{}({},{})".format(self.type, self.coor[0], self.coor[1])


class Configuration:
    def __init__(self, path):
        if path:
            with open(path) as f:
                file_lines = f.read().splitlines()
                self.player = file_lines[0][0].upper()
                self.algorithm = file_lines[1]
                self.depth_limit = int(file_lines[2])
                self.initial_map = [line.split(',') for line in file_lines[3:11]]
                self.row_values = map(int, file_lines[11].split(','))

    def generate_configuration_from_string(self, par):
        string = par.splitlines()
        self.player = string[0][0].upper()
        self.algorithm = string[1]
        self.depth_limit = int(string[2])
        self.initial_map = [line.split(',') for line in string[3:11]]
        self.row_values = map(int, string[11].split(','))


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
