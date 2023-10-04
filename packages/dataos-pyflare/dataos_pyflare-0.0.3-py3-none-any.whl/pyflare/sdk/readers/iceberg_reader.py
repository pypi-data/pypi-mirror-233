import ast

from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.utils import logger, generic_utils

log = logger.get(__name__)


class IcebergInputReader(FileInputReader):
    ICEBERG_CONF = '''[
            ("spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog"),
            ("spark.sql.catalog.{catalog_name}.type", "hadoop"),
            ("spark.sql.catalog.{catalog_name}.warehouse", "{depot_base_path}")
        ]'''
    
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
        log.debug("calling : ", f"_{self.read_config.depot_type()}_{self.read_config.io_format}")
        return getattr(self, f"_{self.read_config.depot_type()}_{self.read_config.io_format}")()
    
    def _abfss_iceberg(self):
        dataset_absolute_path = self.read_config.dataset_absolute_path()
        depot_base_path = dataset_absolute_path.split(self.read_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.read_config.depot_name(),
                                                                 depot_base_path=depot_base_path))
        iceberg_conf.append(generic_utils.get_abfss_spark_conf(self.read_config))
        return iceberg_conf
