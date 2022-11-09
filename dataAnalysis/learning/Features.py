class Features:
    def __init__(self, data):
        self.data = data

    def get_x(self):
        feature_columns = ["Age","Sex", "HGB", "MCV", "PLT", "RBC", "WBC"]
        return self.data[feature_columns].replace(to_replace='W', value=1).replace(to_replace='M', value=0)

    def get_y(self):
        return self.data["Diagnosis"]
