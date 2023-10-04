from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import Reader
from pyflare.sdk.utils import logger, generic_utils

log = logger.get(__name__)


class BigqueryInputReader(Reader):

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = generic_utils.get_dataset_path(self.read_config)
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        depot_name = self.read_config.depot_details['depot']
        secret_file_path = f"{depot_name}_secrets_file_path"
        keyfile_path = self.read_config.depot_details.get("secrets", {}).get(secret_file_path, "")

        connection_details = self.read_config.depot_details.get("connection", {})
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", ""),
            "dataset": connection_details.get("dataset", ""),
            "table": connection_details.get("table", ""),
            "credentialsFile": keyfile_path
        }
        self.read_config.spark_options = bigquery_spark_option
        bigquery_conf = [
            ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", keyfile_path),
            ("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"),
            ("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        ]
        return bigquery_conf
