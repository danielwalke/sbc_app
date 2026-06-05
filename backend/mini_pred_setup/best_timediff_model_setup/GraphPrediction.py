import numpy as np
import torch
from EnsembleFramework import Framework
import pandas as pd
from pydantic import BaseModel
from typing import Optional
from OutPrediction import OutPrediction

class CBC(BaseModel):
	age: float
	sex: str
	HGB: float
	WBC: float
	RBC: float
	MCV: float
	PLT: float
	ground_truth: Optional[int]


class GraphCBC(CBC):
	id: int
	time: float


def diff_user_function(kwargs):
	return kwargs["original_features"] - kwargs["mean_neighbors"]


def get_edges(df):
	source_edge_index = []
	target_edge_index = []
	edge_weights = []
	for Id, group in df.groupby("Id"):
		indices = group.index
		offset = indices[0]
		num_nodes = len(indices)
		edge_index = torch.zeros((2, sum(range(num_nodes + 1))), dtype=torch.long)+offset
        
		edge_index[:, 0:num_nodes] = (torch.arange(num_nodes) + offset).view(1, -1)
		idx = num_nodes
		for i in range(1, num_nodes):
			edge_index[1, idx:idx + i] = i+offset
			edge_index[0, idx:idx + i] = torch.arange(i)+offset
			idx += i
		src_idc = edge_index[0, :] - offset
		trt_idc = edge_index[1, :] - offset
		group_time = np.expand_dims(group["Time"].values, 0) if group["Time"].values.shape[0] <= 1 else (group["Time"].values - group["Time"].values.min()) / (group["Time"].values.max() - group["Time"].values.min())
        
		time_diff = 1 - (group_time[trt_idc] - group_time[src_idc])
		source_edge_index.extend(edge_index[0, :].numpy().tolist())
		target_edge_index.extend(edge_index[1, :].numpy().tolist())
		edge_weights.extend(time_diff.tolist())

	edge_index = np.asarray([np.asarray(source_edge_index), np.asarray(target_edge_index)])
	edge_index = torch.tensor(edge_index)
	edge_weight = torch.tensor(edge_weights)
	return edge_index, edge_weight


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
		edge_weight = self.graph["edge_weight"]

		X_new = torch.cat([X, ref_node.unsqueeze(0)], dim=0)
		mask = torch.ones(X_new.shape[0], dtype=torch.bool)
		mask[-1] = False
		ref_target_nodes = torch.arange(X_new.shape[0])
		ref_source_nodes = torch.ones_like(ref_target_nodes) * (X_new.shape[0] - 1)
		ref_edge_index = torch.stack([ref_source_nodes, ref_target_nodes])
		edge_index_new = torch.cat([edge_index, ref_edge_index], dim=-1)
		edge_weight_new = torch.cat([edge_weight, torch.ones(ref_edge_index.shape[1])])
		self.graph["X"] = X_new.numpy()
		self.graph["edge_index"] = edge_index_new
		self.graph["mask"] = mask
		self.graph["edge_weight"] = edge_weight_new
		return self.graph

	def construct_directed_graph(self):
		data = np.zeros((len(self.graph_cbc_items), 9 + 1))
		y = np.zeros((len(self.graph_cbc_items)))
		columns = ["Id", "Time", "ground_truth", "age", "categorical_sex", "HGB", "WBC", "RBC", "MCV", "PLT"]
		for i, cbc_item in enumerate(self.graph_cbc_items):
			categorical_sex = 1 if cbc_item.sex == "W" else 0

			cbc_array = [cbc_item.id, cbc_item.time, cbc_item.ground_truth, cbc_item.age, categorical_sex,
						 cbc_item.HGB, cbc_item.WBC,
						 cbc_item.RBC, cbc_item.MCV,
						 cbc_item.PLT]
			data[i, :] = cbc_array
			y[i] = cbc_item.ground_truth

		data = pd.DataFrame(data, columns=columns)
		data = data.sort_values(by=["Id", "Time"])
		original_index = np.argsort(data.index)
		data = data.reset_index(drop=True)
		print(data.columns)
		edge_index, edge_weight = get_edges(data)

		self.graph = {
			# "X": data.values[:, :],
			"X": data.values[:, 3:],
			"edge_index": edge_index,
			"edge_weight": edge_weight,
			"labels": data.values[:, 2],
			"original_index": original_index,
			"mask": torch.ones(data.shape[0], dtype=torch.bool),
			"is_reversed": False
			# "columns": columns
		}
		if self.ref_node is not None:
			self.append_ref_node(self.ref_node)

	def set_pred_proba(self):
		X, edge_index, _, original_index, mask, edge_weight = self.get_graph()
		features_origin, features_time = self.framework.get_features(X, edge_index.type(torch.long), edge_weight, mask)
		combined_features = torch.cat([features_origin.detach().cpu(), features_time.detach().cpu()], dim=-1)
		if self.standard_scaler is not None:
			combined_features = self.standard_scaler.transform(combined_features)
		self.pred_proba = self.model.predict_proba(combined_features)[original_index, 1]

	def get_graph(self):
		return self.graph["X"], self.graph["edge_index"], self.graph["labels"], self.graph["original_index"], \
			self.graph["mask"], self.graph["edge_weight"]

	def get_features_list(self):
		X, edge_index, _, original_index, mask, edge_weight = self.get_graph()
		return list(map(lambda features: features[original_index, :].cpu(),
						self.framework.get_features(X, edge_index.type(torch.long), edge_weight, mask)))

	def get_pred_proba(self):
		return self.pred_proba

	def get_prediction(self):
		return self.get_pred_proba() >= self.threshold

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


