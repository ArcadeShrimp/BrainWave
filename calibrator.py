""" This file keeps synchronizes with PsychoPy and categorizes relax and focus
    states. """
from multiprocessing import Process
import threading
import time
import buffer
import pandas as pd

from muselsl import *
import numpy as np
from pylsl import StreamInlet, resolve_byprop
import json
import warnings
import utils
import metrics
from data_record import DataRecord, MetricStats
from data_processor import DataProcessor
from settings import NUM_CHANNELS, BUFFER_LENGTH, EPOCH_LENGTH, OVERLAP_LENGTH, SHIFT_LENGTH
from PsychoPy_Code.PsychoRun import Modes, Stages

class Calibrator:
    """
    Tracks PsychoPy Calibration and MuseLsL Data
    keepRecording:
    currentMode:
    currentStage:
    readyToRecord:
    recordingProcess:
    inlet:
    info:
    threshold: A matrix that col

    """

    def __init__(self, buff):
        """
        Initialize with inlet.
        :param inlet:
        """

        # Whether or not we are ready to record
        self.readyToRecord = True
        self.keepRecording = False

        self.currentMode = None
        self.currentStage = None

        # to hold the process that will do the recording
        self.recordingProcess = None

        self.buff = buff
        self.data_frames = dict()
        self.weights = None
        self.bias = None


    def _record(self, mode, stage):
        """
            Records data into the provided DataProcessor if self.keepRecording

            :param info: muselsl info about the channel, with info about the sampling frequency
            :param inlet: the inlet created from the muselsl info
            :param data_processor: DataProcessor object
            :return: Nothing
        """
        fs = self.buff.fs

        print('Press Ctrl-C in the console to break the while loop.')

        try:
            # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
            while self.keepRecording:
                self.buff.update_buffer_with_next_chunk()
                nextData = self.buff.get_band_buffer_average()
                self.data_frames[(mode, stage)] = self.data_frames[(mode, stage)].append(nextData, ignore_index=True)

        except KeyboardInterrupt:
            print('Closing!')

    def start_stage(self, mode, stage):
        """
            Start relax stage and record data.

        :return:
        """

        fs = self.buff.fs

        df = pd.DataFrame()
        self.data_frames[(mode, stage)] = df

        if self.recordingProcess is None or ~self.recordingProcess.is_alive():
            self.keepRecording = True
            self.recordingProcess = threading.Thread(target=self._record, args=(mode, stage))
            self.currentMode = mode
            self.currentStage = stage
            self.recordingProcess.start()

        else:
            print("Unable to start process because already running")

    def end_stage(self, mode, stage):

        self.keepRecording = False
        self.currentMode = None
        self.currentStage = None

    def create_fooof(self, mode=None, stage=0):
        # create freqs and powers
        pass

    def L_w_b(self, X, Y, w, b):
        loss = sum(np.log(self.sigmoid(Y.reshape((-1,1))*(np.matmul(X,w)+b))))
        return -loss

    # gradient of loss function L(w, b)
    def L_prime_w_b(self, X, Y, w, b):
        #####################################
        # This function returns the tuple(gradient for w, gradient for b)
        #####################################

        grad_b = 0
        grad_w = 0

        #print(np.matmul(X,w)+b) THIS WORKS
        #print(Y.reshape((-1,1))*np.matmul(X,w)+b) Also WORKS
        #-Y.reshape((-1,1))*
        print("y_shape", Y.reshape((-1,1)).shape) # = (variable,1)
        print("rest_shape",(1-self.sigmoid(Y.reshape((-1,1))*(np.matmul(X,w)+b))).shape) # = (variable,1)

        #print(-Y.reshape((1,1)))
        #print("b",-Y.reshape((-1,1))*(1-self.sigmoid(Y.reshape((-1,1))*(np.matmul(X,w)+b))))
        #print("Y",Y.reshape((1,1)))
        #print("rest", (np.matmul(X,w)+b).shape)
        grad_b = -Y.reshape((-1,1))*(1-self.sigmoid(Y.reshape((-1,1))*(np.matmul(X,w)+b)))
        grad_w = -Y.reshape((-1,1))*X*(1-self.sigmoid(Y.reshape((-1,1))*(np.matmul(X,w)+b)))
        #print("gradb",grad_b)
        #print("gradw",grad_w)

        grad_w = np.sum(grad_w,axis=0)
        grad_b = np.sum(grad_b,axis=0)
        return grad_w.reshape((-1,1)), grad_b

    def sigmoid(self, z):
        return 1.0/(1.0 + np.exp(-z))


    """ NOT donE YETS """
    def getXAndY(self) :
        X_train = np.zeros(shape=(1, 20))
        Y_train = np.zeros(shape=(1))
        isFirst = True

        for mode in Modes:
            for stage in Stages:
                df: DataFrame = self.data_frames[(mode.value, stage.value)]
                if(isFirst):
                    X_train = df.to_numpy()
                else :
                    X_train = np.concatenate((X_train,df.to_numpy()))

                print(mode)
                if(mode == Modes.FOCUS) :
                    Y_train = np.concatenate((Y_train,np.ones(len(df))))
                else :
                    if(isFirst):
                        Y_train = np.zeros(shape=(1))
                    else:
                        Y_train = np.concatenate((Y_train, np.zeros(len(df))))
                print(Y_train)
                print(Y_train.shape)
                isFirst = False

        return X_train, Y_train
# learning_rate = 0.01
# n_iter = 10000
# w = np.zeros((X_train.shape[1], 1))
# b = 0
#
# # We will keep track of training loss over iterations
# iterations = [0]
# L_w_b_list = [self.L_w_b(X_train, Y_train, w, b)]
# for i in range(n_iter):
#     gradient_w, gradient_b = self.L_prime_w_b(X_train, Y_train, w, b)
#     w_new = w - learning_rate * gradient_w
#     b_new = b - learning_rate * gradient_b
#
#     '''if i % 300 == 0 :
#         print("gradw",gradient_w)
#         print("gradb" + str(gradient_b))
#         print("bnew", b_new)
#         print("wnew", w_new)
#         '''
#     iterations.append(i+1)
#     L_w_b_list.append(self.L_w_b(X_train, Y_train, w_new, b_new))
#     if np.linalg.norm(w_new - w, ord = 1) + abs(b_new - b) < 0.001:
#         print("gradient descent has converged after " + str(i) + " iterations")
#         break
#     '''
#     if i % 300 == 0 :
#         print("w is " + str(w))
#         print("b is " + str(b))'''
#     w = w_new
#     b = b_new


        self.weights = w
        self.bias = b

    def predict(self, X):
        """
        Returns a number 0 to 1 with the probability of the input dp
        being a "wave" output.
        """
        return np.matmul(X, self.weights) + self.bias
