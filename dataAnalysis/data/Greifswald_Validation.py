from dataAnalysis.data.Features import Features


class GreifswaldValidation(Features):
    def __init__(self, data):
        greifswald_validation_data = data.query("Center == 'Greifswald' & Set == 'Validation'")
        Features.__init__(self, greifswald_validation_data)
