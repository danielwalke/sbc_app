import numpy as np
import shap
import torch
import math
from sklearn.metrics import roc_auc_score

from service.impl.EnsembleFramework import Framework
from service.meta.OutPrediction import OutPrediction
from service.meta.GraphCBC import GraphCBC
import pandas as pd


def user_function(kwargs):
    return kwargs["original_features"] - kwargs["mean_neighbors"]


def get_edge_index(df):
    edge_index = []
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
    edge_index = torch.from_numpy(np.concatenate(edge_index)).type(torch.long)
    return edge_index.transpose(0, 1)


def get_reversed_edge_index(edge_index):
    rev_edge_index = torch.zeros_like(edge_index)
    rev_edge_index[0, :] = edge_index[1, :]
    rev_edge_index[1, :] = edge_index[0, :]
    return rev_edge_index


class GraphPrediction:
    def __init__(self, graph_cbc_items: list[GraphCBC], model, threshold):
        self.graph_cbc_items: list[GraphCBC] = graph_cbc_items
        self.model = model
        hops = [0, 1]
        self.framework = Framework(hops_list=hops,
                              clfs=[None for _ in hops],
                              attention_configs=[None for i in hops],
                              handle_nan=0.0,
                              gpu_idx=0,
                              user_functions=[user_function for i in hops]
                              )
        self.framework.trained_clfs = model
        self.threshold = threshold
        self.graph = None
        self.pred_proba = None

    def construct_directed_graph(self):
        data = np.zeros((len(self.graph_cbc_items), 9 + 1))
        y = np.zeros((len(self.graph_cbc_items)))
        for i, cbc_item in enumerate(self.graph_cbc_items):
            categorical_sex = 1 if cbc_item.sex == "W" else 0
            cbc_array = [cbc_item.id, cbc_item.order, cbc_item.ground_truth, cbc_item.age, categorical_sex,
                         cbc_item.HGB, cbc_item.WBC,
                         cbc_item.RBC, cbc_item.MCV,
                         cbc_item.PLT]
            data[i, :] = cbc_array
            y[i] = cbc_item.ground_truth

        data = pd.DataFrame(data)
        data = data.sort_values(by=[0, 1])
        original_index = np.argsort(data.index)
        data = data.reset_index(drop=True)
        edge_index = get_edge_index(data)
        self.graph = {
            "X": data.values[:, 3:],
            "edge_index": edge_index,
            "labels": data.values[:, 2],
            "original_index": original_index
        }

    def construct_reversed_directed_graph(self):
        self.construct_directed_graph()
        self.graph["edge_index"] = get_reversed_edge_index(self.graph["edge_index"])

    def set_pred_proba(self):
        X, edge_index, _, original_index = self.get_graph()
        features_origin, features_time = self.framework.get_features(X, edge_index.type(torch.long), torch.ones(X.shape[0]).type(torch.bool))
        combined_features = torch.cat([features_origin, features_time], dim=-1)
        self.pred_proba = self.model.predict_proba(combined_features)[original_index, 1]

    def get_graph(self):
        return self.graph["X"], self.graph["edge_index"], self.graph["labels"], self.graph["original_index"]

    def get_features_list(self):
        X, edge_index, _, original_index = self.get_graph()
        return list(map(lambda features: features[original_index, :], self.framework.get_features(X, edge_index.type(torch.long), torch.ones(X.shape[0]).type(torch.bool))))

    def get_pred_proba(self):
        return self.pred_proba

    def get_prediction(self):
        return self.get_pred_proba() >= self.threshold

    def get_auroc(self):
        X, edge_index, y, original_index = self.get_graph()
        return None if np.unique(y).shape[0] != 2 else roc_auc_score(y[original_index], self.get_pred_proba())

    def get_output(self):
        self.set_pred_proba()
        output = OutPrediction()
        print("Start classification")
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        output.set_auroc(self.get_auroc())
        print("Finished classification")
        return output

    def get_prospective_output(self):
        self.construct_directed_graph()
        return self.get_output()

    def get_retrospective_output(self):
        self.construct_reversed_directed_graph()
        return self.get_output()