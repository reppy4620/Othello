from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from Game.rule import Rule
from Game import OthelloEnv, TreeNode, MontecarloTreeSearch
from Game.data import Color, Result, Position
from NeuralNetwork import NNetWrapper
from config import CFG


black = 'image/black.png'
white = 'image/white.png'
empty = 'image/empty.png'


class OthelloApp(App):
    def build(self):
        return Gui()


class Tile(ButtonBehavior, Image):
    def __init__(self, source, root, x, y):
        super(Tile, self).__init__(source=source)
        self.root = root
        self.action_x, self.action_y = x, y

    def on_press(self):
        action = Position(self.action_x, self.action_y)
        self.root.step(action)


class Gui(BoxLayout):
    grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.env = OthelloEnv()
        self.net = NNetWrapper()
        self.net.load('best_model')
        self.mcts = MontecarloTreeSearch(self.net)
        self.node = TreeNode()
        self.game_over = False
        self.value = 0
        super(Gui, self).__init__(**kwargs)
        self.tiles = [list() for _ in range(Rule.BoardSize)]
        for y in range(Rule.BoardSize):
            for x in range(Rule.BoardSize):
                if (x, y) in Rule.Black:
                    im = Tile(black, self, x, y)
                elif (x, y) in Rule.White:
                    im = Tile(white, self, x, y)
                else:
                    im = Tile(empty, self, x, y)
                self.tiles[y].append(im)
                self.grid.add_widget(im)

    def check_game_over(self):
        game_over, value = self.env.is_game_over()
        if game_over:
            if value == Result.BlackWin:
                print('Win black')
            elif value == Result.WhiteWin:
                print('Win white')
            else:
                assert value == Result.Draw
                print('Draw')

    def step(self, action):
        movable = self.env.board.get_movable(Color.Black)
        if len(movable) != 0:
            if self.env.is_valid(action):
                pos, flippable = self.env.step(action)
                if pos is not None:
                    self.check_game_over()
                    self.tiles[pos.y][pos.x].source = black if self.env.current_player == Color.White else white
                    for x, y in flippable:
                        self.tiles[y][x].source = black if self.env.current_player == Color.White else white
        movable = self.env.board.get_movable(Color.White)
        if len(movable) != 0:
            best_child = self.mcts.search(self.env, TreeNode(), CFG.TempFinal)
            action = best_child.action
            pos, flippable = self.env.step(action)
            if pos is not None:
                self.check_game_over()
                self.tiles[pos.y][pos.x].source = black if self.env.current_player == Color.White else white
                for x, y in flippable:
                    self.tiles[y][x].source = black if self.env.current_player == Color.White else white
                self.check_game_over()


if __name__ == '__main__':
    Window.size = (720, 720)
    OthelloApp().run()
