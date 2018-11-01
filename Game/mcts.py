from config import CFG

import math


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

    def expand(self, board, color, psa_vector):
        self.child_psas = psa_vector
        valid = board.get_movable(color)
        for idx, move in enumerate(valid):
            if move[0] is not None:
                self.add_child_node(parent=self, action=move,
                                    psa = psa_vector[idx])

    def add_child_node(self, parent, action, psa=0.0):
        child_node = TreeNode(parent=parent, action=action, psa=psa)
        self.children.append(child_node)


class MontecarloTreeSearch:

    def __init__(self):
        pass
