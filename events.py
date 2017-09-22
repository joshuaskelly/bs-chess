class PlayerInputEvent(object):
    def __init__(self):
        self.type = 'PLAYER_INPUT'
        self.move = ''
        self.player_name = 'player'
        self.player_color = None
