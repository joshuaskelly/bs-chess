import os

import pyglet

from views import view


class PygletView(view.View):
    def __init__(self):
        super().__init__()
        self.window = None

    def init(self):
        working_dir = os.path.dirname(__file__)
        image_file = 'data/chessman.png'
        image_path = os.path.normpath(os.path.join(working_dir, image_file))
        self.image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(self.image)

        self.window = pyglet.window.Window()
        pyglet.options['debug_gl'] = False

        @self.window.event
        def on_draw():
            # Render using the self._board_data attribute
            self.window.clear()
            self.sprite.draw()

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.sprite.position = x, y

    def deinit(self):
        pass

    def draw(self, board_data, move_history):
        pass

    def update(self, time):
        pyglet.clock.tick()

        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip()
