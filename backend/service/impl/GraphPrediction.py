import numpy as np
import shap
import torch
import math
from sklearn.metrics import roc_auc_score

from service.impl.EnsembleFramework import Framework
from service.meta.OutPrediction import OutPrediction
from service.meta.GraphCBC import GraphCBC
import pandas as pd


def diff_user_function(kwargs):
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
    def __init__(self, graph_cbc_items: list[GraphCBC], model, threshold, standard_scaler, ref_node=None,
                 user_function=diff_user_function):
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
        self.standard_scaler = standard_scaler
        self.ref_node = ref_node

    def append_ref_node(self, ref_node):
        X = torch.from_numpy(self.graph["X"]).type(torch.float)
        edge_index = self.graph["edge_index"]

        X_new = torch.cat([X, ref_node.unsqueeze(0)], dim=0)
        mask = torch.ones(X_new.shape[0], dtype=torch.bool)
        mask[-1] = False
        ref_target_nodes = torch.arange(X_new.shape[0])
        ref_source_nodes = torch.ones_like(ref_target_nodes) * (X_new.shape[0] - 1)
        ref_edge_index = torch.stack([ref_source_nodes, ref_target_nodes])
        edge_index_new = torch.cat([edge_index, ref_edge_index], dim=-1)

        self.graph["X"] = X_new.numpy()
        self.graph["edge_index"] = edge_index_new
        self.graph["mask"] = mask
        return self.graph

    def construct_directed_graph(self):
        data = np.zeros((len(self.graph_cbc_items), 9 + 1))
        y = np.zeros((len(self.graph_cbc_items)))
        columns = ["id", "order", "ground_truth", "age", "categorical_sex", "HGB", "WBC", "RBC", "MCV", "PLT"]
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
            # "X": data.values[:, :],
            "X": data.values[:, 3:],
            "edge_index": edge_index,
            "labels": data.values[:, 2],
            "original_index": original_index,
            "mask": torch.ones(data.shape[0], dtype=torch.bool),
            "is_reversed": False
            # "columns": columns
        }
        if self.ref_node is not None:
            self.append_ref_node(self.ref_node)

    def construct_reversed_directed_graph(self):
        if self.graph is None: self.construct_directed_graph()
        if self.graph["is_reversed"]: return self.graph
        self.graph["edge_index"] = get_reversed_edge_index(self.graph["edge_index"])

    def set_pred_proba(self):
        X, edge_index, _, original_index, mask = self.get_graph()
        features_origin, features_time = self.framework.get_features(X, edge_index.type(torch.long), mask)
        combined_features = torch.cat([features_origin, features_time], dim=-1)
        if self.standard_scaler is not None:
            combined_features = self.standard_scaler.transform(combined_features)
        self.pred_proba = self.model.predict_proba(combined_features)[original_index, 1]

    def get_graph(self):
        return self.graph["X"], self.graph["edge_index"], self.graph["labels"], self.graph["original_index"], \
            self.graph["mask"]

    def get_features_list(self):
        X, edge_index, _, original_index, mask = self.get_graph()
        return list(map(lambda features: features[original_index, :],
                        self.framework.get_features(X, edge_index.type(torch.long), mask)))

    def get_pred_proba(self):
        return self.pred_proba

    def get_prediction(self):
        return self.get_pred_proba() >= self.threshold

    def get_auroc(self):
        X, edge_index, y, original_index, mask = self.get_graph()
        if not np.isnan(y).any() and np.unique(y).shape[0] == 2:
            print(roc_auc_score(y[original_index], self.get_pred_proba()))
        return None if np.unique(y).shape[0] != 2 else roc_auc_score(y[original_index], self.get_pred_proba())

    def get_output(self):
        self.set_pred_proba()
        output = OutPrediction()
        print("Start classification")
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        try:
            output.set_auroc(self.get_auroc())
        except:
            print("Couldnt calculate auroc")
        print("Finished classification")
        return output

    def get_prospective_output(self):
        self.construct_directed_graph()
        return self.get_output()

    def get_retrospective_output(self):
        self.construct_reversed_directed_graph()
        return self.get_output()

if __name__ == "__main__":
    from joblib import load
    graph_cbc_instance = GraphCBC(
        id=101,
        order=1.0,
        age=58.0,
        sex='F',
        HGB=13.5,
        WBC=6.7,
        RBC=4.5,
        MCV=92.0,
        PLT=210.0,
        ground_truth=0
    )
    graph_cbc_items = [graph_cbc_instance]
    model = load('../../models/prospective/prospective_xgb.joblib')
    threshold = 0.5
    standard_scaler = None
    graph_pred = GraphPrediction(graph_cbc_items, model, threshold, standard_scaler, ref_node=None,
                 user_function=diff_user_function)