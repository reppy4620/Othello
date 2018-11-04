from Game import OthelloEnv, MontecarloTreeSearch, TreeNode
from evaluate import Evaluate
from NeuralNetwork import NNetWrapper
from config import CFG


class Train:

    def __init__(self, net):
        self.net = net
        self.eval_net = NNetWrapper()

    def start(self):
        for i in range(CFG.NumIterations):
            print(f'Iteration : {i+1}')

            training_data = list()

            for j in range(CFG.NumGames):
                print(f'Start Training Self-Play Game : {j}')
                self.play_game(training_data)

            self.net.save()
            self.eval_net.load()

            self.net.train(training_data)

            current_mcts = MontecarloTreeSearch(self.net)
            eval_mcts = MontecarloTreeSearch(self.eval_net)

            evaluator = Evaluate(current_mcts, eval_mcts)

            wins, losses, draw = evaluator.evaluate()

            print(f'wins : {wins}')
            print(f'loss : {losses}')

            win_rate = wins / (wins+losses+draw)

            print(f'win rate : {win_rate}')

            if win_rate > CFG.EvalWinRate:
                print('New models saved as best models.')
                self.net.save('best_model')
            else:
                print('New models discarded and previous models loaded.')
                self.net.load()

    def play_game(self, training_data):
        game = OthelloEnv()
        mcts = MontecarloTreeSearch(self.net)
        game_over = False
        value = 0
        self_play_data = list()
        count = 0

        node = TreeNode()
        while not game_over:
            if count < CFG.TempThresh:
                best_child = mcts.search(game, node, CFG.TempInit)
            else:
                best_child = mcts.search(game, node, CFG.TempFinal)
            if best_child.action is not None:
                self_play_data.append([game.board.state,
                                       best_child.parent.child_psas,
                                       0])
            action = best_child.action
            game.step(action)

            game_over, value = game.is_game_over()

            best_child.parent = None
            node = best_child

        for data in self_play_data:
            value = -value
            data[2] = value
            training_data.append(data)
