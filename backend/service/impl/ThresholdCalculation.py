from sklearn.metrics import roc_curve
from service.constants import Classifiers

class ThresholdCalculation:
	def __init__(self, df, default_thresholds, min_sensitivity=None):
		self.df = df
		self.default_thresholds = default_thresholds
		self.min_sensitivity = min_sensitivity

	def get_thresholds(self):
		if self.min_sensitivity is None: return self.default_thresholds
		threshold_dict = dict()
		y_true = self.df.loc[:, "y"]
		for classifier in Classifiers.CLASSIFIER_LIST:
			if self.min_sensitivity >= 1:
				threshold_dict[classifier] = 0
				continue
			if self.min_sensitivity <= 0:
				threshold_dict[classifier] = 1
				continue
			pred_proba = self.df[classifier]
			fpr, tpr, thresholds = roc_curve(y_true, pred_proba)
			sensitivity_index = (tpr < self.min_sensitivity).sum()
			threshold_dict[classifier] = thresholds[sensitivity_index]
		print(threshold_dict)
		return threshold_dict
