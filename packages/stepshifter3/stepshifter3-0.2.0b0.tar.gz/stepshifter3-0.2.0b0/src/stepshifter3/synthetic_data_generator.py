import pandas as pd
import numpy as np
import dask.dataframe as dd
from dask.delayed import delayed
from stepshifter3.logger import AppLogger
from typing import Optional


class SyntheticDataGenerator:
    """
    Generate synthetic data, of the form:
        (month_id, location_id, targer_variable, feature_1, feature_2, ...)
    """

    def __init__(self, loa: str, n_time: int, n_prio_grid_size: int, n_country_size: int, n_features: int, use_dask: bool = False, logger: Optional[AppLogger] = None):
        """
        Initialize the SyntheticDataGenerator.

        Arguments:
            loa (str): The level of analysis, defined as either 'cm' or else 'pgm'.
            n_time (int): The number of time periods.
            n_prio_grid_size (int): The number of priogrids.
            n_country_size (int): The number of countries.
            n_features (int): The number of features.
            use_dask (bool): Whether to use Dask to generate the data.
        Returns:
            None
        """
        self.loa = loa
        self.n_time = n_time
        self.n_prio_grid_size = n_prio_grid_size
        self.n_country_size = n_country_size
        self.n_features = n_features
        self.use_dask = use_dask
        self.df = None

        if logger is None:
            self.logger = AppLogger(name=__name__).get_logger()
        else:
            self.logger = logger.get_logger()

        if self.loa not in ['pgm', 'cm']:
            self.logger.error('loa must be either "pgm" or "cm".')
            raise ValueError('loa must be either "pgm" or "cm".')

    def _initialize_data_dict(self, n: int) -> dict:
        """
        Initialize a dictionary of data to be used to create a Pandas DataFrame.

        Arguments:
            n (int): The number of rows to generate.

        Returns:
            dict: The dictionary of data.
        """
        data = {}
        data['ln_ged_sb_dep'] = np.random.rand(n)
        for i in range(1, self.n_features + 1):
            feature_name = f'pca_{i}'
            data[feature_name] = np.random.rand(n)

        return data

    def _generate_sequential_data_dict(self, n: int, target: str) -> dict:
        """
        Generate a sequential dictionary of data to be used to create a Pandas DataFrame.

        Arguments:
            n (int): The number of rows to generate.
            target (str): The name of the target variable.

        Returns:
            dict: The dictionary of data.
        """
        data = {}
        data[target] = np.arange(n)
        for i in range(1, self.n_features + 1):
            feature_name = f'pca_{i}'
            data[feature_name] = np.arange(n)

        return data

    def _generate_index(self) -> pd.MultiIndex:
        """
        Generate the index for the Pandas DataFrame.

        Arguments:
            None

        Returns:
            pd.MultiIndex: The index for the Pandas DataFrame.
        """
        if self.loa == 'cm':
            country_ids = range(1, self.n_country_size + 1)
            return pd.MultiIndex.from_product([range(1, self.n_time + 1), country_ids], names=('month_id', 'country_id'))
        elif self.loa == 'pgm':
            priogrid_ids = range(1, self.n_prio_grid_size + 1)
            return pd.MultiIndex.from_product([range(1, self.n_time + 1), priogrid_ids], names=('month_id', 'priogrid_id'))

    def _generate_small_dataframe_chunk(self, start_time: int, end_time: int) -> pd.DataFrame:
        """
        Generate a small chunk of the Pandas DataFrame.

        Arguments:
            start_time (int): The starting time period.
            end_time (int): The ending time period.

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """

        chunk_index = self._generate_index_time_slice(start_time, end_time)
        n = len(chunk_index)
        data = self._initialize_data_dict(n)

        return pd.DataFrame(data, index=chunk_index)

    def _generate_sequential_dataframe_chunk(self, start_time: int, end_time: int) -> pd.DataFrame:
        """
        Generate a small chunk of the Pandas DataFrame.

        Arguments:
            start_time (int): The starting time period.
            end_time (int): The ending time period.

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """

        chunk_index = self._generate_index_time_slice(start_time, end_time)
        n = len(chunk_index)
        data = self._generate_sequential_data_dict(n, target='target')

        return pd.DataFrame(data, index=chunk_index)

    def _generate_index_time_slice(self, start_time: int, end_time: int) -> pd.MultiIndex:
        """
        Generate a slice of the index for the Pandas DataFrame.

        Arguments:
            start_time (int): The starting time period.
            end_time (int): The ending time period.

        Returns:
            pd.MultiIndex: The index for the Pandas DataFrame.
        """

        if self.loa == 'cm':
            country_ids = range(1, self.n_country_size + 1)
            return pd.MultiIndex.from_product([range(start_time, end_time + 1), country_ids], names=('month_id', 'country_id'))
        elif self.loa == 'pgm':
            priogrid_ids = range(1, self.n_prio_grid_size + 1)
            return pd.MultiIndex.from_product([range(start_time, end_time + 1), priogrid_ids], names=('month_id', 'priogrid_id'))

    def _generate_dask_dataframe(self, n: int, time_chunk_size: int = 30) -> dd.DataFrame:
        """
        Generate a Dask DataFrame.

        Arguments:
            n (int): The number of rows to generate.
            time_chunk_size (int): The number of time periods to generate per chunk.

        Returns:
            dd.DataFrame: The Dask DataFrame.
        """
        num_time_chunks = self.n_time // time_chunk_size
        last_time_chunk_size = self.n_time % time_chunk_size

        delayed_frames = []
        for i in range(num_time_chunks):
            start_time = i * time_chunk_size + 1
            end_time = start_time + time_chunk_size - 1
            df_chunk = delayed(self._generate_small_dataframe_chunk)(start_time, end_time)
            delayed_frames.append(df_chunk)

        if last_time_chunk_size > 0:
            start_time = self.n_time - last_time_chunk_size + 1
            end_time = self.n_time
            df_chunk = delayed(self._generate_small_dataframe_chunk)(start_time, end_time)
            delayed_frames.append(df_chunk)

        # Set divisions for better indexing such that we can use loc
        divisions = list(range(0, n, time_chunk_size * self.n_prio_grid_size)) + [n]
        ddf = dd.from_delayed(delayed_frames, divisions=divisions)

        return ddf

    def _generate_sequential_dask_dataframe(self, n: int, time_chunk_size: int = 30) -> dd.DataFrame:
        """
        Generate a Dask DataFrame.

        Arguments:
            n (int): The number of rows to generate.
            time_chunk_size (int): The number of time periods to generate per chunk.

        Returns:
            dd.DataFrame: The Dask DataFrame.
        """
        num_time_chunks = self.n_time // time_chunk_size
        last_time_chunk_size = self.n_time % time_chunk_size

        delayed_frames = []
        for i in range(num_time_chunks):
            start_time = i * time_chunk_size + 1
            end_time = start_time + time_chunk_size - 1
            df_chunk = delayed(self._generate_sequential_dataframe_chunk)(start_time, end_time)
            delayed_frames.append(df_chunk)

        if last_time_chunk_size > 0:
            start_time = self.n_time - last_time_chunk_size + 1
            end_time = self.n_time
            df_chunk = delayed(self._generate_sequential_dataframe_chunk)(start_time, end_time)
            delayed_frames.append(df_chunk)

        # Set divisions for better indexing such that we can use loc
        divisions = list(range(0, n, time_chunk_size * self.n_prio_grid_size)) + [n]
        ddf = dd.from_delayed(delayed_frames, divisions=divisions)

        return ddf

    def generate_dataframe(self) -> pd.DataFrame:
        """
        Generate a Pandas DataFrame.

        Arguments:
            None

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """
        index = self._generate_index()
        n = len(index)

        if self.use_dask:
            self.df = self._generate_dask_dataframe(n)
        else:
            data = self._initialize_data_dict(n)
            self.df = pd.DataFrame(data, index=index)

        return self.df

    def generate_sequential_dataframe(self) -> pd.DataFrame:
        """
        Generate a Pandas DataFrame with sequential data.

        Arguments:
            None

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """
        index = self._generate_index()
        n = len(index)

        if self.use_dask:
            self.df = self._generate_sequential_dask_dataframe(n)
        else:
            data = self._generate_sequential_data_dict(n, target='target')
            self.df = pd.DataFrame(data, index=index)

        return self.df

    def generate_csv(self, filename: str):
        """
        Generate a CSV file from the Pandas DataFrame.

        Arguments:
            filename (str): The name of the CSV file to generate.

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """
        if self.use_dask:
            self.df.to_csv(filename, single_file=True)
        else:
            self.df.to_csv(filename)

    def generate_parquet(self, filename: str):
        """
        Generate a Parquet file from the Pandas DataFrame.

        Arguments:
            filename (str): The name of the Parquet file to generate.

        Returns:
            pd.DataFrame: The Pandas DataFrame.
        """
        if self.use_dask:
            self.df.to_parquet(filename, write_options={'compression': 'gzip'})
        else:
            self.df.to_parquet(filename)
