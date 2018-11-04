from Game import OthelloEnv, TreeNode
from Game.data import Color, Result
from config import CFG


class Evaluate:

    def __init__(self, net, eval_net):
        self.trained = net
        self.current = eval_net

    def evaluate(self):
        wins = 0
        losses = 0
        draws = 0

        for i in range(CFG.NumEvalGames):
            print(f'Start Evaluation Game : {i}')

            game = OthelloEnv()
            game_over = False
            value = 0
            node = TreeNode()

            while not game_over:
                game.display()
                if game.current_player == Color.Black:
                    best_child = self.trained.search(game, node, CFG.TempFinal)
                else:
                    assert game.current_player == Color.White
                    best_child = self.current.search(game, node, CFG.TempFinal)

                action = best_child.action
                game.step(action)

                game_over, value = game.is_game_over()

                best_child.parent = None
                node = best_child
            game.display()

            if value == Result.BlackWin:
                wins += 1
            elif value == Result.WhiteWin:
                losses += 1
            else:
                assert value == Result.Draw
                draws += 1
        return wins, losses, draws
