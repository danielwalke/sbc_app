import tensorflow as tf
from tensorflow import keras

import os
import tempfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

METRICS = [
    keras.metrics.TruePositives(name='tp'),
    keras.metrics.FalsePositives(name='fp'),
    keras.metrics.TrueNegatives(name='tn'),
    keras.metrics.FalseNegatives(name='fn'),
    keras.metrics.BinaryAccuracy(name='accuracy'),
    keras.metrics.Precision(name='precision'),
    keras.metrics.Recall(name='recall'),
    keras.metrics.AUC(name='auc'),
    keras.metrics.AUC(name='prc', curve='PR'),  # precision-recall curve
]
EPOCHS = 50
BATCH_SIZE = 4096

feature_columns = ["Age", "Sex", "HGB", "MCV", "PLT", "RBC", "WBC"]


class FeedForwardNeuralNetwork:

    def __init__(self, training, testing, testing_greifswald):
        train_df, val_df = train_test_split(training.get_data(), test_size=0.25)
        test_df = testing.get_data()
        test_df_greifswald = testing_greifswald.get_data()

        oversample = RandomOverSampler(random_state=42)
        undersample = RandomUnderSampler(sampling_strategy=0.5)

        train_df["Label"] = (train_df["Label"] == "Sepsis").astype(int)
        val_df["Label"] = (val_df["Label"] == "Sepsis").astype(int)
        test_df["Label"] = (test_df["Label"] == "Sepsis").astype(int)
        test_df_greifswald["Label"] = (test_df_greifswald["Label"] == "Sepsis").astype(int)

        train_features = train_df.loc[:, feature_columns].replace(to_replace='W', value=1).replace(to_replace='M',
                                                                                                        value=0)
        train_labels = train_df["Label"]

        x_train_ros, y_train_ros = oversample.fit_resample(train_features, train_labels)

        self.train_features = x_train_ros
        self.train_labels = y_train_ros

        self.val_features = val_df.loc[:, feature_columns].replace(to_replace='W', value=1).replace(to_replace='M',
                                                                                                    value=0)
        self.val_labels = val_df["Label"]

        self.test_features = testing.get_x()
        self.test_labels = test_df["Label"]

        self.test_greifswald_features = testing_greifswald.get_x()
        self.test_greifswald_labels = test_df_greifswald["Label"]

        # self.early_stopping = tf.keras.callbacks.EarlyStopping(
        #     monitor='val_prc',
        #     verbose=1,
        #     patience=10,
        #     mode='max',
        #     restore_best_weights=True)
        self.model = self.make_model()
        print(self.model.summary())

    def train(self):
        baseline_history = self.model.fit(
            self.train_features,
            self.train_labels,
            batch_size=BATCH_SIZE,
            epochs=EPOCHS,
            callbacks=[],#self.early_stopping
            validation_data=(self.val_features, self.val_labels))
        self.plot_metrics(baseline_history)

    def evaluate(self):
        # train_predictions_baseline = self.model.predict(self.train_features, batch_size=BATCH_SIZE)
        test_predictions_baseline = self.model.predict(self.test_features, batch_size=BATCH_SIZE)
        test_greifswald_predictions_baseline = self.model.predict(self.test_greifswald_features, batch_size=BATCH_SIZE)
        baseline_results = self.model.evaluate(self.test_features, self.test_labels,
                                               batch_size=BATCH_SIZE, verbose=0)
        baseline_greifwald_results = self.model.evaluate(self.test_greifswald_features, self.test_greifswald_labels,
                                               batch_size=BATCH_SIZE, verbose=0)
        for name, value in zip(self.model.metrics_names, baseline_results):
            print(name, ': ', value)
        print()
        for name, value in zip(self.model.metrics_names, baseline_greifwald_results):
            print(name, ': ', value)

        self.plot_cm(self.test_labels, test_predictions_baseline)
        self.plot_cm(self.test_greifswald_labels, test_greifswald_predictions_baseline)

    def make_model(self, metrics=METRICS):
        created_model = keras.Sequential([
            keras.layers.Dense(
                32, activation='relu',
                input_shape=(self.train_features.shape[-1],)),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dense(1, activation='sigmoid'),
        ])

        created_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=1e-3),
            loss=keras.losses.BinaryCrossentropy(),
            metrics=metrics)

        return created_model

    def plot_metrics(self, history):
        metrics = ['loss', 'prc', 'precision', 'recall']
        for n, metric in enumerate(metrics):
            name = metric.replace("_", " ").capitalize()
            plt.subplot(2, 2, n + 1)
            plt.plot(history.epoch, history.history[metric], label='Train')
            plt.plot(history.epoch, history.history['val_' + metric], linestyle="--", label='Val')
            plt.xlabel('Epoch')
            plt.ylabel(name)
            if metric == 'loss':
                plt.ylim([0, plt.ylim()[1]])
            elif metric == 'auc':
                plt.ylim([0.8, 1])
            else:
                plt.ylim([0, 1])

            plt.legend()

    def plot_cm(self, labels, predictions, p=0.5):
        cm = confusion_matrix(labels, predictions > p)
        plt.figure(figsize=(5, 5))
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title('Confusion matrix @{:.2f}'.format(p))
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')

        print('Legitimate Transactions Detected (True Negatives): ', cm[0][0])
        print('Legitimate Transactions Incorrectly Detected (False Positives): ', cm[0][1])
        print('Fraudulent Transactions Missed (False Negatives): ', cm[1][0])
        print('Fraudulent Transactions Detected (True Positives): ', cm[1][1])
        print('Total Fraudulent Transactions: ', np.sum(cm[1]))
