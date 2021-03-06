from Game import NormalGame
from Game.players import RandomPlayer
from Game.data import Color


def play():
    game = NormalGame(player1=RandomPlayer(Color.Black), player2=RandomPlayer(Color.White))
    game.play()


if __name__ == '__main__':
    play()
