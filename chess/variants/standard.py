N = -10
S = 10
W = -1
E = 1

directions = {
    'P': (N, N+W, N+E),
    'R': (N, W, S, E),
    'N': (N+N+W, N+N+E, W+W+N, W+W+S, S+S+W, S+S+E, E+E+N, E+E+S),
    'B': (N+W, N+E, S+W, S+E),
    'Q': (N, W, S, E, N+W, N+E, S+W, S+E),
    'K': (N, W, S, E, N+W, N+E, S+W, S+E),
    'p': (S, S + W, S + E),
    'r': (N, W, S, E),
    'n': (N + N + W, N + N + E, W + W + N, W + W + S, S + S + W, S + S + E, E + E + N, E + E + S),
    'b': (N + W, N + E, S + W, S + E),
    'q': (N, W, S, E, N + W, N + E, S + W, S + E),
    'k': (N, W, S, E, N + W, N + E, S + W, S + E)
}

valid_square = 'PRNBQKprnbqk.'


def valid_destination(piece, dest):
    if piece.upper() == piece:
        return dest in 'prnbqk.'

    else:
        return dest in 'PRNBQK.'


def translate_index(index):
    row = (index // 10) - 2
    col = (index % 10) - 1

    return col + (row * 8)


def generate_moves(board_state):
    # Pads board with white space for easier out of bounds detection
    board = ''
    for i in range(0, 63, 8):
        sub_string = board_state[i:i+8]
        board += ' {} '.format(sub_string)

    board = '          ' * 2 + board + '          ' * 2

    # Determine set of valid moves
    for i, square in enumerate(board):
        if square in '. ':
            continue

        # Check all possible directions
        for d in directions[square]:
            # Check all squares along the given direction
            for r in range(1, 8):
                dest = i + (d * r)

                # Check to see if the move is off the board
                if not valid_destination(square, board[dest]):
                    break

                # Special case: Pawns only move diagonal when capturing
                if square == 'P' and d != N:
                    if board[dest] == '.':
                        break

                if square == 'p' and d != S:
                    if board[dest] == '.':
                        break

                # Special case: Pawns can only capture diagonally
                if square == 'P' and d == N:
                    if board[dest] in 'kqbnrp':
                        break

                if square == 'p' and d == S:
                    if board[dest] in 'KQBNRP':
                        break

                yield translate_index(i), translate_index(dest)

                # Special case: Pawns can move two square for first move
                if square == 'P' and 80 <= i < 90 and d == N:
                    dest = i + (d * 2)

                    # Don't capture on a two square move
                    if board[dest] in 'kqbnrp':
                        break

                    yield translate_index(i), translate_index(dest)

                if square == 'p' and 30 <= i < 40 and d == S:
                    dest = i + (d * 2)

                    # Don't capture on a two square move
                    if board[dest] in 'KQBNRP':
                        break

                    yield translate_index(i), translate_index(dest)

                # Stop pieces that only move once
                if square.upper() not in 'QBR':
                    break
