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

    def output(self, message):
        # Update the output buffer
        # TODO: Make this thread safe
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
            print(self.buffer)
            evt = PlayerInputEvent()
            evt.message = input('Enter move: ')
            pubsub.publish('PLAYER_INPUT', evt)
