from __future__ import annotations

import glob
import re

# from gateway.gateway_client import GatewayClientBuilder, GatewayClient

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession

from pyflare.sdk.config.constants import INPUT_STRING, OUTPUT_STRING
from pyflare.sdk.utils import logger
from pyflare.sdk.config import constants
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.depots import client

# DO NOT REMOVE IMPORTS, readers used at runtime
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.readers.iceberg_reader import IcebergInputReader
from pyflare.sdk.readers.jdbc_reader import JDBCInputReader
from pyflare.sdk.readers.delta_reader import DeltaInputReader
from pyflare.sdk.readers.fastbase_reader import FastBaseInputReader
from pyflare.sdk.readers.snowflake_reader import SnowflakeInputReader
from pyflare.sdk.readers.bigquery_reader import BigqueryInputReader

# DO NOT REMOVE IMPORTS, writers used at runtime
from pyflare.sdk.writers.writer import Writer
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyflare.sdk.writers.iceberg_writer import IcebergOutputWriter
from pyflare.sdk.writers.jdbc_writer import JDBCOutputWriter
from pyflare.sdk.writers.delta_writer import DeltaOutputWriter
from pyflare.sdk.writers.fastbase_writer import FastBaseOutputWriter
from pyflare.sdk.writers.snowflake_writer import SnowflakeOutputWriter
from pyflare.sdk.writers.bigquery_writer import BigqueryOutputWriter

from pyflare.sdk.core.dataos_input import DataOSInput
from pyflare.sdk.core.minerva_input import MinervaInput
from pyflare.sdk.core.dataos_output import DataOSOutput
from pyflare.sdk.utils.generic_utils import get_jars_path

from urllib.parse import urlparse
from py4j.java_gateway import java_import
import os
from pyspark.sql import DataFrame
# from flare.sdk.utils.DataGovernor import DataGovernor

log = logger.get(__name__)

spark: SparkSession
g_inputs: dict
g_outputs: dict
g_dataos_token: str
# gateway_client: GatewayClient


