import numpy as np
import shap
import torch
from sklearn.ensemble import RandomForestClassifier
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


def get_reversed_edge_index(df):
    edge_index = get_edge_index(df)
    rev_edge_index = torch.zeros_like(edge_index)
    rev_edge_index[0, :] = edge_index[1, :]
    rev_edge_index[1, :] = edge_index[0, :]
    return rev_edge_index


class GraphPrediction:
    def __init__(self, graph_cbc_items: list[GraphCBC], models):
        self.graph_cbc_items: list[GraphCBC] = graph_cbc_items
        self.models = models
        hops = [0, 3]
        self.framework = Framework(hops_list=hops,
                              clfs=models,
                              attention_configs=[None for i in hops],
                              handle_nan=0.0,
                              gpu_idx=0,
                              user_functions=[user_function for i in hops]
                              )
        self.framework.trained_clfs = models

    def get_graph(self):
        X = np.zeros((len(self.graph_cbc_items), 9))
        y = np.zeros((len(self.graph_cbc_items), 1))
        for i, cbc_item in enumerate(self.graph_cbc_items):
            categorical_sex = 1 if cbc_item.sex == "W" else 0
            cbc_array = [cbc_item.id, cbc_item.order, cbc_item.age, categorical_sex, cbc_item.HGB, cbc_item.WBC,
                         cbc_item.RBC, cbc_item.MCV,
                         cbc_item.PLT]
            X[i, :] = cbc_array
            y[i, 0] = cbc_item.ground_truth
        X = pd.DataFrame(X).sort_values(by=[0, 1]).reset_index(drop=True)
        edge_index = get_reversed_edge_index(X)
        return X.values[:, 2:], edge_index, y

    def get_features_list(self):
        X, edge_index, y = self.get_graph()
        return self.framework.get_features(X, edge_index.type(torch.long), torch.ones(X.shape[0]).type(torch.bool))

    def get_pred_proba(self):
        X, edge_index, y = self.get_graph()
        return self.framework.predict_proba(X, edge_index.type(torch.long), torch.ones(X.shape[0]).type(torch.bool))[:, 1]

    def get_prediction(self):
        return self.get_pred_proba() >= 0.5

    def get_shapley_values(self):
        X_0, X_3 = self.get_features_list()
        explainer_0 = shap.TreeExplainer(self.models[0])
        shap_values_0 = explainer_0.shap_values(X_0)

        explainer_3 = shap.TreeExplainer(self.models[1])
        shap_values_3= explainer_3.shap_values(X_3)

        return shap_values_0[1] + shap_values_3[1] ## TODO return dict in future for this (own features, neighborhood, combined contribution)

    def get_output(self):
        output = OutPrediction()
        print("Start classification")
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        print("Finished classification")
        print("Started Shapley values calculation")
        # output.set_shap_values(self.get_shapley_values().tolist())
        print("Finished Shapley values calculation")
        return output
