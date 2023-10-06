import pytest
import json
import pandas as pd
from lightgbm.dask import DaskLGBMRegressor
from lightgbm import LGBMRegressor
from xgboost.dask import DaskXGBRegressor
from sklearn.utils.validation import check_is_fitted
from stepshifter3.stepshifter import StepShifter
from stepshifter3.synthetic_data_generator import SyntheticDataGenerator
from stepshifter3.dask_client_manager import DaskClientManager
import os

# create /home/runner/work/stepshifter3/logs/stepshifter.log'
os.makedirs("/home/runner/work/stepshifter3/logs", exist_ok=True)
# Establish a connection with the dask client manager
dask_client = DaskClientManager(is_local=True, n_workers=2, threads_per_worker=1, memory_limit="16GB", remote_addresses=None)

stepshifter_config_regression = {"target_column": "ln_ged_sb_dep",                 # the target column in your training dataset
                                 "ID_columns": ["month_id", "priogrid_id"],       # the ID columns in your training dataset
                                 "time_column": "month_id",                       # the time column in your training dataset
                                 "mlflow_run_name": 'my_first_run',                      # the name of the run in mlflow, should be changes every time a new model type is run
                                 "mlflow_experiment_name": 'ensemble_models',            # the name of the experiment in mlflow
                                 "mlflow_tracking_uri": 'http://127.0.0.1:5000',  # the uri of the mlflow server, if not set the default is localhost:5000 or 127.0.0.1:5000
                                 "S": 5,                                          # number of steps ahead to predict
                                 "metrics_report": True,                          # not used at the moment
                                 "fit_params": {},
                                 "is_dask_reset_index": True,
                                 "dask_client": dask_client,
                                 "is_dask": True,
                                 "track_to_mlflow": False,
                                 }

stepshifter_shift_config = {"target_column": "target",                       # the target column in your training dataset
                            "ID_columns": ["month_id", "priogrid_id"],       # the ID columns in your training dataset
                            "time_column": "month_id",                       # the time column in your training dataset
                            "mlflow_run_name": 'my_first_run',                      # the name of the run in mlflow, should be changes every time a new model type is run
                            "mlflow_experiment_name": 'ensemble_models',            # the name of the experiment in mlflow
                            "mlflow_tracking_uri": 'http://127.0.0.1:5000',  # the uri of the mlflow server, if not set the default is localhost:5000 or 127.0.0.1:5000
                            "S": 5,                                          # number of steps ahead to predict
                            "metrics_report": True,                          # not used at the moment
                            "fit_params": {},
                            "is_dask_reset_index": True,
                            "dask_client": None,
                            "is_dask": False,
                            "track_to_mlflow": False,
                            }


@pytest.fixture(scope="module")
def df_synthetic():
    """
    Test docstring
    """
    # Create synthetic test data
    df_synthetic = SyntheticDataGenerator("pgm", n_time=516, n_prio_grid_size=100, n_country_size=242, n_features=15, use_dask=True).generate_dataframe()
    df_synthetic = df_synthetic.reset_index()

    return df_synthetic


@pytest.fixture(scope="module")
def df_sequential():
    """
    Test docstring
    """
    df_sequential = SyntheticDataGenerator("pgm", n_time=10, n_prio_grid_size=10, n_country_size=242, n_features=2, use_dask=False).generate_sequential_dataframe()
    return df_sequential


def test_dask_xgboost_fit(df_synthetic):
    """
    Test the fit function for the XGBoost DaskXGBRegressor
    """
    # Initialize stepshifter with the DaskXGBRegressor

    test_params_lgbm_reg = json.load(open("tests/configs/xgboost_reg_standard.json"))
    stepshifter = StepShifter(DaskXGBRegressor(**test_params_lgbm_reg), stepshifter_config_regression)

    # Start dask client
    stepshifter.start_dask_client()

    # Validate synthetic test data
    # what part of the data should be validated
    validation_range = [1, 516]
    X, y = stepshifter.validate_and_filter_data(df_synthetic, validation_range)

    # Fit
    tau_start_fit = 121
    tau_end_fit = 316
    stepshifter.fit(X, y, tau_start_fit, tau_end_fit)

    # Check if the models have been fitted
    for s in stepshifter.models.keys():
        check_is_fitted(stepshifter.models[s])

    # Stop dask client
    stepshifter.stop_dask_client()


def test_dask_lgbm_fit(df_synthetic):
    """
    Test the fit function for the LightGBM DaskLGBMRegressor
    """
    # Initialize stepshifter with the DaskLGBMRegressor

    test_params_lgbm_reg = json.load(open("tests/configs/lgbm_reg_standard.json"))
    stepshifter = StepShifter(DaskLGBMRegressor(**test_params_lgbm_reg), stepshifter_config_regression)

    # Start dask client
    stepshifter.start_dask_client()

    # Validate synthetic test data
    # what part of the data should be validated
    validation_range = [1, 516]
    X, y = stepshifter.validate_and_filter_data(df_synthetic, validation_range)

    # Fit
    tau_start_fit = 121
    tau_end_fit = 316
    stepshifter.fit(X, y, tau_start_fit, tau_end_fit)

    # Check if the models have been fitted
    for s in stepshifter.models.keys():
        check_is_fitted(stepshifter.models[s])


def test_stepshifted(df_sequential):
    """
    Test the stepshifted function
    """
    X_true_shifted = pd.read_parquet("tests/test_data/test_stepshifted_X.parquet")
    y_true_shifted = pd.read_parquet("tests/test_data/test_stepshifted_y.parquet")
    # Initialize stepshifter with any estimator
    test_params_lgbm_reg = json.load(open("tests/configs/lgbm_reg_standard.json"))
    stepshifter = StepShifter(LGBMRegressor(**test_params_lgbm_reg), stepshifter_shift_config)
    df_sequential = df_sequential.reset_index()
    # Fit
    X_shifted, y_shifted = stepshifter.stepshifted(df_sequential, s=2, tau_start=1, tau_end=10)

    # Check if the predictions have the correct length
    assert len(X_shifted) == len(X_true_shifted)
    assert len(y_shifted) == len(y_true_shifted)
