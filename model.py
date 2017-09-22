class MoveHistoryItem(object):
    def __init__(self, move, valid, player_name='player', player_color=None):
        self.player_name = player_name
        self.player_color = player_color
        self.move = move
        self.valid = valid


class Model(object):
    def __init__(self):
        # TODO: Decide on chessboard data structure
        self.data = "rnbqkbnr" + \
                    "pppppppp" + \
                    "........" + \
                    "........" + \
                    "........" + \
                    "........" + \
                    "PPPPPPPP" + \
                    "RNBQKBNR"

        self.move_history = []