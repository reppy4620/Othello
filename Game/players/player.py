class Player:

    def __init__(self, color):
        self.color = color

    def action(self, board):
        raise NotImplementedError
