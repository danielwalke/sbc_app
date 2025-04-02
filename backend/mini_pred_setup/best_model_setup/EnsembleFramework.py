import torch
from sklearn.base import BaseEstimator
from typing import TypedDict
import numpy as np
import numpy
from sklearn.base import clone
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.manifold import TSNE
from sklearn.inspection import PartialDependenceDisplay
from sklearn.inspection import permutation_importance
from torch.nn.functional import normalize


def norm_user_function(kwargs):
    return normalize(kwargs["original_features"] + kwargs["summed_neighbors"], p=2.0, dim=1)


def user_function(kwargs):
    return kwargs["original_features"] + kwargs["summed_neighbors"]


def mean_function(kwargs):
    return kwargs["original_features"] + kwargs["mean_neighbors"]


def target_plus_mean_function(kwargs):
    return kwargs["original_features"] + kwargs["mean_neighbors"]


def mean_function(kwargs):
    return kwargs["original_features"] + kwargs["mean_neighbors"]


def sum_function(kwargs):
    return kwargs["summed_neighbors"]


## Pre-implemented aggregation functions
USER_FUNCTIONS = {
    'sum': sum_function,
    'mean': mean_function,
    'target_plus_sum': user_function,
    'normalized_target_plus_sum': norm_user_function,
    'target_plus_mean': target_plus_mean_function
}


def softmax(x):
    """
    This function calculates the softmax of an array, i.e., e^x/(sum(e^x))
    """
    e_coef = np.exp(x)
    softmax_coef = e_coef / np.sum(e_coef)
    return softmax_coef


