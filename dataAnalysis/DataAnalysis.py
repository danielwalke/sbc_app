from dataAnalysis.Age import Age
from dataAnalysis.Diagnosis import Diagnosis
from dataAnalysis.Sex import Sex
from dataAnalysis.Center import Center
from dataAnalysis.Set import Set
from dataAnalysis.WBC import WBC

## TODO: There is an error due to multiple ids (Distrotion error)
class DataAnalysis:
    def __init__(self, data):
        self.data = data
        self.age_analysis = Age(data)
        self.sex_analysis = Sex(data)
        self.diagnoses_analysis = Diagnosis(data)
        self.center_analysis = Center(data)
        self.set_analysis = Set(data)
        self.wbc_analysis = WBC(data)

    def show_text_information(self):
        self.age_analysis.get_avg_age()
        median_age = self.age_analysis.get_media_age()
        header = self.data.columns.values.tolist()

        print(f"The median age is {round(median_age,1)}")
        print(f"The average age is {round(self.age_analysis.get_avg_age(),1)}")
        print(f"The median number of white blood cells is {round(self.wbc_analysis.get_median_wbc(),1)}")
        print(f"The average number of white blood cells is {round(self.wbc_analysis.get_average_wbc(),1)}")
        print(header)
        print(self.data.head())

    def show_diagrams(self):
        self.age_analysis.visualize_age()
        self.sex_analysis.visualize_sex()
        self.diagnoses_analysis.visualize_diagnoses()
        self.center_analysis.visualize_diagnoses()
        self.set_analysis.visualize_sets()
