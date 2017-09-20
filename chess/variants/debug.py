def generate_moves(board_state):
    for i, square in enumerate(board_state):
        if square == '.':
            continue

        for j in range(64):
            yield i, j
