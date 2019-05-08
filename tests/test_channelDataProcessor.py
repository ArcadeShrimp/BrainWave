from unittest import TestCase, skip
import json
from process import ChannelDataProcessor
from data_processor import _get_dataframe
from metrics import Metrics
import numpy as np


class TestChannelDataProcessor(TestCase):
    """
        TODO: implement
    """

    @skip("Test not implemented")
    def test_feed_new_data(self):
        self.fail()

    @skip("Test not implemented")
    def test__setup_buffers(self):
        self.fail()

    @skip("Test not implemented")
    def test__retrieve_channel_data(self):
        self.fail()

    @skip("Test not implemented")
    def test__get_data_epoch(self):
        self.fail()

    @skip("Test not implemented")
    def test_get_channel_smooth_band_powers(self):
        self.fail()

    def test_get_dataframe(self):
        r = [{('TP9', 'DELTA'): 0.07607643690467895, ('TP9', 'THETA'): 0.0430910067475004, (
        'TP9', 'ALPHA'): 0.03305502179306974, ('TP9', 'BETA'): 0.025302164033459102, (
        'TP9', 'AD'): 0.43449750195959486, ('TP9', 'AT'): 0.7670979233964446, ('TP9', 'AB'): 1.3064108567693422, (
        'TP9', 'BT'): 0.5871796911527674, ('FP1', 'DELTA'): 0.04415585925427515, (
        'FP1', 'THETA'): 0.011999151385739905, ('FP1', 'ALPHA'): 0.0007869201335461981, (
        'FP1', 'BETA'): -0.008268964597794928, ('FP1', 'AD'): 0.017821420460071985, ('FP1', 'AT'): 0.0655813155654819, (
        'FP1', 'AB'): -0.09516549795799643, ('FP1', 'BT'): -0.6891291168825469, ('FP2', 'DELTA'): 0.04726365215863342, (
        'FP2', 'THETA'): 0.021045254898142678, ('FP2', 'ALPHA'): 0.005169219041044824, (
        'FP2', 'BETA'): -0.002850558753348302, ('FP2', 'AD'): 0.10936986045206809, ('FP2', 'AT'): 0.24562396920652296, (
        'FP2', 'AB'): -1.813405541974181, ('FP2', 'BT'): -0.1354490010762414, ('TP10', 'DELTA'): 0.047799412661101846, (
        'TP10', 'THETA'): 0.0193384205942109, ('TP10', 'ALPHA'): 0.014735310962555436, (
        'TP10', 'BETA'): 0.01813458868128899, ('TP10', 'AD'): 0.3082738917113666, ('TP10', 'AT'): 0.7619707561312716, (
        'TP10', 'AB'): 0.8125528084217934, ('TP10', 'BT'): 0.9377492124004022, ('DRL', 'DELTA'): 0.046208352149686494, (
        'DRL', 'THETA'): 0.017116803573350423, ('DRL', 'ALPHA'): 0.012192791410115474, (
        'DRL', 'BETA'): 0.017779846694266226, ('DRL', 'AD'): 0.26386553172505195, ('DRL', 'AT'): 0.7123287568187517, (
        'DRL', 'AB'): 0.6857647098862497, ('DRL', 'BT'): 1.0387363866199943},
              {('TP9', 'DELTA'): 0.07286219804710001, ('TP9', 'THETA'): 0.04687692809609739,
               ('TP9', 'ALPHA'): 0.04048896485352779, ('TP9', 'BETA'): 0.028654294943180596,
               ('TP9', 'AD'): 0.5556923334560218, ('TP9', 'AT'): 0.8637290560193212, ('TP9', 'AB'): 1.413015568305362,
               ('TP9', 'BT'): 0.6112664824034434, ('FP1', 'DELTA'): 0.05178713820917149,
               ('FP1', 'THETA'): 0.01271813918968212, ('FP1', 'ALPHA'): 0.0057088185913824405,
               ('FP1', 'BETA'): -0.006159810388322988, ('FP1', 'AD'): 0.110236224452569,
               ('FP1', 'AT'): 0.4488721585948556, ('FP1', 'AB'): -0.9267847923053796,
               ('FP1', 'BT'): -0.4843326760663442, ('FP2', 'DELTA'): 0.056449236337240825,
               ('FP2', 'THETA'): 0.018377368381875005, ('FP2', 'ALPHA'): 0.011033897859205458,
               ('FP2', 'BETA'): 0.0005528651393967618, ('FP2', 'AD'): 0.1954658481699627,
               ('FP2', 'AT'): 0.6004068498778001, ('FP2', 'AB'): 19.957666115907916, ('FP2', 'BT'): 0.0300840211671457,
               ('TP10', 'DELTA'): 0.05883787113486534, ('TP10', 'THETA'): 0.018727240042700363,
               ('TP10', 'ALPHA'): 0.020703563912509926, ('TP10', 'BETA'): 0.018256212767530543,
               ('TP10', 'AD'): 0.3518747961674924, ('TP10', 'AT'): 1.1055320413100547,
               ('TP10', 'AB'): 1.1340557965741997, ('TP10', 'BT'): 0.9748480142244228,
               ('DRL', 'DELTA'): 0.059094008213987165, ('DRL', 'THETA'): 0.015358139217255116,
               ('DRL', 'ALPHA'): 0.017799181641431402, ('DRL', 'BETA'): 0.017356789535758647,
               ('DRL', 'AD'): 0.3012011230813491, ('DRL', 'AT'): 1.1589412877201775, ('DRL', 'AB'): 1.025488129861881,
               ('DRL', 'BT'): 1.1301362287599277}]

        df = _get_dataframe(r)
        print(df)
        print(df.keys())
        print(df.get( ('FP1', 'THETA') ))


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
            print(csbp)

            # Run calculations on csbp to obtain desired metrics
            alpha_metric = Metrics.alpha_beta_ratio(csbp, Band)
            print("alpha_beta_ratio: {}".format(alpha_metric))

            index_channel = [i]
            metrics[i] = alpha_metric
            self.assertIsNotNone(alpha_metric, "metric is not None")

        print("alpha metric for 4 sensors are separately: {}".format(metrics))

