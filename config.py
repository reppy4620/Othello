class CFG:

    BoardSize = 8

    MemoryLength = 7
    ActionSize = BoardSize * BoardSize
    NumIterations = 10 ** 4
    NumGames = 30

    IsLoad = False

    NumEvalGames = 10
    EvalWinRate = 0.55

    TempThresh = 10
    TempInit = 1
    TempFinal = 1e-3

    ModelDir = 'models'

    NumInput = 17
    NumBlock = 19
    IsCuda = True
    NumEpoch = 100
    BatchSize = 64
    Cpuct = 1

    NumMCTSSimus = 30
    DirichletAlpha = 0.5
    Epsilon = 0.25
