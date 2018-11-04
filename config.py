class CFG:

    BoardSize = 8

    MemoryLength = 8
    ActionSize = BoardSize * BoardSize
    NumIterations = 10 ** 4
    NumGames = 30

    IsLoad = True

    NumEvalGames = 1
    EvalWinRate = 0.55

    TempThresh = 10
    TempInit = 1
    TempFinal = 1e-3

    ModelDir = 'models'

    NumInput = 17
    NumBlock = 19
    IsCuda = True
    NumEpoch = 20
    BatchSize = 64

    NumMCTSSimus = 50
    DirichletAlpha = 0.5
    Epsilon = 0.25
    Cpuct = 1
