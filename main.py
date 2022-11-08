import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis


data = pd.read_csv(r"extdata\sbcdata.csv", header=0)
data_analysis = DataAnalysis(data)
data_analysis.show_diagrams()
data_analysis.show_text_information()