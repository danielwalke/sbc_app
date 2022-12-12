
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
        non_icu_unique_data = unique_data.query("~(Sender.str.contains('ICU')) & ~(~SecToIcu.isnull() & SecToIcu < 0)", engine='python')
        first_non_icu_unique_data = non_icu_unique_data.query("Episode == 1 ", engine='python')
        complete_first_non_icu_unique_data = first_non_icu_unique_data.query("~(WBC.isnull() | HGB.isnull() | "
                                                                             "MCV.isnull() | PLT.isnull() | "
                                                                             "RBC.isnull())", engine='python')
        sirs_complete_first_non_icu_unique_data = complete_first_non_icu_unique_data.query("Diagnosis != 'SIRS'",
                                                                                           engine='python')
        self.data = sirs_complete_first_non_icu_unique_data
        self.control_data = self.data.query("(Diagnosis == 'Control' | (SecToIcu > 6*3600 & "
                                            "(~TargetIcu.isnull() & TargetIcu.str.contains('MICU'))))", engine='python')
        self.sepsis_data = self.data.query("Diagnosis == 'Sepsis'", engine='python')
        self.sepsis_data = self.sepsis_data.query("(~TargetIcu.isnull() & TargetIcu.str.contains('MICU'))",
                                                  engine='python')
        self.sepsis_data = self.sepsis_data.query("SecToIcu <= 6*3600", engine='python')

    def get_x(self):
        feature_columns = ["Age","Sex", "HGB", "MCV", "PLT", "RBC", "WBC"]
        return self.data[feature_columns].replace(to_replace='W', value=1).replace(to_replace='M', value=0)

    def get_y(self):
        return self.data["Diagnosis"]

    def get_control_data(self):
        return self.control_data

    def get_sepsis_data(self):
        return self.sepsis_data

    def get_data(self):
        return self.data
