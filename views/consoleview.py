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

    def output(self, message):
        # Update the output buffer
        with self._buffer_lock:
            self.buffer = message

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
            with self._buffer_lock:
                print(self.buffer)

            evt = PlayerInputEvent()
            evt.message = input('Enter move: ')
            pubsub.publish('PLAYER_INPUT', evt)
