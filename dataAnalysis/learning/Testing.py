from dataAnalysis.learning.Features import Features


class Testing(Features):
    def __init__(self, data):
        self.testing_data = data.query("Set == 'Validation'")
        Features.__init__(self, self.testing_data)
