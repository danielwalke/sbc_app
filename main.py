import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from dataAnalysis.Subplot import Subplot

subplot = Subplot(1, 2)
data = pd.read_csv(r"extdata\sbcdata.csv", header=0)
data_analysis = DataAnalysis(data)


# data_analysis.extra_trees()
# data_analysis.random_forest()
# # data_analysis.bagging_classifier()
# data_analysis.rus_boost()
# data_analysis.k_neighbors()
# data_analysis.logistic_regression()

# data_analysis.lazy_predict()
# data_analysis.support_vector_machine()
# data_analysis.show_diagrams()
# # data_analysis.show_text_information()
# data_analysis.show_comparison_diagrams()