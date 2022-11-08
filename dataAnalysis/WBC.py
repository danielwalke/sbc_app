import numpy as np

class WBC:
    def __init__(self, data):
        self.wbc = data["WBC"]

    def get_numpy_wbc(self):
        np_wbc = np.array(self.wbc, dtype=np.double)
        # np_wbc_numbers = np_wbc[~np.isnan(np_wbc)]
        return np_wbc

    def get_median_wbc(self):
        return np.median(self.get_numpy_wbc())

    def get_average_wbc(self):
        return np.average(self.get_numpy_wbc())
