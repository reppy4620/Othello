from Game.rule import Rule


class CFG:

    MemoryLength = 7
    ActionSize = Rule.BoardSize * Rule.BoardSize

    NumInput = 17
    NumBlock = 19
    IsCuda = True
    NumEpoch = 100
    BatchSize = 64
    Cpuct = 1
