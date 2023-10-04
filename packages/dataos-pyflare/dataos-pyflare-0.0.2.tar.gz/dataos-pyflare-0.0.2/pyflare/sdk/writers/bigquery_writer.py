import ast

from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import logger
from pyflare.sdk.writers.writer import Writer

log = logger.get(__name__)


class BigqueryOutputWriter(Writer):

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)

    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = self.write_config.spark_options
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.options(**spark_options).format("bigquery").mode(self.write_config.mode).save()

    def write_stream(self):
        pass

    def get_conf(self):
        depot_name = self.write_config.depot_details['depot']
        secret_file_path = f"{depot_name}_secrets_file_path"
        keyfile_path = self.write_config.depot_details.get("secrets", {}).get(secret_file_path, "")

        connection_details = self.write_config.depot_details.get("connection", {})
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", ""),
            "dataset": connection_details.get("dataset", ""),
            "table": connection_details.get("table", ""),
            "credentialsFile": keyfile_path
        }
        self.write_config.spark_options = bigquery_spark_option
        bigquery_conf = [
            ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", keyfile_path),
            ("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"),
            ("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        ]
        return bigquery_conf
