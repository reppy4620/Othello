from .nnet import DualNet
from Game.rule import Rule
from config import CFG

import os
import numpy as np
import torch
import torch.optim as optim


class NNetWrapper:

    def __init__(self):
        self.net = DualNet()
        self.board_x, self.board_y = Rule.BoardSize, Rule.BoardSize
        self.action_size = CFG.ActionSize

        self.optimizer = optim.Adam(self.net.parameters())

        self.net.cuda()

    def train(self, examples):
        print('Start Train')

        for epoch in range(CFG.NumEpoch):
            print(f'Epoch {epoch+1}')
            self.net.train()

            batch_idx = 0
            while batch_idx < int(len(examples) / CFG.BatchSize):
                sample_idxs = np.random.randint(len(examples), size=CFG.BatchSize)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_idxs]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                if CFG.IsCuda:
                    boards = boards.contiguous().cuda()
                    target_pis = target_pis.contiguous().cuda()
                    target_vs = target_vs.contiguous().cuda()

                out_pi, out_v = self.net(boards)
                l_pi = self.loss_pi(out_pi, target_pis)
                l_v = self.loss_v(out_v, target_vs)
                total_loss = l_pi + l_v + 0

                self.optimizer.zero_grad()
                total_loss.backward()
                self.optimizer.step()
                batch_idx += 1

    def predict(self, board):
        state = board.state
        state = torch.FloatTensor(state).contiguous()
        if CFG.IsCuda:
            state = state.contiguous().cuda()
        with torch.no_grad():
            state = state.view(CFG.NumInput, self.board_x, self.board_y)

            self.net.eval()
            pi, v = self.net(state)

        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    @staticmethod
    def loss_pi(outputs, targets):
        return -torch.sum(targets * outputs) / targets.size()[0]

    @staticmethod
    def loss_v(outputs, targets):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save(self, file_name='current_model'):
        file_path = os.path.join(CFG.ModelDir, file_name+'.pth')
        try:
            torch.save({'model': self.net.state_dict(),
                        'optimizer': self.optimizer.state_dict()}, file_path)
            print('save model and optimizer successfully')
        except IOError:
            print('Cannot save model and optimizer.')

    def load(self, file_name='current_model', load_optimizer=False):
        file_path = os.path.join(CFG.ModelDir, file_name+'pth')
        try:
            loads = torch.load(file_path)
            self.net.load_state_dict(loads['model'])
            print('Load model successfully.')
            if load_optimizer:
                self.optimizer.load_state_dict(loads['optimizer'])
                print('Load optimizer successfully.')
        except IOError:
            print('Cannot load model and optimizer.')
