import controller
import model
import view

c = controller.Controller(model.Model())
v = view.View()

c.run()
