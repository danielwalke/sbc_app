from dataAnalysis.learning.Features import Features


class Training(Features):
    def __init__(self, data):
        self.training_data = data.query("Set == 'Training'")
        Features.__init__(self, self.training_data)
