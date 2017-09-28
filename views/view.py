import time
import threading

import pubsub

import events


class View(object):
    def __init__(self):
        self._worker_thread = None
        self._running = False
        self._board_data = ''
        self._move_history = ''
        self._board_data_lock = threading.Lock()

        pubsub.subscribe('DISPLAY', self._update_board_data)

    def draw(self, board_data):
        """Override this to render out the board state"""

    def update(self, time):
        """Override this to handle per frame logic"""

    def init(self):
        """Override this with view specific initialization logic."""

    def deinit(self):
        """Override this with view specific clean up logic."""

    def send_move(self, move, player_name, player_color):
        evt = events.PlayerInputEvent()
        evt.move = move
        evt.player_name = player_name
        evt.player_color = player_color

        pubsub.publish('PLAYER_INPUT', evt)

    def _update_board_data(self, board_data, move_history):
        """Updates the cached version of the model.

        Note: This is called out of process.
        """
        with self._board_data_lock:
            self._board_data = board_data
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
        self.init()
        last_time = time.time()

        while self._running:
            self.draw(self._board_data)
            self.update(time.time() - last_time)
            last_time = time.time()

        self.deinit()
