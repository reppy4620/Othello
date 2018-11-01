from Game import NormalGame
from Game.players import RandomPlayer
from Game.data import Color


def check():
    game = NormalGame(player1=RandomPlayer(Color.Black), player2=RandomPlayer(Color.White))
    print(game.env.state)
