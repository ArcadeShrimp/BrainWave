from unittest import TestCase, skip
import json
from process_data import ChannelDataProcessor, Metrics
import numpy as np


# @skip("Test not implemented")
class TestChannelDataProcessor(TestCase):
    def test_feed_new_data(self):
        self.fail()

    def test__setup_buffers(self):
        self.fail()

    def test__retrieve_channel_data(self):
        self.fail()

    def test__get_data_epoch(self):
        self.fail()

    def test_get_channel_smooth_band_powers(self):
        self.fail()

    def test_all(self):
        class Band:
            Delta = 0
            Theta = 1
            Alpha = 2
            Beta = 3

        # We are working with 4 channels (Billy) [0], [1], [2], [3] as 4 index_channel values
        NUM_CHANNELS = 4

        # Length of the EEG data buffer (in seconds)
        # This buffer will hold last n seconds of data and be used for calculations
        BUFFER_LENGTH = 5

        # Length of the epochs used to compute the FFT (in seconds)
        EPOCH_LENGTH = 1

        # Amount of overlap between two consecutive epochs (in seconds)
        OVERLAP_LENGTH = 0.8

        # Amount to 'shift' the start of each next consecutive epoch
        SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

        def get_fs(_info):
            return int(_info.nominal_srate())

        def get_fs_mock():
            return 256  # For testing purposes

        fs = get_fs_mock()

        def _acquire_eeg_data_mock():
            """ Get eeg_data and timestamp from json for testing purposes.

            :return: tuple: _eeg_data, _timestamp
            """
            json_file = open("to_send.json")
            k = json.loads(json_file.read())
            _eeg_data = k[0]["eeg_data"]
            _timestamp = k[0]["timestamp"]
            return _eeg_data, _timestamp

            # Obtain EEG data from the LSL stream
            # eeg_data, timestamp = _acquire_eeg_data(inlet)

        eeg_data, timestamp = _acquire_eeg_data_mock()

        c = ChannelDataProcessor(buffer_length=BUFFER_LENGTH,
                                 epoch_length=EPOCH_LENGTH,
                                 overlap_length=OVERLAP_LENGTH,
                                 shift_length=SHIFT_LENGTH, fs=fs, band_cls=Band)

        c.feed_new_data(eeg_data=eeg_data)  # Feed new data generated in the epoch
        metrics = np.zeros(4)

        for i in range(NUM_CHANNELS):  # Iterate through all separate channels

            # Record channel smooth band power
            csbp = c.get_channel_smooth_band_powers(i)

            # Run calculations on csbp to obtain desired metrics
            alpha_metric = Metrics.alpha_protocol(csbp, Band)
            print("Alpha metric: {}".format(alpha_metric))

            index_channel = [i]
            metrics[i] = alpha_metric
            self.assertIsNotNone(alpha_metric, "metric is not None")

        print("alpha metric for 4 sensors are separately: {}".format(metrics))

