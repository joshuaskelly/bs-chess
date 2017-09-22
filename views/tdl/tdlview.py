import os
import threading

import tdl

import pubsub


class TDLView(object):
    def __init__(self):
        self._worker_thread = None
        self._running = False
        self._buffer = ''
        self._buffer_lock = threading.Lock()
        pubsub.subscribe('DISPLAY', self.output)

    def output(self, data):
        with self._buffer_lock:
            self._buffer = data

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
        console = tdl.init(10, 10, 'BS.CHESS()', renderer='GLSL')

        while self._running:
            console.clear()
            self.draw(console)
            tdl.flush()

            for event in tdl.event.get():
                if event.type == 'QUIT':
                    self._running = False
                    self.join()

    def draw(self, console):
        win = tdl.Window(console, 0, 0, 1, 10)
        win.draw_str(0, 0, ' 87654321')
        win = tdl.Window(console, 0, 9, 10, 1)
        win.draw_str(0, 0, ' abcdefgh')
        win = tdl.Window(console, 1, 1, 8, 8)

        for i, p in enumerate(self._buffer):
            row = i // 8
            col = i % 8

            bg = 192, 192, 192

            if (i + row) % 2:
                bg = 128, 128, 128

            fg = 255, 255, 255

            if p.islower():
                fg = 32, 32, 32

            if p == '.':
                p = ' '

            win.draw_str(col, row, p, fg, bg)
