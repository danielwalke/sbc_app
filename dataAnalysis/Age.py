import numpy as np
import matplotlib.pyplot as plt


class Age:
    def __init__(self, data):
        self.ages = data["Age"]

    def get_numpy_ages(self):
        np_ages = self.ages.to_numpy(dtype=np.uintc)
        return np_ages

    def get_avg_age(self):
        avg = np.average(self.get_numpy_ages())
        return avg

    def get_media_age(self):
        return np.median(self.get_numpy_ages())

    def visualize_age(self):
        ages = self.get_numpy_ages()
        plt.hist(ages, bins=len(np.unique(ages)))
        plt.ylabel('frequency')
        plt.xlabel('age')
        plt.show()
