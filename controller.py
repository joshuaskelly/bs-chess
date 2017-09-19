import pubsub


class Controller(object):
    def __init__(self, model):
        self.model = model
        pubsub.subscribe('PLAYER_INPUT', self.handle_events)

    def handle_events(self, event):
        pass

    def update(self):
        pubsub.publish('DISPLAY', self.model.data)
