import os
import shap
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Union
from stepshifter3.stepshifter import StepShifter
from stepshifter3.logger import AppLogger
from typing import Optional


class Report():
    """
    A class to represent a Report.
    """
    def __init__(self, stepshifter: StepShifter, X: pd.DataFrame, y: Union[pd.DataFrame, pd.Series], logger: Optional[AppLogger] = None):
        """
        Initialize the Report.

        Arguments:
            stepshifter: The stepshifter object for which we would like to explain/interpret the trained models (StepShifter).
            X: The features (training data) (Pandas DataFrame).
            y: The target (training data) (Pandas DataFrame or Series).

        Attributes:
            X: The features (training data) (Pandas DataFrame).
            y: The target (training data) (Pandas DataFrame or Series).
            shap: SHAP values (Dict).
            X_corr: The correlation matrix (Pandas DataFrame).
            feature_importance: The feature importance (Dict).
            models: The trained models, extracted from the stepshifter object (Dict).
            ID_columns: The ID columns, extracted from the stepshifter object (List).
            estimator: The estimator, extracted from the stepshifter object (sklearn-compatible estimator).
            target_column: The target column, extracted from the stepshifter object (str).
        """
        self.X = X
        self.y = y
        self.shap = None
        self.X_corr = None
        self.feature_importance = None
        self.models = stepshifter.models
        self.ID_columns = stepshifter.ID_columns
        self.estimator = stepshifter.base_estimator
        self.target_column = stepshifter.target_column

        if logger is None:
            self.logger = AppLogger(name=__name__).get_logger()
        else:
            self.logger = logger.get_logger()

    def calculate_metrics(self, shap: bool = True, X_corr: bool = True, feature_importance: bool = True):
        """
        Calculate the metrics.

        Arguments:
            shap: Whether or not the shap values should be calculated (bool). Default is True.
            X_corr: Whether the correlation matrix should be calculated (bool). Default is True.
            feature_importance: Whether the feature importance should be calculated (bool). Default is True.

        Returns:
            None
        """
        # If X contains the ID columns or the target column, drop them
        # If X does not contain any of these columns, do nothing
        try:
            self.X.drop(columns=self.ID_columns, inplace=True)
            self.logger.info("Dropped ID columns")
        except KeyError:
            pass

        try:
            self.X.drop(columns=self.target_column, inplace=True)
            self.logger.info("Dropped target column")
        except KeyError:
            self.logger.error("Target column not found in X")
            pass

        # Calculate the relevant metrics if they haven't been calculated yet
        if shap and self.shap is None:
            self.calculate_shap_values()
        if X_corr and self.X_corr is None:
            self.calculate_correlation_matrix()
        if feature_importance and self.feature_importance is None:
            self.calculate_feature_importance()

    def calculate_shap_values(self):
        """
        Calculate the shap values for all models.

        Arguments:
            None

        Returns:
            None
        """
        shap_values_dict = {}
        for s in self.models.keys():
            shap_values_dict[s] = self.calculate_shap_values_for_model(s)
        self.shap = shap_values_dict

    def calculate_shap_values_for_model(self, s: int) -> np.ndarray:
        """
        Calculate the shap values for a specific model.

        Arguments:
            s: Model number & the number of months into the future the model predicts (int)

        Returns:
            np.ndarray: The shap values for the specified model.
        """
        explainer = shap.TreeExplainer(self.models[s])
        shap_values = explainer.shap_values(self.X)

        return shap_values

    def calculate_correlation_matrix(self):
        """
        Calculate the correlation matrix.

        Arguments:
            None

        Returns:
            None
        """
        df = self.X.copy()
        self.X_corr = df.corr().round(2)

    def calculate_feature_importance(self):
        """
        Calculate the feature importance for all models.

        Arguments:
            None

        Returns:
            None
        """
        feature_importances_dict = {}
        for s in self.models.keys():
            feature_importances_dict[s] = self.calculate_feature_importance_for_model(s)

        self.feature_importance = feature_importances_dict

    def calculate_feature_importance_for_model(self, s):
        """
        Calculate the feature importance for a specific model.

        Arguments:
            s: Model number & the number of months into the future the model predicts (int)

        Returns:
            Dict: The feature importance for the specified model.
        """
        feature_names = self.X.columns.tolist()
        importances = self.models[s].feature_importances_
        importances_dict = dict(zip(feature_names, importances))

        return importances_dict

    def visualize_metrics(self, save=False, destination_dir=None):
        """
        Visualize the metrics that have been calculated.

        Arguments:
            save: Whether or not to save the plots (bool).
            destination_dir: The destination directory to save the plots to (str).

        Returns:
            None
        """
        if self.X_corr is not None:
            self.visualize_correlation_matrix(save, destination_dir)
        if self.feature_importance is not None:
            self.visualize_feature_importance(save, destination_dir)
        if self.shap is not None:
            self.visualize_shap_values(save, destination_dir)

    def visualize_shap_values(self, save=False, destination_dir=None):
        """
        Visualize the shap values.

        Arguments:
            save: Whether or not to save the plots (bool).
            destination_dir: The destination directory to save the plots to (str).

        Returns:
            None
        """
        for model_name, shap_values in self.shap.items():
            shap.summary_plot(shap_values, self.X, show=False, plot_size=None)
            plt.title("Model " + str(model_name), y=0.98, fontsize=20, loc="left")
            if save:
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                individual_shap_file = destination_dir + f"shap_values_{model_name}.png"
                plt.savefig(individual_shap_file)
            else:
                plt.show()
            plt.close()

    def visualize_correlation_matrix(self, save=False, destination_dir=None):
        """
        Visualize the correlation matrix.

        Arguments:
            save: Whether or not to save the plots (bool).
            destination_dir: The destination directory to save the plots to (str).

        Returns:
            None
        """
        plt.figure(figsize=(12, 12))
        sns.heatmap(self.X_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        if save:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            plt.savefig(destination_dir + "correlation_matrix.png")
            plt.close()

        else:
            plt.show()

    def visualize_feature_importance(self, save=False, destination_dir=None):
        """
        Visualize the feature importances.

        Arguments:
            save: Whether or not to save the plots (bool).
            destination_dir: The destination directory to save the plots to (str).

        Returns:
            None
        """
        # Determine the number of models
        n_models = len(self.feature_importance.keys())

        # Set up the figure with appropriate number of subplots
        if n_models <= 3:
            n_cols = n_models
        else:
            n_cols = 4

        # Calculate required rows based on number of models
        n_rows = int(np.ceil(n_models / n_cols))

        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))

        # Handle edge case where there's only one row of plots
        if n_rows == 1:
            axs = np.expand_dims(axs, axis=0)

        for i, model_number in enumerate(self.feature_importance.keys()):
            row = i // n_cols
            col = i % n_cols

            importance_df = pd.DataFrame.from_dict(data=self.feature_importance[model_number],
                                                   orient='index',
                                                   columns=[f"Importance type: {self.estimator.importance_type}"])

            importance_df.plot.bar(title="Model for s = " + str(model_number), ax=axs[row, col])
            axs[row, col].set_ylabel(f"Importance type: {self.estimator.importance_type}")

        # If the number of models isn't a perfect multiple of n_cols, turn off any unused subplots
        for j in range(i+1, n_rows * n_cols):
            row = j // n_cols
            col = j % n_cols
            axs[row, col].axis('off')

        if save:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            plt.savefig(destination_dir + "feature_importance.png")
            plt.close()
        else:
            plt.tight_layout()
            plt.show()
