import time

import controller
import model

from views import consoleview

c = controller.Controller(model.Model())
v = consoleview.ConsoleView()

c.start()
v.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    c.join()
    v.join()

