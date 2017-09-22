import configparser
import os
import re
import threading

from twitchobserver import Observer

import events
import pubsub


class TwitchChatInputView(object):
    """Class for handling Twitch chat input."""
    def __init__(self):
        self._worker_thread = None
        self._running = False
        self._buffer = ''
        self._buffer_lock = threading.Lock()

        pubsub.subscribe('QUIT', self.on_quit)

    def on_quit(self):
        self._running = False

    def start(self):
        if self._running:
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self.run)
        self._worker_thread.start()

    def join(self, timeout=0):
        if not self._worker_thread:
            return

        worker = self._worker_thread
        self._worker_thread = None
        self._running = False
        worker.join(timeout)

    def run(self):
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

        with Observer(nickname, password) as observer:
            observer.join_channel(channel)

            while self._running:
                for event in observer.get_events():
                    if event.type == 'TWITCHCHATMESSAGE':
                        move = event.message

                        # Filter Twitch chat input
                        if re.match('[a-h][1-8][a-h][1-8]', move):
                            evt = events.PlayerInputEvent()
                            evt.move = move.lower()
                            evt.player_name = event.nickname

                            hex_color = event.tags['color'].strip('#')
                            r = int(hex_color[0:2], 16)
                            g = int(hex_color[2:4], 16)
                            b = int(hex_color[4:6], 16)

                            evt.player_color = r, g, b

                            pubsub.publish('PLAYER_INPUT', evt)
