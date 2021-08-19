# GrippingForcePrediction
Repository for gripping force prediction with the goal of gripping control of a hand prosthesis

1. Recording both EMG raw signals and gripping force simultaneously during precision-type gripping

      EMG signals are recorded via a Myo armband from Thalmiclabs.
     
      Gripping force is the Z-axis force measured using a mini 45 F/T sensor from ATI Industrial Automation Inc.
      
2. Signal processing

3. Dataset

      Data is derived form 10 healthy subjects with an average age of 23.8 years old (9 males and one female).

4. Force prediction

      Gripping force is predicted using MLP, simple RNN, GRU and LSTM neural networks.
      
5. Visualization

      Performance of different networks with prediction horizens of 1-12 is plotted.
      
      Error Distributions of all implemented networks are shown in a boxplot.
      
      


