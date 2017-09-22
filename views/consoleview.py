import threading

import pubsub

from events import PlayerInputEvent


class ConsoleView(object):
    """Class that encapsulates logic for console display and input"""
    def __init__(self):
        pubsub.subscribe('DISPLAY', self.output)
        self.worker_thread = None
        self.running = False
        self.buffer = ''
        self._buffer_lock = threading.Lock()
        self.is_dirty = True

    def output(self, message, move_history):
        # Update the output buffer
        with self._buffer_lock:
            self.buffer = message
            self.is_dirty = True

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

    def run(self):
        while self.running:
            if self.is_dirty:
                with self._buffer_lock:
                    row = [8, 7, 6, 5, 4, 3, 2, 1]
                    for i in range(0, 64, 8):
                        print(str(row.pop(0)) + self.buffer[i:i+8])
                    print(' abcdefgh')

                evt = PlayerInputEvent()
                evt.move = input('Enter move: ')
                pubsub.publish('PLAYER_INPUT', evt)
                self.is_dirty = False
