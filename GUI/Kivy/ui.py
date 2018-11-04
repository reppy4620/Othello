from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

from Game.rule import Rule


black = Image(source='image/black.png').texture
white = Image(source='image/white.png').texture
empty = Image(source='image/empty.png').texture


class OthelloApp(App):
    def build(self):
        return Gui()


class Tile(ButtonBehavior, Image):
    def __init__(self, source):
        super(Tile, self).__init__(source=source)

    def on_press(self):
        self.source = 'image/black.png'
        self.reload()


class Gui(BoxLayout):
    grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Gui, self).__init__(**kwargs)
        self.tiles = list()
        for y in range(Rule.BoardSize):
            self.tiles.append(list())
            for x in range(Rule.BoardSize):
                if (x, y) in Rule.Black:
                    im = Tile(source='image/black.png')
                elif (x, y) in Rule.White:
                    im = Tile(source='image/white.png')
                else:
                    im = Tile(source='image/empty.png')
                self.tiles[y].append(im)
                self.grid.add_widget(im)


if __name__ == '__main__':
    Window.size = (720, 720)
    OthelloApp().run()
