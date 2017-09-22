import re
import threading

import pubsub

from chess.variants import debug as current_variant


class Controller(object):
    def __init__(self, model):
        self.model = model
        pubsub.subscribe('PLAYER_INPUT', self.receive_events)
        pubsub.subscribe('QUIT', self.on_quit)
        self.worker_thread = None
        self.running = False
        self.is_dirty = True
        self.event_queue = []
        self._event_queue_lock = threading.Lock()

    def receive_events(self, event):
        """Callback for pubsub notifications. This will queue up events
        to be processed later. This method is thread safe.

        event: The event to be queued and later processed.
        """
        with self._event_queue_lock:
            self.event_queue.append(event)

    def on_quit(self):
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        self.worker_thread = threading.Thread(target=self.run)
        self.worker_thread.start()

    def join(self, timeout=0):
        if not self.worker_thread:
            return

        worker = self.worker_thread
        self.worker_thread = None
        self.running = False
        worker.join(timeout)

    def get_events(self):
        with self._event_queue_lock:
            result = self.event_queue
            self.event_queue = []

        return result

    def validate_move(self, move):
        return re.match('[a-h][1-8][a-h][1-8]', move)

    def perform_move(self, coord):
        # Update our model and possibly mark dirty?
        x, y = coord
        piece = self.model.data[x]
        self.model.data = self.model.data[:x] + '.' + self.model.data[x+1:]
        self.model.data = self.model.data[:y] + piece + self.model.data[y+1:]

    def move_to_coords(self, move):
        start = move[:2]
        col = ord(start[0]) - ord('a')
        row = 7 - (int(start[1]) - 1)
        val1 = (8 * row) + col

        finish = move[2:]
        col = ord(finish[0]) - ord('a')
        row = 7 - (int(finish[1]) - 1)
        val2 = (8 * row) + col

        return val1, val2

    def handle_player_input(self, event):
        if event.type != 'PLAYER_INPUT':
            return

        move = event.move
        if not self.validate_move(move):
            return

        move = self.move_to_coords(move)

        if move in current_variant.generate_moves(self.model.data):
            self.perform_move(move)

    def run(self):
        while self.running:
            if self.is_dirty:
                pubsub.publish('DISPLAY', self.model.data)
                self.is_dirty = False

            for event in self.get_events():
                self.handle_player_input(event)
                self.is_dirty = True

        self.worker_thread.join()