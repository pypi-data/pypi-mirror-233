import warnings
import pandas as pd
import mlflow
import os
import dask.dataframe as dd
import requests
import tqdm as tqdm
import subprocess
import dill as pickle
import io
import tempfile

from typing import Union, List, Optional, Dict, Tuple
from sklearn.base import BaseEstimator, clone
from stepshifter3.logger import AppLogger
from sklearn.model_selection import KFold
from dask_ml.model_selection import KFold as DaskKFold


class StepShifter(BaseEstimator):
    """
    Stepshifter3 is a general purpose stepshifting algorithm for tabular data based on Hegre et.al 2019.
    It is designed to be used with any scikit-learn compatible estimator for regular dataframes,
    and for most of the estimators in dask-ml for dask dataframes.
    It is further designed to be used with tabular data on dask and pandas dataframes.
    """

    def __init__(self, base_estimator, config: dict = None, logger: Optional[AppLogger] = None):
        """
        Initializes the StepShifter class.

        Arguments:
            base_estimator (object): The estimator to be used for training and prediction.
            config (dict): A dictionary containing the configuration for the model,
            see the example config file for more information.

        Returns:
            None
        """
        if config is None:
            raise ValueError("config must be a dictionary.")
        self.track_to_mlflow = False
        self.base_estimator = base_estimator  # The wrapped estimator, could be xgboost, sklearn, etc.
        self.S = config['S']
        self.ID_columns = config['ID_columns']
        self.mlflow_tracking_uri = config['mlflow_tracking_uri']
        self.metrics_report = config['metrics_report']
        self.mlflow_experiment_name = config['mlflow_experiment_name']
        self.mlflow_run_name = config['mlflow_run_name']
        self.target_column = config['target_column']
        self.predictions = None
        self.is_dask = config['is_dask']
        self.models = {}
        self.dask_client = config['dask_client']
        self.mlflow_process = None
        self._validate_params()

        if logger is None:
            self.logger = AppLogger(name=__name__).get_logger()
        else:
            self.logger = logger.get_logger()

    def _validate_params(self):
        """
        Validates the Arguments:.

        Arguments:
            None

        Returns:
            None
        """
        # Check that S is an integer
        if not isinstance(self.S, int):
            self.logger.error("S must be an integer.")
            raise ValueError("S must be an integer.")

        # Check that two ID_columns are privided:
        if len(self.ID_columns) != 2:
            raise ValueError("Two ID columns must be provided.")

    def end_mlflow_run(self):
        """
        Stops an mlflow run.

        Arguments:
            None

        Returns:
            None
        """
        if self.mlflow_run_name:
            mlflow.end_run()
        else:
            self.logger.info("No active MLflow run to stop.")

        self.logger.info("ended mlflow run")

    def set_new_mlflow_run(self, run_name: str):
        """
        Sets a new mlflow run.

        Arguments:
            run_name (str): The name of the new run.

        Returns:
            None
        """
        if self.mlflow_run_name:
            mlflow.end_run()
            self.mlflow_run_name = None
        mlflow.start_run(run_name=run_name)
        self.mlflow_run_name = mlflow.active_run()
        self.track_to_mlflow = True
        self.logger.info(f"started new mlflow run with run_id: {mlflow.active_run().info.run_id}")

    def set_new_mlflow_experiment(self, experiment_name: str):
        """
        Sets a new mlflow experiment.

        Arguments:
            experiment_name (str): The name of the new experiment.

        Returns:
            None
        """
        mlflow.set_experiment(experiment_name)
        self.mlflow_experiment_name = experiment_name
        self.track_to_mlflow = True
        self.logger.info(f"set new mlflow experiment with experiment_id: {mlflow.get_experiment_by_name(experiment_name).experiment_id}")

    def stop_mlflow(self):
        """
        Stops the mlflow run if it was started by start_mlflow method.

        Arguments:
            None

        Returns:
            None
        """
        if self.mlflow_process is not None:
            try:
                self.mlflow_process.terminate()
                self.mlflow_process.wait()
                self.logger.info("Stopped mlflow server.")
            except Exception as e:
                self.logger.error(f"Could not stop mlflow server, error: {e}")
                warnings.warn(f"Could not stop mlflow server, error: {e}")
            finally:
                self.mlflow_process = None
        else:
            self.logger.info("MLflow server was not started by this instance, cannot stop it.")

        self.track_to_mlflow = False
        self.mlflow_run_name = None
        self.mlflow_tracking_uri = None
        self.mlflow_experiment_name = None
        self.logger.info("Stopped mlflow tracking.")

    def start_mlflow(self):
        """
        Starts an mlflow run.

        Arguments:
            None

        Returns:
            None
        """

        # Check if the mlflow server is running:
        response = requests.get(self.mlflow_tracking_uri)

        if response.status_code == 200:
            self.logger.info("Status is 200 OK.")
        else:
            warnings.warn(f"Status is not 200 OK, but {response.status_code}, trying to start mlflow server, locally")
            try:
                # Open MLFlow as a subprocess:
                self.mlflow_process = subprocess.Popen(["mlflow", "server", "--host", "127.0.0.1:5000"])
                self.logger.info(f"mlflow tracking uri set to: {self.mlflow_tracking_uri}")
            except Exception as e:
                self.logger.error(f"Could not start mlflow server, error: {e}")
                mlflow.set_tracking_uri(self.mlflow_tracking_uri)
        # Set MLflow tracking to True
        self.track_to_mlflow = True
        self.logger.info(f"Started mlflow tracking, you can access the mlflow server at: {self.mlflow_tracking_uri}")

    @staticmethod
    def shift_target_partition(df: dd.DataFrame, shift_axis: str, target_column: str, s: int) -> dd.DataFrame:
        """
        Shifts the target column for a Dask DataFrame.

        Arguments:
            df (DataFrame): The Dask DataFrame to be used.
            shift_axis (str): The column to group by.
            target_column (str): The target column to shift.
            s (int): The number of steps to shift.

        Returns:
            df (Dask DataFrame): The shifted Dask DataFrame.
        """
        shifted = df.groupby(shift_axis)[target_column].shift(-s)
        return df.assign(**{target_column: shifted})

    def start_dask_client(self):
        """
        Starts a Dask client.

        Arguments:
            None

        Returns:
            None
        """
        self.dask_client.start_dask_client()

    def stop_dask_client(self):
        """
        Stops a Dask client.

        Arguments:
            None

        Returns:
            None
        """
        self.dask_client.stop_dask_client()

        # Verify that the client and cluster is stopped:
        if self.dask_client.client is None:
            self.logger.info("The dask client is stopped.")
        # else:
        #     raise warnings.warn("The dask client is not properly stopped.")

        if self.dask_client.cluster is None:
            self.logger.info("The dask cluster is stopped.")
        # else:
        #     raise warnings.warn("The dask cluster is not properly stopped.")

    import mlflow.sklearn

    def fit(self, X: Union[pd.DataFrame, dd.DataFrame], y: Union[pd.Series, dd.Series], tau_start: int, tau_end: int, fit_params: Optional[dict] = {}) -> None:
        """
        Fits the model.

        Arguments:
            X (DataFrame): The DataFrame to be used for training.
            y (Series): The target Series to be used for training.
            tau_start (int): The starting time id for the training period.
            tau_end (int): The ending time id for the training period.

        Returns:
            None
        """
        # Reappend y to X for shifting
        X[self.target_column] = y

        if self.is_dask:
            if self.dask_client.client is None:
                warnings.warn("The dask client is not running, please start the dask client for your session by calling the <your_stepshifter_instance>.start_dask_client() method.")

        # Start MLflow run if tracking is enabled
        if self.track_to_mlflow:
            mlflow.set_experiment(self.mlflow_experiment_name)
            mlflow.start_run(run_name=self.mlflow_run_name)

            self.logger.info(f"MLflow run started, with run_id{ mlflow.active_run().info.run_id}  and experiment_id: \
                              {mlflow.get_experiment_by_name(self.mlflow_experiment_name).experiment_id}")

        # Loop through steps
        for s in tqdm.tqdm(range(1, self.S + 1)):
            X_m, y_s = self.stepshifted(X, s, tau_start, tau_end)
            X_m = X_m.drop([self.ID_columns[0], self.ID_columns[1]], axis=1)  # Drop the ID columns before fitting

            model = clone(self.base_estimator)
            model.client = self.dask_client.client
            model.fit(X_m, y_s, **fit_params)

            # Store the fitted model
            self.models[s] = model
            # Log model to MLflow if tracking is enabled
            if self.track_to_mlflow:
                mlflow.sklearn.log_model(model, f"model_step_{s}")

    def _debug_verify_shifting(self, before_frame: dd.DataFrame, after_frame: dd.DataFrame) -> dd.DataFrame:
        """
        Verifies that the shifting is correct.

        Arguments:
            before_frame (DataFrame): The DataFrame before shifting.
            after_frame (DataFrame): The DataFrame after shifting.

        Returns:
            output (DataFrame): A DataFrame containing the before and after values for the target column.
        """
        # Check 1 id and print before/after_frame[target_column same dataframe]
        before_frame = before_frame[before_frame[self.ID_columns[1]] == 1]
        after_frame = after_frame[after_frame[self.ID_columns[1]] == 1]
        output = dd.concat([before_frame[self.target_column], after_frame[self.target_column]], axis=1)
        return output

    def predict(self, X: Union[pd.DataFrame, dd.DataFrame], tau_start: int, tau_end: int, steps_to_predict: Optional[List[int]] = None) -> List[List[float]]:
        """
        Generates predictions for the specified period.

        Arguments:
            X (DataFrame): The DataFrame to be used for prediction.
            tau_start (int): The starting time id for the prediction period.
            tau_end (int): The ending time id for the prediction period.
            steps_to_predict (List[int], optional): List of steps to generate predictions for. Defaults to all steps up to self.S.

        Returns:
            prediction_matrix (list): A list of lists containing the predictions for each step and time.
        """

        # If steps_to_predict is None, predict for all steps up to self.S
        if steps_to_predict is not None:
            # Check that the maximum step in steps_to_predict is not greater than self.S
            if max(steps_to_predict) > self.S:
                raise ValueError(f"The maximum value in steps_to_predict should be less than or equal to self.S ({self.S}).")
        else:
            steps_to_predict = list(range(1, self.S + 1))

        prediction_matrix = []

        for taus in tqdm.tqdm(range(tau_start, tau_end)):
            if self.is_dask:
                X_m = X[X[self.ID_columns[0]].between(taus, taus)]
            else:
                mask = (X[self.ID_columns[0]] >= tau_start) & (X[self.ID_columns[0]] <= tau_end)
                X_m = X[mask]

            identificators = [self.ID_columns[0], self.ID_columns[1], self.target_column]
            X_m = X_m.drop(identificators, axis=1, errors='ignore')

            # Replace the inner for loop
            predictions_for_step = [self.models[s].predict(X_m) for s in steps_to_predict]

            prediction_matrix.append(predictions_for_step)

        self.predictions = prediction_matrix

    def cross_validate_score(self, X: Union[pd.DataFrame, dd.DataFrame], y: Union[pd.Series, dd.Series], tau_start_val: int, tau_end_val: int, cv: int = 5) -> Dict:
        """
        Performs k-fold cross validation on all models.

        Arguments:
            X (Pandas or Dask DataFrame): The DataFrame to be used for cross validation.
            y (Pandas or Dask Series): The target Series to be used for cross validation.
            tau_start_val (int): The starting time for the validation period.
            tau_end_val (int): The ending time for the validation period.
            cv (int): The number of folds to use for cross validation.

        Returns:
            scores_dict (dict): A dictionary containing the scores for each model.
        """
        scores_dict = {}

        # Copying y to avoid modifying the original data
        y_start = y.copy()

        # Loop through steps
        for s in tqdm.tqdm(range(1, self.S + 1)):

            # Copying X to avoid modifying the original data
            X_m = X.copy()

            # Adding the target column if it is not present
            if self.target_column not in X_m.columns:
                X_m[self.target_column] = y_start

            # Shifting the target column
            X_m, y_s = self.stepshifted(X_m, s, tau_start_val, tau_end_val)

            # Dropping the ID columns
            X_m = X_m.drop([self.ID_columns[0], self.ID_columns[1]], axis=1)

            cv_results = []

            if self.is_dask:
                if self.dask_client.client is None:
                    warnings.warn("The dask client is not running, please start the dask client for your session by calling the <your_stepshifter_instance>.start_dask_client() method.")

                kf = DaskKFold(n_splits=cv)

                X_m = X_m.to_dask_array(lengths=True)
                y_s = y_s.to_dask_array(lengths=True)

                for train_index, test_index in kf.split(X_m):
                    X_train, X_test = X_m[train_index.compute()], X_m[test_index.compute()]
                    y_train, y_test = y_s[train_index.compute()], y_s[test_index.compute()]

                    model = clone(self.base_estimator)
                    model.client = self.dask_client.client
                    model.fit(X_train, y_train)

                    score = model.score(X_test, y_test)
                    cv_results.append(score)

            else:
                kf = KFold(n_splits=cv)

                X_m = X_m.to_numpy()
                y_s = y_s.to_numpy()

                for train_index, test_index in kf.split(X_m):
                    X_train, X_test = X_m[train_index], X_m[test_index]
                    y_train, y_test = y_s[train_index], y_s[test_index]

                    model = clone(self.base_estimator)
                    model.client = self.dask_client.client
                    model.fit(X_train, y_train)

                    score = model.score(X_test, y_test)
                    cv_results.append(score)

            scores_dict[s] = cv_results

        return scores_dict

    def pickle_predictions_to_mlflow(self):
        """
        Pickles the predictions to MLflow.

        Arguments:
            None

        Returns:
            None
        """
        try:
            # Here, you should ensure that self.mlflow_run_name is an mlflow Run object.
            if self.mlflow_run_name is None:
                self.logger.error("MLflow run has not been started or is improperly configured.")
                raise AttributeError("MLflow run has not been started or is improperly configured.")

            predictions_buffer = io.BytesIO()
            pickle.dump(self.predictions, predictions_buffer)
            predictions_buffer.seek(0)  # Reset buffer position to the beginning

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(predictions_buffer.getvalue())
                mlflow.log_artifact(tmp.name, "predictions.pkl")

            # Optionally delete the temporary file if you do not need it after logging
            os.remove(tmp.name)

        except AttributeError as ae:
            self.logger.error(f"AttributeError: {ae}")
            raise ae
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise e

    def get_model_for_step(self, step_number: int) -> BaseEstimator:
        """
        Retrieve the model for a given step number.

        Arguments:
            step_number (int): The step number to retrieve the model for.

        Returns:
            model (BaseEstimator): The model for the given step number.
        """
        return self.models[step_number]

    def validate_and_filter_data(self, df: Union[pd.DataFrame, dd.DataFrame],
                                 validation_range: List[int]) -> Tuple[Union[pd.DataFrame, dd.DataFrame], Union[pd.Series, dd.Series]]:
        """
        Validates and filters the DataFrame based on the validation_range.
        This function must be called before fit when using both pandas and dask dataframes.
        For Dask Dataframes the function repartitiones the data such that all relevant data for a given location is in the same partition.
        For Pandas DataFrames the function we check that all relevant data in the validation_range is present for each location.

        Arguments:
            df (DataFrame): The DataFrame to be validated and filtered.
            validation_range (list): A list containing the starting and ending time id for the validation period.

        Returns:
            X (DataFrame): The filtered DataFrame containing the features.
            y (Series): The filtered Series containing the target.
            is_dask (bool): Whether the DataFrame is a Dask DataFrame or not.
        """

        # Required time measurements based on validation_range (using set directly)
        required_time_measurements = set(range(validation_range[0], validation_range[1] + 1))

        # Based on df_type, proceed with validation and filtering
        if self.is_dask:
            self._check_for_dask_errors(df)
            df = self._adaptive_repartition(df)
        else:
            valid_locations = []
            for location, group in df.groupby(self.ID_columns[1]):
                if required_time_measurements.issubset(set(group[self.ID_columns[0]].unique())):
                    valid_locations.append(location)
            # Filter DataFrame based on valid_locations (directly, without new variable)
            df = df[df[self.ID_columns[1]].isin(valid_locations)]

        # Split into X and y (using inplace=True)
        y = df.pop(self.target_column)
        X = df  # Since we popped the target_column, what remains is X

        return X, y

    def stepshifted(self, df: Union[pd.DataFrame, dd.DataFrame], s: int, tau_start: int, tau_end: int) -> Union[pd.DataFrame, dd.DataFrame]:
        """
        Shifts the target column for a DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to be used.
            s (int): The number of steps to shift.
            tau_start (int): The starting time id for the training period.
            tau_end (int): The ending time id for the training period.

        Returns:
            df (DataFrame): The shifted DataFrame.
        """
        if self.is_dask:
            # Dask DataFrame logic
            # Shift the target feature s steps
            shift_axis = self.ID_columns[1]
            target_column = self.target_column
            dd_shifted = df.map_partitions(
                                transform_divisions=True,
                                func=self.shift_target_partition,
                                shift_axis=shift_axis,
                                target_column=target_column,
                                s=s,
            )
            # Slice the DataFrame to only include the data in time column range [tau_start, tau_end - s]
            df_sliced = dd_shifted[dd_shifted[self.ID_columns[0]].between(tau_start, tau_end - s)]
        else:
            # Pandas DataFrame logic
            df_shifted = df.groupby(self.ID_columns[1], group_keys=False).apply(lambda x: x.shift(-s))
            mask = (df_shifted[self.ID_columns[0]] >= tau_start) & (df_shifted[self.ID_columns[0]] <= tau_end - s)
            df_sliced = df_shifted[mask]

        # Prepare features and target for model fitting
        y_s = df_sliced.pop(self.target_column)

        return df_sliced, y_s

    def _check_for_dask_errors(self, df: Union[pd.DataFrame, dd.DataFrame]):
        """
        Checks for dask errors.

        Arguments:
            df (DataFrame): The DataFrame to be used.

        Returns:
            None
        """
        # check if the df is a dask dataframe:
        if not isinstance(df, dd.DataFrame):
            raise ValueError("You have sent in is_dask=True, but the dataframe is not a dask dataframe.")
        # check if the dask client is running:
        if self.dask_client.client is None:
            warnings.warn("The dask client is not running, please start the dask client for your session by calling the <your_stepshifter_instance>.start_dask_client() method.")

    def _debug_get_nan_positions(self, df: Union[pd.DataFrame, dd.DataFrame], column: str) -> List[int]:
        """
        Get the positions of NaN values in a DataFrame column.

        Arguments:
            df (DataFrame): The DataFrame to be used.
            column (str): The column to check for NaN values.

        Returns:
            output (list): A list containing the positions of NaN values.
        """
        return df[column].isnull().to_dask_array(lengths=True).compute().nonzero()[0].tolist()

    @staticmethod
    def estimate_dataset_memory(df: Union[pd.DataFrame, dd.DataFrame]):
        """
        Estimate the memory usage of a pandas or dask dataframe.

        Parameters:
            df (Union[pd.DataFrame, dd.DataFrame]): The dataframe to estimate memory usage for.

        Returns:
            float: The estimated memory usage of the dataframe in GB.
        """
        df_sample = df.head(10000)

        # Memory usage sample without calling .compute()
        memory_usage_sample = df_sample.memory_usage(deep=True).sum()

        # Check if dataframe is a Dask dataframe
        if isinstance(df, dd.DataFrame):
            total_rows = df.shape[0].compute()
        else:  # It's a pandas dataframe
            total_rows = len(df)

        sample_rows = len(df_sample)
        estimated_memory_gb = (memory_usage_sample / sample_rows) * total_rows / (1024**3)  # In GB
        return estimated_memory_gb

    def _adaptive_repartition(self, df):
        """
        Repartitions a dask dataframe based on the memory available per worker and the size of each partition.

        Args:
            df (dask.dataframe): The dask dataframe to repartition.

        Returns:
            dask.dataframe: The repartitioned dask dataframe.
        """
        self.logger.info("Finding unique locations...")
        unique_locations = df[self.ID_columns[1]].compute().unique()

        # Estimate memory footprint for a single 'location'
        sample_location = df[df[self.ID_columns[1]] == unique_locations[0]].compute()
        avg_location_memory = sample_location.memory_usage(deep=True).sum()

        def to_GB(x):
            return x / (1024**3)
        # Find number of locations nearest 1 GB:

        avg_location_memory_GB = to_GB(avg_location_memory)

        # https://docs.dask.org/en/latest/dataframe-parquet.html#:~:text=We%20recommend%20aiming%20for%2010,the%20overhead%20of%20Dask%20dominates.
        number_of_locations_per_partition = int(0.25 / avg_location_memory_GB)

        self.logger.info(f"{number_of_locations_per_partition} locations per partition")
        self.logger.info("Starting repartitioning of dask dataframe...")

        divisions = []
        for i in tqdm.tqdm(range(0, len(unique_locations), number_of_locations_per_partition)):
            divisions.append(unique_locations[i])

        self.logger.info(f"{len(divisions)} is the number of divisions")
        # Your check for last division
        self.logger.info("Checking if the last element in divisions is the same as the last element in unique_locations...")
        if divisions[-1] != unique_locations[-1]:
            divisions.append(unique_locations[-1])

        self.logger.info("Setting index...")
        df = df.set_index(self.ID_columns[1]).repartition(divisions=divisions).reset_index()

        self.logger.info("Sorting dataframe...")
        df = df.sort_values(by=[self.ID_columns[1], self.ID_columns[0]])

        return df

    def _validate_estimator(self):
        """
        Validates the estimator based on the is_dask parameter.

        Parameters:
            estimator (object): The estimator to be used for training and prediction.
            is_dask (bool): Whether the estimator is a dask estimator or not.

        Returns:
            None
        """
        if self.is_dask:
            if not hasattr(self.base_estimator, 'client'):
                raise ValueError("You have sent in is_dask=True, but the estimator does not have a client attribute.")
        else:
            if hasattr(self.base_estimator, 'client'):
                raise ValueError("You have sent in is_dask=False, but the estimator has a client attribute.")
