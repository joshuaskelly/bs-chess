import threading

import pubsub


class Controller(object):
    def __init__(self, model):
        self.model = model
        pubsub.subscribe('PLAYER_INPUT', self.handle_events)
        self.worker_thread = None
        self.running = False
        self.is_dirty = True

    def handle_events(self, event):
        # TODO: Make this thread safe
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
                pubsub.publish('DISPLAY', self.model.data)
                self.is_dirty = False
