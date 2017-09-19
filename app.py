import controller
import model

from views import consoleview

c = controller.Controller(model.Model())
v = consoleview.ConsoleView()

running = True

while running:
    c.update()
    v.update()
