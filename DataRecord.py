""" A DataRecord holds information for a single PsychoPy Trial, ex) Relax_1, Focus_1"""
import utils

class DataRecord:

    def __init__(self):
        self.deltas = []
        self.thetas = []
        self.alphas = []
        self.betas = []
        
        fooofs = {}

    def get_metrics(self, channel_index):
        """

        :return: a list of average powers for each channel
        """

        deltas = [l[channel_index] for l in self.deltas]
        thetas = [l[channel_index] for l in self.thetas]
        alphas = [l[channel_index] for l in self.alphas]
        betas = [l[channel_index] for l in self.betas]

        return MetricStats(avg_deltas=np.mean(deltas),
                           avg_thetas=np.mean(thetas),
                           avg_alphas=np.mean(alphas),
                           avg_betas=np.mean(betas))

class MetricStats:

    def __init__(self, avg_deltas=0, avg_thetas=0, avg_alphas=0, avg_betas=0):
        self.avg_deltas = avg_deltas
        self.avg_thetas = avg_thetas
        self.avg_alphas = avg_alphas
        self.avg_betas = avg_betas


