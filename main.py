from NeuralNetwork import NNetWrapper
from config import CFG
from train import Train

import os


if __name__ == '__main__':
    net = NNetWrapper()
    if CFG.IsLoad:
        print('Load Network')
        net.load()
    else:
        if not os.path.isdir(CFG.ModelDir):
            print(f'Make directory : {CFG.ModelDir}')
            os.mkdir(CFG.ModelDir)
        print('Train Network from scratch.')

    train = Train(net)
    train.start()
