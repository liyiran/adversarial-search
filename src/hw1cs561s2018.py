from collections import namedtuple

# ______________________________________________________________________________
# Minimax Search
infinity = float('inf')
NOOP = 'Noop'
node_counter = 1


def minimax_decision(state, game, depth_limit=infinity):
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

    if game.terminal_test(state):
        min_action = 'Noop'
        farsighted = state.utility
        myopic = state.utility
        if state.is_only_one_play():
            return min_action, myopic, farsighted, 1
        else:
            return min_action, myopic, farsighted, 3
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
    return min_action, myopic, farsighted, node_counter


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)
    node_counter = [2]

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
            node_counter[0] += 1
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
            node_counter[0] += 1
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth >= d or
                                         game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    myopic = None
    # Body of minimax_decision:
    if game.terminal_test(state):
        min_action = 'Noop'
        farsighted = state.utility
        myopic = state.utility
        if state.is_only_one_play():
            return min_action, myopic, farsighted, 1
        else:
            return min_action, myopic, farsighted, 3
    for a in game.actions(state):
        result = game.result(state, a)
        v = min_value(result, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
            myopic = result.utility
    return (best_action, myopic, best_score, node_counter[0])


class Game:

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state):
        # my_action = state.moves(state.to_move)
        # other_action = state.moves(state.to_move == 'S' and 'C' or 'S')
        # return state.is_only_one_play() or (my_action == [NOOP] and other_action == [NOOP])
        return state.is_only_one_play() or state.c_no_move and state.s_no_move

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
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
        new_s_pieces = []
        new_c_pieces = []
        if move_action == NOOP:
            new_state = state
            if state.to_move == 'S':
                state.s_no_move = True
            else:
                state.c_no_move = True
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
        for p in state.s_pieces + state.c_pieces:
            if p.coor == original:
                new_piece = Piece(type=p.type, coor=destination)
                move = p.type
                if p.type == 'S':
                    new_s_pieces.append(new_piece)
                else:
                    new_c_pieces.append(new_piece)
            elif p.coor == eaten:
                pass
            else:
                new_piece = Piece(type=p.type, coor=p.coor)
                if p.type == 'S':
                    new_s_pieces.append(new_piece)
                else:
                    new_c_pieces.append(new_piece)
        to_move = move == 'S' and 'C' or 'S'
        utility = Chess.evaluation(s_pieces=new_s_pieces, c_pieces=new_c_pieces, player=self.config.player, row_values=self.config.row_values)
        return GameState(to_move=to_move, utility=utility, s_pieces=new_s_pieces, c_pieces=new_c_pieces, row_values=self.config.row_values)

    def utility(self, state, player):
        return state.utility

    def __init__(self, path, configuration):
        if configuration:
            self.config = configuration
        else:
            self.config = Configuration(path)
        to_move = self.config.player
        s_pieces = []
        c_pieces = []
        map = self.config.initial_map
        for i in range(len(map)):
            for j in range(len(map[i])):
                if "S" in map[i][j] or "C" in map[i][j]:
                    number = int(map[i][j][1:])
                    for k in range(number):
                        piece = Piece(map[i][j][0], (i, j))
                        if "S" in map[i][j]:
                            s_pieces.append(piece)
                        else:
                            c_pieces.append(piece)
        utility = Chess.evaluation(s_pieces, c_pieces, self.config.player, self.config.row_values)
        game_state = GameState(to_move=to_move, utility=utility, s_pieces=s_pieces, c_pieces=c_pieces, row_values=self.config.row_values)
        self.initial_state = game_state

    @staticmethod
    def evaluation(s_pieces, c_pieces, player, row_values):
        utility_value = 0
        for piece in s_pieces:
            row = piece.coor[0]
            utility = row_values[7 - row]
            if 'S' == player:
                utility_value += utility
            else:
                utility_value -= utility
        for piece in c_pieces:
            row = piece.coor[0]
            utility = row_values[row]
            if 'C' == player:
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
        if op == 'Noop':
            result += 'pass\n'
        else:
            result += self.coor_to_letter(op[0]) + '-' + self.coor_to_letter(op[1]) + '\n'
        result += str(myopic) + '\n'
        result += str(farsighted) + '\n'
        result += str(node) + '\n'
        return result

    def write_to_file(self, string, path='output.txt'):
        with open(path, 'w') as the_file:
            the_file.write(string)


class GameState:
    def __init__(self, to_move, utility, s_pieces, c_pieces, row_values, s_no_move=False, c_no_move=False):
        self.to_move = to_move
        self.utility = utility
        self.s_pieces = s_pieces
        self.c_pieces = c_pieces
        self.row_values = row_values
        self.s_no_move = s_no_move
        self.c_no_move = c_no_move

    def is_only_one_play(self):
        return (not self.c_pieces) != (not self.s_pieces)

    def moves(self, player):
        if self.is_only_one_play():
            return [NOOP]
        if player == 'S':
            pieces = self.s_pieces
        else:
            pieces = self.c_pieces
        action_list = []
        pieces_map = dict()
        for p in self.s_pieces + self.c_pieces:
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


def main():
    chess = Chess(path="../res/input5.txt", configuration=None)
    if chess.config.algorithm == 'MINIMAX':
        result = minimax_decision(game=chess, state=chess.initial_state, depth_limit=chess.config.depth_limit)
    else:
        result = alphabeta_cutoff_search(game=chess, state=chess.initial_state, d=chess.config.depth_limit)
    string = chess.translate(result)
    chess.write_to_file(string=string, path="../res/output5_my.txt")


if __name__ == "__main__":
    main()
