import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from dataAnalysis.Subplot import Subplot

subplot = Subplot(1, 2)
data = pd.read_csv(r"extdata\sbcdata.csv", header=0)
data_analysis = DataAnalysis(data)
data_analysis.show_diagrams()
# # data_analysis.show_text_information()
# # data_analysis.rus_boost()
# data_analysis.show_comparison_diagrams()