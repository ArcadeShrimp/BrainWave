import time
from os import wait

import utils
import numpy as np  # Module that simplifies computations on matrices
import metrics
import pandas as pd
from metrics import *
import itertools
from settings import NUM_CHANNELS, BUFFER_LENGTH, EPOCH_LENGTH, OVERLAP_LENGTH, SHIFT_LENGTH


# TODO: migrate
import matplotlib.pyplot as plt
import numpy as np


def _get_dataframe(_df):
    # p = list(itertools.product(
    #         [c.name for c in utils.Channel],
    #         [b.name for b in utils.Band]
    # ))
    # print(p)
    # multi_index = pd.MultiIndex.from_tuples(
    #     tuples=p,
    #     names=["channel", "band"])
    df = pd.DataFrame().from_dict(_df)
    return df


def _get_hist(eegdata: np.ndarray, fs):
    # print(eegdata)
    # 1. Compute the PSD
    winSampleLength, nbCh = eegdata.shape

    # Apply Hamming window
    w = np.hamming(winSampleLength)
    dataWinCentered = eegdata - np.mean(eegdata, axis=0)  # Remove offset
    dataWinCenteredHam = (dataWinCentered.T * w).T

    NFFT = nextpow2(winSampleLength)
    Y = np.fft.fft(dataWinCenteredHam, n=NFFT, axis=0) / winSampleLength
    PSD = 2 * np.abs(Y[0:int(NFFT / 2), :])
    f = fs / 2 * np.linspace(0, 1, int(NFFT / 2))



    # print(Y)
    #
    # fig, (ax1, ax2) = plt.subplots(nrows=2)
    # ax1.plot(f, Y)
    # Pxx, freqs, bins, im = ax2.specgram(Y, NFFT=NFFT, Fs=fs, noverlap=900)
    # # The `specgram` method returns 4 objects. They are:
    # # - Pxx: the periodogram
    # # - freqs: the frequency vector
    # # - bins: the centers of the time bins
    # # - im: the matplotlib.image.AxesImage instance representing the data in the plot
    # plt.show()



    # dt = 1 / 256
    # t = np.arange(0.0, 1.0, dt)

    x = eegdata.flatten()

    # NFFT = 1024  # the length of the windowing segments
    # Fs = int(1.0 / dt)  # the sampling frequency
    # print(x)
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(f, x[:f.shape[0]])
    Pxx, freqs, bins, im = ax2.specgram(x, NFFT=NFFT, Fs=fs)
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot
    plt.show()

    # while True:
    #     wait()
    # f.dump("f")


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
        self.df = list()
        # self.df = pd.DataFrame()

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
        data_epoch: np.ndarray = self._get_data_epoch(eeg_buffer=eeg_buffer)

        # Uncomment to save the data for testing
        # data_epoch.dump("data_epoch")

        # Compute band powers
        band_powers = utils.compute_band_powers(data_epoch, self.fs)
        return band_powers

    def get_dataframe(self):
        return _get_dataframe(self.df)

    def _get_window_channel(self, index_channel):
        # Get eeg_buffer and filter_state for this channel
        eeg_buffer, filter_state = self._retrieve_channel_data(eeg_data=self.eeg_data, index_channel=index_channel)
        data_epoch = self._get_data_epoch(eeg_buffer=eeg_buffer)
        return data_epoch

    def refresh_specgram(self):
        """

        :param index_channel: the channel to work on. Example: [0]
        :return: smooth_band_powers
        """

        data_epoch = self._get_window_channel([0])
        _get_hist(data_epoch, self.fs)
        time.sleep(1)
        # res = dict()
        # for channel in utils.Channel:  # Iterate through all separate channels
        #     window = self._get_window_channel(channel)

        #     # Initialize the band power buffer (for plotting)
        #     # bands will be ordered: [delta, theta, alpha, beta]
        #     band_powers = self._get_band_powers(channel.value)
        #     band_buffer = np.zeros((self.n_win_test, 4))
        #     band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))
        #
        #     # Record channel smooth band power
        #     csbp = self.get_smooth_band_powers(band_buffer)
        #
        #     # Aquires power values for interative channel
        #     for band in utils.Band:
        #         res[(channel.name, band.name)] = csbp[band.value]
        #
        #     # Add Ratio measures
        #     ratios_measures = Metrics.get_ratios(csbp)
        #     for ratio in utils.Ratios:
        #         res[(channel.name, ratio.name)] = ratios_measures[ratio.value]
        #
        # self.df.append(res)



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

        self.df.append(res)
    #
    # def get_recent_slice():
    #     return self.df.tail(1)
