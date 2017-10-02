from toast import game


class ToastViewGame(game.Game):
    def __init__(self, resolution=(480, 270), initial_scene=None):
        super().__init__(resolution, initial_scene)

    def update(self, time):
        pass

    def draw(self, board_data, move_history):
        pass

    def quit(self):
        pass