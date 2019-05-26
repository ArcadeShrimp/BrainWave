"""
Muse LSL Example Auxiliary Tools
These functions perform the lower-level operations involved in buffering,
epoching, and transforming EEG data into frequency bands
@author: Cassani
"""

import os
import sys
from tempfile import gettempdir
from subprocess import call
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from scipy.signal import butter, lfilter, lfilter_zi

from settings import *
from data_processor import DataProcessor


NOTCH_B, NOTCH_A = butter(4, np.array([55, 65]) / (256 / 2), btype='bandstop')

class Channel(Enum):
    TP9 = 0
    FP1 = 1
    FP2 = 2
    TP10 = 3
    DRL = 4

class Band(Enum):
    DELTA = 0
    THETA = 1
    ALPHA = 2
    BETA = 3

class Ratios(Enum):
    AD = 0
    AT = 1
    AB = 2
    BT = 3


def epoch(data, samples_epoch, samples_overlap=0):
    """Extract epochs from a time series.
    Given a 2D array of the shape [n_samples, n_channels]
    Creates a 3D array of the shape [wlength_samples, n_channels, n_epochs]
    Args:
        data (numpy.ndarray or list of lists): data [n_samples, n_channels]
        samples_epoch (int): window length in samples
        samples_overlap (int): Overlap between windows in samples
    Returns:
        (numpy.ndarray): epoched data of shape
    """

    if isinstance(data, list):
        data = np.array(data)

    n_samples, n_channels = data.shape

    samples_shift = samples_epoch - samples_overlap

    n_epochs = int(
        np.floor((n_samples - samples_epoch) / float(samples_shift)) + 1)

    # Markers indicate where the epoch starts, and the epoch contains samples_epoch rows
    markers = np.asarray(range(0, n_epochs + 1)) * samples_shift
    markers = markers.astype(int)

    # Divide data in epochs
    epochs = np.zeros((samples_epoch, n_channels, n_epochs))

    for i in range(0, n_epochs):
        epochs[:, :, i] = data[markers[i]:markers[i] + samples_epoch, :]

    return epochs


def compute_band_powers(eegdata, fs):
    """Extract the features (band powers) from the EEG.
    Args:
        eegdata (numpy.ndarray): array of dimension [number of samples,
                number of channels]
        fs (float): sampling frequency of eegdata
    Returns:
        (numpy.ndarray): feature matrix of shape [number of feature points,
            number of different features]
    """
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

    # SPECTRAL FEATURES
    # Average of band powers
    # Delta <4
    ind_delta, = np.where(f < 4)
    meanDelta = np.mean(PSD[ind_delta, :], axis=0)
    # Theta 4-8
    ind_theta, = np.where((f >= 4) & (f <= 8))
    meanTheta = np.mean(PSD[ind_theta, :], axis=0)
    # Alpha 8-12
    ind_alpha, = np.where((f >= 8) & (f <= 12))
    meanAlpha = np.mean(PSD[ind_alpha, :], axis=0)
    # Beta 12-30
    ind_beta, = np.where((f >= 12) & (f < 30))
    meanBeta = np.mean(PSD[ind_beta, :], axis=0)


    feature_vector = np.concatenate((meanDelta, meanTheta, meanAlpha,
                                     meanBeta), axis=0)

    feature_vector = np.log10(feature_vector)

    return feature_vector


def get_fs(_info):
    return int(_info.nominal_srate())


def nextpow2(i):
    """
    Find the next power of 2 for number i
    """
    n = 1
    while n < i:
        n *= 2
    return n


def compute_feature_matrix(epochs, fs):
    """
    Call compute_feature_vector for each EEG epoch
    """
    n_epochs = epochs.shape[2]

    for i_epoch in range(n_epochs):
        if i_epoch == 0:
            feat = compute_band_powers(epochs[:, :, i_epoch], fs).T
            # Initialize feature_matrix
            feature_matrix = np.zeros((n_epochs, feat.shape[0]))

        feature_matrix[i_epoch, :] = compute_band_powers(
            epochs[:, :, i_epoch], fs).T

    return feature_matrix


def get_feature_names(ch_names):
    """Generate the name of the features.
    Args:
        ch_names (list): electrode names
    Returns:
        (list): feature names
    """
    bands = ['delta', 'theta', 'alpha', 'beta']

    feat_names = []
    for band in bands:
        for ch in range(len(ch_names)):
            feat_names.append(band + '-' + ch_names[ch])

    return feat_names


def update_buffer(data_buffer, new_data, notch=False, filter_state=None):
    """
    Concatenates "new_data" into "data_buffer", and returns an array with
    the same size as "data_buffer"
    """
    if new_data.ndim == 1:
        new_data = new_data.reshape(-1, data_buffer.shape[1])


    print("data buffer: " + str(data_buffer) + " shape " + str(data_buffer.shape))
    print("new data: " + str(new_data) + " shape " + str(new_data.shape))
    new_buffer = np.concatenate((data_buffer, new_data), axis=0)
    new_buffer = new_buffer[new_data.shape[0]:, :]
    print("new buffer: " + str(new_buffer) + " shape " + str(new_buffer.shape))


    return new_buffer, filter_state


def get_last_data(data_buffer, newest_samples):
    """
    Obtains from "buffer_array" the "newest samples" (N rows from the
    bottom of the buffer)
    """
    new_buffer = data_buffer[(data_buffer.shape[0] - newest_samples):, :]

    return new_buffer

def create_eeg_buffer(fs, buffer_length):
    """ Initialize raw EEG data buffer
    :param fs:
    :return:
    """
    eeg_buffer = np.zeros((int(fs * buffer_length), 1))
    return eeg_buffer


def create_filter_state():
    """ for use with the notch filter

    :return:
    """
    filter_state = None
    return filter_state


def get_num_epoch(buffer_length=BUFFER_LENGTH, epoch_length=EPOCH_LENGTH, shift_length=SHIFT_LENGTH):
    """ Compute the number of epochs in "buffer_length"

    :param buffer_length:
    :param epoch_length:
    :param shift_length:
    :return:
    """
    n_win_test = int(np.floor((buffer_length - epoch_length)*(epoch_length/shift_length)))
    ###TESTING^^^^ n_win_test = int(np.floor((buffer_length - epoch_length) /shift_length + 1))
    return n_win_test

def acquire_eeg_data(_inlet, fs):
    """ Pull EEG data from inlet and return.

    :return: tuple: _eeg_data, _timestamp
    """
    _eeg_data, _timestamp = _inlet.pull_chunk(
        timeout=1, max_samples=int(SHIFT_LENGTH * fs))
    return _eeg_data, _timestamp

def aquire_and_append_metrics(inlet, fs, data_processor: DataProcessor):
    """Get metrics from inlet and append to data processor

    Parameters:
    -----------

    Returns:
    --------
    None: updates dataprocessor
    """
    # Obtain EEG data from the LSL stream
    eeg_data, timestamp = acquire_eeg_data(inlet, fs)

    data_processor.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch
    data_processor.append_metrics()
