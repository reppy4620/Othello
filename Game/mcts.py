from config import CFG
from Game.data import Position

import math
import numpy as np


class TreeNode:

    def __init__(self, parent=None, action=None, psa=0.0, child_psas=None):
        if child_psas is None:
            child_psas = list()
        self.Nsa = 0
        self.Wsa = 0.0
        self.Qsa = 0.0
        self.Psa = psa
        self.action = action
        self.children = list()
        self.child_psas = child_psas
        self.parent = parent

    def is_not_leaf(self):
        return True if len(self.children) > 0 else False

    def select_child(self):
        cpuct = CFG.Cpuct

        highest_uct = 0
        highest_idx = 0

        for idx, child in enumerate(self.children):
            uct = child.Qsa + child.Psa * cpuct * (
                math.sqrt(self.Nsa) / (1 + child.Nsa))
            if uct > highest_uct:
                highest_uct = uct
                highest_idx = idx

        return self.children[highest_idx]

    def expand(self, valid, psa_vector):
        self.child_psas = psa_vector
        for idx, move in enumerate(valid):
            if move is not None:
                assert isinstance(move, Position)
                self.add_child_node(parent=self, action=move,
                                    psa=psa_vector[idx])

    def add_child_node(self, parent, action, psa=0.0):
        child_node = TreeNode(parent=parent, action=action, psa=psa)
        self.children.append(child_node)

    def back_prop(self, wsa, v):
        self.Nsa += 1
        self.Wsa = wsa + v
        self.Qsa = self.Wsa / self.Nsa


class MontecarloTreeSearch:

    def __init__(self, net):
        self.root = None
        self.game = None
        self.net = net

    def search(self, game, node, tau):
        self.root = node
        self.game = game

        for i in range(CFG.NumMCTSSimus):
            node = self.root
            game = self.game.clone()

            while node.is_not_leaf():
                node = node.select_child()
                game.step(node.action)

            psa_vector, v = self.net.predict(game.board)

            if node.parent is None:
                psa_vector = self.add_dirichlet_noise(psa_vector)

            valid = game.board.get_movable(game.current_player)
            for idx, move in enumerate(valid):
                if move is None:
                    psa_vector[idx] = 0

            psa_sum = sum(psa_vector)
            if psa_sum > 0:
                psa_vector /= psa_sum

            node.expand_node(valid)
            game_over, wsa = game.is_game_over()

            while node is not None:
                wsa = -wsa
                v = -v
                node.back_prop(wsa, v)
                node = node.parent

        highest_nsa = 0
        highest_idx = 0

        tau = 1 / tau
        for idx, child in enumerate(self.root.children):

            if child.Nsa ** tau > highest_nsa:
                highest_nsa = child.Nsa ** tau
                highest_idx = idx

        return self.root.children[highest_idx]

    @staticmethod
    def add_dirichlet_noise(psa_vector):
        dirichlet_input = [CFG.DirichletAlpha for _ in range(CFG.ActionSize)]

        dirichlet_list = np.random.dirichlet(dirichlet_input)
        noisy_psa_vector = list()

        for idx, psa in enumerate(psa_vector):
            noisy_psa_vector.append(
                (1 - CFG.Epsilon) * psa + CFG.Epsilon * dirichlet_list[idx])

        return noisy_psa_vector
