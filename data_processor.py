
import utils
import numpy as np  # Module that simplifies computations on matrices
import metrics

class DataProcessor:
    """

    Example usage:
        c = DataProcessor(...)               # Specify data-recording parameters
        c.feed_new_data(eeg_data=eeg_data)          # Feed new data generated in the epoch
        for channel in [0,1,2,3]:                   # Iterate through all separate channels

            # Record channel smooth band power
            csbp = c.get_channel_smooth_band_powers(channel)

            # Run calculations on csbp to obtain desired metrics
            a = Metrics.alpha_protocol(csbp, Band)
            print("Alpha metric: {}".format(a))

    """

    def __init__(self, buffer_length=5, epoch_length=1, overlap_length=0.8, shift_length=None, fs=None, band_cls=None, chans=None):
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
        assert shift_length is not None
        self.shift_length = shift_length
        self.buffer_length = buffer_length
        self.epoch_length = epoch_length
        self.overlap_length = overlap_length

        self.n_win_test = utils.get_num_epoch(buffer_length=self.buffer_length,
                                         epoch_length=self.epoch_length,
                                         shift_length=self.shift_length)

        self.eeg_data = None  # Current Epoch EEG Data

        assert fs is not None  # Check that fs is defined
        self.fs = fs

        self.eeg_buffer = None
        self.filter_state = None

        self.band_cls = band_cls  # To store Band -> Number
        
        self.chans = chans
        
        self.df = list()

    def feed_new_data(self, eeg_data=None):
        self._setup_buffers()
        assert eeg_data is not None  # Check that eeg_data is passed in
        self.eeg_data = eeg_data

    def _setup_buffers(self):
        """ Set up buffers shared by all channels
        :return:
        """

        self.eeg_buffer = utils.create_eeg_buffer(fs=self.fs, buffer_length=self.buffer_length)
        self.filter_state = utils.create_filter_state()

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

            index_channel = channel.value
            
            # Initialize the band power buffer (for plotting)
            # bands will be ordered: [delta, theta, alpha, beta]
            band_powers = self._get_band_powers(index_channel)
            band_buffer = np.zeros((self.n_win_test, 4))
            band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))

            # Record channel smooth band power
            csbp = self.get_smooth_band_powers(band_buffer)

            
            
            #acquires power values for interative channel
            for i in range(len(bands)):
                band = bands[i]
                # eg. res[("TP1", "alpha")] = cbsp[0]
                res[(channel, band)] = csbp[i]


            # acquire ratio measures for channel
            
#             metrics[channel][4:] = Metrics.get_ratios(csbp, utils.Band)
            self.df.append(res)  # TODO: change to dataframe 

#         return red

#     def 
#     def get_all_smooth_band_powers(self):
        
#         powers = []
        
#         for
        
        
#                 for channel in range(NUM_CHANNELS):  # Iterate through all separate channels

#                     # Record channel smooth band power
#                     csbp = c.get_channel_smooth_band_powers(channel)
                    
#                     #acquires power values for interative channel
#                        #metrics[channel][0:4] = csbp[0:4]

#                     # acquire ratio measures for channel
                    
#                        #metrics[channel][4:] = Metrics.get_ratios(csbp, utils.Band)
        
#         metrics = {
#                     "delta": None,
#                     "theta": None,
#                     "alpha": None,
#                     "beta": None,
#                     "alpha/delta": None,
#                     "alpha/theta": None,
#                     "alpha/beta": None,
#                     "beta/theta": None} 

