import pubsub


class View(object):
    def __init__(self):
        pubsub.subscribe('OUTPUT', self.output)
        pubsub.subscribe('DISCONNECT', self.disconnect)

    def output(self, message):
        print(message)

    def disconnect(self):
        pubsub.unsubscribe('OUTPUT', self.output)
        pubsub.unsubscribe('DISCONNECT', self.disconnect)
