""" This file keeps synchronizes with PsychoPy and categorizes relax and focus
    states. """
from multiprocessing import Process
import threading
import time

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


def aquire_and_append_metrics(inlet, fs, data_processor: DataProcessor):
    """Get metrics from inlet and append to data processor

    Parameters:
    -----------

    Returns:
    --------
    None: updates dataprocessor
    """
    # Obtain EEG data from the LSL stream
    eeg_data, timestamp = utils.acquire_eeg_data(inlet, fs)

    data_processor.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch
    data_processor.append_metrics()


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

    def __init__(self, inlet, info):
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

        self.inlet = inlet
        self.info = info
        self.data_processors = dict()
        self.weights = None
        self.bias = None


    def _record(self, inlet, dp: DataProcessor):
        """
            Records data into the provided DataProcessor if self.keepRecording

            :param info: muselsl info about the channel, with info about the sampling frequency
            :param inlet: the inlet created from the muselsl info
            :param data_processor: DataProcessor object
            :return: Nothing
        """
        fs = get_fs(self.info)

        print('Press Ctrl-C in the console to break the while loop.')

        try:
            # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
            while self.keepRecording:
                aquire_and_append_metrics(inlet, fs, dp)

        except KeyboardInterrupt:
            print('Closing!')

    def start_stage(self, mode, stage):
        """
            Start relax stage and record data.

        :return:
        """

        fs = get_fs(inlet.info())

        dp = DataProcessor(fs=fs)
        self.data_processors[(mode, stage)] = dp

        if self.recordingProcess is None or ~self.recordingProcess.is_alive():
            self.keepRecording = True
            self.recordingProcess = threading.Thread(target=self._record, args=(self.info, self.inlet, dp))
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


    """ NOT donE YETS """
    def _trainMetrics() :
        X = np.array()
        Y = np.array()
        for mode in Modes :
            for stage in Stages :
                dp: DataProcessor = self.data_processors[(mode, stage)]
                df: DataFrame = dp.get_dataframe()

                X.concatenate(df.to_numpy())

                if(mode == Modes.RELAX) :
                    Y.append(np.ones(df.shape[0]))
                else :
                    Y.append(np.zeros(df.shape[0]))

        #X_train = self.data_processors[to_numpy


    def predictMetrics(dp: DataProcessor) :
        """
        Returns a number 0 to 1 with the probability of the input dp
        being a "wave" output.


        :param dp: DataProcessor with the data collected from the subjec
        """
        pass
