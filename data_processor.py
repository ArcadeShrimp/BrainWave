import pandas as pd
import utils
import numpy as np  # Module that simplifies computations on matrices
import pandas
from metrics import *
import settings
from data_record import *

class DataProcessor:
    """ Records and holds data from inlet
    """
    def __init__(self, shift_length=None, fs=None):

        """

        :param buffer_length: Length of the EEG data buffer (in seconds)
             This buffer will hold last n seconds of data and be used for calculations
        :param epoch_length: Length of the epochs used to compute the FFT (in seconds)
        :param overlap_length: Amount of overlap between two consecutive epochs (in seconds)
        :param fs: Amount to 'shift' the start of each next consecutive epoch
        :param shift_length: Amount to 'shift' the start of each next consecutive epoch
        :param band_cls: enum to store Band -> Number
        :param chans: channels eg. ["TP1", "TP9", ... ]
        """

        self.n_win_test = utils.get_num_epoch(buffer_length=utils.BUFFER_LENGTH, epoch_length=utils.EPOCH_LENGTH, shift_length=utils.SHIFT_LENGTH)

        self.eeg_data = None  # Current Epoch EEG Data
        self.eeg_buffer = None
        self.filter_state = None
        self.fs = fs
        self.df = pd.DataFrame()
        self.data_record = DataRecord()

    def feed_new_data(self, eeg_data=None):
        self._setup_buffers()
        self.eeg_data = eeg_data

    def _setup_buffers(self):
        """ Set up buffers shared by all channels
        :return:
        """

        self.eeg_buffer = utils.create_eeg_buffer(fs=self.fs, buffer_length=utils.BUFFER_LENGTH)
        self.filter_state = utils.create_filter_state()

    def _retrieve_channel_data(self, eeg_data, index_channel):

        # Only keep the channel we're interested in
        ch_data = np.array(eeg_data)[:, index_channel]

        # Update EEG buffer with the new data
        new_eeg_buffer, new_filter_state = utils.update_buffer(self.eeg_buffer, ch_data, notch=True, filter_state=self.filter_state)
        return new_eeg_buffer, new_filter_state

    def _get_data_epoch(self, eeg_buffer):
        """ Get newest samples from the buffer

        :param eeg_buffer:
        :return:
        """
        data_epoch = utils.get_last_data(eeg_buffer, utils.EPOCH_LENGTH * self.fs)
        return data_epoch

    def get_smooth_band_powers(self,band_buffer):
        """

        :param band_buffer:
        :return:
        """

        # Compute the average band powers for all epochs in buffer
        # This helps to smooth out noise
        smooth_band_powers = np.mean(band_buffer, axis=0)
        return smooth_band_powers

    def _get_band_powers(self, index_channel):
         # Get eeg_buffer and filter_state for this channel
        eeg_buffer, filter_state = self._retrieve_channel_data(eeg_data=self.eeg_data, index_channel=index_channel)
        data_epoch = self._get_data_epoch(eeg_buffer=eeg_buffer)

        # Compute band powers
        band_powers = utils.compute_band_powers(data_epoch, self.fs)
        return band_powers

    def append_metrics(self):
        """

        :param index_channel: the channel to work on. Example: [0]
        :return: smooth_band_powers
        """

        res = dict()
        for channel in utils.Channel:  # Iterate through all separate channels

            # Initialize the band power buffer (for plotting)
            # bands will be ordered: [delta, theta, alpha, beta]
            band_powers = self._get_band_powers(channel.value)
            band_buffer = np.zeros((self.n_win_test, 4))
            band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))

            # Record channel smooth band power
            csbp = self.get_smooth_band_powers(band_buffer)

            # Aquires power values for interative channel
            for band in utils.Band:
                res[(channel.name, band.name)] = csbp[band.value]

            # Add Ratio measures
            ratios_measures = Metrics.get_ratios(csbp)
            for ratio in utils.Ratios:
                res[(channel.name, ratio.name)] = ratios_measures[ratio.value]
