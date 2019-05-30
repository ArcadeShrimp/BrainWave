""" The metrics used to analyze neural data"""
import utils

class Metrics:
    """
    3.3 COMPUTE NEUROFEEDBACK METRICS
        These metrics could also be used to drive brain-computer interfaces
    """

    @staticmethod
    def alpha_delta_ratio(smooth_band_powers):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by delta waves in order to rule out noise

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_d_metric = smooth_band_powers[utils.Band.ALPHA.value] / \
                       smooth_band_powers[utils.Band.DELTA.value]

        return a_d_metric

    @staticmethod
    def alpha_theta_ratio(smooth_band_powers):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by theta

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_t_metric = smooth_band_powers[utils.Band.ALPHA.value] / \
                       smooth_band_powers[utils.Band.THETA.value]

        return a_t_metric

    @staticmethod
    def alpha_beta_ratio(smooth_band_powers):
        """ Alpha Protocol:
            Simple readout of alpha power, divided by theta

        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        a_b_metric = smooth_band_powers[utils.Band.ALPHA.value] / \
                       smooth_band_powers[utils.Band.BETA.value]

        return a_b_metric

    @staticmethod
    def beta_theta_ratio(smooth_band_powers):
        """ Beta Protocol:
            Beta waves have been used as a measure of mental activity and concentration
            This beta over theta ratio is commonly used as neurofeedback for ADHD
        :param smooth_band_powers:
        :param band_cls:
        :return:
        """
        beta_metric = smooth_band_powers[utils.Band.BETA.value]/smooth_band_powers[utils.Band.THETA.value]

        return beta_metric

    @staticmethod
    def get_ratios(sm_b_pws):

        return [Metrics.alpha_delta_ratio(sm_b_pws),\
                Metrics.alpha_theta_ratio(sm_b_pws),\
                Metrics.alpha_beta_ratio(sm_b_pws),\
                Metrics.beta_theta_ratio(sm_b_pws)]
