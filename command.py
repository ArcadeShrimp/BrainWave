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


class DataRecord:
    def __init__(self):
        self.deltas = []
        self.thetas = []
        self.alphas = []
        self.betas = []

    def get_average_power(self, metric_str="alpha"):
        """

        :return: a list of average alpha powers for each channel
        """
        pass


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


class Tracker:
    """
    Tracks PsychoPy Calibration and MuseLsL Data
    """

    def __init__(self, inlet):
        """
        Initialize with inlet.
        :param inlet:
        """
        self.inlet = inlet

    def _start_recording(self, arr):
        """ Write smooth band power to the df

        :return:
        """
        pass

    @staticmethod
    def _record(info, inlet, d: DataRecord):
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
            while True:
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
                print(" ")
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
        pass

