"""
Copyright © 2018, authors of muselsl
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the names of muselsl authors nor the names of any
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Adapted / Refactored from:
    https://github.com/alexandrebarachant/muse-lsl/blob/master/examples/neurofeedback.py

"""

import utils
import numpy as np  # Module that simplifies computations on matrices


def _create_eeg_buffer(fs, buffer_length):
    """ Initialize raw EEG data buffer
    :param fs:
    :return:
    """
    eeg_buffer = np.zeros((int(fs * buffer_length), 1))
    return eeg_buffer


def _create_filter_state():
    """ for use with the notch filter

    :return:
    """
    filter_state = None
    return filter_state


def _get_num_epoch(buffer_length, epoch_length, shift_length):
    """ Compute the number of epochs in "buffer_length"

    :param buffer_length:
    :param epoch_length:
    :param shift_length:
    :return:
    """
    n_win_test = int(np.floor((buffer_length - epoch_length) /
                              shift_length + 1))
    return n_win_test


def _get_smooth_band_powers(band_buffer):
    """

    :param band_buffer:
    :return:
    """

    # Compute the average band powers for all epochs in buffer
    # This helps to smooth out noise
    smooth_band_powers = np.mean(band_buffer, axis=0)
    return smooth_band_powers


class ChannelDataProcessor:
    """

    Example usage:
        c = ChannelDataProcessor(...)               # Specify data-recording parameters
        c.feed_new_data(eeg_data=eeg_data)          # Feed new data generated in the epoch
        for channel in [0,1,2,3]:                   # Iterate through all separate channels

            # Record channel smooth band power
            csbp = c.get_channel_smooth_band_powers(channel)

            # Run calculations on csbp to obtain desired metrics
            a = Metrics.alpha_protocol(csbp, Band)
            print("Alpha metric: {}".format(a))

    """

    def __init__(self, buffer_length=5, epoch_length=1, overlap_length=0.8, shift_length=None, fs=None, band_cls=None):
        """

        :param buffer_length: Length of the EEG data buffer (in seconds)
             This buffer will hold last n seconds of data and be used for calculations
        :param epoch_length: Length of the epochs used to compute the FFT (in seconds)
        :param overlap_length: Amount of overlap between two consecutive epochs (in seconds)
        :param fs: Amount to 'shift' the start of each next consecutive epoch
        :param shift_length: Amount to 'shift' the start of each next consecutive epoch
        :param band_cls: enum to store Band -> Number
        """
        assert shift_length is not None
        self.shift_length = shift_length
        self.buffer_length = buffer_length
        self.epoch_length = epoch_length
        self.overlap_length = overlap_length

        self.n_win_test = _get_num_epoch(buffer_length=self.buffer_length,
                                         epoch_length=self.epoch_length,
                                         shift_length=self.shift_length)

        self.eeg_data = None  # Current Epoch EEG Data

        assert fs is not None  # Check that fs is defined
        self.fs = fs

        self.eeg_buffer = None
        self.filter_state = None

        self.band_cls = band_cls  # To store Band -> Number

    def feed_new_data(self, eeg_data=None):
        self._setup_buffers()
        assert eeg_data is not None  # Check that eeg_data is passed in
        self.eeg_data = eeg_data

    def _setup_buffers(self):
        """ Set up buffers shared by all channels
        :return:
        """

        self.eeg_buffer = _create_eeg_buffer(fs=self.fs, buffer_length=self.buffer_length)
        self.filter_state = _create_filter_state()

    def _retrieve_channel_data(self, eeg_data, index_channel):

        # Only keep the channel we're interested in
        ch_data = np.array(eeg_data)[:, index_channel]

        # Update EEG buffer with the new data
        new_eeg_buffer, new_filter_state = utils.update_buffer(
            self.eeg_buffer, ch_data, notch=True,
            filter_state=self.filter_state)
        return new_eeg_buffer, new_filter_state

    def _get_data_epoch(self, eeg_buffer):
        """ Get newest samples from the buffer

        :param eeg_buffer:
        :return:
        """
        data_epoch = utils.get_last_data(eeg_buffer,
                                         self.epoch_length * self.fs)
        return data_epoch

    def get_channel_smooth_band_powers(self, index_channel):
        """

        :param index_channel: the channel to work on. Example: [0]
        :return: smooth_band_powers
        """

        # Get eeg_buffer and filter_state for this channel
        eeg_buffer, filter_state = self._retrieve_channel_data(eeg_data=self.eeg_data, index_channel=index_channel)

        """ 3.2 COMPUTE BAND POWERS """

        data_epoch = self._get_data_epoch(eeg_buffer=eeg_buffer)

        # Initialize the band power buffer (for plotting)
        # bands will be ordered: [delta, theta, alpha, beta]
        band_buffer = np.zeros((self.n_win_test, 4))

        # Compute band powers
        band_powers = utils.compute_band_powers(data_epoch, self.fs)
        band_buffer, _ = utils.update_buffer(band_buffer,
                                             np.asarray([band_powers]))

       # print('Delta: ', band_powers[self.band_cls.Delta], ' Theta: ', band_powers[self.band_cls.Theta],
        #      ' Alpha: ', band_powers[self.band_cls.Alpha], ' Beta: ', band_powers[self.band_cls.Beta])

        smooth_band_powers = _get_smooth_band_powers(band_buffer)

        return smooth_band_powers


class Metrics:
    """
    3.3 COMPUTE NEUROFEEDBACK METRICS
        These metrics could also be used to drive brain-computer interfaces
    """

    @staticmethod
    def alpha_protocol(smooth_band_powers, band_cls):
        """ Alpha Protocol:
            Simple redout of alpha power, divided by delta waves in order to rule out noise

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        alpha_metric = smooth_band_powers[band_cls.Alpha] / \
                       smooth_band_powers[band_cls.Delta]
        #print('Alpha Relaxation: ', alpha_metric)
        return alpha_metric

    @staticmethod
    def beta_protocol(smooth_band_powers, band_cls):
        """ Beta Protocol:
            Beta waves have been used as a measure of mental activity and concentration
            This beta over theta ratio is commonly used as neurofeedback for ADHD
        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        tb_ratio = smooth_band_powers[band_cls.Theta]/smooth_band_powers[band_cls.Beta]
        
        return tb_ratio

    @staticmethod
    def theta_protocol(smooth_band_powers, band_cls):
        """ Alpha/Theta Protocol:
            This is another popular neurofeedback metric for stress reduction
            Higher theta over alpha is supposedly associated with reduced anxiety

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        #
        theta_metric = smooth_band_powers[band_cls.Theta] / \
                       smooth_band_powers[band_cls.Alpha]
        #print('Theta Relaxation: ', theta_metric)
        return theta_metric
