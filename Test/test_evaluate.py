from Game import OthelloEnv, TreeNode, MontecarloTreeSearch
from Game.data import Color, Result
from NeuralNetwork import NNetWrapper
from config import CFG


def test():
    n1 = NNetWrapper()
    n1.load()
    n2 = NNetWrapper()
    n2.load('best_model')
    m1 = MontecarloTreeSearch(n1)
    m2 = MontecarloTreeSearch(n2)

    game = OthelloEnv()
    game_over = False
    value = 0
    node1 = TreeNode()
    node2 = TreeNode()

    while not game_over:
        game.display()
        if game.current_player == Color.Black:
            best_child = m1.search(game, node1, CFG.TempFinal)
        else:
            best_child = m2.search(game, node2, CFG.TempFinal)

        action = best_child.action
        game.step(action)

        game_over, value = game.is_game_over()

        best_child.parent = None
        if game.current_player == Color.Black:
            node1 = best_child
        else:
            node2 = best_child
    game.display()
    if value == Result.BlackWin:
        print('Win black')
    elif value == Result.WhiteWin:
        print('Win white')
    else:
        assert value == Result.Draw
        print('Draw')


if __name__ == '__main__':
    test()
