import torch
from sklearn.base import BaseEstimator
from typing import TypedDict
import numpy as np
import numpy
from sklearn.base import clone
from sklearn.model_selection import GridSearchCV

USER_FUNCTIONS = {
    'sum': lambda origin_features, updated_features, sum_neighbors, mul_neighbors, num_neighbors: sum_neighbors,
    'mean': lambda origin_features, updated_features, sum_neighbors, mul_neighbors,
                   num_neighbors: sum_neighbors / num_neighbors,
    'diff_of_origin_mean': lambda origin_features, updated_features, sum_neighbors, mul_neighbors,
                                  num_neighbors: origin_features - sum_neighbors / num_neighbors,
    'diff_of_updated_mean': lambda origin_features, updated_features, sum_neighbors, mul_neighbors,
                                   num_neighbors: updated_features - sum_neighbors / num_neighbors,
    'sum_of_origin_mean': lambda origin_features, updated_features, sum_neighbors, mul_neighbors,
                                 num_neighbors: origin_features + sum_neighbors / num_neighbors,
    'sum_of_updated_mean': lambda origin_features, updated_features, sum_neighbors, mul_neighbors,
                                  num_neighbors: updated_features + sum_neighbors / num_neighbors,
}


## Assumption: the overall prediction perf improved when the performance of inidividual predictiors improves
##TODO More input_validation, grid search method whoch accepts the same params
class Framework:

    def __init__(self, user_functions,
                 hops_list: list[int],
                 clfs: list,
                 multi_target_class: bool = False,
                 gpu_idx: int | None = None,
                 handle_nan: float | None = None,
                 attention_configs: list = []) -> None:
        self.user_functions = user_functions
        self.hops_list: list[int] = hops_list
        self.clfs: list[int] = clfs
        self.trained_clfs = None
        self.gpu_idx: int | None = gpu_idx
        self.handle_nan: float | int | None = handle_nan
        self.attention_configs = attention_configs
        self.multi_target_class = multi_target_class
        self.device: torch.DeviceObjType = torch.device(
            f"cuda:{str(self.gpu_idx)}") if self.gpu_idx is not None and torch.cuda.is_available() else torch.device(
            "cpu")

    def update_user_function(self):
        if self.user_function in USER_FUNCTIONS:
            self.user_function = USER_FUNCTIONS[self.user_function]
        else:
            raise Exception(
                f"Only the following string values are valid inputs for the user function: {[key for key in USER_FUNCTIONS]}. You can also specify your own function for aggregatioon.")

    def get_features(self,
                     X: torch.FloatTensor | numpy._typing.NDArray,
                     edge_index: torch.LongTensor | numpy._typing.NDArray,
                     mask: torch.BoolTensor | numpy._typing.NDArray,
                     is_training: bool = False) -> tuple[torch.FloatTensor, torch.FloatTensor]:
        if mask is None:
            mask = torch.ones(X.shape[0]).type(torch.bool)
        #         if isinstance(self.user_function, str):
        #             self.update_user_function()
        ## To tensor
        X = Framework.get_feature_tensor(X)
        edge_index = Framework.get_edge_index_tensor(edge_index)
        mask = Framework.get_mask_tensor(mask)

        ## To device
        X = self.shift_tensor_to_device(X)
        edge_index = self.shift_tensor_to_device(edge_index)
        mask = self.shift_tensor_to_device(mask)

        aggregated_train_features_list = []
        ## Aggregate
        for hop_idx in range(len(self.hops_list)):
            neighbor_features = self.aggregate(X, edge_index, hop_idx, is_training)
            aggregated_train_features_list.append(neighbor_features[mask])
        return aggregated_train_features_list

    def feature_aggregations(self, features, target, source_lift):
        summed_neighbors = torch.zeros_like(features, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(
            features.shape[1], 1).t(), source_lift, reduce="sum", include_self=False)
        multiplied_neighbors = torch.ones_like(features, device=self.device).scatter_reduce(0,
                                                                                            target.unsqueeze(0).repeat(
                                                                                                features.shape[1],
                                                                                                1).t(), source_lift,
                                                                                            reduce="prod",
                                                                                            include_self=False)
        mean_neighbors = torch.zeros_like(features, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(
            features.shape[1], 1).t(), source_lift, reduce="mean", include_self=False)
        max_neighbors = torch.zeros_like(features, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(
            features.shape[1], 1).t(), source_lift, reduce="amax", include_self=False)
        min_neighbors = torch.zeros_like(features, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(
            features.shape[1], 1).t(), source_lift, reduce="amin", include_self=False)
        return summed_neighbors, multiplied_neighbors, mean_neighbors, max_neighbors, min_neighbors

    def aggregate(self, X: torch.FloatTensor, edge_index: torch.LongTensor, hop_idx,
                  is_training: bool = False) -> torch.FloatTensor:
        original_features = X
        features_for_aggregation: torch.FloatTensor = torch.clone(X)
        hops_list = self.hops_list[hop_idx]
        for i, hop in enumerate(range(hops_list)):
            if self.attention_configs[hop_idx] and self.attention_configs[hop_idx]["inter_layer_normalize"]:
                features_for_aggregation = torch.nn.functional.normalize(features_for_aggregation, dim=0)
            source_lift = features_for_aggregation.index_select(0, edge_index[0])
            source_origin_lift = original_features.index_select(0, edge_index[0])
            target = edge_index[1]

            if self.attention_configs[hop_idx] and self.attention_configs[hop_idx]["use_pseudo_attention"]:
                source_lift = self.apply_attention_mechanism(source_lift, features_for_aggregation, target,
                                                             self.attention_configs[hop_idx], is_training)

            summed_neighbors, multiplied_neighbors, mean_neighbors, max_neighbors, min_neighbors = self.feature_aggregations(
                features_for_aggregation, target, source_lift)
            summed_origin_neighbors, multiplied_origin_neighbors, mean_origin_neighbors, max_origin_neighbors, min_origin_neighbors = self.feature_aggregations(
                original_features, target, source_origin_lift)
            # summed_neighbors = torch.zeros_like(features_for_aggregation, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(features_for_aggregation.shape[1], 1).t(), source_lift, reduce="sum", include_self = False)
            # multiplied_neighbors = torch.ones_like(features_for_aggregation, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(features_for_aggregation.shape[1], 1).t(), source_lift, reduce="prod", include_self = False)
            # mean_neighbors = torch.zeros_like(features_for_aggregation, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(features_for_aggregation.shape[1], 1).t(), source_lift, reduce="mean", include_self = False)
            # max_neighbors = torch.zeros_like(features_for_aggregation, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(features_for_aggregation.shape[1], 1).t(), source_lift, reduce="amax", include_self = False)
            # min_neighbors = torch.zeros_like(features_for_aggregation, device=self.device).scatter_reduce(0, target.unsqueeze(0).repeat(features_for_aggregation.shape[1], 1).t(), source_lift, reduce="amin", include_self = False)

            num_source_neighbors = torch.zeros(features_for_aggregation.shape[0], dtype=torch.float, device=self.device)
            num_source_neighbors.scatter_reduce(0, target,
                                                torch.ones_like(target, dtype=torch.float, device=self.device),
                                                reduce="sum", include_self=False)
            num_source_neighbors = num_source_neighbors.unsqueeze(-1)

            user_function = self.user_functions[hop_idx]
            updated_features = features_for_aggregation  ## just renaming so that the key in the user function is clear
            user_function_kwargs = {
                'original_features': original_features,
                'updated_features': updated_features,
                'summed_neighbors': summed_neighbors,
                'multiplied_neighbors': multiplied_neighbors,
                'mean_neighbors': mean_neighbors,
                'max_neighbors': max_neighbors,
                'min_neighbors': min_neighbors,
                'summed_origin_neighbors': summed_origin_neighbors,
                'multiplied_origin_neighbors': multiplied_origin_neighbors,
                'mean_origin_neighbors': mean_origin_neighbors,
                'max_origin_neighbors': max_origin_neighbors,
                'min_origin_neighbors': min_origin_neighbors,
                'num_source_neighbors': num_source_neighbors,
                'hop': hop}
            out = user_function(user_function_kwargs)

            if self.handle_nan is not None:
                out = torch.nan_to_num(out, nan=self.handle_nan)
            features_for_aggregation = out
        return features_for_aggregation

    def apply_attention_mechanism(self, source_lift: torch.FloatTensor,
                                  features_for_aggregation: torch.FloatTensor,
                                  target: torch.LongTensor,
                                  attention_config,
                                  is_training: bool = False) -> torch.FloatTensor:
        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        score = cos(source_lift, features_for_aggregation.index_select(0, target))
        dropout_tens = None

        origin_scores = torch.clone(score)
        if attention_config["cosine_eps"]:
            score[score < attention_config["cosine_eps"]] = -torch.inf
        if attention_config["dropout_attn"] is not None and is_training:
            dropout_tens = torch.FloatTensor(score.shape[0]).uniform_(0, 1)
            score[dropout_tens < attention_config["dropout_attn"]] = -torch.inf
        exp_score = torch.exp(score)
        summed_exp_score = torch.zeros_like(exp_score).scatter(0, target, exp_score, reduce="add")
        target_lifted_summed_exp_score = summed_exp_score.index_select(0, target)
        normalized_scores = exp_score / target_lifted_summed_exp_score
        source_lift = normalized_scores.unsqueeze(1) * source_lift
        return source_lift

    def fit(self,
            X_train: torch.FloatTensor | numpy._typing.NDArray,
            edge_index: torch.LongTensor | numpy._typing.NDArray,
            y_train: torch.LongTensor | numpy._typing.NDArray,
            train_mask: torch.BoolTensor | numpy._typing.NDArray | None,
            kwargs_fit_list=None,
            transform_kwargs_fit=None,
            kwargs_multi_clf_list=None
            ) -> BaseEstimator:
        if train_mask is None:
            train_mask = torch.ones(X_train.shape[0]).type(torch.bool)

        y_train = Framework.get_label_tensor(y_train)
        y_train = y_train[train_mask]

        self.validate_input()

        aggregated_train_features_list = self.get_features(X_train, edge_index, train_mask, True)

        trained_clfs = []
        for i, aggregated_train_features in enumerate(aggregated_train_features_list):
            clf = clone(self.clfs[i])
            if self.multi_target_class:
                kwargs_multi_clf = kwargs_multi_clf_list[i] if kwargs_multi_clf_list and len(
                    kwargs_multi_clf_list) > i is not None else {}
                clf = MultiOutputClassifier(clf, **kwargs_multi_clf)
            kwargs = kwargs_fit_list[i] if kwargs_fit_list and len(kwargs_fit_list) > i is not None else {}
            transformed_kwargs = transform_kwargs_fit(self, kwargs, i) if transform_kwargs_fit is not None else kwargs
            clf.fit(aggregated_train_features.cpu().numpy(), y_train, **transformed_kwargs)
            trained_clfs.append(clf)
        self.trained_clfs = trained_clfs
        return trained_clfs

    def predict_proba(self, X_test: torch.FloatTensor | numpy._typing.NDArray,
                      edge_index: torch.LongTensor | numpy._typing.NDArray,
                      test_mask: torch.BoolTensor | numpy._typing.NDArray | None,
                      weights=None,
                      kwargs_list=None):
        if test_mask is None:
            test_mask = torch.ones(X_test.shape[0]).type(torch.bool)
        aggregated_test_features_list = self.get_features(X_test, edge_index, test_mask)

        pred_probas = []
        for i, clf in enumerate(self.trained_clfs):
            aggregated_test_features = aggregated_test_features_list[i]
            kwargs = kwargs_list[i] if kwargs_list is not None else {}
            pred_proba = clf.predict_proba(aggregated_test_features.cpu().numpy(),
                                           **kwargs) if kwargs else clf.predict_proba(
                aggregated_test_features.cpu().numpy())
            pred_probas.append(pred_proba)
        final_pred_proba = np.average(np.asarray(pred_probas), weights=weights, axis=0)
        return final_pred_proba

    def predict(self,
                X_test: torch.FloatTensor | numpy._typing.NDArray,
                edge_index: torch.LongTensor | numpy._typing.NDArray,
                test_mask: torch.BoolTensor | numpy._typing.NDArray | None,
                weights=None,
                kwargs_list=None):
        return self.predict_proba(X_test, edge_index, test_mask, weights, kwargs_list).argmax(1)

    def validate_input(self):
        pass

    @staticmethod
    def get_feature_tensor(X: torch.FloatTensor | numpy._typing.NDArray) -> torch.FloatTensor | None:
        if not torch.is_tensor(X):
            try:
                return torch.from_numpy(X).type(torch.float)
            except:
                raise Exception("Features input X must be numpy array or torch tensor!")
                return None
        return X

    @staticmethod
    def get_label_tensor(y: torch.LongTensor | numpy._typing.NDArray) -> torch.LongTensor | None:
        if not torch.is_tensor(y):
            try:
                return torch.from_numpy(y).type(torch.long)
            except:
                raise Exception("Label input y must be numpy array or torch tensor!")
                return None
        return y

    @staticmethod
    def get_mask_tensor(mask: torch.BoolTensor | numpy._typing.NDArray) -> torch.BoolTensor | None:
        if not torch.is_tensor(mask):
            try:
                return torch.from_numpy(mask).type(torch.bool)
            except:
                raise Exception("Input mask must be numpy array or torch tensor!")
                return None
        return mask

    @staticmethod
    def get_edge_index_tensor(edge_index: torch.LongTensor | numpy._typing.NDArray) -> torch.LongTensor | None:
        if not torch.is_tensor(edge_index):
            try:
                edge_index = torch.from_numpy(edge_index).type(torch.long)
                Framework.validate_edge_index(edge_index)
                return edge_index
            except:
                raise Exception("Edge index must be numpy array or torch tensor")
                return None
        return edge_index

    @staticmethod
    def validate_edge_index(edge_index: torch.LongTensor) -> None:
        if edge_index.shape[0] != 2:
            raise Exception("Edge index must have the shape 2 x NumberOfEdges")
            # TODO: check max edge index and shape of features

    def shift_tensor_to_device(self,
                               t: torch.FloatTensor) -> torch.FloatTensor:
        if self.gpu_idx is not None:
            return t.to(self.device)
        return t

    def validate_grid_input(self, grid_params):
        if len(grid_params) != 1 and self.use_feature_based_aggregation:
            raise Exception("You need to provide grid parameter for the classifier!")
        if len(grid_params) != 2 and not self.use_feature_based_aggregation:
            raise Exception("You need to provide two grid parameter, one for each classifier!")
        return

    def hyper_param_tuning(spaces, objectives, n_iter, X_train, y_train, X_val, y_val):
        ## bayes optim
        pass