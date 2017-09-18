import pubsub


class Controller(object):
    def __init__(self, model):
        self.model = model

    def run(self):
        pubsub.publish('OUTPUT', self.model.data, test='Test')
        pubsub.publish('DISCONNECT')
        pubsub.publish('OUTPUT', 'This should not display')
