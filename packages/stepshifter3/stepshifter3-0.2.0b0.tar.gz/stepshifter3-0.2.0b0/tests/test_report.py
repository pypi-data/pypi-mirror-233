import pytest
import json
import pandas as pd
from xgboost import XGBRegressor
from sklearn.utils.validation import check_is_fitted
from stepshifter3.stepshifter import StepShifter
from stepshifter3.synthetic_data_generator import SyntheticDataGenerator
from stepshifter3.dask_client_manager import DaskClientManager
from stepshifter3.report import Report
import os
os.makedirs("/home/runner/work/stepshifter3/logs", exist_ok=True)
open("/home/runner/work/stepshifter3/logs/stepshifter.log", "w").close()

# Establish a connection with the dask client manager
dask_client = DaskClientManager(is_local=True, n_workers=2, threads_per_worker=1, memory_limit="16GB", remote_addresses=None)

stepshifter_config_regression = {"target_column": "ln_ged_sb_dep",                  # the target column in your training dataset
                                 "ID_columns": ["month_id", "priogrid_id"],         # the ID columns in your training dataset
                                 "time_column": "month_id",                         # the time column in your training dataset
                                 "mlflow_tracking_uri": 'http://127.0.0.1:5000',    # the uri of the mlflow server, if not set the default is localhost:5000 or 127.0.0.1:5000
                                 "S": 2,                                            # number of steps ahead to predict
                                 "metrics_report": True,                            # not used at the moment
                                 "mlflow_run_name": "some_run_name",                # the name of the run in mlflow, should be changes every time a new model type is run
                                 "mlflow_experiment_name": "some_experiment_name",  # the name of the experiment in mlflow
                                 "fit_params": {},
                                 "is_dask_reset_index": True,
                                 "dask_client": dask_client,
                                 "is_dask": False,
                                 }


@pytest.fixture(scope="module")
def df_synthetic():
    """
    Test docstring
    """
    # Create synthetic test data
    df_synthetic = SyntheticDataGenerator("pgm", n_time=516, n_prio_grid_size=100, n_country_size=242, n_features=15, use_dask=False).generate_dataframe()
    df_synthetic = df_synthetic.reset_index()

    return df_synthetic


@pytest.fixture(scope="module")
def df_sequential():
    """
    Test docstring
    """
    df_sequential = SyntheticDataGenerator("pgm", n_time=10, n_prio_grid_size=10, n_country_size=242, n_features=2, use_dask=False).generate_sequential_dataframe()
    return df_sequential


def test_dask_xgboost_report(df_synthetic):
    """
    Test the report class after fitting models using the XGBoost DaskXGBRegressor
    """
    # Initialize stepshifter with the DaskXGBRegressor

    test_params_xgb_reg = json.load(open("tests/configs/xgboost_reg_standard.json"))
    stepshifter = StepShifter(XGBRegressor(**test_params_xgb_reg), stepshifter_config_regression)

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

    report = Report(stepshifter, X, y)
    report.calculate_metrics()
    report.visualize_metrics(save=True, destination_dir="tests/reports/")

    for i in ["shap", "X_corr", "feature_importance"]:
        assert getattr(report, i) is not None

    assert isinstance(report.shap, dict)
    assert isinstance(report.X_corr, pd.DataFrame)
    assert isinstance(report.feature_importance, dict)
