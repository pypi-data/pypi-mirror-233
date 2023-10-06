import psutil
import multiprocessing
from dask.distributed import Client, LocalCluster
from stepshifter3.logger import AppLogger
from typing import Optional


class DaskClientManager:
    def __init__(self, is_local=True, df_size=None, n_workers=None, threads_per_worker=None,
                 memory_limit='4GB', host=None, remote_addresses=None, logger: Optional[AppLogger] = None):
        """
        Initialize the DaskClientManager.

        Arguments:
            is_local (bool): Whether to start a local Dask cluster or connect to a remote cluster.
            df_size (int): The size of the dataframe to be processed.
            n_workers (int): The number of workers to start in the local cluster.
            threads_per_worker (int): The number of threads to start per worker in the local cluster.
            memory_limit (str): The amount of memory to allocate per worker in the local cluster.
            host (str): The host address to use for the local cluster.
            remote_addresses (list): A list of addresses to try to connect to for the remote cluster.

        Returns:
            None
        """
        self.is_local = is_local
        self.fixed_n_workers = n_workers
        self.n_workers = None
        self.threads_per_worker = threads_per_worker
        self.memory_limit = memory_limit
        self.remote_addresses = remote_addresses if isinstance(remote_addresses, list) else [remote_addresses]
        self.cluster = None
        self.client = None
        self.host = host
        if logger is None:
            self.logger = AppLogger(name=__name__).get_logger()
        else:
            self.logger = logger.get_logger()

    def optimize_local_settings(self):
        """
        Optimize the local settings for the Dask cluster.

        Parameters:
            fixed_n_workers (int): The number of workers to use in the local cluster. If None, the number of workers
                                   will be calculated based on the available CPU cores and memory.

        Returns:
            None
        """
        total_cpu_cores = multiprocessing.cpu_count()
        total_memory = psutil.virtual_memory().total / (1024**3)  # In GB

        if self.fixed_n_workers:
            self.n_workers = self.fixed_n_workers
        else:
            self.n_workers = total_cpu_cores // 2  # Adjust based on your tests

        self.threads_per_worker = 1  # Adjust based on your tests
        self.memory_limit = f"{(total_memory / self.n_workers)}GB"  # Keeping some memory in reserve

    def start_dask_client(self):
        """
        Start a Dask client based on the initialized settings.

        Arguments:
            None

        Returns:
            dask.distributed.Client: The Dask Client object.
        """

        self.logger.info("Starting Dask client...")

        if self.is_local:
            self.optimize_local_settings()

            # Create a LocalCluster and Client
            self.cluster = LocalCluster(n_workers=self.n_workers,
                                        threads_per_worker=self.threads_per_worker,
                                        memory_limit=self.memory_limit,
                                        host=self.host)
            self.client = Client(self.cluster)
            self.logger.info(f"Connected to local Dask cluster with {self.n_workers} workers with {self.memory_limit}GB \
                   limit and {self.threads_per_worker} threads per worker. The worker can be reached at {self.client.dashboard_link}")
        else:
            # Connection to remote clusters remains unchanged
            for address in self.remote_addresses:
                try:
                    self.client = Client(address)
                    self.logger.info(f"Connected to remote Dask cluster at {address}")
                    break
                except Exception as e:
                    self.logger.error(f"Failed to connect to remote Dask cluster at {address}: {e}")
                    raise ConnectionError(f"Failed to connect to remote Dask cluster at {address}: {e}")
            else:
                raise ConnectionError(f"Failed to connect to any remote Dask cluster at addresses: {self.remote_addresses}")
        return self.client

    def stop_dask_client(self):
        """
        Stop the Dask client.

        Arguments:
            None

        Returns:
            None
        """
        try:
            self.client.close()
            self.cluster.close()
            self.logger.info("Closed Dask client and cluster.")
        except Exception as e:
            self.logger.error(f"Failed to close Dask client and cluster: {e}")
            raise ConnectionError(f"Failed to close Dask client and cluster: {e}")
