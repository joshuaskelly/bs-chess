import pubsub

from events import PlayerInputEvent


class ConsoleView(object):
    """Class that encapsulates logic for console display and input"""
    def __init__(self):
        pubsub.subscribe('DISPLAY', self.output)

    def output(self, message):
        # Draw stuff to the screen
        print(message)

    def update(self):
        evt = PlayerInputEvent()
        evt.message = input('Enter move: ')
        pubsub.publish('PLAYER_INPUT', evt)
