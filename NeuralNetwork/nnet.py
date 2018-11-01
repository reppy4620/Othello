import torch
import torch.nn as nn
import torch.nn.functional as F

from Game.config import CFG
from Game.rule import Rule


class ResidualBlock(nn.Module):

    def __init__(self):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(256, 256, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(256)
        self.conv2 = nn.Conv2d(256, 256, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(256)

    def forward(self, x):
        h = F.relu(self.bn1(self.conv1(x)))
        h = self.bn2(self.conv2(h))
        return F.relu(h+x)


class DualNet(nn.Module):

    def __init__(self):
        super(DualNet, self).__init__()
        self.conv0 = nn.Conv2d(CFG.NumInput, 256, 3, padding=1)
        self.bn0 = nn.BatchNorm2d(256)
        self.residuals = nn.Sequential(*[ResidualBlock() for _ in range(CFG.NumBlock)])

        self.conv_p1 = nn.Conv2d(256, 2, 1)
        self.bn_p1 = nn.BatchNorm2d(2)
        self.fc_p2 = nn.Linear(Rule.BoardSize * Rule.BoardSize * 2, CFG.ActionSize)

        self.conv_v1 = nn.Conv2d(256, 1, 1)
        self.bn_v1 = nn.BatchNorm2d(1)
        self.fc_v2 = nn.Linear(Rule.BoardSize * Rule.BoardSize, 256)
        self.fc_v3 = nn.Linear(256, 1)

    def forward(self, x):
        x = x.view(-1, CFG.NumInput, Rule.BoardSize, Rule.BoardSize)
        h = F.relu(self.bn0(self.conv0(x)))
        h = self.residuals(h)
        h_p = F.relu(self.bn_p1(self.conv_p1(h)))
        h_p = self.fc_p2(h_p.view(h_p.size(0), -1))

        h_v = F.relu(self.bn_v1(self.conv_v1(h)))
        h_v = F.relu(self.fc_v2(h_v.view(h_v.size(0), -1)))
        h_v = torch.tanh(self.fc_v3(h_v))
        return F.log_softmax(h_p, dim=1), h_v