class SparkSessionBuilder:
    spark: SparkSession = None
    spark_conf = list()
    parsed_inputs: dict = dict()
    parsed_outputs: dict = dict()
    api_token: str = ""
    dataos_fqdn: str = ""
    # gateway_client: GatewayClient = None

    # def __init__(self, api_token: str):
    #     self.api_token = api_token

    def build_session(self) -> SparkSession:
        if not self.spark:
            self.load_default_spark_conf()
            conf_obj = SparkConf().setAll(list(self.spark_conf))
            spark_builder = SparkSession.builder.config(conf=conf_obj)
            log.info(f"spark_conf: {[c for c in conf_obj.getAll()]}")
            self.spark = spark_builder.getOrCreate()
            # self.gateway_client = GatewayClientBuilder().set_base_url(os.environ.get("DATAOS_GATEWAY_BASEURL"))\
            #     .set_apikey(self.api_token).build()
        refresh_global_data(self)
        return self.spark

    def load_default_spark_conf(self) -> SparkSessionBuilder:
        # self.spark_conf.insert(0, ("spark.app.name", constants.SPARK_APP_NAME))
        # self.spark_conf.insert(0, ("spark.master", "local[*]"))
        self.spark_conf.insert(0, ("spark.redaction.regex", "(?i)secret|password|key|abfss|dfs|apikey"))
        self.spark_conf.insert(0, ("spark.driverEnv.DATAOS_RUN_AS_APIKEY", self.api_token))
        self.spark_conf.insert(0, ("spark.heimdall.udf.provider",
                                   "io.dataos.flare.authz.DataOSSparkUdfProvider"))
        self.spark_conf.insert(0, ("spark.sql.extensions", "org.apache.iceberg.spark.extensions"
                                                           ".IcebergSparkSessionExtensions"))
        jar_files = glob.glob("pyflare/jars/*.jar")
        self.spark_conf.insert(0, ("spark.jars", ",".join(jar_files)))
        return self

    def with_spark_conf(self, conf) -> SparkSessionBuilder:
        self.spark_conf += conf
        return self

    def with_readers(self, reader_address_list) -> SparkSessionBuilder:
        pass

    def with_writers(self, writer_address_list) -> SparkSessionBuilder:
        pass

    def with_depot(self, depot_address: str, acl: str = "r") -> SparkSessionBuilder:
        if re.search(r'wr|rw', acl.casefold().strip()):
            self.add_reader_instance(depot_address)
            self.add_writer_instance(depot_address)
        elif "w" == acl.casefold().strip():
            self.add_writer_instance(depot_address)
        else:
            self.add_reader_instance(depot_address)
        return self

    def add_writer_instance(self, depot_address):
        writer_instance = self.__get_write_instance(depot_address)
        writer_instance._view_name = depot_address
        self.parsed_outputs[depot_address] = {"writer_instance": writer_instance}
        self.spark_conf += writer_instance.get_conf()

    def add_reader_instance(self, depot_address):
        reader_instance = self.__get_read_instance(depot_address)
        reader_instance._view_name = depot_address
        self.parsed_inputs[depot_address] = {"reader_instance": reader_instance}
        self.spark_conf += reader_instance.get_conf()

    def with_user_apikey(self, apikey: str):
        self.api_token = apikey
        return self

    def with_dataos_fqdn(self, dataos_fqdn: str):
        self.dataos_fqdn = dataos_fqdn
        constants.DATAOS_BASE_URL = dataos_fqdn
        return self

    def load_input_conf(self, depot_input: dict) -> SparkSessionBuilder:
        self.parsed_inputs = self.__parse_input(depot_input)
        return self

    def __parse_input(self, input_dictionary: dict):
        for k, v in input_dictionary.items():
            reader_instance = self.__get_read_instance(v)
            reader_instance._view_name = k
            input_dictionary[k] = {"reader_instance": reader_instance}
            self.spark_conf += reader_instance.get_conf()
        return input_dictionary

    def __get_read_instance(self, depot_address: str) -> Reader:
        if self.__is_local(depot_address):
            depot_details = {"type": "local", "connection": {"localUrl": f"{depot_address}"}}
        else:
            depot_details = client.DepotClientAPI(self.api_token).get_depot_details(depot_address)
        conf_obj = ReadConfig(depot_details=depot_details)
        return self.__create_input_instance("Reader", conf_obj)

    def load_output_conf(self, depot_output: dict) -> SparkSessionBuilder:
        self.parsed_outputs = self.__parse_output(depot_output)
        return self

    def __parse_output(self, output_dictionary: dict):
        for k, v in output_dictionary.items():
            writer_instance = self.__get_write_instance(v)
            writer_instance._view_name = k
            output_dictionary[k] = {"writer_instance": writer_instance}
            self.spark_conf += writer_instance.get_conf()
        return output_dictionary

    def __get_write_instance(self, depot_address: str) -> Writer:
        depot_details = client.DepotClientAPI(self.api_token).get_depot_details(depot_address)
        conf_obj = WriteConfig(depot_details=depot_details)
        return self.__create_output_instance("Writer", conf_obj)

    def __create_input_instance(self, class_suffix: str, conf_obj: ReadConfig) -> Reader:
        io_format = conf_obj.io_format.casefold()
        log.debug(f"input_format: {io_format}")
        if io_format in ["pulsar"]:
            return globals()[f"FastBase{INPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ["delta", "deltabase"]:
            return globals()[f"Delta{INPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ("postgresql", "postgres", "jdbc", "mysql", "oracle", "redshift"):
            return globals()[f"JDBC{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "iceberg":
            return globals()[f"Iceberg{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "snowflake":
            return globals()[f"Snowflake{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "bigquery":
            return globals()[f"Bigquery{INPUT_STRING}{class_suffix}"](conf_obj)
        else:
            return globals()[f"File{INPUT_STRING}{class_suffix}"](conf_obj)

    def __create_output_instance(self, class_suffix: str, conf_obj: WriteConfig) -> Writer:
        io_format = conf_obj.io_format.casefold()
        log.debug(f"output_format: {io_format}")
        if io_format in ["pulsar"]:
            return globals()[f"FastBase{OUTPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ["delta", "deltabase"]:
            return globals()[f"Delta{OUTPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ("postgresql", "jdbc", "mysql", "oracle", "redshift"):
            return globals()[f"JDBC{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "iceberg":
            return globals()[f"Iceberg{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "snowflake":
            return globals()[f"Snowflake{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "bigquery":
            return globals()[f"Bigquery{OUTPUT_STRING}{class_suffix}"](conf_obj)
        else:
            return globals()[f"FileOutput{class_suffix}"](conf_obj)

    def __is_local(self, path):
        if os.path.exists(path):
            return True
        elif urlparse(path).scheme in ['', 'file']:
            return True
        return False


def refresh_global_data(spark_session_builder: SparkSessionBuilder):
    global g_inputs, g_outputs, spark, g_dataos_token
    g_inputs = spark_session_builder.parsed_inputs
    g_outputs = spark_session_builder.parsed_outputs
    g_dataos_token = spark_session_builder.api_token
    spark = spark_session_builder.spark
    # gateway_client = spark_session_builder.gateway_client
    log.debug(f"Parsed_inputs: {g_inputs}, Parsed_outputs: {g_outputs}")
    logger.set_spark_log_level(spark, log.getEffectiveLevel())


def load(name, format=None, driver=None, query=None, options=None):
    """

        Read dataset from the source with the supplied parameters.

        Args:
            name (str): Name of input key to read
            optional params -
            format (str): Read format
            driver (str): driver need to read source
            query (str): Query to be executed
            options (dict): Spark and other supported properties to be used during read

        Example:
            ------------- Icebase --------------
            read_options = {
                'compression': 'gzip',
                'iceberg': {
                    'table_properties': {
                        'read.split.target-size': 134217728,
                        "read.split.metadata-target-size": 33554432
                        }
                }
            }

            @dataos_source(name="ct", source_format="iceberg", options=read_options)

            ------------- JDBC --------------
            read_options = {
                'compression': 'gzip',
                "partitionColumn": "last_update",
                "lowerBound": datetime.datetime(2008,1,1),
                "upperBound": datetime.datetime(2009,1,1),
                "numPartitions": 6
                }

            @dataos_source(name="ct", source_format="postgresql", driver="com.mysql.cj.jdbc.Driver", options=read_options)
            Supported JDBC sub-protocols:
                * postgresql: org.postgresql.Driver
                * mysql: com.mysql.cj.jdbc.Driver

    """
    global g_inputs, spark, g_dataos_token
    java_import(spark._jvm, "io.dataos.spark.authz.util.DataGovernor")
    java_import(spark._jvm, "io.dataos.spark.authz.util.DataPolicyClient")
    java_import(spark._jvm, "io.dataos.datapolicy.model.DepotCollectionDataset")
    # to-do parse depot name form  depot address
    os_input = DataOSInput(name=name, parsed_inputs=g_inputs, spark=spark, source_format=format,
                           driver=driver, query=query, options=options)
    source_df = os_input.process_inputs()
    depot_details = os_input.parsed_inputs[name]['reader_instance'].read_config.depot_details
    dataset_address = ".".join([depot_details.get("depot", ""), depot_details.get("collection", ""),
                               depot_details.get("dataset", "")])
    dp_client = spark._jvm.DataPolicyClient.getInstance(os.environ.get("GATEWAY_BASE_URL", ""), g_dataos_token)
    data_govern_jvm = spark._jvm.DataGovernor.getInstance(dp_client)
    governed_data = data_govern_jvm.govern(dataset_address, source_df._jdf)
    governed_df = source_df
    if governed_data._1().isDefined():
        # here we are extracting first element of tuple we got from govern() response and converting java datafrme to
        # python df
        governed_df = DataFrame(governed_data._1().get(), spark)
    return governed_df


def minerva_input(name, query, driver="io.trino.jdbc.TrinoDriver", options=None):
    """

        Read dataset from the source with the supplied parameters.

        Args:
            name (str): Name of input key to read
            query (str): Query to be executed

            optional params -
            driver (str): driver needed to read source. Default driver is jdbc.TrinoDriver.
            options (dict): Spark and other supported properties to be used during read.

        Example:
            read_options = { "source": "pyflare.sdk/0.0.20.0" }
            query = "SELECT city_id, city_name, cast(ts_city AS varchar) "ts_city FROM icebase.retail.city"
            @minerva_input(name="ice", query=q2, options=read_options)
    """
    global g_inputs, spark
    minerva_in = MinervaInput(name=name, parsed_inputs=g_inputs, spark=spark, driver=driver, query=query,
                              options=options)
    minerva_df = minerva_in.process_inputs()
    return minerva_df


def save(name: str, dataframe, format: str = None, mode="append", driver=None, options=None):
    """
        Write the transformed dataset to sink, with the supplied parameters.

        Args:
            name (str): Name of output key to write
            format (str): Write format
            mode (str): Write format, default value "append"
            driver (str): driver need to read source
            options (dict): Spark and other supported properties to be used during write

        Example:
            write_options = {
                "compression": "gzip",
                "iceberg": {
                    "table_properties": {
                        "write.format.default": "parquet",
                        "write.parquet.compression-codec": "gzip",
                        "write.metadata.previous-versions-max": 3,
                        "parquet.page.write-checksum.enabled": "false"
                    },
                    "partition": [
                        {
                            "type": "months",
                            "column": "ts_city"
                        },
                        {
                            "type": "bucket",
                            "column": "city_id",
                            "bucket_count": 8
                        },
                        {
                            "type": "identity",
                            "column": "city_name"
                        }
                    ]
                }
            }

            @dataos_sink(name="c360", sink_format="iceberg", mode="append", options=write_options)
            :param dataframe:

        """
    global g_outputs, spark
    # to-do parse depot name form  depot address
    DataOSOutput(name=name, dataframe=dataframe, parsed_outputs=g_outputs, spark=spark, sink_format=format, mode=mode,
                 driver=driver, options=options)
