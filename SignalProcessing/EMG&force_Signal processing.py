import pandas as pd
import glob
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from scipy.signal import butter, filtfilt
from scipy import signal
import scipy.signal as signal
from datetime import datetime
from sklearn import preprocessing
import statistics
import time
 

path = r'C:\Users\l e n o v o\Desktop\thesis\sensors\myo-python-master\myo-python-master\examples\data\paper+vedadi\raw'  ## path of all raw data files

all_files = glob.glob(path + "/*.csv")
g = 0
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    pda = np.array(df)
    
    dim = np.shape(pda)[0]
    temp = np.zeros((dim, 9)) ##temp is all EMG and force data before filtering
    for i in range(1, 9):
        temp[:,i-1] = pda[:,i].astype(np.float)
    temp[:,8] = pda[:,0].astype(np.float)

    for j in range(temp.shape[0]):
        if temp[j,8] > 3000:
            temp[j,8] = temp[j,8] % 1000
    
################################### filter design
    N = 2    # Filter order 
    ## sampling frequency (fs) = 200 Hz
    Wn_notch = 45, 55
    Wn_bandpass_f = 1, 99
    Wn_bandpass_emg = 10, 99

    ###band-stop filter (notch) for EMG and force
    F, E = signal.butter(N, Wn_notch, btype='bandstop', analog=False, output='ba', fs=200)

    ###band-pass filter (high+low) for EMG
    A, B = signal.butter(N, Wn_bandpass_emg, btype='bandpass', analog=False, output='ba', fs=200)

    ###band-pass filter (high+low) for force
    H, G = signal.butter(N, Wn_bandpass_f, btype='bandpass', analog=False, output='ba', fs=200)

################################### filtering temp
    temp_filtered_all = np.zeros((dim, 9))
    notch_filtered = np.zeros((dim, 9))
    temp_filtered_each = np.zeros((dim, 9))

    ##################### EMG 
    for i in range(8):
        notch_filtered[:,i] = signal.filtfilt(F, E, temp[:,i])
        temp_filtered_each[:, i] = signal.filtfilt(A, B, notch_filtered[:,i])
        temp_filtered_all[:, i] = notch_filtered[:,i]-temp_filtered_each[:, i]
    ##################### force
    notch_filtered[:,8] = signal.filtfilt(F, E, temp[:,8])
    temp_filtered_each[:, 8] = signal.filtfilt(H, G, notch_filtered[:,8])
    temp_filtered_all[:, 8] = notch_filtered[:,8]-temp_filtered_each[:, 8]
    
    g = g + 1
    np.savetxt(f'filtered_{g}.csv', temp_filtered_all, delimiter=',')    






    
