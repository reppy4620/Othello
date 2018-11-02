from .env import OthelloEnv
from .data import Result


class NormalGame:

    def __init__(self, player1, player2):
        self.env = OthelloEnv()
        self.players = [None, player1, player2]

    def play(self):
        game_over = False
        value = 0
        while not game_over:
            self.env.display()
            action = self.players[self.env.current_player].action(self.env.board)
            _, _, game_over, value = self.env.step(action)
        self.env.display()
        if value == Result.BlackWin:
            print('Black Win !!')
        elif value == Result.WhiteWin:
            print('White Win !!')
        else:
            print('Draw')
