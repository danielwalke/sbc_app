from dataAnalysis.learning.Features import Features


class Training(Features):
    def __init__(self, data):
        leipzig_training_data = data.query("Center == 'Leipzig' & Set == 'Training'")
        Features.__init__(self, leipzig_training_data)
