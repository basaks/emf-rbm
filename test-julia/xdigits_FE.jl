using Boltzmann
using HDF5

function run_xdigits()

    X = h5open("xdigits.h5", "r") do file
        read(file, "X")
    end

    println("norm X ",norm(X))

    # Set parameters
    Epochs         = 1
    BatchSize      = 100
    HiddenUnits    = 64
    Approx         = "tap2"
    ApproxSteps    = 5
    LearnRate      = 0.005
    MonitorEvery   = 1
    PersistStart   = 1
    Momentum       = 0.5
    DecayMagnitude = 0.001
    DecayType      = "l1"

    
    #normalize_samples!(X)           # Pin to range [0,1]
    #binarize!(X;threshold=0.001)    # Create binary data
    # Hold out a validation set
    TrainSet     = X
    ValidSet     = X
    #[:,1:100]

    print("size, norm train set ",size(TrainSet),norm(TrainSet))
    print("size, norm valid set ",size(ValidSet),norm(ValidSet))

    # Initialize Model
    m = BernoulliRBM(8*8, HiddenUnits,(8,8); 
                     momentum  = Momentum, 
                     TrainData = TrainSet,
                     sigma     = 0.0000000000000001)

    # Run Training
    rbm,monitor = fit(m, TrainSet; n_iter           = Epochs, 
                                   batch_size       = BatchSize,
                                   weight_decay     = DecayType,
                                   decay_magnitude  = DecayMagnitude,
                                   lr               = LearnRate,
                                   persistent       = false,
                                   validation       = ValidSet,
                                   NormalizationApproxIter = ApproxSteps,
                                   monitor_every    = 1,
                                   monitor_vis      = false,
                                   approx           = Approx,
                                   persistent_start = PersistStart)

end


run_xdigits()



