""" File to do Buffer operatios"""

import settings
import numpy as np

class Buffer:

    DEFAULT_BUFFER_LENGTH = 5 # seconds. Buffer holds the memory of the EEG data.
    DEFAULT_EPOCH_LENGTH = 1 # seconds. Epoch is the length of time we're interested in analyzing at a time.
    DEFAULT_SHIFT_LENGTH = 0.2 # seconds. Shift is the amount of time we get more of when we try to aquire new data.

    def __init__(self, inlet, fs, buffer_length=DEFAULT_BUFFER_LENGTH, epoch_length=DEFAULT_EPOCH_LENGTH, shift_length=DEFAULT_SHIFT_LENGTH, dp=None):

        self.BUFFER_LENGTH = buffer_length
        self.EPOCH_LENGTH = epoch_length
        self.SHIFT_LENGTH = shift_length
        self.NUM_POWERS_IN_BAND_BUFFER = (buffer_length - epoch_length) * (epoch_length / shift_length)

        self.buffer = np.zeros((settings.NUM_CHANNELS, fs*buffer_length))
        self.band_buffer = np.zeros((settings.NUM_CHANNELS, self.NUM_POWERS_IN_BAND_BUFFER))
        self.inlet = inlet
        self.fs = fs
        self.dp = dp


    def _update_buffer_with_next_chunk(self):
        """
            Pull EEG data from inlet and update buffer. This needs to be called
        continuously to have a continuous time of data.

        """
        # 5 channels [TP9, AF7, AF8, TP10, RIGHT_AUX]
        # Each row is a timepoint data
        _eeg_data, _timestamp = self.inlet.pull_chunk(
            timeout=1, max_samples=int(self.SHIFT_LENGTH * self.fs))

        transposedData = np.transpose(np.array(_eeg_data))
        newBuffer = np.concatenate((self.buffer, transposedData), axis=1)



        self.buffer = newBuffer[:, -(self.BUFFER_LENGTH * self.fs):]
        self.band_buffer = newBandBuffer[:, -(self.NUM_POWERS_IN_BAND_BUFFER):]

    def get_last_epoch(self):
        """
            Returns last epoch from buffer. Call this right after
            update_with_next_chunk to get the most recent epoch.

        """
        self._update_buffer_with_next_chunk()
        return self.buffer[:, -(self.EPOCH_LENGTH * self.fs):]

    def get_band_buffer(self) :
