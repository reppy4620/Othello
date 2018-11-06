from GUI import OthelloApp
from kivy.core.window import Window


if __name__ == '__main__':
    Window.size = (720, 720)
    app = OthelloApp()
    app.run()
