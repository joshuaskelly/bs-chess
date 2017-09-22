import time

import controller
import model
# from views.consoleview import ConsoleView as View
from views.tdl import View as TdlView
from views.twitchchat import View as TwitchView

c = controller.Controller(model.Model())
v = TdlView()
tc = TwitchView()

c.start()
v.start()
tc.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    c.join()
    v.join()
    tc.join()
