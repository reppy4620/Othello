from Game.rule import Rule


class CFG:

    MemoryLength = 7
    NumInput = 17
    NumBlock = 19
    ActionSize = Rule.BoardSize * Rule.BoardSize
    IsCuda = True
    NumEpoch = 100
    BatchSize = 64
