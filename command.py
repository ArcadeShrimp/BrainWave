from multiprocessing import Process
import threading 
import time

from muselsl import *
import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop
import json
import warnings

from process_data import ChannelDataProcessor, Metrics

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

mock_arr = list()


class MetricStats:

    def __init__(self, avg_deltas=0, avg_thetas=0, avg_alphas=0, avg_betas=0):
        self.avg_deltas = avg_deltas
        self.avg_thetas = avg_thetas
        self.avg_alphas = avg_alphas
        self.avg_betas = avg_betas


class DataRecord:

    def __init__(self):
        self.deltas = []
        self.thetas = []
        self.alphas = []
        self.betas = []
        
        fooofs = {}

    def get_metrics(self, channel_index):
        """

        :return: a list of average powers for each channel
        """

        deltas = [l[channel_index] for l in self.deltas]
        thetas = [l[channel_index] for l in self.thetas]
        alphas = [l[channel_index] for l in self.alphas]
        betas = [l[channel_index] for l in self.betas]

        return MetricStats(avg_deltas=np.mean(deltas),
                           avg_thetas=np.mean(thetas),
                           avg_alphas=np.mean(alphas),
                           avg_betas=np.mean(betas))


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3
    

class Tracker:
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
                #             eeg_data, timestamp = _acquire_eeg_data_mock()

                c = ChannelDataProcessor(buffer_length=BUFFER_LENGTH,
                                         epoch_length=EPOCH_LENGTH,
                                         overlap_length=OVERLAP_LENGTH,
                                         shift_length=SHIFT_LENGTH, fs=fs, band_cls=Band)

                c.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch
                metrics = np.zeros(NUM_CHANNELS)

                delta_sample = []
                theta_sample = []
                alpha_sample = []
                beta_sample = []
                for i in range(NUM_CHANNELS):  # Iterate through all separate channels

                    # Record channel smooth band power
                    csbp = c.get_channel_smooth_band_powers(i)
                    delta_sample.append(csbp[0])
                    theta_sample.append(csbp[1])
                    alpha_sample.append(csbp[2])
                    beta_sample.append(csbp[3])

                    # Run calculations on csbp to obtain desired metrics
                    beta_metric = Metrics.beta_protocol(csbp, Band)
                    # print("Alpha metric: {}".format(alpha_metric))

                    metrics[i] = beta_metric

                # print("alpha metric for 4 sensors are separately: {}".format(metrics))
                #print(" ")
                d.deltas.append(delta_sample)
                d.thetas.append(theta_sample)
                d.alphas.append(alpha_sample)
                d.betas.append(beta_sample)

                
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
#             self.recordingProcess = Process(target=_record, args=(self.info, self.inlet, data_record,))
#             arr = mock_arr
            #self.recordingProcess = Process(target=self._start_recording, args=(self.inlet, self.info, data_record, ))
            self.recordingProcess = threading.Thread(target=self._record, args=(self.info, self.inlet, data_record, ))
            self.currentMode = mode
            self.currentStage = stage

            self.recordingProcess.start()
        else:
            print("Unable to start process because already running")

    def end_stage(self, mode=None, stage=0):

        #self.recordingProcess.terminate()
        
        self.keepRecording = False
        self.currentMode = None
        self.currentStage = None

        data_record: DataRecord = self.data_records[(mode, stage)]
        m: MetricStats = data_record.get_metrics(channel_index=self.channelIndex)
        print("average theta: {}".format(m.avg_thetas))

    def create_fooof(self, mode=None, stage=0):
        # create freqs and powers
        raise NotImplementedError
        
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
