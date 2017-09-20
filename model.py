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

#a8 -> 07
#a1 -> 00 (8 * row) + col