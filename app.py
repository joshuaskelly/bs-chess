import time

import controller
import model
#from views.tdl import View
from views.pyglet import View
from views.twitchchat import View as TwitchView

v = View()
c = controller.Controller(model.Model())
tc = TwitchView()

v.start()
c.start()
tc.start()



try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    v.join()
    c.join()
    tc.join()
