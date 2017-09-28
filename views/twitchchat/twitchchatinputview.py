import configparser
import os
import re

from twitchobserver import Observer

import pubsub

from views import view


class TwitchChatInputView(view.View):
    """Class for handling Twitch chat input."""
    def __init__(self):
        super().__init__()
        self.observer = None

        pubsub.subscribe('QUIT', self.on_quit)

    def on_quit(self):
        self._running = False

    def init(self):
        working_dir = os.path.dirname(__file__)
        config_path = os.path.normpath(os.path.join(working_dir, './config.cfg'))

        if not os.path.exists(config_path):
            raise RuntimeError('Missing Twitch chatbot config.cfg file')

        # Import Twitch bot settings
        config = configparser.ConfigParser()
        config.read(config_path)
        nickname = config['TWITCH']['Nickname']
        password = config['TWITCH']['Password']
        channel = config['TWITCH']['Channel']

        self.observer = Observer(nickname, password)
        self.observer.start()
        self.observer.join_channel(channel)

    def deinit(self):
        self.observer.join()

    def update(self, time):
        for event in self.observer.get_events():
            if event.type == 'TWITCHCHATMESSAGE':
                move = event.message

                # Filter Twitch chat input
                if re.match('[a-h][1-8][a-h][1-8]', move):
                    move = move.lower()
                    player_name = event.nickname

                    player_color = event.tags['color']

                    if not player_color:
                        player_color = '#FFFFFF'

                    hex_color = player_color.strip('#')
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)

                    player_color = r, g, b

                    self.send_move(move, player_name, player_color)