class Framework:
    """
    Framework object is used to make classical machine learning algorithms like logistic regression or XGBoost graph-aware, i.e., by aggregating different
    orders of neighborhood the algorithms are capable of analyzing graph strcutured data citation network or protein-protein interaction networks.

    Parameters
    ----------
    hops_list: list[int]
        List of integers that represent the order of neighrbohood that should be aggregated for each instance in the ensemble
        Example: [0, 2]
    user_functions : list[def] or list[str]
        List of functions that represent the aggregation executed for each order of neighborhood, i.e., the i-th order of neighborhood provided in hops-list is
        aggregated with the i-th aggregation scheme in user_functions
        Or list of strings where the string is either sum, mean, target_plus_sum, normalized_target_plus_sum, target_plus_mean
        Example: [lambda kwargs: kwargs["original_features"] + kwargs["mean_neighbors"], kwargs["original_features"] + kwargs["mean_neighbors"]]
    clfs: list[classifierInstance]
        List of classifier instances from scikit-learn or XGBoost library, i.e., the i-th order of neighborhood provided in hops-list is aggregated with the i-
        th aggregation scheme in user_functions and the output is passed to the classifiers .fit() function
        Example: [sklearn.linear_model.LogisticRegression(), sklearn.linear_model.LogisticRegression()]
    multi_target_class: Boolean
        Optional boolean value that represents whether we want to predict multiple targets, e.g., instead of a single output we want a list of outputs like in
        the protein-protein interaction tasks containing a label with 121 dimensions (https://pytorch-
        geometric.readthedocs.io/en/latest/generated/torch_geometric.datasets.PPI.html)
        Example/Default: False
    gpu_idx: Union[int, None]
        Optional represents either the integer of the cuda-compatible GPU we can use for the aggregation. If there is no cuda-compatible GPU (i.e, None), the
        execution is done on the CPU
        Example/Default: None
        handle_nan: Union[float, None]
        Optional float value which is used to replace nan values in case somewhere is a division by 0 or multiplication with inf or -inf
        Example/Default: None
    attention_configs: list[dict()]
        Optional list of dictionaries used for calculating the influence score and setting a threshold for similarity
        Example: [
        {'inter_layer_normalize': False, ##Boolean whether to normalize values aftetr each aggregation
        'use_pseudo_attention': True, ##Boolean whether to apply cosine-similarity based weighting on neighbors
        'cosine_eps': 0.01, ##Float-threshold to filter out nodes with to low similarity
        'dropout_attn': None} ##Float or None - Dropout of edges for training to filter out edges
        ]
    Attributes
    ----------
    hops_list: list[int]
    user_functions : list[def]
    clfs: list[classifierInstance]
    trained_clfs: list[classifierInstance]
        Will store the final trained classifiers
    multi_target_class: Boolean
    gpu_idx: Union[int, None]
    device: Device used for the aggregations
    handle_nan: Union[float, None]
    attention_configs: list[dict()]
    dataset: dict
        Dataset required for calculationg feature importance in the case that there are no direct feature importance of coefficients atatched to the classifier
        dict with features in key "X", edge index in key "edge_index" and labels in key "y", boolean mask under "mask"
    """

    def __init__(self,
                 hops_list,
                 user_functions,
                 clfs: list,
                 multi_target_class: bool = False,
                 gpu_idx=None,
                 handle_nan=None,
                 attention_configs=[],
                 classifier_on_device=False) -> None:
        self.user_functions = user_functions
        self.hops_list = hops_list
        self.clfs = clfs
        self.trained_clfs = None
        self.gpu_idx = gpu_idx
        self.handle_nan = handle_nan
        self.attention_configs = attention_configs
        self.multi_target_class = multi_target_class
        self.device: torch.DeviceObjType = torch.device(
            f"cuda:{str(self.gpu_idx)}") if self.gpu_idx is not None and torch.cuda.is_available() else torch.device(
            "cpu")
        self.num_classes = None
        self.dataset = None
        self.multi_out = None
        self.classifier_on_device = classifier_on_device

    def update_user_function(self, user_function):
        """
        This function updates the user function, i.e, if someone provided a string the function for this string is returned
        Parameters
        ----------
        user_function :str
            String for an aggregation function from the list of Strings in USER_FUNCTIONS
        Returns
        ----------
        user_function :def
            Function for aggregation
        """
        if user_function in USER_FUNCTIONS:
            user_function = USER_FUNCTIONS[user_function]
        else:
            raise Exception(
                f"Only the following string values are valid inputs for the user function: {[key for key in USER_FUNCTIONS]}. You can also specify your own function for aggregatioon.")
        return user_function

    def get_features(self,
                     X,
                     edge_index: torch.LongTensor,
                     mask: torch.BoolTensor,
                     is_training: bool = False) -> tuple[torch.FloatTensor, torch.FloatTensor]:
        """
        This function aggregates the features to get the graph-aware feature sets, i.e., it will return a list of features with the length equal to the number
        of neighrbors we want to aggregate
        E.g., When we want to aggregate neighbors of the 0th and 2nd order it will return a list of length with features aggregated from the 0-th and from the
        2nd order
        Parameters
        ----------
        X :torch.Tensor with shape [Number of Nodes, Number of features]
            Original features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index for the feature aggregation in the COO format
        mask: torch.BoolTensor with shape [Number of Nodes]
            Boolean mask for only returning a subset of nodes (e.g., training nodes)
        is_training: Boolean
            Indicates whether the features are calculated for training
        Returns
        ----------
        aggregated_train_features_list: list[torch.Tensor] where each tensor has the shape [Number of Nodes, Number of features]
            List of torch tensor where the i-th tensor resulting from the aggregation of the i-th neighborhood provided in hops_list with the i-th aggregation
            function provided in user_functions
        """
        if mask is None:
            mask = torch.ones(X.shape[0]).type(torch.bool)

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
        """
        This function performs the feature aggregation on the source nodes indexed on the edge index
        Parameters
        ----------
        features :torch.Tensor with shape [Number of Nodes, Number of features]
            Original features without aggregation
        target: torch.LongTensor shape [1, Number of Edges]
            Target index of all edges for the feature aggregation
        source_lift: torch.Tensor with shape [Number of Edges, Number of features]
            Node features lifted on the source edge index
        Returns
        ----------
        summed_neighbors: torch.Tensor with shape [Number of Nodes, Number of features]
            Summed features from the source neighbors
        multiplied_neighbors: torch.Tensor with shape [Number of Nodes, Number of features]
            Multiplied features from the source neighbors
        mean_neighbors: torch.Tensor with shape [Number of Nodes, Number of features]
            Averaged features from the source neighbors
        max_neighbors: torch.Tensor with shape [Number of Nodes, Number of features]
            Maximum features from the source neighbors
        min_neighbors: torch.Tensor with shape [Number of Nodes, Number of features]
            Minimum features from the source neighbors
        """
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

    def aggregate(self, X, edge_index, hop_idx, is_training=False):
        """
        This function performs the iterative feature aggregation for each hop (order of neighborhood) and aggregation function requested for the i-th index and returns the aggregated features
        Parameters
        ----------
        X :torch.Tensor with shape [Number of Nodes, Number of features]
            Original features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index of all edges in the COO format
        hop_idx: int
            Index that specifies the i for the i-th feature aggregation
        is_training: Boolean
            Boolean value whether the aggregation is for trainign or testing
        Returns
        ----------
        features_for_aggregation: torch.Tensor with shape [Number of Nodes, Number of features]
            Aggregated features according to the i-th entry in the order of neighborhood (hops_list) and the i-th aggregation scheme (user_function)
        """
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

            num_source_neighbors = torch.zeros(features_for_aggregation.shape[0], dtype=torch.float, device=self.device)
            num_source_neighbors.scatter_reduce(0, target,
                                                torch.ones_like(target, dtype=torch.float, device=self.device),
                                                reduce="sum", include_self=False)
            num_source_neighbors = num_source_neighbors.unsqueeze(-1)

            user_function = self.user_functions[hop_idx]
            if isinstance(user_function, str):
                user_function = self.update_user_function(user_function)
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

    def apply_attention_mechanism(self,
                                  source_lift,
                                  features_for_aggregation,
                                  target,
                                  attention_config,
                                  is_training: bool = False):
        """
        This function applies the weightinig based on the consine similarity, i.e., more similar neighbors get higher weights than dissimilar ones
        Parameters
        ----------
        source_lift :torch.Tensor with shape [Number of Edges, Number of features]
            Node features lifted on the source edge index
        features_for_aggregation: torch.Tensor with shape [Number of Nodes, Number of features]
            Aggregated node features
        target: torch.LongTensor shape [1, Number of Edges]
            Target index of all edges for the feature aggregation
        attention_config: dict
            dictionary used for calculating the influence score and setting a threshold for similarity
            Example:
                {'inter_layer_normalize': False, ##Boolean whether to normalize values aftetr each aggregation
                'use_pseudo_attention': True, ##Boolean whether to apply cosine-similarity based weighting on neighbors
                'cosine_eps': 0.01, ##Float-threshold to filter out nodes with to low similarity
                'dropout_attn': None} ##Float or None - Dropout of edges for training to filter out edges
        is_training: Boolean
            Boolean value whether the aggregation is for trainign or testing
        Returns
        ----------
        features_for_aggregation: torch.Tensor with shape [Number of Nodes, Number of features]
            Aggregated features according to the i-th entry in the order of neighborhood (hops_list) and the i-th aggregation scheme (user_function)
        """
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
            X_train,
            edge_index,
            y_train,
            train_mask=None,
            kwargs_fit_list=None,
            transform_kwargs_fit=None,
            kwargs_multi_clf_list=None
            ):
        """
        This function fits the classifiers to aggregated features
        Parameters
        ----------
        X_train :torch.FloatTensor with shape [Number of Nodes, Number of features]
            Original train features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index of all edges in the COO format
        y_train: torch.LongTensor with shape [Number of Nodes, Number of Labels/tasks]
            Original train labels
        train_mask: torch.BoolTensor with shape [Number of Nodes] or None
            optional boolean mask for training
            If none all features and labels from X_train and y_train are used
        kwargs_fit_list: list[kwargs]
            optional list of kwargs passed to the sklearn or XGBoost estimators .fit() function
        transform_kwargs_fit: list[def]
            optional list of functions that transform the kwargs before passing them to .fit() function
            Functions has the framework instance as argument, the kwargs that should be transformed, and the current index of the aggregation
        kwargs_multi_clf_list: list[kwargs]
            optional list of kwargs that are directly passed to the MultiOutputClassifier in the case of a multi output/task prediction
        Returns
        ----------
        trained_clfs: list[]
            List of trained sklearn or XGBoost estimators
        """
        if train_mask is None:
            train_mask = torch.ones(X_train.shape[0]).type(torch.bool)

        y_train = Framework.get_label_tensor(y_train)
        y_train = y_train[train_mask]
        self.num_classes = len(y_train.unique(return_counts=True)[0])
        self.multi_out = y_train.shape[-1]

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
            if self.classifier_on_device:
                clf.fit(aggregated_train_features, y_train.to(self.device), **transformed_kwargs)
            else:
                clf.fit(aggregated_train_features.cpu().numpy(), y_train.numpy(), **transformed_kwargs)
            trained_clfs.append(clf)
        self.trained_clfs = trained_clfs
        return trained_clfs

    def predict_proba(self,
                      X_test,
                      edge_index,
                      test_mask=None,
                      weights=None,
                      kwargs_list=None):
        """
        This function return prediction probabilities for the fitted classifiers
        Parameters
        ----------
        X_test :torch.FloatTensor with shape [Number of Nodes, Number of features]
            Original test features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index of all edges in the COO format
        test_mask: torch.BoolTensor with shape [Number of Nodes] or None
            optional boolean mask for testing
            If none all features from X_test are used
        weights: list[float]
            optional list of weights to assign different weights to individual estimator instances in the ensemble
        kwargs_list: list[kwargs]
            list of kwargs that are driectly passed to the .predict_proba() function of the trained classifier, the i-th instance of the kwargs_list is passed
            to the i-th estimator
        Returns
        ----------
        final_pred_proba: np.array
            Return the resulting probability predictions
        """
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
        if self.multi_target_class:
            return np.transpose(final_pred_proba, axes=[1, 0, 2])
        return final_pred_proba

    def predict(self,
                X_test,
                edge_index,
                test_mask=None,
                weights=None,
                kwargs_list=None):
        """
        This function makes predictions with the fitted classifiers
        Parameters
        ----------
        X_test :torch.FloatTensor with shape [Number of Nodes, Number of features]
            Original test features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index of all edges in the COO format
        test_mask: torch.BoolTensor with shape [Number of Nodes] or None
            optional boolean mask for testing
            If none all features from X_test are used
        weights: list[float]
            optional list of weights to assign different weights to individual estimator instances in the ensemble
        kwargs_list: list[kwargs]
            list of kwargs that are driectly passed to the .predict_proba() function of the trained classifier, the i-th instance of the kwargs_list is passed
            to the i-th estimator
        Returns
        ----------
        pred_list: np.array
            Return the maximum argument of the resulting prediction probabilities
        """
        return self.predict_proba(X_test, edge_index, test_mask, weights, kwargs_list).argmax(-1)

    @staticmethod
    def get_feature_tensor(X):
        """
        Transforms numpy array in torch tensors if necessary
        Parameters
        ----------
        X: torch.Tensor or numpy.array
            features
        Raises
        ----------
        Exception
            Raises exception if input is neither numpy array nor torch tensor
        Returns
        ----------
        X: torch.Tensor
            features
        """
        if not torch.is_tensor(X):
            try:
                return torch.from_numpy(X).type(torch.float)
            except:
                raise Exception("Features input X must be numpy array or torch tensor!")
                return None
        return X

    @staticmethod
    def get_label_tensor(y):
        """
        Transforms numpy array in torch tensors if necessary
        Parameters
        ----------
        y: torch.Tensor or numpy.array
            labels
        Raises
        ----------
        Exception
            Raises exception if input is neither numpy array nor torch tensor
        Returns
        ----------
        y: torch.Tensor
            labels
        """
        if not torch.is_tensor(y):
            try:
                return torch.from_numpy(y).type(torch.long)
            except:
                raise Exception("Label input y must be numpy array or torch tensor!")
                return None
        return y

    @staticmethod
    def get_mask_tensor(mask):
        """
        Transforms numpy array in torch tensors if necessary
        Parameters
        ----------
        mask: torch.Tensor or numpy.array
            mask for masking nodes
        Raises
        ----------
        Exception
            Raises exception if input is neither numpy array nor torch tensor
        Returns
        ----------
        mask: torch.Tensor
            mask for masking nodes as tensor
        """
        if not torch.is_tensor(mask):
            try:
                return torch.from_numpy(mask).type(torch.bool)
            except:
                raise Exception("Input mask must be numpy array or torch tensor!")
                return None
        return mask

    @staticmethod
    def get_edge_index_tensor(edge_index):
        """
        Transforms numpy array in torch tensors if necessary
        Parameters
        ----------
        edge_index: torch.Tensor or numpy.array
            edge index in COO for the aggregation
        Raises
        ----------
        Exception
            Raises exception if input is neither numpy array nor torch tensor
        Returns
        ----------
        edge_index: torch.Tensor
            edge index in COO for the aggregation as troch tensor
        """
        if not torch.is_tensor(edge_index):
            try:
                edge_index = torch.from_numpy(edge_index).type(torch.long)
                return edge_index
            except:
                raise Exception("Edge index must be numpy array or torch tensor")
                return None
        return edge_index

    def shift_tensor_to_device(self,
                               t):
        """
        This function shifts data to the specified device
        Parameters
        ----------
        t: torch.tensor
            data
        Returns
        ----------
        t: torch.tensor
            data shifted to the specified device
        """
        if self.gpu_idx is not None:
            return t.to(self.device)
        return t

    def set_dataset(self, dataset):
        """
        This function is for setting a dataset for calculating the feature importance in the case that there is no default feature importance or coefficients
        attached to the classifiers
        Used for the permutation_importance calculation
        dict with features in key "X", edge index in key "edge_index" and labels in key "y", mask under "mask"
        """
        ## dict with features in key "X", edge index in key "edge_index" and labels in key "y", mask under "mask"
        self.dataset = dataset

    def feature_importance(self, n_repeats=10):
        """
        This function calculates the feature importance for individual features for the final predictions
        If neither feature importance nor coefficients are given, permutation importance is used
        Parameters
        ----------
        n_repeats: int
            Optional-Only used for permutation importance, number of repeats for calculating the permutation importance
        Returns
        ----------
        mean: np.array
            Calculated feature importances averaged over individual classifiers
        """
        framework = self
        num_classes = self.num_classes if not self.multi_target_class else self.multi_out
        if not num_classes: raise Exception("Not fitted yet")
        if self.multi_target_class:
            is_tree_clfs = all([hasattr(framework.trained_clfs[i].estimators_[0], 'feature_importances_') for i in
                                range(len(framework.trained_clfs))])
            if is_tree_clfs:
                return np.mean([np.mean([framework.trained_clfs[i].estimators_[class_idx].feature_importances_ for i in
                                         range(len(framework.trained_clfs))], axis=0) for class_idx in
                                range(num_classes)], axis=0)
            is_linear_clfs = all([hasattr(framework.trained_clfs[i].estimators_[0], 'coef_') for i in
                                  range(len(framework.trained_clfs))])
            if is_linear_clfs:
                return np.mean([softmax(np.mean(
                    [softmax(np.abs(framework.trained_clfs[i].estimators_[class_idx].coef_[0])) for i in
                     range(len(framework.trained_clfs))], axis=0)) for class_idx in range(num_classes)], axis=0)
            if self.dataset is None: raise Exception(
                "Dataset have to be set for calculating feature importance in non-tree-based or non-linear Classifiers")
            return np.mean([np.mean([permutation_importance(framework.trained_clfs[i].estimators_[class_idx],
                                                            framework.get_features(self.dataset["X"],
                                                                                   self.dataset["edge_index"],
                                                                                   self.dataset["mask"])[i].cpu(),
                                                            self.dataset["y"][self.dataset["mask"]][:, class_idx],
                                                            n_repeats=10,
                                                            random_state=0)["importances_mean"] for class_idx in
                                     range(num_classes)], axis=0) for i in range(len(framework.trained_clfs))], axis=0)
        if not self.multi_target_class:
            is_tree_clfs = all([hasattr(framework.trained_clfs[i], "feature_importances_") for i in
                                range(len(framework.trained_clfs))])
            if is_tree_clfs:
                return np.mean(
                    [framework.trained_clfs[i].feature_importances_ for i in range(len(framework.trained_clfs))],
                    axis=0)
            is_linear_clfs = all(
                [hasattr(framework.trained_clfs[i], "coef_") for i in range(len(framework.trained_clfs))])
            if is_linear_clfs:
                return softmax(
                    np.mean([np.abs(framework.trained_clfs[i].coef_) for i in range(len(framework.trained_clfs))],
                            axis=0))
        if self.dataset is None: raise Exception(
            "Dataset dict({'X':features, 'y':labels, 'edge_index':edge_index, 'mask':boolean-mask}) have to be set (set_dataset) for calculating feature importance in non-tree-based or non-linear Classifiers")
        return np.mean([permutation_importance(framework.trained_clfs[i], framework.get_features(self.dataset["X"],
                                                                                                 self.dataset[
                                                                                                     "edge_index"],
                                                                                                 self.dataset["mask"])[
            i].cpu(), self.dataset["y"][self.dataset["mask"]],
                                               n_repeats=n_repeats,
                                               random_state=0)["importances_mean"] for i in
                        range(len(framework.trained_clfs))], axis=0)

    def plot_feature_importances(self, fig_size=(30, 10), mark_top_n_peaks=3, which_grid="both", file_name=None,
                                 dpi=100, font_size=16):
        """
        This function plots the feature importance for the trained classifiers
        Parameters
        ----------
        fig_size: tuple(int,int)
            Optional figure size for the plot
        mark_top_n_peaks: int
            Optional number of peaks that should be highlighted (i.e., highlight the n most important features)
        which_grid: str (both, major or minor)
            Optional argument what grid should be used for plotting
        file_name: str
            Optional  filename for storing the plot
        dpi: int
            Optional for adopting the resolution of the plot
        font_size: int
            Optional for adopting the font size inn the plot
        Returns
        ----------
        plt: matplotlib.pyplot
            Return the resulting plot
        """
        y = self.feature_importance()
        x = np.arange(y.shape[0])
        peaks_idx = y.argsort()[::-1][:mark_top_n_peaks]
        fig, ax = plt.subplots(figsize=(fig_size))
        ax.bar(x, y)
        ax.set_ylabel("Relative Importance")
        ax.set_xlabel("Features")
        ax.set_xlim(0, y.shape[0])
        ax.scatter(x[peaks_idx], y[peaks_idx], c='red', marker='o')
        for i, peak in enumerate(peaks_idx):
            ax.annotate(f'{x[peak]:.0f}', (x[peak], y[peak]), textcoords="offset points", xytext=(0, 10), ha='center')
        if which_grid:
            ax.grid(visible=True, which=which_grid)
        ax.tick_params(axis='both', labelsize=font_size)
        plt.show()
        plt.draw()
        if file_name: fig.savefig(f"{file_name}.png", dpi=dpi, bbox_inches='tight')
        return plt

    def plot_tsne(self, X, edge_index, y, mask=None, label_to_color_map=None, fig_size=(12, 8), dpi=100, file_name=None,
                  font_size=16):
        """
        This function plots the t-SNE embedding of the prediction probabilities for individual classifiers
        Parameters
        ----------
        X :torch.FloatTensor with shape [Number of Nodes, Number of features]
            Original train features without aggregation
        edge_index: torch.LongTensor shape [2, Number of Edges]
            Edge index of all edges in the COO format
        y: torch.LongTensor with shape [Number of Nodes, Number of Labels/tasks]
            Original labels
        mask: torch.BoolTensor with shape [Number of Nodes] or None
            optional boolean mask for selecting only specific nodes
            If none all features and labels from X and y are used
        label_to_color_map: dict
            Dictionary for providing a specific color for the class
            Example: {0: "#42bcf5", 1: "#f54269"}
        fig_size: tuple(int,int)
            Optional figure size for the plot
        mark_top_n_peaks: int
            Optional number of peaks that should be highlighted (i.e., highlight the n most important features)
        file_name: str
            Optional  filename for storing the plot
        dpi: int
            Optional for adopting the resolution of the plot
        font_size: int
            Optional for adopting the font size inn the plot
        Raises:
            Exception if Visualization is currently nmot supported (i.e., multi label/task prediction)
        Returns
        ----------
        plt: matplotlib.pyplot
            Return the resulting plot
        """
        mask = torch.ones(X.shape[0]).type(torch.bool) if mask is None else mask
        scores = self.predict_proba(X, edge_index, mask)
        node_labels = y[mask].cpu().numpy()
        if self.multi_target_class or (self.num_classes == 2 and score.shape[-1] > 2): raise Exception(
            "Currently not supported for multi class prediction")

        num_classes = self.num_classes
        t_sne_embeddings = TSNE(n_components=2, perplexity=30, method='barnes_hut').fit_transform(scores)

        fig, ax = plt.subplots(figsize=fig_size, dpi=dpi)
        label_to_color_map = {i: (np.random.random(), np.random.random(), np.random.random()) for i in
                              range(num_classes)} if label_to_color_map is None else label_to_color_map
        for class_id in range(num_classes):
            ax.scatter(t_sne_embeddings[node_labels == class_id, 0], t_sne_embeddings[node_labels == class_id, 1], s=20,
                       color=label_to_color_map[class_id], edgecolors='black', linewidths=0.2)
        ax.legend(label_to_color_map.keys(), fontsize='large')
        ax.tick_params(axis='both', labelsize=font_size)
        plt.show()
        plt.draw()
        if file_name: fig.savefig(f"{file_name}.png", dpi=dpi, bbox_inches='tight')
        return plt