from dataAnalysis.data.Features import Features


class Validation(Features):
    def __init__(self, data):
        leipzig_validation_data = data.query("Center == 'Greifswald' & Set == 'Validation'")
        Features.__init__(self, leipzig_validation_data)
