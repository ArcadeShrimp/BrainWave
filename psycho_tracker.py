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
from process import ChannelDataProcessor


# We are working with 4 channels (Billy) [0], [1], [2], [3] as 4 index_channel values
NUM_CHANNELS = 5

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH    

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

class Calibrator:
    """
    Tracks PsychoPy Calibration and MuseLsL Data
    """

    # to hold the eeg data
    # eeg_data = {('relax',1) : list(), "relax2": list(), "relax3": list(), "focus1": list(), "focus2": list(), "focus3": list()}
    # mydata = list()
    
    def __init__(self, inlet, info, channel_index):
        """
        Initialize with inlet.
        :param inlet:
        :channel_index: list of channels 
        """

        self.keepRecording = False
        self.currentMode = None
        self.currentStage = None

        # Whether or not we are ready to record
        self.readyToRecord = True

        # Keep track of whether something is already recording
        self.isRecording = False

        # to hold the process that will do the recording
        self.recordingProcess = None

        self.inlet = inlet
        self.info = info
        self.data_records = dict()
        self.threshold = None
        self.channelIndex = channel_index

        
    def _record(self, info, inlet, d: DataRecord):
        """

        :param info:
        :param inlet:
        :param d: DataRecord object
        :return:
        """

        def get_fs(_info):
            return int(_info.nominal_srate())

        fs = get_fs(info)

        def _acquire_eeg_data(_inlet):
            """ Pull EEG data from inlet and return.

            :return: tuple: _eeg_data, _timestamp
            """
            _eeg_data, _timestamp = _inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            return _eeg_data, _timestamp

        # The try/except structure allows to quit the while loop by aborting the
        # script with <Ctrl-C>
        print('Press Ctrl-C in the console to break the while loop.')

        try:
            # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
            while self.keepRecording:
                #
                
                """ 3.1 ACQUIRE DATA """

                # Obtain EEG data from the LSL stream
                eeg_data, timestamp = _acquire_eeg_data(inlet)

                c = ChannelDataProcessor(buffer_length=BUFFER_LENGTH,
                                         epoch_length=EPOCH_LENGTH,
                                         overlap_length=OVERLAP_LENGTH,
                                         shift_length=SHIFT_LENGTH, fs=fs, band_cls=Band)

                c.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch
                metrics = {
                    "delta": None,
                    "theta": None,
                    "alpha": None,
                    "beta": None,
                    "alpha/delta": None,
                    "alpha/theta": None,
                    "alpha/beta": None,
                    "beta/theta": None} 
                    
                
                for channel in range(NUM_CHANNELS):  # Iterate through all separate channels

                    # Record channel smooth band power
                    csbp = c.get_channel_smooth_band_powers(channel)
                    
                    #acquires power values for interative channel
                       #metrics[channel][0:4] = csbp[0:4]

                    # acquire ratio measures for channel
                    
                       #metrics[channel][4:] = Metrics.get_ratios(csbp, utils.Band)

                d.matricies.append(metrics)

                
        except KeyboardInterrupt:
            print('Closing!')
         
    def start_stage(self, mode=None, stage=0):
        """
            Start relax stage and record data.

        :return:
        """
        
        data_record = DataRecord()
        self.data_records[(mode, stage)] = data_record

        if self.recordingProcess is None or ~self.recordingProcess.is_alive():
            self.isRecording = True
            self.keepRecording = True
            self.recordingProcess = threading.Thread(target=self._record, args=(self.info, self.inlet, data_record, ))
            self.currentMode = mode
            self.currentStage = stage
            self.recordingProcess.start()
            
        else:
            print("Unable to start process because already running")

    def end_stage(self, mode=None, stage=0):

        self.keepRecording = False
        self.currentMode = None
        self.currentStage = None

        data_record: DataRecord = self.data_records[(mode, stage)]
            
        
        m: MetricStats = data_record.get_metrics(channel_index=self.channelIndex)

    def create_fooof(self, mode=None, stage=0):
        # create freqs and powers
        pass


    def update_stage_threshold(self):
        self.threshold = self.get_threshold()

    def get_threshold(self):
        """

        :return: the threshold determined as the average between relax_theta and focus_theta
        """
        relax_datas = [self.data_records[key] for key in self.data_records if key[0] == 'relax']
        relax_thetas = [data_record.get_metrics(channel_index=self.channelIndex).avg_thetas for data_record in relax_datas]
        relax_theta = np.mean(relax_thetas)

        focus_datas = [self.data_records[key] for key in self.data_records if key[0] == 'focus']
        focus_thetas = [data_record.get_metrics(channel_index=self.channelIndex).avg_thetas for data_record in focus_datas]
        focus_theta = np.mean(focus_thetas)

        return np.mean([relax_theta, focus_theta])
