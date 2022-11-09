from dataAnalysis.Age import Age
from dataAnalysis.Diagnosis import Diagnosis
from dataAnalysis.Sex import Sex
from dataAnalysis.Center import Center
from dataAnalysis.Set import Set
from dataAnalysis.WBC import WBC
from dataAnalysis.TargetIcu import TargetIcu
from dataAnalysis.Time import Time
from dataAnalysis.SecToIcu import SecToIcu
from dataAnalysis.Episode import Episode
from dataAnalysis.Sender import Sender


class DataAnalysis:
    def __init__(self, data):
        leipzig_data = data.query("Center == 'Leipzig'")
        leipzig_data = leipzig_data.drop_duplicates()
        leipzig_data = leipzig_data.query("Episode == 1", engine='python')
        leipzig_data = leipzig_data[~leipzig_data["Sender"].str.contains("ICU")]
        leipzig_unique_data = leipzig_data[~leipzig_data["Diagnosis"].str.contains("SIRS")]
        # leipzig_unique_data = leipzig_data.drop_duplicates()
        # leipzig_unique_data = leipzig_data.drop_duplicates(subset=["Id"])
        # in the dataset are duplicated identifier
        # based on the center, so first separate centers then remove duplicates and keep first
        print(len(leipzig_data))
        leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['WBC'].isnull()]
        leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['RBC'].isnull()]
        leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['PLT'].isnull()]
        # leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['PCT'].isnull()]
        leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['MCV'].isnull()]
        leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['HGB'].isnull()]
        # leipzig_unique_data = leipzig_unique_data[~leipzig_unique_data['CRP'].isnull()]
        ## without icus?
        self.data = leipzig_unique_data
        self.data = leipzig_unique_data
        self.age_analysis = Age(self.data)
        self.sex_analysis = Sex(self.data)
        self.diagnoses_analysis = Diagnosis(self.data)
        self.center_analysis = Center(self.data)
        self.set_analysis = Set(self.data)
        self.wbc_analysis = WBC(self.data)
        self.target_icus = TargetIcu(self.data)
        # self.time = Time(self.data)
        print(20*"%")
        # self.episode = Episode(self.data)
        # print(20*"%")
        self.sender = Sender(self.data)
        # print(20*"%")
        # self.sec_to_icu = SecToIcu(self.data)

    def show_text_information(self):
        self.age_analysis.get_avg_age()
        median_age = self.age_analysis.get_media_age()
        header = self.data.columns.values.tolist()
        print(20 * "#")
        print(f"The median age is {round(median_age, 1)}")
        print(f"The average age is {round(self.age_analysis.get_avg_age(), 1)}")
        print(20 * "#")
        print(len(self.data))
        print(f"Number of sepsis cases {self.diagnoses_analysis.get_numer_of_cases()}")
        print(f"Number of sirs cases {self.diagnoses_analysis.get_numer_of_sirs()}")
        print(f"Number of control cases {self.diagnoses_analysis.get_number_of_controls()}")
        print(20 * "#")
        print(f"The median number of white blood cells is {round(self.wbc_analysis.get_median_wbc(), 1)}")
        print(f"The average number of white blood cells is {round(self.wbc_analysis.get_average_wbc(), 1)}")
        print(header)
        print(self.data.head())

    def show_diagrams(self):
        self.age_analysis.visualize_age()
        self.sex_analysis.visualize_sex()
        self.diagnoses_analysis.visualize_diagnoses()
        self.center_analysis.visualize_diagnoses()
        self.set_analysis.visualize_sets()
