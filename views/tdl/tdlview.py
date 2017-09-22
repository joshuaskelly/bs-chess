import os
import threading

import tdl

import pubsub

ROOK = chr(128)
KNIGHT = chr(129)
BISHOP = chr(130)
QUEEN = chr(131)
KING = chr(132)
PAWN = chr(133)


def char_to_semigraphic(char):
    """Converts a char to a special semigraphic character.

    char: A string. Should be in 'rnbqkpRNBQKP '

    Returns: A string mapping to the semigraphic representing the given chess
        piece. Will return a single space if no appropriate mapping can be
        found.
    """
    if char.upper() == 'R':
        return ROOK
    elif char.upper() == 'N':
        return KNIGHT
    elif char.upper() == 'B':
        return BISHOP
    elif char.upper() == 'Q':
        return QUEEN
    elif char.upper() == 'K':
        return KING
    elif char.upper() == 'P':
        return PAWN

    return ' '


class Colors(object):
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    LIGHT_GREY = 192, 192, 192
    GREY = 128, 128, 128
    DARK_GREY = 32, 32, 32


class TDLView(object):
    """TDL view implementation"""
    def __init__(self):
        self._worker_thread = None
        self._running = False
        self._buffer = ''
        self._move_history = ''
        self._buffer_lock = threading.Lock()

        pubsub.subscribe('DISPLAY', self.output)

    def output(self, data, move_history):
        with self._buffer_lock:
            self._buffer = data
            self._move_history = move_history

    def start(self):
        if self._running:
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self.run)
        self._worker_thread.start()

    def join(self, timeout=0):
        if not self._worker_thread:
            return

        worker = self._worker_thread
        self._worker_thread = None
        self._running = False
        worker.join(timeout)

    def run(self):
        working_dir = os.path.dirname(__file__)

        # Get path to font file
        font_file = 'data/terminal32x32_gs_ro.png'
        font_path = os.path.normpath(os.path.join(working_dir, font_file))
        if not os.path.exists(font_path):
            raise RuntimeError('Missing font file: {}'.format(font_file))

        # Init TDL
        tdl.set_font(font_path)
        console = tdl.init(10, 21, 'BS.CHESS()', renderer='GLSL')

        while self._running:
            console.clear()
            self.draw(console)
            tdl.flush()

            for event in tdl.event.get():
                if event.type == 'QUIT':
                    pubsub.publish('QUIT')
                    self._running = False

    def draw(self, console):
        # Draw y-axis legend
        win = tdl.Window(console, 0, 0, 1, 10)
        win.draw_str(0, 0, ' 87654321', Colors.LIGHT_GREY)

        # Draw x-axis legend
        win = tdl.Window(console, 0, 9, 10, 1)
        win.draw_str(0, 0, ' abcdefgh', Colors.LIGHT_GREY)

        # Draw board
        win = tdl.Window(console, 1, 1, 8, 8)

        for i, p in enumerate(self._buffer):
            row = i // 8
            col = i % 8

            # Set square color
            bg = Colors.LIGHT_GREY
            if (i + row) % 2:
                bg = Colors.GREY

            # Set piece color
            fg = Colors.WHITE
            if p.islower():
                fg = Colors.DARK_GREY

            win.draw_str(col, row, char_to_semigraphic(p), fg, bg)

        # Draw move history
        win = tdl.Window(console, 0, 11, 10, 10)
        for i, history in enumerate(reversed(self._move_history[-10:])):
            move = history.move

            x, y = move
            row = 7 - (x // 8) + 1
            col = x % 8
            col = chr(ord('a') + col)
            x = '{}{}'.format(col, row)

            row = 7 - (y // 8) + 1
            col = y % 8
            col = chr(ord('a') + col)
            y = '{}{}'.format(col, row)

            move = '{}{}'.format(x, y)

            name = history.player_name
            fg = history.player_color

            move_color = Colors.WHITE

            if not history.valid:
                move_color = Colors.GREY
                fg = tuple(map(lambda x: int(x / 2), fg))

            win.draw_str(0, i, move, fg=move_color)
            win.draw_str(4, i, name[:6], fg=fg)
