import numpy as np
import shap
from service.meta.OutPrediction import OutPrediction
from service.meta.GraphCBC import GraphCBC
import pandas as pd

class GraphPrediction:
    def __init__(self, graph_cbc_items:list[GraphCBC], model):
        self.graph_cbc_items:list[GraphCBC] = graph_cbc_items
        self.model = model

    def get_graph(self):
        X = np.zeros((len(self.graph_cbc_items), 9))
        for i, cbc_item in enumerate(self.cbc_items):
            categorical_sex = 1 if cbc_item.sex == "W" else 0
            cbc_array = [cbc_item.id, cbc_item.time, cbc_item.age, categorical_sex, cbc_item.HGB, cbc_item.WBC,
                         cbc_item.RBC, cbc_item.MCV,
                         cbc_item.PLT]
            X[i, :] = cbc_array
        X = pd.DataFrame(X).sort_values(by=[0, 1]).reset_index(drop=True)
        edge_index = self.get_edge_index(X)
        return X, edge_index



    def get_edge_index(self, df):
        edge_index = []
        ## group df by ids
        for identifier, group in df.groupby(0):
            offset = group.index[0]
            triu_matrix = np.triu((group.index.values + np.identity(1))[0])
            triu_exp_matrix = np.expand_dims(triu_matrix, axis=-1)

            idx_shape = group.index.shape[0]
            idx_matrix = np.ones((idx_shape, idx_shape)) * np.arange(idx_shape) + 1 + offset
            idx_matrix = np.transpose(idx_matrix)
            idx_exp_matrix = np.expand_dims(idx_matrix, axis=-1)

            unprocess_edges = np.concatenate((idx_exp_matrix, triu_exp_matrix), axis=-1)
            reshaped_unprocess_edges = np.reshape(unprocess_edges, (-1, 2))
            mask = (reshaped_unprocess_edges[:, 0] * reshaped_unprocess_edges[:, 1]) != 0
            edge_index.append((reshaped_unprocess_edges[mask] - 1).astype(np.int64))
        return edge_index

    def get_pred_proba(self):
        X = self.get_features()
        return self.model.predict_proba(X)[:, 1]

    def get_prediction(self):
        return self.get_pred_proba() >= 0.3547

    def get_shapley_values(self):
        X = self.get_features()
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        return shap_values[1]

    def get_output(self):
        output = OutPrediction()
        print("Start classification")
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        print("Finished classification")
        print("Started Shapley values calculation")
        output.set_shap_values(self.get_shapley_values().tolist())
        print("Finished Shapley values calculation")
        return output
