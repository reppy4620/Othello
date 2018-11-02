from NeuralNetwork import NNetWrapper
from config import CFG
from train import Train


if __name__ == '__main__':
    net = NNetWrapper()
    if CFG.IsLoad:
        net.load()

    train = Train(net)
    train.start()
