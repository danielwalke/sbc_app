from service.meta.OutDetailsPrediction import  OutDetailsPrediction
from service.meta.OutGraphDetailsPredictions import  OutGraphDetailsPredictions
from typing import Union
## extendable if someone wants to add some meta information as outout in the future ;)


class OutDetailsPredictions:
    prediction_details: Union[list[OutDetailsPrediction], list[OutGraphDetailsPredictions]] = []

    def __init__(self):
        super().__init__()
        self.prediction_details = []

    def set_prediction_details(self, prediction_details):
        self.prediction_details = prediction_details

    def add_prediction_detail(self, prediction_detail):
        self.prediction_details.append(prediction_detail)