""" The metrics used to analyze neural data"""

class Metrics:
    """
    3.3 COMPUTE NEUROFEEDBACK METRICS
        These metrics could also be used to drive brain-computer interfaces
    """

    @staticmethod
    def alpha_delta_ratio(smooth_band_powers, band_cls):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by delta waves in order to rule out noise

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_d_metric = smooth_band_powers[band_cls.Alpha] / \
                       smooth_band_powers[band_cls.Delta]
        
        return a_d_metric
    
    @staticmethod
    def alpha_theta_ratio(smooth_band_powers, band_cls):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by theta

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_t_metric = smooth_band_powers[band_cls.Alpha] / \
                       smooth_band_powers[band_cls.Theta]
        
        return a_t_metric
    
    @staticmethod
    def alpha_beta_ratio(smooth_band_powers, band_cls):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by theta

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_b_metric = smooth_band_powers[band_cls.Alpha] / \
                       smooth_band_powers[band_cls.Beta]
        
        return a_b_metric

    @staticmethod
    def beta_theta_ratio(smooth_band_powers, band_cls):
        """ Beta Protocol:
            Beta waves have been used as a measure of mental activity and concentration
            This beta over theta ratio is commonly used as neurofeedback for ADHD
        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        beta_metric = smooth_band_powers[band_cls.Beta]/smooth_band_powers[band_cls.Theta]
        
        return beta_metric