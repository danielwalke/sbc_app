import pandas as pd
import numpy as np
from dataAnalysis.DataAnalysis import DataAnalysis
from service.impl.GraphPrediction import GraphPrediction
from service.meta.GraphCBC import GraphCBC
from typing import List


def get_data_by_set_name(data_analysis, set_type: str):
    data = None
    if set_type == 'train':
        data = data_analysis.get_training_data()
    if set_type == 'test':
        data = data_analysis.get_testing_data()
    if set_type == 'val':
        data = data_analysis.get_gw_testing_data()
    return data


def get_cbc_items(set_type):
    data = pd.read_csv(r"./extdata/sbcdata.csv", header=0)
    data_analysis = DataAnalysis(data)
    data = get_data_by_set_name(data_analysis, set_type)
    data = data.loc[:, ["Id", "Time", "Age", "Sex", "HGB", "WBC", "RBC", "MCV", "PLT", "Label"]]
    data["Label"] = data["Label"] == "Sepsis"
    data = data.rename(
        columns={"Id": "id", "Time": "order", "Age": "age", "Sex": "sex", "Label": "ground_truth"})
    columns = data.columns
    graph_cbc_items = [GraphCBC(**row) for row in data.to_dict(orient="records")]
    return graph_cbc_items, columns


def export_csv_data_for_neo4j_by_set_type(set_type, offset):
    assert set_type in ['train', 'test', "val"]
    graph_cbc_items, columns = get_cbc_items(set_type)
    graph_constr = GraphPrediction(graph_cbc_items, None, None, None)
    graph_constr.construct_directed_graph()
    features = pd.DataFrame(data=graph_constr.graph["X"], columns=graph_constr.graph["columns"])
    features["node_id"] = np.arange(features.shape[0]) + offset
    features["set_type"] = set_type
    # features["label"] = graph_constr.graph["labels"]
    features = features.loc[:, ["node_id", *graph_constr.graph["columns"]]]
    edge_index_dir = pd.DataFrame(data=graph_constr.graph["edge_index"].numpy().transpose() + offset,
                                  columns=["source", "target"])
    graph_constr.construct_reversed_directed_graph()
    edge_index_rev_dir = pd.DataFrame(data=graph_constr.graph["edge_index"].numpy().transpose() + offset,
                                      columns=["source", "target"])
    features.to_csv(f"{set_type}_features.csv", index=False)
    edge_index_dir.to_csv(f"{set_type}_dir_edge_index.csv", index=False)
    edge_index_rev_dir.to_csv(f"{set_type}_rev_dir_edge_index.csv", index=False)
    return features.shape[0]


def export_csv_data_for_neo4j():
    offset = 0
    for set_type in ['train', 'test', 'val']:

        offset = export_csv_data_for_neo4j_by_set_type(set_type, offset)


if __name__ == '__main__':
    export_csv_data_for_neo4j()
