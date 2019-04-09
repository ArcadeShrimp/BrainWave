


from muselsl import *
import time
import numpy as np

import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop
import json
import warnings
from command import Tracker, SHIFT_LENGTH, NUM_CHANNELS, EPOCH_LENGTH, OVERLAP_LENGTH, BUFFER_LENGTH, Band
import xml.dom.minidom
import serial

# In[3]:




"""
Estimate Relaxation from Band Powers
This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.
The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al
Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
from process_data import ChannelDataProcessor, Metrics
from PsychoPy_Code.BrainWave import run_psychopy

# Handy little enum to make code more readable



class Channel:
    TP0 = 0
    FP1 = 1
    FP2 = 2
    TP10 = 3
    DRL = 4



def _acquire_eeg_data_mock():
    """ Get eeg_data and timestamp from json for testing purposes.

    :return: tuple: _eeg_data, _timestamp
    """
    json_file = open("to_send.json")
    k = json.loads(json_file.read())
    _eeg_data = k[0]["eeg_data"]
    _timestamp = k[0]["timestamp"]
    return _eeg_data, _timestamp

if __name__ == "__main__":

    """
    1. CONNECT TO EEG STREAM

    """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    """
    2. Obtain Threshold from PsycoPy

    """

    cmd = Tracker(inlet=inlet, info=info, channel_index=Channel.FP1)

    cmd.start_stage(mode='relax', stage=1)

    time.sleep(1)

    cmd.end_stage(mode='relax', stage=1)

    #run_psychopy(cmd=cmd)
   # cmd.update_stage_threshold()
    threshold = 0.013716588909309062
    print("FINAL THRESH", threshold)

    """
    3. Record data and wave hand if metric is above threshold.

    """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')


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

    arduinoData = serial.Serial('com3',9600)
    try:

        c = ChannelDataProcessor(buffer_length=BUFFER_LENGTH, epoch_length=EPOCH_LENGTH,
                                 overlap_length=OVERLAP_LENGTH,
                                 shift_length=SHIFT_LENGTH, fs=fs, band_cls=Band)

        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            #
            """ 3.1 ACQUIRE DATA """

            # Obtain EEG data from the LSL stream
            eeg_data, timestamp = _acquire_eeg_data(inlet)

            c.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch

            metrics = []

            for i in range(NUM_CHANNELS):  # Iterate through all separate channels

                # Record channel smooth band power
                csbp = c.get_channel_smooth_band_powers(i)
                # Run calculations on csbp to obtain desired metrics
                theta_metric = csbp[1]

                metrics.append(theta_metric)

            metric = metrics[Channel.FP1]  # TODO: switch to the correct channel

            def check_positive(_metric, _threshold):
                """
                Returns True if beta_metric is less than the threshold
                :return:
                """
                return _metric > _threshold

            def hand_wave():

                action = '1'    #pass in the input of either 1 or 0
                arduinoData.write(action.encode('utf-8'))
                print("hand waved")

            def hand_stay():
                print("hand stayed still")
                action = '0'
                arduinoData.write(action.encode('utf-8'))

            if check_positive(_metric=metric, _threshold=threshold):

                hand_wave()
            else:
                hand_stay()

    except KeyboardInterrupt:
        print('Closing!')
    arduinoData.close()
