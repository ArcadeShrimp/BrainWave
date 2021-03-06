""" File to do Buffer operations"""

import settings
from utils import Band, Channel
import numpy as np
import pandas as pd
from neurodsp import timefrequency # to calculate the power at frequency bands


class Buffer:

    DEFAULT_BUFFER_LENGTH = 5 # seconds. Buffer holds the memory of the EEG data.
    DEFAULT_EPOCH_LENGTH = 1 # seconds. Epoch is the length of time we're interested in analyzing at a time.
    DEFAULT_SHIFT_LENGTH = 0.2 # seconds. Shift is the amount of time we get more of when we try to aquire new data.

    def __init__(self, inlet, fs, buffer_length=DEFAULT_BUFFER_LENGTH, epoch_length=DEFAULT_EPOCH_LENGTH, shift_length=DEFAULT_SHIFT_LENGTH):

        self.BUFFER_LENGTH = buffer_length
        self.EPOCH_LENGTH = epoch_length
        self.SHIFT_LENGTH = shift_length
        self.NUM_POWERS_IN_BAND_BUFFER = int((buffer_length - epoch_length) * (epoch_length / shift_length))

        self.timestamps = np.zeros((settings.NUM_CHANNELS, fs*buffer_length))

        self.buffer = np.zeros((settings.NUM_CHANNELS, fs*buffer_length))
        self.bandBuffer = pd.DataFrame()
        self.inlet = inlet
        self.fs = fs

    def _compute_bandpowers (self, eegdata) :
        deltaFreq = (2, 4)
        thetaFreq = (4, 8)
        alphaFreq = (8, 12)
        betaFreq = (12, 30)

        toAdd = dict()

        for channel in Channel :
            channelIndex = channel.value
            numToPad = 5
            padded_data = [0 if not (i >= numToPad and i < (len(eegdata[channelIndex]) + numToPad)) else eegdata[channelIndex][i - numToPad] for i in range(len(eegdata[channelIndex]) + (numToPad * 2))]
            padded_data = np.asarray(padded_data)

            toAdd[str(Band.DELTA.name + "_" + channel.name)] = np.nanmean(timefrequency.amp_by_time(padded_data, self.fs, f_range=deltaFreq, verbose=False, filter_kwargs={"n_seconds": 1}))
            toAdd[str(Band.THETA.name + "_" + channel.name)] = np.nanmean(timefrequency.amp_by_time(padded_data, self.fs, f_range=thetaFreq, verbose=False, filter_kwargs={"n_seconds": 1}))
            toAdd[str(Band.ALPHA.name + "_" + channel.name)] = np.nanmean(timefrequency.amp_by_time(padded_data, self.fs, f_range=alphaFreq, verbose=False, filter_kwargs={"n_seconds": 1}))
            toAdd[str(Band.BETA.name + "_" + channel.name)] = np.nanmean(timefrequency.amp_by_time(padded_data, self.fs, f_range=betaFreq, verbose=False, filter_kwargs={"n_seconds": 1}))

        return toAdd


    def update_buffer_with_next_chunk(self):
        """
            Pull EEG data from inlet and update buffer. This needs to be called
        continuously to have a continuous time of data.

        """
        # 5 channels [TP9, AF7, AF8, TP10, RIGHT_AUX]
        # Each row is a timepoint data
        _eeg_data, _timestamp = self.inlet.pull_chunk(
            timeout=1, max_samples=int(self.SHIFT_LENGTH * self.fs))

        # Transpose so that the channels are the rows.
        transposedData = np.transpose(np.array(_eeg_data))

        # Concatenate old buffer with the transposed data to concatenate the new time data.
        newBuffer = np.concatenate((self.buffer, transposedData), axis=1)

        # Truncate the time series so we only keep the most recent 5 seconds of data.
        self.buffer = newBuffer[:, -(self.BUFFER_LENGTH * self.fs):]

        # Get the last second of time data.
        lastSecondTimeData = self.get_last_epoch()

        # Calculate the band powers for each channel. CH1 [delta, theta, alpha, beta]
        newBandSlice = self._compute_bandpowers(lastSecondTimeData)
        self.bandBuffer = self.bandBuffer.append(newBandSlice, ignore_index = True)
        self.bandBuffer = self.bandBuffer.tail(len(self.bandBuffer) if (len(self.bandBuffer) < self.NUM_POWERS_IN_BAND_BUFFER) else self.NUM_POWERS_IN_BAND_BUFFER-1)


    def get_last_epoch(self):
        """
            Returns last epoch from buffer. Call this right after
            update_with_next_chunk to get the most recent epoch.

        """
        return self.buffer[:, -(self.EPOCH_LENGTH * self.fs):]

    def get_band_buffer(self) :
        """
            Returns the band buffer of the last 5 seconds of band powers.
        """
        return self.bandBuffer

    def get_band_buffer_average(self) :
        """
            Returns the smoothed band power, over the last 5 seconds.
        """
        return self.bandBuffer.mean(axis=0, skipna=True)

    def flush(self) :
        """
            Flushes buffer and bandBuffer so you can start a new recording.
        """
        self.buffer = np.zeros((settings.NUM_CHANNELS, fs*buffer_length))
        self.bandBuffer = pd.DataFrame()
        pass
