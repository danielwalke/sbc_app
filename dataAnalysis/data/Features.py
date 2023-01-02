import pandas as pd


def count_cbc_cases(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())",
                           engine='python')
    unique_data = comp_data.drop_duplicates(subset=["Id", "Center"])
    return len(unique_data)


def count_cbc(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())",
                           engine='python')
    return len(comp_data)


class Features:
    def __init__(self, data):
        unique_data = data.drop_duplicates(subset=["Id", "Center", "Time"], keep=False)
        non_icu_unique_data = unique_data.query("~(Sender.str.contains('ICU')) & ~(~SecToIcu.isnull() & SecToIcu < 0)",
                                                engine='python')
        first_non_icu_unique_data = non_icu_unique_data.query("Episode == 1 ", engine='python')
        complete_first_non_icu_unique_data = first_non_icu_unique_data.query("~(WBC.isnull() | HGB.isnull() | "
                                                                             "MCV.isnull() | PLT.isnull() | "
                                                                             "RBC.isnull())", engine='python')
        sirs_complete_first_non_icu_unique_data = complete_first_non_icu_unique_data.query("Diagnosis != 'SIRS'",
                                                                                           engine='python')
        self.data = sirs_complete_first_non_icu_unique_data
        self.data['Label'] = self.data['Diagnosis']

        control_filter = (self.data["Diagnosis"] == 'Control') | \
                         ((self.data["SecToIcu"] > 3600 * 6) & (
                                     ~self.data["TargetIcu"].isnull() & self.data["TargetIcu"]
                                     .str.contains('MICU', na=False)))
        sepsis_filter = (self.data["Diagnosis"] == 'Sepsis') & \
                        (self.data["SecToIcu"] <= 3600 * 6) & \
                        (self.data["TargetIcu"].str.contains('MICU', na=False))
        self.data.loc[control_filter, "Label"] = "Control"
        self.data.loc[sepsis_filter, "Label"] = "Sepsis"

        self.control_data = self.data.loc[control_filter]
        print(self.control_data.shape)
        self.sepsis_data = self.data.loc[sepsis_filter]
        print(self.sepsis_data.shape)

    def get_x(self):
        feature_columns = ["Age", "Sex", "HGB", "MCV", "PLT", "RBC", "WBC"]
        return self.data[feature_columns].replace(to_replace='W', value=1).replace(to_replace='M', value=0)

    def get_y(self):
        return self.data["Label"]

    def get_control_data(self):
        return self.control_data

    def get_sepsis_data(self):
        return self.sepsis_data

    def get_data(self):
        return self.data
