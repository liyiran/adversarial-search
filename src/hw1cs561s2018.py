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
                        number = int(map[i][j][1])
                        for k in range(number):
                            piece = Piece(map[i][j][0], (i, j))
                            self.pieces.append(piece)


class Utility:
    def evaluation(self, config, board):
        player = config.player
        utility_value = 0
        for piece in board.pieces:
            row = piece.coor[0]
            if piece.type == "S":
                utility = config.row_values[7 - row]
            else:
                utility = config.row_values[row]
            if piece.type == player:
                utility_value += utility
            else:
                utility_value -= utility
        return utility_value
