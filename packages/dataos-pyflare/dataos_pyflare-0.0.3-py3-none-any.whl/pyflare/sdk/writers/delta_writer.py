import ast
import base64

import pyspark.sql.functions as F
from pyflare.sdk.config import constants
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import logger
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyspark.sql.readwriter import DataFrameWriter

log = logger.get(__name__)


class DeltaOutputWriter(FileOutputWriter):
    DELTA_CONF = '''[
            ("spark.sql.catalog.{catalog_name}","org.apache.spark.sql.delta.catalog.DeltaCatalog"),
            ("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        ]'''

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)

    def write(self, df):
        spark_options = self.write_config.spark_options
        io_format = self.write_config.io_format
        dataset_path = self.write_config.dataset_absolute_path()
        # df = self.spark.sql(f"select * from {self.view_name}")
        df_writer = df.write.format(io_format)
        if spark_options:
            df_writer = df_writer.options(**spark_options)
        log.info(f"spark options: {spark_options}")
        df_writer = self.__process_partition_conf(df_writer)
        df_writer.mode(self.write_config.mode).save(dataset_path)

    def write_stream(self):
        pass

    def get_conf(self):
        # print("calling write -> :", f"_{self.write_config.depot_type()}_{self.write_config.io_format}")
        return getattr(self, f"_{self.write_config.depot_type()}_{self.write_config.io_format}")()

    def _abfss_delta(self):
        dataset_absolute_path = self.write_config.dataset_absolute_path()
        delta_conf = ast.literal_eval(self.DELTA_CONF.format(catalog_name=self.write_config.depot_name))
        dataset_auth_token = self._get_secret_token()
        account = self.write_config.depot_details.get("connection", {}).get("account", "")
        endpoint_suffix = dataset_absolute_path.split(account)[1].split("/")[0].strip(". ")
        dataset_auth_key = "{}.{}.{}".format(constants.AZURE_ACCOUNT_KEY_PREFIX, account, endpoint_suffix)
        delta_conf.append((dataset_auth_key, dataset_auth_token))
        return delta_conf

    def _get_secret_token(self):
        encoded_secret = self.write_config.depot_details.get("secrets", {}).get("data", {})[0].get("base64Value", "")
        decoded_secrets_list = base64.b64decode(encoded_secret).decode('UTF8').split("\n")
        secret_token = ""
        for decoded_secret in decoded_secrets_list:
            if constants.STORAGE_ACCOUNT_KEY in decoded_secret:
                secret_token = decoded_secret.split(f"{constants.STORAGE_ACCOUNT_KEY}=")[1]
        return secret_token

    def __process_partition_conf(self, df_writer):
        for temp_dict in self.write_config.extra_options.get("partition", []):
            partition_column = temp_dict.get("column", [])
            if partition_column:
                log.info(f"partition column: {partition_column}")
                df_writer = df_writer.partitionBy(partition_column)
        return df_writer

