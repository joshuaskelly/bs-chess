from toast.scene_graph import Scene

from .toastviewgame import ToastViewGame
from views import view


class ToastView(view.View):
    def __init__(self):
        super().__init__()

    def draw(self, board_data, move_history):
        self.game.draw(board_data, move_history)

    def update(self, time):
        self.game.run_step()

    def init(self):
        self.game = ToastViewGame(initial_scene=Scene)
        #self.game.run()

    def deinit(self):
        self.game.quit()
