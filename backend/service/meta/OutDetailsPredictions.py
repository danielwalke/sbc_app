from service.meta.OutDetailsPrediction import  OutDetailsPrediction

## extendable if someone wants to add some meta information as outout in the future ;)


class OutDetailsPredictions:
    prediction_details: OutDetailsPrediction = None

    def __init__(self):
        super().__init__()
        self.prediction_detail = None

    def set_prediction_detail(self, prediction_detail):
        self.prediction_detail = prediction_detail
